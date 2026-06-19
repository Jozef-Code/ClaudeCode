import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .models import OutreachRecord

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SUBJECT = "Kandidaat voor jullie {role} functie | Next-Hire"


def _subject(role: str) -> str:
    return EMAIL_SUBJECT.format(role=role)


def _build_message(record: OutreachRecord, gmail_user: str, from_name: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = _subject(record.inferred_role)
    msg["From"] = formataddr((from_name, gmail_user))
    msg["To"] = record.hiring_manager.email
    msg.attach(MIMEText(record.message, "plain", "utf-8"))
    return msg


def _preview(record: OutreachRecord) -> str:
    lines = [
        f"  Aan:       {record.hiring_manager.email}",
        f"  Bedrijf:   {record.company.name} → {record.hiring_manager.full_name}",
        f"  Onderwerp: {_subject(record.inferred_role)}",
        "  " + "-" * 50,
    ]
    for line in record.message.splitlines():
        lines.append(f"  {line}")
    return "\n".join(lines)


def send_batch(records: List[OutreachRecord], dry_run: bool = False) -> dict:
    """Show preview, ask confirmation, then send via Gmail SMTP.

    Returns {"sent": int, "skipped": int, "failed": list[str]}
    """
    sendable = [r for r in records if r.hiring_manager.email]
    skipped = len(records) - len(sendable)

    if not sendable:
        print("Geen records met e-mailadres gevonden — niets te versturen.")
        return {"sent": 0, "skipped": skipped, "failed": []}

    print(f"\n{'=' * 60}")
    print(f"  E-mail Preview — {len(sendable)} berichten")
    print(f"{'=' * 60}\n")
    for i, record in enumerate(sendable, 1):
        print(f"[{i}/{len(sendable)}]")
        print(_preview(record))
        print()

    if dry_run:
        print("[DRY RUN] Geen e-mails verstuurd.")
        return {"sent": 0, "skipped": skipped, "failed": []}

    answer = input(f"Verstuur {len(sendable)} e-mails? [j/N] ").strip().lower()
    if answer not in ("j", "ja", "y", "yes"):
        print("Geannuleerd — geen e-mails verstuurd.")
        return {"sent": 0, "skipped": skipped, "failed": []}

    gmail_user = os.environ.get("GMAIL_USER", "")
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    from_name = os.environ.get("GMAIL_FROM_NAME", "Next-Hire")

    if not gmail_user or not app_password:
        raise EnvironmentError(
            "GMAIL_USER en/of GMAIL_APP_PASSWORD niet ingesteld in .env\n"
            "Zie .env.example voor instructies."
        )

    sent_count = 0
    failed: List[str] = []

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmail_user, app_password)

        for record in sendable:
            try:
                msg = _build_message(record, gmail_user, from_name)
                smtp.sendmail(gmail_user, record.hiring_manager.email, msg.as_string())
                sent_count += 1
                print(f"  [ok] {record.company.name} → {record.hiring_manager.email}")
            except Exception as e:
                failed.append(record.hiring_manager.email)
                print(f"  [err] {record.company.name}: {e}")

    return {"sent": sent_count, "skipped": skipped, "failed": failed}
