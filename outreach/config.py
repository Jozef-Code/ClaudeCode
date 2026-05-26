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
    "Bericht",
    "Status",
    "Notities",
]

MESSAGE_TEMPLATE = """Hi {hiring_manager_first_name},

Wij kennen elkaar nog niet maar ik zag dat jullie op zoek waren naar een {role_name} met {skill_1} en {skill_2} ervaring.

Ik spreek momenteel een paar {role_name} die goed aansluiten op dit type omgeving, dus wilde even checken of jullie nog openstaan voor extra instroom naast jullie huidige traject.

Zelf kom ik ook uit de IT, dus ik kijk vrij inhoudelijk mee op dit soort rollen scheelt vaak in snelheid en kwaliteit van de match.

Als het relevant is, kom ik graag even kort (15 min) in contact hierover."""
