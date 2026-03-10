"""
C5-DEC CAD — Cryptography module.

Provides native Python implementations of:

1. SHA-256 file integrity (MRS-025)
   - compute_hash(path) → hex string
   - verify_hash(path, expected_hash) → bool

2. GnuPG file signing and encryption (MRS-046)
   - gpg_sign_file(path, key_id, output_path) → str
   - gpg_verify_signature(file_path, sig_path) → bool
   - gpg_encrypt_file(path, recipients, output_path) → str
   - gpg_decrypt_file(path, output_path, passphrase) → str

3. Shamir's Secret Sharing over GF(p) (MRS-024)
   - split_secret(secret_hex, n, k) → list[str]
   - recover_secret(shares) → str

4. PyNaCl signing helpers (MRS-046 native path)
   - nacl_keygen_signing() → (verify_key_hex, signing_key_hex)
   - nacl_sign(message_bytes, signing_key_hex) → bytes
   - nacl_verify(signed_bytes, verify_key_hex) → bytes

Post-quantum cryptography (Kyber/Dilithium via OQS-OpenSSL) is available in
the dedicated C5-DEC cryptography DevContainer. See docs/manual/cryptography.md.
"""

import hashlib
import secrets
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

import nacl.encoding
import nacl.exceptions
import nacl.signing

from c5dec import common

logger = common.logger(__name__)

# ---------------------------------------------------------------------------
# 1. SHA-256 File Integrity (MRS-025)
# ---------------------------------------------------------------------------

HASH_BLOCK_SIZE = 65536  # 64 KB chunks for large file support


