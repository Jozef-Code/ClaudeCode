#!/usr/bin/env python3
"""
Voert de dagelijkse outreach pipeline uit.
Genereert berichten voor 20 IT bedrijven en slaat op in SQLite + Google Sheets.

Gebruik: python run_pipeline.py --data outreach_input.json
         python run_pipeline.py --demo  (voor test met hardcoded data)
"""
import sys
import json
import os
from datetime import datetime
from outreach.models import Company, HiringManager, OutreachRecord
from outreach.storage import save_outreach_record, get_contacted_company_ids, init_db
from outreach.message_generator import generate_message
from outreach.sheets_exporter import records_to_csv, build_sheet_title
from outreach.config import SHEET_HEADERS


def load_pipeline_data(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def process_pipeline(pipeline_data: list) -> list[OutreachRecord]:
    """Verwerk bedrijven+contacten naar OutreachRecords met gegenereerde berichten."""
    contacted_ids = get_contacted_company_ids()
    records = []

    for item in pipeline_data:
        company_data = item["company"]
        manager_data = item["manager"]

        # Skip al gecontacteerde bedrijven
        if company_data["lusha_id"] in contacted_ids:
            print(f"  [skip] {company_data['name']} - al gecontacteerd")
            continue

        company = Company(
            lusha_id=company_data["lusha_id"],
            name=company_data["name"],
            domain=company_data.get("domain"),
            industry=company_data.get("industry"),
            location=company_data.get("location"),
            employee_count=company_data.get("employee_count"),
        )
        manager = HiringManager(
            lusha_id=manager_data["lusha_id"],
            first_name=manager_data["first_name"],
            last_name=manager_data["last_name"],
            full_name=manager_data["full_name"],
            title=manager_data.get("title"),
            linkedin_url=manager_data.get("linkedin_url"),
            email=manager_data.get("email"),
            company_name=company.name,
        )

        print(f"  Genereer bericht voor {company.name} → {manager.full_name} ({manager.title})")
        record = generate_message(company, manager)
        save_outreach_record(record)
        records.append(record)
        print(f"    ✓ Opgeslagen")

    return records


def build_csv_content(records: list[OutreachRecord]) -> str:
    return records_to_csv(records)


if __name__ == "__main__":
    if "--data" in sys.argv:
        idx = sys.argv.index("--data")
        data_path = sys.argv[idx + 1]
        pipeline_data = load_pipeline_data(data_path)
    elif "--demo" in sys.argv:
        # Demo: gebruik outreach_input.json indien aanwezig
        if os.path.exists("outreach_input.json"):
            pipeline_data = load_pipeline_data("outreach_input.json")
        else:
            print("Geen outreach_input.json gevonden. Maak eerst een inputbestand aan.")
            sys.exit(1)
    else:
        print("Gebruik: python run_pipeline.py --data <pad> of --demo")
        sys.exit(1)

    init_db()
    print(f"\n=== IT Outreach Pipeline - {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    print(f"Verwerken van {len(pipeline_data)} bedrijven...\n")

    records = process_pipeline(pipeline_data)

    print(f"\n✓ {len(records)} berichten gegenereerd")

    # Sla CSV op voor gebruik door main script
    csv_content = build_csv_content(records)
    with open("outreach_output.csv", "w") as f:
        f.write(csv_content)
    print(f"✓ CSV opgeslagen: outreach_output.csv")
    print("\nKlaar! Upload outreach_output.csv naar Google Sheets.")
