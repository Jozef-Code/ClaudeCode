import csv
import io
from typing import List
from datetime import datetime
from .models import OutreachRecord
from .config import SHEET_HEADERS


def records_to_csv(records: List[OutreachRecord]) -> str:
    """Convert outreach records to CSV string for Google Sheets upload."""
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(SHEET_HEADERS)
    for record in records:
        writer.writerow(record.to_sheet_row())
    return output.getvalue()


def build_sheet_title() -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"IT Outreach Pipeline - {today}"
