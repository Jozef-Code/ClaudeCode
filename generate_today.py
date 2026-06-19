#!/usr/bin/env python3
"""
Dagelijkse outreach batch runner.
Leest vandaag's batch uit today_batch.json (gegenereerd door Claude op basis van Indeed vacatures).

Gebruik:
  python generate_today.py                    # genereer CSV
  python generate_today.py --send             # genereer + verstuur e-mails
  python generate_today.py --dry-run          # genereer + preview (geen verzending)
  python generate_today.py custom_batch.json  # gebruik ander batchbestand
"""
import sys
import json
import os
import argparse
from outreach.models import Company, HiringManager, OutreachRecord
from outreach.storage import save_outreach_record, get_contacted_company_ids, init_db
from outreach.sheets_exporter import records_to_csv, build_sheet_title

TEMPLATE = """Hi {first_name},

Ik zag dat jullie zoeken naar een {role} — ik spreek op dit moment een aantal sterke kandidaten met {skill_1} en {skill_2} achtergrond die actief op zoek zijn.

Kan ik je een korte samenvatting sturen van het meest passende profiel?

Met vriendelijke groet,
Jozef
Next-Hire | jozef@next-hire.nl"""


def load_batch(path: str = "today_batch.json") -> tuple[str, list]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["date"], data["entries"]


def build_records(date: str, entries: list) -> list[OutreachRecord]:
    contacted = get_contacted_company_ids()
    records = []

    for item in entries:
        c = item["company"]
        m = item["manager"]

        if c["lusha_id"] in contacted:
            print(f"  [skip] {c['name']} - al gecontacteerd")
            continue

        company = Company(
            lusha_id=c["lusha_id"],
            name=c["name"],
            domain=c.get("domain"),
            industry=c.get("industry"),
            location=c.get("location"),
            employee_count=c.get("employee_count"),
        )
        manager = HiringManager(
            lusha_id=m["lusha_id"],
            first_name=m["first_name"],
            last_name=m["last_name"],
            full_name=m["full_name"],
            title=m.get("title"),
            linkedin_url=m.get("linkedin_url"),
            email=m.get("email"),
            company_name=company.name,
        )
        message = TEMPLATE.format(
            first_name=m["first_name"],
            role=item["role"],
            skill_1=item["skill_1"],
            skill_2=item["skill_2"],
        )
        record = OutreachRecord(
            date=date,
            company=company,
            hiring_manager=manager,
            inferred_role=item["role"],
            skill_1=item["skill_1"],
            skill_2=item["skill_2"],
            message=message,
            job_url=item.get("job_url", ""),
        )
        save_outreach_record(record)
        records.append(record)
        print(f"  ✓ {company.name} → {manager.full_name} ({manager.title}) | {item['role']}")

    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outreach batch verwerker")
    parser.add_argument(
        "batch_file",
        nargs="?",
        default="today_batch.json",
        help="Pad naar het batchbestand (standaard: today_batch.json)",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Verstuur e-mails na het genereren (vraagt om bevestiging)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Toon e-mail preview zonder daadwerkelijk te versturen",
    )
    args = parser.parse_args()

    if not os.path.exists(args.batch_file):
        print(f"Fout: {args.batch_file} niet gevonden.")
        print("Genereer eerst today_batch.json via Claude (draai de dagelijkse outreach pipeline).")
        sys.exit(1)

    init_db()
    date, entries = load_batch(args.batch_file)
    print(f"\n=== IT Outreach Batch - {date} ===")
    print(f"Verwerken van {len(entries)} bedrijven...\n")

    records = build_records(date, entries)

    if not records:
        print("\nGeen nieuwe bedrijven om te verwerken.")
        sys.exit(0)

    csv_content = records_to_csv(records)
    with open("outreach_output.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)

    print(f"\n✓ {len(records)} berichten klaar")
    print(f"✓ CSV opgeslagen: outreach_output.csv")
    print(f"\nSheet titel: {build_sheet_title(date)}")

    if args.send or args.dry_run:
        from outreach.gmail_sender import send_batch
        from outreach.storage import update_record_status

        result = send_batch(records, dry_run=args.dry_run)

        if not args.dry_run and result["sent"] > 0:
            for record in records:
                email = record.hiring_manager.email
                if email and email not in result["failed"]:
                    update_record_status(record.company.lusha_id, "Verstuurd")

        print(
            f"\n[email] Verstuurd: {result['sent']} | "
            f"Overgeslagen: {result['skipped']} | "
            f"Mislukt: {len(result['failed'])}"
        )
