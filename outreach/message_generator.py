import anthropic
import os
from .config import MESSAGE_TEMPLATE, CLAUDE_MODEL
from .models import Company, HiringManager, OutreachRecord
from datetime import datetime


def _client():
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def infer_role_and_skills(company: Company, manager: HiringManager) -> dict:
    """Use Claude to infer the most likely IT role and skills based on company profile."""
    client = _client()
    prompt = f"""Je bent een IT recruitment specialist in Nederland.

Geef op basis van dit bedrijfsprofiel een waarschijnlijke IT-rol waarvoor ze recruiten en 2 belangrijke skills.

Bedrijf: {company.name}
Industrie: {company.industry or 'IT'}
Locatie: {company.location or 'Nederland'}
Medewerkers: {company.employee_count or 'onbekend'}
Hiring manager titel: {manager.title or 'onbekend'}

Antwoord ALLEEN met dit JSON formaat (geen uitleg):
{{
  "role": "exacte functienaam in het Nederlands of Engels (bijv. Java Developer, DevOps Engineer)",
  "skill_1": "eerste belangrijke technische skill",
  "skill_2": "tweede belangrijke technische skill"
}}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        text = response.content[0].text.strip()
        # Extract JSON if wrapped in markdown
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        return json.loads(text)
    except Exception:
        return {
            "role": "IT Consultant",
            "skill_1": "cloud-infrastructuur",
            "skill_2": "agile werkmethoden"
        }


def generate_message(
    company: Company,
    manager: HiringManager,
) -> OutreachRecord:
    """Generate a personalized outreach message for a hiring manager."""
    role_data = infer_role_and_skills(company, manager)

    first_name = manager.first_name or manager.full_name.split()[0]

    message = MESSAGE_TEMPLATE.format(
        hiring_manager_first_name=first_name,
        role_name=role_data["role"],
        skill_1=role_data["skill_1"],
        skill_2=role_data["skill_2"],
    )

    return OutreachRecord(
        date=datetime.now().strftime("%Y-%m-%d"),
        company=company,
        hiring_manager=manager,
        inferred_role=role_data["role"],
        skill_1=role_data["skill_1"],
        skill_2=role_data["skill_2"],
        message=message,
    )
