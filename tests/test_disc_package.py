import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.build_disc_package import iter_files


class DiscPackageTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)

    def test_disc_inputs_include_only_git_tracked_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "public.txt").write_text("Public handoff instructions\n")
            (root / ".env").write_text("PASSWORD=synthetic-only\n")
            (root / "private.pdf").write_bytes(b"%PDF-synthetic")
            subprocess.run(["git", "add", "public.txt"], cwd=root, check=True)

            packaged = [path.relative_to(root).as_posix() for path in iter_files(root)]

        self.assertEqual(packaged, ["public.txt"])

    def test_disc_inputs_reject_tracked_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            (root / "public.txt").write_text("Public handoff instructions\n")
            os.symlink(root / "public.txt", root / "linked.txt")
            subprocess.run(["git", "add", "public.txt", "linked.txt"], cwd=root, check=True)

            with self.assertRaisesRegex(RuntimeError, "symbolic link"):
                list(iter_files(root))

    def test_disc_inputs_reject_tracked_files_in_scanner_skipped_directories(self):
        for directory in ("dist", "node_modules"):
            with self.subTest(directory=directory), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.init_repo(root)
                skipped_dir = root / directory
                skipped_dir.mkdir()
                skipped_file = skipped_dir / "private.txt"
                skipped_file.write_text("Synthetic private handoff\n")
                subprocess.run(
                    ["git", "add", "--force", skipped_file.relative_to(root)],
                    cwd=root,
                    check=True,
                )

                with self.assertRaisesRegex(
                    RuntimeError, "scanner-skipped directory"
                ):
                    list(iter_files(root))

    def test_disc_inputs_reject_control_character_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            unsafe_file = root / "public.txt\nforged-manifest-row"
            unsafe_file.write_text("Public handoff instructions\n")
            subprocess.run(["git", "add", unsafe_file.name], cwd=root, check=True)

            with self.assertRaisesRegex(RuntimeError, "control characters"):
                list(iter_files(root))


if __name__ == "__main__":
    unittest.main()
