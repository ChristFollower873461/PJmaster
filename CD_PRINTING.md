# CD Printing

This repo is prepared for a public GitHub-to-CD submission.

## Public Repo URL

Once published, use:

`https://github.com/ChristFollower873461/PJmaster`

## Form Fields

The form asks for:

- GitHub username: `ChristFollower873461`
- Public repo URL: `https://github.com/ChristFollower873461/PJmaster`
- Ownership confirmation.
- Shipping name.
- Email.
- Country.
- Shipping address.
- Phone.

Only the owner should submit the shipping details.

## Local Disc Package

Run:

```bash
make disc
```

That creates:

- `dist/PJmaster-disc.zip`
- `dist/PJmaster-disc-manifest.txt`
- `print/PJmaster-CD-label.pdf`

The builder refuses to run when the public-safety scan has findings and includes only
Git-tracked regular files. Untracked workspace files and symbolic links are never disc
inputs.

## Physical Label

The printable PDF is a simple letter-size sheet with a disc outline. Print at 100 percent
scale if possible.

Do not use this repo or printed CD as the only copy of private records. Treat it as the
map, not the vault.
