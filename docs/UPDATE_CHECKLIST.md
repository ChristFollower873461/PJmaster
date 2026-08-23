# Update Checklist

Use this before publishing changes.

1. Read the changed files.
2. Confirm no private data is included.
3. Confirm any new binary file or symbolic link is removed; only the generated CD label
   is approved as a binary repository artifact.
4. Run `make qa`.
5. Review `dist/PJmaster-disc-manifest.txt` and confirm every entry is intended and
   Git-tracked.
6. Open `print/PJmaster-CD-label.pdf`.
7. Commit with a clear message.
8. Push to GitHub only after CI passes.
9. If a physical disc or printed label exists, decide whether it needs replacement.
