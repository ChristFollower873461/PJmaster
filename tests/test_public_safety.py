import tempfile
import unittest
from pathlib import Path

from tools.scan_public_safety import is_luhn_valid, scan


class PublicSafetyScanTests(unittest.TestCase):
    def test_luhn_validates_payment_card_like_numbers(self):
        valid_number = " ".join(["4111", "1111", "1111", "1111"])
        invalid_number = " ".join(["4111", "1111", "1111", "1112"])

        self.assertTrue(is_luhn_valid(valid_number))
        self.assertFalse(is_luhn_valid(invalid_number))

    def test_scan_flags_private_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_token = "ghp_" + "abcdefghijklmnopqrstuvwxyz"
            key_name = "tok" + "en"
            (root / "README.md").write_text(f"{key_name} = '{fake_token}'\n")

            findings = scan(root)

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].kind, "github token")

    def test_scan_allows_public_safe_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Primary coordinator: <private>\n")

            findings = scan(root)

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
