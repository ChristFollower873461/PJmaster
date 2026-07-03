# QA Note

## Task

Create a public-safe `PJmaster` repo for a family handoff and GitHub CD submission.

## Risk Surfaces

- Privacy: the repo is intended to be public and must not contain sensitive family data.
- Operability: family should have a clear first-read path from a CD.
- Durability: generated artifacts should be reproducible from checked-in scripts.

## Required Checks

Run from the repo root:

```bash
make qa
```

Expected result:

- Unit tests pass.
- Public safety scan reports no findings.
- Disc zip, manifest, and printable CD label are generated.

## Gaps

The shipping form still requires owner-supplied shipping details and final submission.
