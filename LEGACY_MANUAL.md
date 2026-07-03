# Legacy Manual

This manual is the public-safe version of PJmaster. It tells the family how the plan is
organized without exposing the private contents.

## Roles

Fill these in only on a private copy or in the private vault.

- Primary family coordinator: `<private>`
- Backup family coordinator: `<private>`
- Executor or legal decision-maker: `<private>`
- Attorney: `<private>`
- Accountant: `<private>`
- Financial advisor: `<private>`
- Business operations contact: `<private>`
- Technical helper: `<private>`

## Private Records

The private vault should explain where to find:

- Will, trust, power of attorney, health directives, and related legal records.
- Tax records and accountant contact details.
- Insurance policies.
- Banking and investment records.
- Business ownership and operating records.
- Password manager recovery instructions.
- Device passcodes and recovery keys.
- Funeral, burial, memorial, or personal wishes.
- Letters, photos, and family notes that are not meant for the public internet.

Use [PRIVATE_VAULT_MANIFEST.template.md](PRIVATE_VAULT_MANIFEST.template.md) to keep that
private map consistent.

## Digital Life

Do not rush digital cleanup. Many services use email or phone access for recovery.

Important categories to inventory privately:

- Primary email accounts.
- Phone accounts.
- Password manager.
- Cloud storage.
- Domain names and DNS.
- Social media and creator accounts.
- GitHub and code repositories.
- Business software and customer systems.
- Payment processors and subscriptions.
- Computers, phones, tablets, drives, and security keys.

## Business And Customer Data

If there is any business data, assume it may include customer information, contracts,
payments, or confidential work.

Before moving or publishing anything:

1. Identify the owner.
2. Identify what contains customer data.
3. Preserve the data.
4. Do not email exports around casually.
5. Ask a qualified person before deleting accounts or changing access.

## Family Values And Intent

This section can be expanded over time with public-safe values:

- Keep the family calm and informed.
- Preserve what matters before optimizing anything.
- Avoid irreversible decisions in the first few days.
- Ask for help from professionals when legal, tax, business, medical, or security issues
  are involved.
- Treat private information like it belongs to the whole family, not the whole internet.

## Update Procedure

1. Edit the relevant template or doc.
2. Keep private details out of the public repo.
3. Run `make qa`.
4. Commit with a plain-language message.
5. Push to GitHub.
6. Rebuild the disc package with `make disc`.
7. Replace the old printed copy or CD label if the visible instructions changed.
