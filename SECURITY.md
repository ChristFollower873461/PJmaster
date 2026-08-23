# Security and Privacy

PJmaster is public by design. Its primary security boundary is preventing private family, account, identity, legal, medical, financial, credential, and customer data from entering the repository or its generated disc package.

## Reporting

Report suspected vulnerabilities or private-data exposure through [GitHub private vulnerability reporting](https://github.com/ChristFollower873461/PJmaster/security/advisories/new). Do not place credentials, personal information, exploit details, or exposed records in a public issue.

If private reporting is unavailable, open a public issue that asks for a private maintainer contact without disclosing the sensitive details.

## Public-Safety Invariants

- Real private records belong outside this repository.
- The public scanner must fail closed on sensitive filenames, symbolic links, unapproved binary files, and recognized secret or personal-data patterns.
- The disc builder may package only Git-tracked regular files outside scanner-skipped generated or dependency directories, and must stop when the public-safety scan has findings or a tracked path would bypass scanner coverage.
- The generated CD label at `print/PJmaster-CD-label.pdf` is the only approved binary artifact in the repository.
- CI and local `make qa` runs must not upload the generated disc package or expose its contents in logs.

## Exposure Response

If sensitive data is committed, stop publishing and distributing the repository or disc package, revoke or rotate affected credentials, and use GitHub private reporting to coordinate cleanup. Removing a file in a later commit does not remove it from Git history; history rewriting or public-repository visibility changes require a separately reviewed incident plan.
