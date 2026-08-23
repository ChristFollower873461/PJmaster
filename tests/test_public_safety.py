from contextlib import redirect_stdout
from io import StringIO
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.scan_public_safety import is_luhn_valid, main, scan


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

    def test_scan_reports_match_metadata_without_sensitive_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            synthetic_value = "synthetic-sensitive-value-1234"
            key_name = "api" + "_key"
            (root / "settings.py").write_text(
                f'{key_name} = "{synthetic_value}"\n', encoding="utf-8"
            )
            output = StringIO()

            with patch("sys.argv", ["scan_public_safety.py", str(root)]):
                with redirect_stdout(output):
                    result = main()

        rendered = output.getvalue()
        self.assertEqual(result, 1)
        self.assertIn("settings.py", rendered)
        self.assertIn("generic api key assignment", rendered)
        self.assertNotIn(synthetic_value, rendered)

    def test_scan_flags_and_escapes_control_character_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "public.txt\nforged-row").write_text("Public handoff instructions\n")
            output = StringIO()

            findings = scan(root)
            with patch("sys.argv", ["scan_public_safety.py", str(root)]):
                with redirect_stdout(output):
                    result = main()

        self.assertIn("control character in path", [finding.kind for finding in findings])
        self.assertEqual(result, 1)
        self.assertIn(r"public.txt\nforged-row", output.getvalue())
        self.assertNotIn("public.txt\nforged-row", output.getvalue())


if __name__ == "__main__":
    unittest.main()
