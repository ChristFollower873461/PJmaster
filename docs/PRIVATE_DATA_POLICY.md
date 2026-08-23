# Private Data Policy

This repo is public by design. The family handoff system is split into two parts:

1. Public repo: instructions, templates, maintenance process, and CD-safe artifacts.
2. Private vault: real names, addresses, account details, passwords, legal records,
   medical information, family letters, and sensitive business data.

## Never Commit

- Passwords, passphrases, recovery codes, or seed phrases.
- API keys, access tokens, private keys, certificates, or `.env` files.
- Account numbers, SSNs, tax IDs, routing numbers, or payment card numbers.
- Full personal contact records.
- Medical, legal, financial, customer, or identity documents.
- Private family letters or photos.

## Before Every Push

Run:

```bash
make qa
```

If the scanner flags something, treat it as a stop sign until reviewed.

The scanner also stops on sensitive filenames, symbolic links, and binary files other
than the generated CD label. Disc packaging is restricted to Git-tracked regular files,
but an unsafe untracked file in the repository workspace still blocks the build so it
cannot be overlooked during review.

## When In Doubt

If the content answers "what private thing is it?" instead of "where should family look
for the private thing?", keep it out of this repo.