def compute_hash(path: str) -> str:
    """Compute the SHA-256 hash of a file.

    Parameters
    ----------
    path : str
        Absolute or relative path to the file.

    Returns
    -------
    str
        Hex-encoded SHA-256 digest.

    Raises
    ------
    common.C5decError
        If the file does not exist or cannot be read.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise common.C5decError(f"File not found: {path}")

    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(HASH_BLOCK_SIZE)
            while chunk:
                sha256.update(chunk)
                chunk = f.read(HASH_BLOCK_SIZE)
    except OSError as exc:
        raise common.C5decError(f"Cannot read file '{path}': {exc}") from exc

    digest = sha256.hexdigest()
    logger.debug("SHA-256 of '%s': %s", path, digest)
    return digest


def verify_hash(path: str, expected_hash: str) -> bool:
    """Verify that a file's SHA-256 hash matches an expected value.

    Parameters
    ----------
    path : str
        Path to the file to verify.
    expected_hash : str
        Expected hex-encoded SHA-256 digest (case-insensitive).

    Returns
    -------
    bool
        True if the hash matches, False otherwise.
    """
    actual = compute_hash(path)
    match = actual.lower() == expected_hash.lower()
    if match:
        logger.info("Hash verification PASSED for '%s'", path)
    else:
        logger.warning(
            "Hash verification FAILED for '%s': expected %s, got %s",
            path, expected_hash, actual,
        )
    return match


# ---------------------------------------------------------------------------
# 2. GnuPG File Signing and Encryption (MRS-046)
# ---------------------------------------------------------------------------

def _run_gpg(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Internal helper to invoke the system gpg executable."""
    cmd = ["gpg", "--batch", "--yes"] + args
    logger.debug("Running GPG command: %s", " ".join(cmd))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
        )
        return result
    except FileNotFoundError as exc:
        raise common.C5decError(
            "GnuPG (gpg) is not available on this system. "
            "Install GnuPG or use the C5-DEC dev container."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise common.C5decError(
            f"GPG command failed (exit {exc.returncode}): {exc.stderr.strip()}"
        ) from exc


def gpg_sign_file(
    path: str,
    key_id: Optional[str] = None,
    output_path: Optional[str] = None,
    detach: bool = True,
) -> str:
    """Create a GnuPG detached (or inline) signature for a file.

    Parameters
    ----------
    path : str
        The file to sign.
    key_id : str, optional
        GPG key ID or fingerprint. Uses the default key if omitted.
    output_path : str, optional
        Destination for the signature file. Defaults to ``<path>.sig``.
    detach : bool
        If True (default) create a detached signature. Otherwise inline.

    Returns
    -------
    str
        Path to the generated signature file.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise common.C5decError(f"File to sign not found: {path}")

    sig_path = output_path or str(file_path) + ".sig"
    args = ["--detach-sign" if detach else "--sign", "--output", sig_path]
    if key_id:
        args = ["--local-user", key_id] + args
    args.append(str(file_path))

    _run_gpg(args)
    logger.info("GPG signature written to '%s'", sig_path)
    return sig_path


def gpg_verify_signature(file_path: str, sig_path: str) -> bool:
    """Verify a GnuPG detached signature.

    Parameters
    ----------
    file_path : str
        The signed file.
    sig_path : str
        The detached signature file (.sig or .asc).

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.
    """
    result = _run_gpg(["--verify", sig_path, file_path], check=False)
    if result.returncode == 0:
        logger.info("GPG signature verified OK for '%s'", file_path)
        return True
    logger.warning(
        "GPG signature verification FAILED for '%s': %s",
        file_path, result.stderr.strip(),
    )
    return False


def gpg_encrypt_file(
    path: str,
    recipients: List[str],
    output_path: Optional[str] = None,
) -> str:
    """Encrypt a file for one or more GPG recipients.

    Parameters
    ----------
    path : str
        The file to encrypt.
    recipients : list[str]
        List of GPG recipient key IDs or email addresses.
    output_path : str, optional
        Destination for the encrypted file. Defaults to ``<path>.gpg``.

    Returns
    -------
    str
        Path to the encrypted output file.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise common.C5decError(f"File to encrypt not found: {path}")
    if not recipients:
        raise common.C5decError("At least one recipient key ID must be provided.")

    enc_path = output_path or str(file_path) + ".gpg"
    args = ["--encrypt", "--output", enc_path]
    for rec in recipients:
        args += ["--recipient", rec]
    args.append(str(file_path))

    _run_gpg(args)
    logger.info("GPG encrypted output written to '%s'", enc_path)
    return enc_path


def gpg_decrypt_file(
    path: str,
    output_path: Optional[str] = None,
    passphrase: Optional[str] = None,
) -> str:
    """Decrypt a GPG-encrypted file.

    Parameters
    ----------
    path : str
        The encrypted file (.gpg or .asc).
    output_path : str, optional
        Destination for the decrypted file. Defaults to path without .gpg suffix.
    passphrase : str, optional
        Passphrase for symmetric decryption.

    Returns
    -------
    str
        Path to the decrypted output file.
    """
    enc_path = Path(path)
    if not enc_path.is_file():
        raise common.C5decError(f"Encrypted file not found: {path}")

    if output_path is None:
        stem = str(enc_path)
        output_path = stem[:-4] if stem.endswith(".gpg") else stem + ".dec"

    args = ["--decrypt", "--output", output_path]
    if passphrase:
        args = ["--passphrase", passphrase, "--pinentry-mode", "loopback"] + args
    args.append(str(enc_path))

    _run_gpg(args)
    logger.info("GPG decrypted output written to '%s'", output_path)
    return output_path


# ---------------------------------------------------------------------------
# 3. Shamir's Secret Sharing over GF(p) (MRS-024)
#
# Uses Mersenne prime p = 2^127 - 1. The secret is a non-negative integer
# smaller than p. Shares are encoded as "<index>:<value_hex>" strings.
# ---------------------------------------------------------------------------

_SHAMIR_PRIME = (1 << 127) - 1  # Mersenne prime M_127


def _eval_polynomial(coefficients: List[int], x: int, prime: int) -> int:
    """Evaluate polynomial at x over GF(prime) using Horner's method."""
    result = 0
    for coeff in reversed(coefficients):
        result = (result * x + coeff) % prime
    return result


def _lagrange_interpolate(x: int, x_s: List[int], y_s: List[int], prime: int) -> int:
    """Lagrange interpolation: recover f(x) from (x_s, y_s) pairs over GF(prime)."""
    k = len(x_s)
    result = 0
    for i in range(k):
        num, den = 1, 1
        for j in range(k):
            if i == j:
                continue
            num = (num * (x - x_s[j])) % prime
            den = (den * (x_s[i] - x_s[j])) % prime
        # Modular inverse via Fermat's little theorem (prime is prime)
        lagrange = (num * pow(den, prime - 2, prime)) % prime
        result = (result + y_s[i] * lagrange) % prime
    return result


def split_secret(secret_hex: str, n: int, k: int) -> List[str]:
    """Split a secret into n shares requiring k to reconstruct (Shamir SSS).

    Parameters
    ----------
    secret_hex : str
        The secret as a hex string. Must represent a value < 2^127 - 1.
    n : int
        Total number of shares to produce (n >= k >= 2).
    k : int
        Minimum number of shares required to reconstruct (threshold).

    Returns
    -------
    list[str]
        List of n shares in ``"<index>:<value_hex>"`` format.

    Raises
    ------
    common.C5decError
        If k > n, the secret is too large, or arguments are invalid.
    """
    if k < 2:
        raise common.C5decError("Threshold k must be at least 2.")
    if k > n:
        raise common.C5decError(f"Threshold k={k} cannot exceed total shares n={n}.")

    secret_int = int(secret_hex, 16)
    if secret_int >= _SHAMIR_PRIME:
        raise common.C5decError(
            "Secret is too large for the prime field (must be < 2^127 - 1, "
            "i.e. at most 126 bits). Split larger secrets into 126-bit chunks."
        )

    coefficients = [secret_int] + [
        secrets.randbelow(_SHAMIR_PRIME - 1) + 1 for _ in range(k - 1)
    ]

    shares = [
        f"{i}:{_eval_polynomial(coefficients, i, _SHAMIR_PRIME):x}"
        for i in range(1, n + 1)
    ]
    logger.info("Secret split into %d shares with threshold %d.", n, k)
    return shares


def recover_secret(shares: List[str]) -> str:
    """Reconstruct a secret from Shamir shares.

    Parameters
    ----------
    shares : list[str]
        At least k share strings in ``"<index>:<value_hex>"`` format.

    Returns
    -------
    str
        Hex-encoded reconstructed secret.

    Raises
    ------
    common.C5decError
        If fewer than 2 shares are provided or shares are malformed.
    """
    if len(shares) < 2:
        raise common.C5decError("At least 2 shares are required for reconstruction.")
    try:
        parsed = [
            (int(s.split(":")[0]), int(s.split(":")[1], 16))
            for s in shares
        ]
    except (ValueError, IndexError) as exc:
        raise common.C5decError(
            "Malformed share format. Expected '<index>:<value_hex>'."
        ) from exc

    x_s = [p[0] for p in parsed]
    y_s = [p[1] for p in parsed]
    secret_int = _lagrange_interpolate(0, x_s, y_s, _SHAMIR_PRIME)
    secret_hex = f"{secret_int:x}"
    logger.info("Secret reconstructed from %d shares.", len(shares))
    return secret_hex


# ---------------------------------------------------------------------------
# 4. PyNaCl Ed25519 Signing Helpers (MRS-046 native Python path)
# ---------------------------------------------------------------------------

def nacl_keygen_signing() -> Tuple[str, str]:
    """Generate a new NaCl Ed25519 signing keypair.

    Returns
    -------
    tuple[str, str]
        ``(verify_key_hex, signing_key_hex)`` — both hex-encoded.
        The verify key is the public key; the signing key is the private key.
    """
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key
    sk_hex = signing_key.encode(encoder=nacl.encoding.HexEncoder).decode()
    vk_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder).decode()
    logger.info("NaCl Ed25519 signing keypair generated.")
    return vk_hex, sk_hex


