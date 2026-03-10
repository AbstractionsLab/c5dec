# Cryptography

## Native Python cryptographic functions

C5-DEC CAD includes a native Python cryptography module (`c5dec/core/cryptography.py`)
that provides four categories of cryptographic operations accessible directly
via the `c5dec crypto` CLI command, without requiring any external containers:

| Category | CLI prefix | Key operations |
|----------|------------|----------------|
| SHA-256 integrity | `c5dec crypto hash` / `verify-hash` | File hashing and verification |
| GnuPG signing/encryption | `c5dec crypto sign` / `verify-sig` / `encrypt` / `decrypt` | Asymmetric signing and file encryption |
| Shamir's Secret Sharing | `c5dec crypto shamir-split` / `shamir-recover` | (k,n)-threshold secret splitting |
| NaCl Ed25519 signing | `c5dec crypto nacl-keygen` / `nacl-sign` / `nacl-verify` | Fast elliptic-curve digital signatures |

### SHA-256 file integrity

Compute or verify the SHA-256 hash of any file. Useful for integrity checking
of SSDLC artefacts before publication or transmission.

```sh
# Compute hash
c5dec crypto hash path/to/file.pdf
# Output: 85fe13fb3d1135ee0bd0a4a02e1322df11804edcefd545f7c361e53a074d73de

# Verify hash
c5dec crypto verify-hash path/to/file.pdf 85fe13fb3d...
# Output: OK  (or MISMATCH on failure)
```

### GnuPG signing and encryption

Requires GnuPG (`gpg`) to be available on the system PATH. GnuPG is
pre-installed in the C5-DEC dev container.

```sh
# Create detached signature (default key)
c5dec crypto sign report.pdf -o report.pdf.sig

# Sign with a specific key
c5dec crypto sign report.pdf --key alice@example.com

# Verify detached signature
c5dec crypto verify-sig report.pdf report.pdf.sig

# Encrypt for one or more recipients
c5dec crypto encrypt sensitive.docx -r alice@example.com bob@example.com

# Decrypt (asymmetric — uses the default private key in the GPG keyring)
c5dec crypto decrypt sensitive.docx.gpg -o sensitive.docx

# Decrypt with passphrase (symmetric GPG encryption)
c5dec crypto decrypt symmetric-file.gpg -o output.txt --passphrase "my-passphrase"
```

To manage GPG keys, use the `gpg` command directly in the dev container:

```sh
gpg --list-keys          # list public keys
gpg --gen-key            # interactive key generation
gpg --import public.asc  # import a public key
```

### Shamir's Secret Sharing

Splits a hex-encoded secret into `n` shares, of which any `k` are sufficient
for reconstruction. Uses a Mersenne prime field GF(2^127 − 1) for cryptographic
security.

```sh
# Split a 32-bit secret into 5 shares (3 needed to reconstruct)
c5dec crypto shamir-split deadbeef -n 5 -k 3
# Output (one share per line):
# 1:749d9615e82fb71f6f92008c...
# 2:693b2c2bd05f6e3edf24011...
# ...

# Reconstruct from any 3 shares
c5dec crypto shamir-recover \
  "1:749d9615..." \
  "3:5dd8c241..." \
  "5:46af6557..."
# Output: deadbeef
```

**Security note**: the `secret_hex` value must represent an integer smaller than
2^127 − 1 (at most 126 bits, i.e., at most 32 hex characters). For larger
secrets, split them into 126-bit chunks or use GPG-based key wrapping.

### NaCl Ed25519 signing

