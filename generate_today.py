#!/usr/bin/env python3
"""
Dagelijkse outreach batch runner.
Leest vandaag's batch uit today_batch.json (gegenereerd door Claude op basis van LinkedIn vacatures).

Gebruik: python generate_today.py
         python generate_today.py custom_batch.json
"""
import sys
import json
import os
from outreach.models import Company, HiringManager, OutreachRecord
from outreach.storage import save_outreach_record, get_contacted_company_ids, init_db
from outreach.sheets_exporter import records_to_csv, build_sheet_title

TEMPLATE = """Hi {first_name},

Wij kennen elkaar nog niet maar ik zag dat jullie op zoek waren naar een {role} met {skill_1} en {skill_2} ervaring.

Ik spreek momenteel een paar {role} die goed aansluiten op dit type omgeving, dus wilde even checken of jullie nog openstaan voor extra instroom naast jullie huidige traject.

Zelf kom ik ook uit de IT, dus ik kijk vrij inhoudelijk mee op dit soort rollen scheelt vaak in snelheid en kwaliteit van de match.

Als het relevant is, kom ik graag even kort (15 min) in contact hierover."""


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
    batch_file = sys.argv[1] if len(sys.argv) > 1 else "today_batch.json"
    if not os.path.exists(batch_file):
        print(f"Fout: {batch_file} niet gevonden.")
        print("Genereer eerst today_batch.json via Claude (draai de dagelijkse outreach pipeline).")
        sys.exit(1)

    init_db()
    date, entries = load_batch(batch_file)
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
