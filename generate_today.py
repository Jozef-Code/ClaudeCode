#!/usr/bin/env python3
"""
Vandaag's outreach batch: 20 Nederlandse IT bedrijven met hiring managers en berichten.
Gegenereerd op 2026-05-26 door Next-Hire.nl outreach systeem.
"""
import sys
import os
from datetime import datetime
from outreach.models import Company, HiringManager, OutreachRecord
from outreach.storage import save_outreach_record, get_contacted_company_ids, init_db
from outreach.sheets_exporter import records_to_csv, build_sheet_title

TODAY = datetime.now().strftime("%Y-%m-%d")

TEMPLATE = """Hi {first_name},

Wij kennen elkaar nog niet maar ik zag dat jullie op zoek waren naar een {role} met {skill_1} en {skill_2} ervaring.

Ik spreek momenteel een paar {role} die goed aansluiten op dit type omgeving, dus wilde even checken of jullie nog openstaan voor extra instroom naast jullie huidige traject.

Zelf kom ik ook uit de IT, dus ik kijk vrij inhoudelijk mee op dit soort rollen scheelt vaak in snelheid en kwaliteit van de match.

Als het relevant is, kom ik graag even kort (15 min) in contact hierover."""

BATCH = [
    {
        "company": ("1330486", "Wolters Kluwer", "wolterskluwer.com", "Software Development", "Den Haag, Nederland", 23082),
        "manager": ("334874328", "Kees", "Voogd", "Kees Voogd", "Director of Software Engineering", "https://www.linkedin.com/in/kjvoogd"),
        "role": "Java Developer", "skill_1": "cloud-native development", "skill_2": "microservices architectuur",
    },
    {
        "company": ("8827713", "HERE Technologies", "here.com", "Software / Mapping Technology", "Eindhoven, Nederland", 9305),
        "manager": ("73607149", "Remco", "Timmer", "Remco Timmer", "Vice President of Product and Technology", "https://www.linkedin.com/in/remcotimmer"),
        "role": "Senior Backend Developer", "skill_1": "distributed systems", "skill_2": "real-time data verwerking",
    },
    {
        "company": ("24354355", "Croonwolter&dros", "croonwolterendros.nl", "IT Consulting & Engineering", "Rotterdam, Nederland", 2846),
        "manager": ("559426082", "Charlie", "Horst", "Charlie Horst", "Head of AI", "https://www.linkedin.com/in/charlie-ter-horst"),
        "role": "Machine Learning Engineer", "skill_1": "Python & MLOps", "skill_2": "computer vision / NLP",
    },
    {
        "company": ("33456041", "Getronics", "getronics.com", "IT Services & Consulting", "Duivendrecht, Nederland", 5273),
        "manager": ("79871653", "Stuart", "Deignan", "Stuart Deignan", "Chief Executive Officer", "https://www.linkedin.com/in/stuartdeignan"),
        "role": "Cloud Engineer", "skill_1": "Azure & AWS", "skill_2": "DevOps & automatisering",
    },
    {
        "company": ("6721780", "HSO", "hso.com", "Microsoft Consulting & IT Services", "Amsterdam, Nederland", 2968),
        "manager": ("29842967", "Freek", "Cox-Aloo", "Freek Cox-Aloo", "Director of Engagement, Data and AI", "https://www.linkedin.com/in/freekcox"),
        "role": "Azure Data Engineer", "skill_1": "Azure Data Factory & Synapse", "skill_2": "Power BI & datamodellering",
    },
    {
        "company": ("57306", "Centric", "centric.eu", "IT Services & Software", "Gouda, Nederland", 2822),
        "manager": ("563744547", "Aart", "Jochem", "Aart Jochem", "Chief Information Security Officer", "https://www.linkedin.com/in/aart-jochem-6812442"),
        "role": "Security Engineer", "skill_1": "cybersecurity & SIEM", "skill_2": "cloud security (Azure/AWS)",
    },
    {
        "company": ("14188140", "JetBrains", "jetbrains.com", "Software Development Tools", "Amsterdam, Nederland", 2887),
        "manager": ("2072099278", "Sergey", "Ignatov", "Sergey Ignatov", "Director of Engineering", "https://www.linkedin.com/in/sergey-ignatov"),
        "role": "Kotlin/JVM Developer", "skill_1": "compiler development", "skill_2": "IDE tooling & plugin development",
    },
    {
        "company": ("14129477", "Exact", "exact.com", "Business Software / ERP / SaaS", "Delft, Nederland", 2705),
        "manager": ("132224694", "Johan", "Gerritsen", "Johan Gerritsen", "Director of Technology", "https://www.linkedin.com/in/johan-gerrits-497a212"),
        "role": "Full Stack Developer", "skill_1": "React & TypeScript", "skill_2": ".NET Core & REST API's",
    },
    {
        "company": ("28385802", "Mews", "mews.com", "Hospitality SaaS / Cloud Software", "Amsterdam, Nederland", 1519),
        "manager": ("1778253", "Debora", "Gallo", "Debora Gallo", "Vice President of Talent Development", "https://www.linkedin.com/in/deboragallo"),
        "role": "Backend Developer (C#)", "skill_1": "C# & .NET", "skill_2": "Azure cloud & event-driven architectuur",
    },
    {
        "company": ("22106475", "Nebius", "nebius.com", "AI Cloud Infrastructure", "Amsterdam, Nederland", 1302),
        "manager": ("110570450", "Gabor", "Nemeth", "Gabor Nemeth", "Chief Information Officer", "https://www.linkedin.com/in/bagione"),
        "role": "Cloud Infrastructure Engineer", "skill_1": "Kubernetes & Terraform", "skill_2": "GPU-computing & HPC",
    },
    {
        "company": ("3999613", "Irdeto", "irdeto.com", "Digital Security / Media Technology", "Hoofddorp, Nederland", 1146),
        "manager": ("713647891", "Andy", "Shaffer", "Andy Shaffer", "Director of Cloud Engineering and DevOps", "https://www.linkedin.com/in/andy-shaffer-g1v3h0p3"),
        "role": "DevOps Engineer", "skill_1": "Kubernetes & CI/CD pipelines", "skill_2": "security-hardening & compliance",
    },
    {
        "company": ("1120583", "ICT Group", "ict.eu", "Industrial IT / Embedded Systems", "Barendrecht, Nederland", 2439),
        "manager": ("480835761", "Arjen", "De Blok", "Arjen De Blok", "Team Lead .NET/Azure", "https://www.linkedin.com/in/arjen-de-blok-b846b4"),
        "role": ".NET Developer", "skill_1": "C# & Azure", "skill_2": "embedded systems integratie",
    },
    {
        "company": ("2580938", "Simac", "simac.com", "IT Services & Infrastructure", "Veldhoven, Nederland", 1521),
        "manager": ("234628943", "Stefan", "Collet", "Stefan Collet", "Technology Lead", "https://www.linkedin.com/in/stefancollet"),
        "role": "Cloud Consultant", "skill_1": "Microsoft Azure", "skill_2": "netwerk- & infrastructuurbeheer",
    },
    {
        "company": ("2383709", "ORTEC", "ortec.com", "Operations Research / Analytics Software", "Zoetermeer, Nederland", 1202),
        "manager": ("1307145369", "Georgios", "Sarigiannidis", "Georgios Sarigiannidis", "Chief Executive Officer", "https://www.linkedin.com/in/georgiossarigiannidis"),
        "role": "Software Developer", "skill_1": "Python & C++ algoritmen", "skill_2": "optimalisatie & operations research",
    },
    {
        "company": ("1375142", "Levi9 Technology Services", "levi9.com", "Software Development & IT Consulting", "Amsterdam, Nederland", 1005),
        "manager": ("149755432", "Boudewijn", "Haas", "Boudewijn Haas", "Director of Cloud and Partnerships", "https://www.linkedin.com/in/boudewijnhaas"),
        "role": "Cloud Architect", "skill_1": "Azure & AWS", "skill_2": "microservices & cloud-native design",
    },
    {
        "company": ("33863869", "ilionx", "ilionx.com", "IT Consulting & Managed Services", "Utrecht, Nederland", 1282),
        "manager": ("256226489", "Anita", "Wartenbergh", "Anita Wartenbergh", "Director of Human Resources", "https://www.linkedin.com/in/anita-wartenbergh-6246154"),
        "role": "Java Developer", "skill_1": "Spring Boot & microservices", "skill_2": "cloud migratie & Agile",
    },
    {
        "company": ("16477447", "Axians NL", "axians.nl", "IT Infrastructure & Network Services", "Laren, Nederland", 1043),
        "manager": ("49846490", "Jeroen", "Kemps", "Jeroen Kemps", "Head of ICT", "https://www.linkedin.com/in/kaboem"),
        "role": "Netwerk Engineer", "skill_1": "Cisco & SD-WAN", "skill_2": "cloud networking & VMware NSX",
    },
    {
        "company": ("9356415", "Fellowmind", "fellowmind.com", "Microsoft Consulting / Business Applications", "Amersfoort, Nederland", 2081),
        "manager": ("591816798", "Anneke", "Nobel", "Anneke Nobel", "Chief Human Resources Officer", "https://www.linkedin.com/in/annekenobel"),
        "role": "Dynamics 365 Consultant", "skill_1": "Microsoft Dynamics 365 F&O", "skill_2": "Power Platform & Azure integratie",
    },
    {
        "company": ("1801173", "Topicus", "topicus.nl", "Software Development / Public Sector IT", "Deventer, Nederland", 945),
        "manager": ("504520182", "Gerben", "Hilberink", "Gerben Hilberink", "Managing Director", "https://www.linkedin.com/in/gerbenhilberink"),
        "role": "Java Developer", "skill_1": "Spring Boot & REST", "skill_2": "agile werken & clean code",
    },
    {
        "company": ("9453825", "ChipSoft Nederland", "chipsoft.nl", "Healthcare IT Software", "Amsterdam, Nederland", 996),
        "manager": ("123643407", "Myrthe", "Sennema", "Myrthe Sennema", "Head of Recruitment", "https://www.linkedin.com/in/myrthesennema"),
        "role": "Medische Softwareontwikkelaar", "skill_1": "HL7/FHIR & zorgstandaarden", "skill_2": "C# & .NET development",
    },
]


