# Maintenance

## Twice-Yearly Review

Review PJmaster twice a year.

- Confirm the public repo still has no private information.
- Confirm the private vault manifest is up to date.
- Confirm family coordinator roles are still correct.
- Confirm attorney, accountant, insurance, and technical helper references are current.
- Confirm the printed CD or USB copy still opens on a normal computer.

## Change Checklist

Before publishing:

1. Search for accidental private information.
2. Run `make qa`.
3. Rebuild disc artifacts with `make disc`.
4. Commit and push.
5. Replace any printed copy if the visible instructions changed.

## Public Safety Rule

If a note would help only family and could hurt if copied by a stranger, keep it out of
this repo. Put it in the private vault instead.
