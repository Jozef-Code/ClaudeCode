#!/usr/bin/env python3
"""
IT Outreach Pipeline - Next-Hire.nl
Dagelijks 20 IT bedrijven vinden, hiring managers identificeren, berichten genereren.
"""
import sys
import json
from outreach.storage import get_stats, init_db, get_contacted_company_ids


def cmd_status():
    init_db()
    stats = get_stats()
    print(f"\n=== IT Outreach Pipeline Status ===")
    print(f"Totaal gecontacteerde bedrijven: {stats['total_contacted']}")
    print(f"Vandaag gecontacteerd: {stats['contacted_today']}")
    if stats['by_status']:
        print("\nStatus verdeling:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count}")
    contacted_ids = get_contacted_company_ids()
    if contacted_ids:
        print(f"\nGecontacteerde Lusha IDs (voor deduplicatie):")
        for id_ in list(contacted_ids)[:5]:
            print(f"  - {id_}")
        if len(contacted_ids) > 5:
            print(f"  ... en {len(contacted_ids) - 5} meer")


def cmd_contacted_ids():
    """Print contacted company IDs as JSON (for pipeline deduplication)."""
    init_db()
    ids = get_contacted_company_ids()
    print(json.dumps(list(ids)))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "status":
        cmd_status()
    elif sys.argv[1] == "contacted-ids":
        cmd_contacted_ids()
    else:
        print(f"Onbekend commando: {sys.argv[1]}")
        print("Gebruik: python main.py [status|contacted-ids]")
        sys.exit(1)
