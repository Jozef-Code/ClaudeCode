from dataclasses import dataclass, field
from typing import List

# Lusha industry IDs for IT targeting
IT_SUB_INDUSTRY_IDS = [
    103,  # IT Consulting & IT Services
    129,  # Software Development
    148,  # Computer Systems Architectural, Design & Services
    128,  # Computer & Network Security Services
]

# Recruitment companies to exclude
EXCLUDED_SUB_INDUSTRY_IDS = [
    9,    # Staffing & Recruiting
    99,   # Human Resources Services
]

EXCLUDED_MAIN_INDUSTRY_IDS = [
    # Only exclude if sub-industry is clearly recruitment
]

# IT main industry IDs to use as OR fallback
IT_MAIN_INDUSTRY_IDS = [
    17,   # Technology, Information & Media
]

# Seniority levels (Lusha IDs) for hiring managers
HIRING_MANAGER_SENIORITY_IDS = [
    5,    # Manager
    6,    # Director
    8,    # Vice President
    9,    # C-Suite
    10,   # Founder
]

# Departments to search for hiring managers
HIRING_MANAGER_DEPARTMENTS = [
    "Human Resources",
    "Engineering & Technical",
    "Information Technology",
    "General Management",
]

TARGET_LOCATION = {"country": "Netherlands"}
DAILY_TARGET = 20
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Google Sheets column headers
SHEET_HEADERS = [
    "Datum",
    "Bedrijf",
    "Website",
    "Industrie",
    "Locatie",
    "Medewerkers",
    "Hiring Manager",
    "Functietitel",
    "LinkedIn URL",
    "Email",
    "Rol waarvoor ze recruiten",
    "Vacature Link",
    "Bericht",
    "Status",
    "Notities",
]

MESSAGE_TEMPLATE = """Hi {hiring_manager_first_name},

Ik zag dat jullie zoeken naar een {role_name} — ik spreek op dit moment een aantal sterke kandidaten met {skill_1} en {skill_2} achtergrond die actief op zoek zijn.

Kan ik je een korte samenvatting sturen van het meest passende profiel?

Met vriendelijke groet,
Jozef
Next-Hire | jozef@next-hire.nl"""

# Keywords that indicate a recruitment/staffing agency — exclude these from outreach
AGENCY_KEYWORDS = [
    "recruitment", "staffing", "werving", "uitzend",
    "detachering", "payroll", "headhunt", "personeelsdienst",
]

# IT roles to search on Indeed.nl (used by Claude when building today_batch.json)
INDEED_ROLES = [
    "developer",
    "security engineer",
    "DevOps engineer",
    "tech lead",
    "security officer",
    "software engineer",
    "applicatiebeheerder",
]
