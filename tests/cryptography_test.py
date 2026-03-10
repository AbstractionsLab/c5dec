import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import c5dec.core.cryptography as crypto
from c5dec import common


# ---------------------------------------------------------------------------
# 1. SHA-256 File Integrity
# ---------------------------------------------------------------------------

class TestComputeHash(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.write(b"hello world")
        self.tmp.flush()
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_known_digest(self):
        expected = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(crypto.compute_hash(self.path), expected)

    def test_empty_file(self):
        empty = tempfile.NamedTemporaryFile(delete=False)
        empty.close()
        try:
            result = crypto.compute_hash(empty.name)
            self.assertEqual(result, hashlib.sha256(b"").hexdigest())
        finally:
            os.unlink(empty.name)

    def test_nonexistent_file_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.compute_hash("/nonexistent/path/file.bin")

    def test_returns_lowercase_hex(self):
        result = crypto.compute_hash(self.path)
        self.assertEqual(result, result.lower())
        int(result, 16)  # must be valid hex


class TestVerifyHash(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.write(b"test data")
        self.tmp.flush()
        self.tmp.close()
        self.path = self.tmp.name
        self.correct_hash = hashlib.sha256(b"test data").hexdigest()

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_matching_hash_returns_true(self):
        self.assertTrue(crypto.verify_hash(self.path, self.correct_hash))

    def test_matching_hash_case_insensitive(self):
        self.assertTrue(crypto.verify_hash(self.path, self.correct_hash.upper()))

    def test_wrong_hash_returns_false(self):
        self.assertFalse(crypto.verify_hash(self.path, "a" * 64))

    def test_propagates_error_for_missing_file(self):
        with self.assertRaises(common.C5decError):
            crypto.verify_hash("/no/such/file", self.correct_hash)


# ---------------------------------------------------------------------------
# 2. GnuPG helpers
# ---------------------------------------------------------------------------

class TestRunGpg(unittest.TestCase):
    @patch("c5dec.core.cryptography.subprocess.run")
    def test_gpg_not_found_raises(self, mock_run):
        mock_run.side_effect = FileNotFoundError
        with self.assertRaises(common.C5decError):
            crypto._run_gpg(["--version"])

    @patch("c5dec.core.cryptography.subprocess.run")
    def test_nonzero_exit_raises(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(2, "gpg", stderr="error")
        with self.assertRaises(common.C5decError):
            crypto._run_gpg(["--sign", "file.txt"])

    @patch("c5dec.core.cryptography.subprocess.run")
    def test_success_returns_completed_process(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = crypto._run_gpg(["--version"])
        self.assertEqual(result.returncode, 0)


class TestGpgSignFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.write(b"data to sign")
        self.tmp.flush()
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)
        sig = self.path + ".sig"
        if os.path.exists(sig):
            os.unlink(sig)

    def test_missing_file_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.gpg_sign_file("/nonexistent/file.txt")

    @patch("c5dec.core.cryptography._run_gpg")
    def test_default_sig_path(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        result = crypto.gpg_sign_file(self.path)
        self.assertEqual(result, self.path + ".sig")

    @patch("c5dec.core.cryptography._run_gpg")
    def test_custom_output_path(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        custom = self.path + ".custom.sig"
        result = crypto.gpg_sign_file(self.path, output_path=custom)
        self.assertEqual(result, custom)

    @patch("c5dec.core.cryptography._run_gpg")
    def test_key_id_included_in_args(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        crypto.gpg_sign_file(self.path, key_id="DEADBEEF")
        call_args = mock_gpg.call_args[0][0]
        self.assertIn("--local-user", call_args)
        self.assertIn("DEADBEEF", call_args)


class TestGpgVerifySignature(unittest.TestCase):
    @patch("c5dec.core.cryptography._run_gpg")
    def test_returns_true_on_success(self, mock_gpg):
        mock_gpg.return_value = MagicMock(returncode=0)
        self.assertTrue(crypto.gpg_verify_signature("file.txt", "file.txt.sig"))

    @patch("c5dec.core.cryptography._run_gpg")
    def test_returns_false_on_failure(self, mock_gpg):
        mock_gpg.return_value = MagicMock(returncode=2, stderr="bad sig")
        self.assertFalse(crypto.gpg_verify_signature("file.txt", "file.txt.sig"))


class TestGpgEncryptFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.write(b"secret content")
        self.tmp.flush()
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_missing_file_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.gpg_encrypt_file("/no/such/file.txt", ["alice@example.com"])

    def test_empty_recipients_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.gpg_encrypt_file(self.path, [])

    @patch("c5dec.core.cryptography._run_gpg")
    def test_default_output_path(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        result = crypto.gpg_encrypt_file(self.path, ["alice@example.com"])
        self.assertEqual(result, self.path + ".gpg")

    @patch("c5dec.core.cryptography._run_gpg")
    def test_multiple_recipients_in_args(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        crypto.gpg_encrypt_file(self.path, ["alice@example.com", "bob@example.com"])
        call_args = mock_gpg.call_args[0][0]
        self.assertEqual(call_args.count("--recipient"), 2)


class TestGpgDecryptFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".gpg", delete=False)
        self.tmp.write(b"encrypted bytes")
        self.tmp.flush()
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_missing_file_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.gpg_decrypt_file("/no/such/file.gpg")

    @patch("c5dec.core.cryptography._run_gpg")
    def test_default_output_strips_gpg_suffix(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        result = crypto.gpg_decrypt_file(self.path)
        self.assertFalse(result.endswith(".gpg"))

    @patch("c5dec.core.cryptography._run_gpg")
    def test_passphrase_included_in_args(self, mock_gpg):
        mock_gpg.return_value = MagicMock()
        crypto.gpg_decrypt_file(self.path, passphrase="s3cr3t")
        call_args = mock_gpg.call_args[0][0]
        self.assertIn("--passphrase", call_args)
        self.assertIn("s3cr3t", call_args)

    @patch("c5dec.core.cryptography._run_gpg")
    def test_non_gpg_extension_gets_dec_suffix(self, mock_gpg):
        tmp = tempfile.NamedTemporaryFile(suffix=".enc", delete=False)
        tmp.write(b"data")
        tmp.flush()
        tmp.close()
        try:
            mock_gpg.return_value = MagicMock()
            result = crypto.gpg_decrypt_file(tmp.name)
            self.assertTrue(result.endswith(".dec"))
        finally:
            os.unlink(tmp.name)


# ---------------------------------------------------------------------------
# 3. Shamir's Secret Sharing
# ---------------------------------------------------------------------------

class TestSplitSecret(unittest.TestCase):
    def test_basic_split_returns_n_shares(self):
        shares = crypto.split_secret("deadbeef", 5, 3)
        self.assertEqual(len(shares), 5)

    def test_share_format(self):
        shares = crypto.split_secret("cafebabe", 3, 2)
        for share in shares:
            idx, val = share.split(":")
            self.assertTrue(idx.isdigit())
            int(val, 16)  # must be valid hex

    def test_share_indices_are_sequential_from_one(self):
        shares = crypto.split_secret("ff", 4, 2)
        indices = [int(s.split(":")[0]) for s in shares]
        self.assertEqual(indices, [1, 2, 3, 4])

    def test_threshold_less_than_two_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.split_secret("ff", 3, 1)

    def test_k_greater_than_n_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.split_secret("ff", 2, 5)

    def test_secret_too_large_raises(self):
        too_large = hex(crypto._SHAMIR_PRIME + 1)[2:]
        with self.assertRaises(common.C5decError):
            crypto.split_secret(too_large, 3, 2)

    def test_different_splits_produce_different_shares(self):
        shares_a = crypto.split_secret("abcdef", 3, 2)
        shares_b = crypto.split_secret("abcdef", 3, 2)
        # Randomised coefficients mean shares differ almost certainly
        self.assertNotEqual(shares_a, shares_b)


class TestRecoverSecret(unittest.TestCase):
    def test_roundtrip_exact_threshold(self):
        original = "aabbccdd"
        shares = crypto.split_secret(original, 5, 3)
        recovered = crypto.recover_secret(shares[:3])
        self.assertEqual(recovered, original)

    def test_roundtrip_all_shares(self):
        original = "1a2b3c"
        shares = crypto.split_secret(original, 4, 2)
        recovered = crypto.recover_secret(shares)
        self.assertEqual(recovered, original)

    def test_any_k_subset_recovers(self):
        original = "fedcba98"
        shares = crypto.split_secret(original, 5, 3)
        for combo in [shares[0:3], shares[1:4], shares[2:5]]:
            self.assertEqual(crypto.recover_secret(combo), original)

    def test_too_few_shares_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.recover_secret(["1:abcd"])

    def test_malformed_share_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.recover_secret(["not-a-share", "also-bad"])

    def test_wrong_format_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.recover_secret(["1:zzzz", "2:ffff"])


# ---------------------------------------------------------------------------
# 4. PyNaCl Ed25519 Signing
# ---------------------------------------------------------------------------

class TestNaclKeygenSigning(unittest.TestCase):
    def test_returns_two_hex_strings(self):
        vk, sk = crypto.nacl_keygen_signing()
        self.assertIsInstance(vk, str)
        self.assertIsInstance(sk, str)
        int(vk, 16)
        int(sk, 16)

    def test_verify_key_length(self):
        vk, _ = crypto.nacl_keygen_signing()
        self.assertEqual(len(vk), 64)  # 32 bytes → 64 hex chars

    def test_signing_key_length(self):
        _, sk = crypto.nacl_keygen_signing()
        self.assertEqual(len(sk), 64)

    def test_each_call_produces_unique_keys(self):
        vk1, sk1 = crypto.nacl_keygen_signing()
        vk2, sk2 = crypto.nacl_keygen_signing()
        self.assertNotEqual(sk1, sk2)
        self.assertNotEqual(vk1, vk2)


class TestNaclSign(unittest.TestCase):
    def setUp(self):
        self.vk_hex, self.sk_hex = crypto.nacl_keygen_signing()

    def test_sign_returns_bytes(self):
        result = crypto.nacl_sign(b"hello", self.sk_hex)
        self.assertIsInstance(result, bytes)

    def test_signed_longer_than_original(self):
        msg = b"test message"
        signed = crypto.nacl_sign(msg, self.sk_hex)
        self.assertGreater(len(signed), len(msg))

    def test_invalid_key_raises(self):
        with self.assertRaises(common.C5decError):
            crypto.nacl_sign(b"data", "not_a_valid_hex_key")


class TestNaclVerify(unittest.TestCase):
    def setUp(self):
        self.vk_hex, self.sk_hex = crypto.nacl_keygen_signing()
        self.message = b"unit test payload"
        self.signed = crypto.nacl_sign(self.message, self.sk_hex)

    def test_verify_returns_original_message(self):
        result = crypto.nacl_verify(self.signed, self.vk_hex)
        self.assertEqual(result, self.message)

    def test_verify_wrong_key_raises(self):
        vk2, _ = crypto.nacl_keygen_signing()
        with self.assertRaises(common.C5decError):
            crypto.nacl_verify(self.signed, vk2)

    def test_verify_tampered_message_raises(self):
        tampered = bytearray(self.signed)
        tampered[-1] ^= 0xFF
        with self.assertRaises(common.C5decError):
            crypto.nacl_verify(bytes(tampered), self.vk_hex)

    def test_verify_empty_message(self):
        signed_empty = crypto.nacl_sign(b"", self.sk_hex)
        result = crypto.nacl_verify(signed_empty, self.vk_hex)
        self.assertEqual(result, b"")


if __name__ == "__main__":
    unittest.main()
