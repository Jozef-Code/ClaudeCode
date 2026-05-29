from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from urllib.parse import quote_plus


@dataclass
class Company:
    lusha_id: str
    name: str
    domain: Optional[str]
    industry: Optional[str]
    location: Optional[str]
    employee_count: Optional[int]
    hiring_signals: list = field(default_factory=list)


@dataclass
class HiringManager:
    lusha_id: str
    first_name: str
    last_name: str
    full_name: str
    title: Optional[str]
    linkedin_url: Optional[str]
    email: Optional[str]
    company_name: str


@dataclass
class OutreachRecord:
    date: str
    company: Company
    hiring_manager: HiringManager
    inferred_role: str
    skill_1: str
    skill_2: str
    message: str
    job_url: str = ""
    status: str = "Te versturen"
    notes: str = ""

    def _build_job_search_url(self) -> str:
        if self.job_url:
            return self.job_url
        q = quote_plus(f'"{self.company.name}" {self.inferred_role}')
        return f"https://www.google.com/search?q=site:linkedin.com/jobs+{q}"

    def to_sheet_row(self) -> list:
        return [
            self.date,
            self.company.name,
            self.company.domain or "",
            self.company.industry or "",
            self.company.location or "",
            str(self.company.employee_count) if self.company.employee_count else "",
            self.hiring_manager.full_name,
            self.hiring_manager.title or "",
            self.hiring_manager.linkedin_url or "",
            self.hiring_manager.email or "",
            self.inferred_role,
            self._build_job_search_url(),
            self.message,
            self.status,
            self.notes,
        ]
