---
name: email-me
description: Send the athlete an email (subject + HTML body) through his own Gmail account, using the app-password credentials in .env. Defaults to emailing the athlete himself. Use when the athlete asks to email him something, send a training brief, digest, or summary to his inbox, or test that email sending works.
---

# email-me

Reusable way to send the athlete a real email from his own Gmail account.

## How it works

- Credentials: reads `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` from `.env` at
  the project root. Never print, log, or echo the app password anywhere in
  output.
- Transport: Gmail SMTP over SSL (`smtp.gmail.com:465`).
- Default recipient: The athlete's own `GMAIL_ADDRESS` — a brief, digest, or summary
  with no explicit recipient always goes to himself.
- Script: `.claude/skills/email-me/send_email.py` — reads a JSON payload from
  stdin: `{"subject": "...", "html_body": "...", "to": "optional override"}`.

## Usage

Run via Bash, piping JSON on stdin through a quoted heredoc (quoted so `$`
and backticks anywhere in the HTML are left alone by the shell):

```bash
python3 .claude/skills/email-me/send_email.py <<'PAYLOAD'
{"subject": "Your subject line", "html_body": "<h2>Heading</h2><p>Body text.</p>"}
PAYLOAD
```

- Keep HTML simple (headings, paragraphs, bold, lists) — this is a personal
  email, not a marketing template.
- Only set `"to"` when the athlete explicitly names a different recipient; otherwise
  omit it so it goes to the athlete.
- On success the script prints the recipient address only, never the
  credentials. Relay that confirmation back to the athlete in one line.
- If the script errors (bad credentials, network issue), surface the actual
  error message — don't guess at the cause.
