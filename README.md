# PJmaster

PJmaster is a public, CD-friendly family handoff repo.

It is meant to answer one question for family: "Where do we start, and what matters?"

This repo is intentionally safe to make public. It should not contain passwords, addresses,
account numbers, private medical details, private keys, recovery codes, bank data, or
anything that would hurt the family if copied by a stranger.

## Start Here

1. Read [FAMILY_START_HERE.md](FAMILY_START_HERE.md).
2. Use [LEGACY_MANUAL.md](LEGACY_MANUAL.md) as the family operating manual.
3. Keep private details in a separate vault, binder, safe, attorney file, or password
   manager. Use [PRIVATE_VAULT_MANIFEST.template.md](PRIVATE_VAULT_MANIFEST.template.md)
   to document where those private records live.
4. Run `make qa` before publishing updates.
5. Run `make disc` to build a local disc package and printable label.

If PDF generation fails because `reportlab` is missing, install the one dependency:

```bash
python3 -m pip install -r requirements.txt
```

`make qa` scans the working tree for recognized private-data patterns, sensitive
filenames, symbolic links, and unapproved binary files before building anything. The
disc builder then packages only Git-tracked regular files outside the scanner's
generated and dependency-directory exclusions. A tracked file under an excluded
directory stops the build. The generated `print/PJmaster-CD-label.pdf` is the
repository's only approved binary artifact.

Report a suspected vulnerability or accidental private-data exposure through
[GitHub private vulnerability reporting](https://github.com/ChristFollower873461/PJmaster/security/advisories/new),
not a public issue containing the sensitive details.

## What Belongs Here

- High-level family instructions.
- A calm first-week checklist.
- Public-safe templates for accounts, people, assets, documents, and devices.
- Notes about how to maintain this repo over time.
- A printable CD label and disc index.

## What Does Not Belong Here

- Passwords, API keys, seed phrases, private keys, or recovery codes.
- Full addresses, phone numbers, email addresses, birthdays, SSNs, or account numbers.
- Bank, insurance, legal, tax, medical, or identity documents.
- Anything that should only be seen by family, an attorney, executor, or trusted advisor.

## GitHub CD Form Notes

The Microsoft Form titled "GitHub Presents: Your Code, On a CD" asks for:

- GitHub username.
- Full public GitHub repo URL.
- Confirmation that you own the repo and grant permission to press it to a CD.
- Shipping name, email, country, address, and phone.

Use the public GitHub URL for this repo once it is published.

## Maintenance Rhythm

Review this repo at least twice a year:

- Around New Year.
- Around your birthday.
- After a major life event, move, business change, new account, new insurance policy,
  new device, or new attorney/executor decision.

The goal is not perfection. The goal is that the people who love you have a clear first
handle to grab when things are hard.