def nacl_sign(message: bytes, signing_key_hex: str) -> bytes:
    """Sign a message with a NaCl Ed25519 signing key.

    Parameters
    ----------
    message : bytes
        The message bytes to sign.
    signing_key_hex : str
        Hex-encoded 32-byte Ed25519 signing key (from :func:`nacl_keygen_signing`).

    Returns
    -------
    bytes
        Signed message (64-byte signature prepended to plaintext).
    """
    try:
        sk = nacl.signing.SigningKey(
            signing_key_hex.encode(),
            encoder=nacl.encoding.HexEncoder,
        )
    except Exception as exc:
        raise common.C5decError(f"Invalid signing key: {exc}") from exc

    signed = sk.sign(message)
    logger.info("NaCl Ed25519 message signed (%d bytes).", len(message))
    return bytes(signed)


def nacl_verify(signed_message: bytes, verify_key_hex: str) -> bytes:
    """Verify a NaCl Ed25519 signed message and return the plaintext.

    Parameters
    ----------
    signed_message : bytes
        The signed message returned by :func:`nacl_sign`.
    verify_key_hex : str
        Hex-encoded Ed25519 verify (public) key.

    Returns
    -------
    bytes
        The original message without the signature.

    Raises
    ------
    common.C5decError
        If signature verification fails.
    """
    try:
        vk = nacl.signing.VerifyKey(
            verify_key_hex.encode(),
            encoder=nacl.encoding.HexEncoder,
        )
        message = vk.verify(signed_message)
    except nacl.exceptions.BadSignatureError as exc:
        raise common.C5decError("NaCl signature verification FAILED.") from exc
    except Exception as exc:
        raise common.C5decError(f"NaCl verify error: {exc}") from exc

    logger.info("NaCl Ed25519 signature verified OK.")
    return bytes(message)