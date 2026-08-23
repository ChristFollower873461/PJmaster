# Repo Map

## Root Files

- `README.md` - overview and public safety rules.
- `FAMILY_START_HERE.md` - first actions for family.
- `LEGACY_MANUAL.md` - public-safe family operating manual.
- `PRIVATE_VAULT_MANIFEST.template.md` - template for the private map.
- `CD_PRINTING.md` - GitHub CD form and local disc package notes.
- `MAINTENANCE.md` - review rhythm and publishing checklist.
- `Makefile` - local QA and disc packaging commands.

## Data Templates

The `data/` directory contains CSV templates. Keep real completed versions private unless
every entry is safe to publish.

## Tools

- `tools/scan_public_safety.py` checks for recognized secrets and private-data patterns,
  sensitive filenames, symbolic links, and unapproved binary files.
- `tools/build_disc_package.py` builds a local zip and manifest from Git-tracked regular
  files after the safety scan passes.
- `tools/create_cd_label.py` creates the printable CD label PDF.

## Tests

- `tests/test_public_safety.py` covers the safety scanner logic.
