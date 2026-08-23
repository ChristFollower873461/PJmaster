import os
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

    def test_scan_flags_sensitive_filenames_and_unapproved_binaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env").write_text("PUBLIC_PLACEHOLDER=true\n")
            (root / "private.pdf").write_bytes(b"%PDF-synthetic")

            findings = scan(root)

        self.assertIn((".env", "sensitive filename"), {
            (finding.path.name, finding.kind) for finding in findings
        })
        self.assertIn(("private.pdf", "unapproved binary file"), {
            (finding.path.name, finding.kind) for finding in findings
        })

    def test_scan_allows_only_the_generated_cd_label_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            print_dir = root / "print"
            print_dir.mkdir()
            (print_dir / "PJmaster-CD-label.pdf").write_bytes(b"%PDF-synthetic")

            findings = scan(root)

        self.assertEqual(findings, [])

    def test_scan_flags_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "public.txt").write_text("Public handoff instructions\n")
            os.symlink(root / "public.txt", root / "linked.txt")

            findings = scan(root)

        self.assertIn(("linked.txt", "symbolic link"), {
            (finding.path.name, finding.kind) for finding in findings
        })

    def test_scan_flags_unknown_non_text_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "payload.bin").write_bytes(b"\xff\xfe\x00\x01")

            findings = scan(root)

        self.assertEqual([finding.kind for finding in findings], ["unreviewed non-text file"])


if __name__ == "__main__":
    unittest.main()