Fast and secure digital signatures using the [PyNaCl](https://pynacl.readthedocs.io/)
Ed25519 implementation. Suitable for signing Doorstop review tokens, SBOM
attestations, or any small message.

```sh
# Generate a keypair
c5dec crypto nacl-keygen
# Output:
# verify_key:  <64-char hex>
# signing_key: <64-char hex>

# Sign a message
c5dec crypto nacl-sign "approved by alice" <signing_key_hex>
# Output: <hex-encoded signed message>

# Verify and recover the message
c5dec crypto nacl-verify <signed_hex> <verify_key_hex>
# Output: approved by alice
```

**Key management**: store `verify_key` (public) freely; keep `signing_key`
(private) secret, e.g., in an encrypted file or a GPG-encrypted store.

---

## Classical cryptography

Cryptography-related features of C5-DEC CAD are implemented via the integration of cryptographic software into the C5-DEC containerized development environment, i.e., via  the [development Dockerfile](https://github.com/AbstractionsLab/c5dec/blob/main/dev.Dockerfile) along with the VS Code [devcontainer.json](https://github.com/AbstractionsLab/c5dec/blob/main/.devcontainer/devcontainer.json) file. Please see the corresponding user manual [installation instructions](https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/installation.md#installation-in-a-containerized-development-environment) for more details.

The C5-DEC dev container (loaded in VS Code via the `dev.Dockerfile` specification), currently integrates the following pieces of cryptographic software for both `amd64` and `arm64` architectures:

- [GnuPG](https://gnupg.org/): installed in the C5-DEC dev container and directly accessible via the shell; you can run verify this, e.g., by running `gpg -h`. 
- [Kryptor](https://www.kryptor.co.uk/): installed in the C5-DEC dev container and directly accessible via the shell; you can verify e.g., by running `kryptor -h` for help.
- [Cryptomator CLI](https://github.com/cryptomator/cli): for unlocking and mounting already existing [Cryptomator](https://github.com/cryptomator/cryptomator) vaults (used for secure cloud storage); you can verify e.g., by running `cryptomator -h` for help.

To use the integrated cryptographic software, you can either run an interactive C5-DEC session using the `c5dec.sh` runner script:

```sh
./c5dec.sh session
```

Alternatively, open the the project repository in VS Code and select the "Reopen in Container" option in the notification that pops up in VS Code; or launch the command palette (Cmd/Ctrl+Shift+P) and select "Dev Containers: Reopen in Container" from the list of available commands. You will then be prompted to select a dev container configuration: the `C5-DEC CAD dev container` provides the bulk of the cryptographic functionality except for PQC support (see below).

## Post-quantum cryptography (PQC)

Finally, regarding **post-quantum cryptography (PQC)**, we currently support the use of a dedicated Docker container providing `OpenSSL` coupled with the `OQS-OpenSSL provider` from the [Open Quantum Safe](https://openquantumsafe.org/) project, powered by the `liboqs` library. The runner and its volume mapping provide an environment with [OpenSSL](https://docs.openssl.org/master/man7/ossl-guide-libcrypto-introduction/) and the [OQS-OpenSSL provider](https://github.com/open-quantum-safe/oqs-provider) preinstalled.

To use the PQC-enabled container, you can run an interactive C5-DEC session using the `c5dec.sh` runner script and the `pqc` argument:

```sh
./c5dec.sh pqc
```

Alternatively, you can use the `C5-DEC CAD cryptography dev container` option in VS Code.

See the user manual page providing instructions on how to [run the OQS-OpenSSL dev container in VS Code](./installation.md#c5-dec-post-quantum-cryptography-dev-container) for more details.

Once the container is running, you can use the `openssl` command line tool to generate and verify signatures, encrypt and decrypt messages, etc. This allows you to use post-quantum cryptography algorithms while benefitting from direct access to your host file system (thanks to volume mounting) such that files created or modified while using the `C5-DEC CAD dev container` remain accessible when using the `C5-DEC cryptography dev container`. To use the OQS-OpenSSL provider, we recommend consulting the [OQS-OpenSSL usage documentation](https://github.com/open-quantum-safe/oqs-provider/blob/main/USAGE.md#sample-commands).

For instance, to get a list of the available quantum-safe signature algorithms, you can run the following command in the terminal:

```sh
openssl list -signature-algorithms -provider oqsprovider
```

Similarly, to get a list of the available quantum-safe KEM algorithms, you can run:

```sh
openssl list -kem-algorithms -provider oqsprovider
```

## Post-Quantum end-to-end tunnels

When it comes to PQC-enabled network endpoints, we recommend the [PQConnect](https://www.pqconnect.net/) software developed by Daniel J. Bernstein et al.

Technical details can be found in the [PQConnect paper](https://www.pqconnect.net/pqconnect-20241206.pdf).

## Roadmap

Our future releases are expected to build on improved versions of the above-mentioned dependencies, with a preference for building on top of verified cryptographic implementations, e.g., see [EverCrypt](https://www.microsoft.com/en-us/research/publication/evercrypt-a-fast-veri%EF%AC%81ed-cross-platform-cryptographic-provider/) and [HACL*](https://hacl-star.github.io/HaclValeEverCrypt.html).