def build_records() -> list[OutreachRecord]:
    contacted = get_contacted_company_ids()
    records = []
    for item in BATCH:
        cid, cname, domain, industry, location, emp = item["company"]
        if cid in contacted:
            print(f"  [skip] {cname} - al gecontacteerd")
            continue

        company = Company(
            lusha_id=cid, name=cname, domain=domain, industry=industry,
            location=location, employee_count=emp,
        )
        mid, fname, lname, fullname, title, linkedin = item["manager"]
        manager = HiringManager(
            lusha_id=mid, first_name=fname, last_name=lname, full_name=fullname,
            title=title, linkedin_url=linkedin, email=None, company_name=cname,
        )
        message = TEMPLATE.format(
            first_name=fname, role=item["role"],
            skill_1=item["skill_1"], skill_2=item["skill_2"],
        )
        record = OutreachRecord(
            date=TODAY, company=company, hiring_manager=manager,
            inferred_role=item["role"], skill_1=item["skill_1"],
            skill_2=item["skill_2"], message=message,
        )
        save_outreach_record(record)
        records.append(record)
        print(f"  ✓ {cname} → {fullname} ({title}) | {item['role']}")

    return records


if __name__ == "__main__":
    init_db()
    print(f"\n=== IT Outreach Batch - {TODAY} ===")
    print(f"Genereer berichten voor {len(BATCH)} IT bedrijven in Nederland...\n")

    records = build_records()

    csv_content = records_to_csv(records)
    with open("outreach_output.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)

    print(f"\n✓ {len(records)} berichten klaar")
    print(f"✓ CSV opgeslagen: outreach_output.csv")
    print(f"\nSheet titel: {build_sheet_title()}")
