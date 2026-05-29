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

TODAY = "2026-05-29"

TEMPLATE = """Hi {first_name},

Wij kennen elkaar nog niet maar ik zag dat jullie op zoek waren naar een {role} met {skill_1} en {skill_2} ervaring.

Ik spreek momenteel een paar {role} die goed aansluiten op dit type omgeving, dus wilde even checken of jullie nog openstaan voor extra instroom naast jullie huidige traject.

Zelf kom ik ook uit de IT, dus ik kijk vrij inhoudelijk mee op dit soort rollen scheelt vaak in snelheid en kwaliteit van de match.

Als het relevant is, kom ik graag even kort (15 min) in contact hierover."""

BATCH = [
    {
        "company": ("92483026", "Piano", "piano.io", "Analytics SaaS / Digital Publishing", "Amsterdam, Nederland", 772),
        "manager": ("615109111", "Nick", "Worth", "Nick Worth", "Chief Executive Officer (Interim)", "https://www.linkedin.com/in/nickworth"),
        "role": "Senior Data Engineer", "skill_1": "Apache Spark & real-time analytics", "skill_2": "Python & Kafka pipelines",
    },
    {
        "company": ("41586938", "Leaseweb", "leaseweb.com", "Cloud Hosting & Infrastructure", "Amsterdam, Nederland", 657),
        "manager": ("534098164", "Sander", "Poelwijk", "Sander Poelwijk", "Chief Technology Officer", "https://www.linkedin.com/in/sander-poelwijk"),
        "role": "Cloud Infrastructure Engineer", "skill_1": "Kubernetes & Terraform", "skill_2": "bare-metal server automatisering",
    },
    {
        "company": ("33205306", "Slimstock", "slimstock.com", "Supply Chain Optimization Software", "Deventer, Nederland", 626),
        "manager": ("33938786", "Daan", "Majoor", "Daan Majoor", "Chief Technology Officer", "https://www.linkedin.com/in/daanmajoor"),
        "role": "Software Developer (C#/.NET)", "skill_1": "C# & .NET algoritmen", "skill_2": "supply chain & voorraadoptimalisatie",
    },
    {
        "company": ("22184160", "Sana Commerce", "sana-commerce.com", "B2B E-commerce Platform", "Rotterdam, Nederland", 404),
        "manager": ("283508432", "Iustina", "Pop", "Iustina Pop", "Senior Engineering Manager", "https://www.linkedin.com/in/iustinapop"),
        "role": ".NET Developer", "skill_1": "C# & Azure", "skill_2": "B2B e-commerce integraties",
    },
    {
        "company": ("68449286", "Sendcloud", "sendcloud.com", "Shipping & Logistics SaaS", "Eindhoven, Nederland", 427),
        "manager": ("101596618", "Bjorn", "Heesakkers", "Bjorn Heesakkers", "Vice President of Engineering", "https://www.linkedin.com/in/bheesakkers"),
        "role": "Backend Developer", "skill_1": "Python & microservices", "skill_2": "logistics API integraties",
    },
    {
        "company": ("17464440", "Bizzdesign", "bizzdesign.com", "Enterprise Architecture Software", "Enschede, Nederland", 440),
        "manager": ("548112276", "Tom", "Jansen", "Tom Jansen", "Chief Technology Officer", "https://www.linkedin.com/in/tpjjansen"),
        "role": "Software Engineer (C#)", "skill_1": "C# & .NET platform development", "skill_2": "enterprise architecture modeling",
    },
    {
        "company": ("9054785", "Ctac", "ctac.nl", "Microsoft & SAP Consulting", "'s-Hertogenbosch, Nederland", 550),
        "manager": ("363955493", "Rob", "Wismans", "Rob Wismans", "Director of Technology and Information Management", "https://www.linkedin.com/in/robwismans"),
        "role": "SAP Consultant", "skill_1": "SAP S/4HANA & cloud migratie", "skill_2": "ERP implementatie & integratie",
    },
    {
        "company": ("100395415", "Wortell", "wortell.nl", "Microsoft Cloud & Security", "Huizen, Nederland", 414),
        "manager": ("302829911", "Melvin", "Boer", "Melvin Boer", "Chief Executive Officer", "https://www.linkedin.com/in/melvindeboer"),
        "role": "Azure Cloud Engineer", "skill_1": "Microsoft 365 & Azure", "skill_2": "cloud security & compliance",
    },
    {
        "company": ("40986462", "DevOn", "devon.nl", "Software Development & IT", "Delft, Nederland", 535),
        "manager": ("269948593", "Peter", "Beijers", "Peter Beijers", "Managing Director", "https://www.linkedin.com/in/ppbeijers"),
        "role": "Java Developer", "skill_1": "Spring Boot & cloud-native", "skill_2": "software kwaliteit & DevOps",
    },
    {
        "company": ("14014374", "Rapid Circle", "rapidcircle.com", "Microsoft Cloud Consultancy", "Amsterdam, Nederland", 396),
        "manager": ("218424086", "Wilco", "Turnhout", "Wilco Turnhout", "Co-Founder & Chief Strategy Officer", "https://www.linkedin.com/in/wilcoturnhout"),
        "role": "Microsoft 365 Developer", "skill_1": "Power Platform & SharePoint", "skill_2": "Teams-integratie & workflow automatisering",
    },
    {
        "company": ("13136058", "SLTN", "sltn.nl", "IT Infrastructure & Managed Services", "Hilversum, Nederland", 842),
        "manager": ("71640348", "Eugene", "Tuijnman", "Eugene Tuijnman", "Founder & Chief Executive Officer", "https://www.linkedin.com/in/eugenetuijnman"),
        "role": "Cloud & Netwerk Engineer", "skill_1": "SD-WAN & Azure networking", "skill_2": "IT infrastructuurbeheer & managed services",
    },
    {
        "company": ("85826553", "Storio group", "storiogroup.com", "E-commerce Photo Platform", "Amsterdam, Nederland", 1085),
        "manager": ("652031000", "Emanuele", "Pane", "Emanuele Pane", "Engineering Director of Customer Experience", "https://www.linkedin.com/in/emanuelepane"),
        "role": "Senior Backend Engineer", "skill_1": "Kotlin/Java & distributed systems", "skill_2": "high-traffic platform & performance",
    },
    {
        "company": ("2872496", "Expereo", "expereo.com", "Global Cloud Networking", "Amsterdam, Nederland", 476),
        "manager": ("326874782", "Jean", "Avelange", "Jean Avelange", "Chief Information Officer", "https://www.linkedin.com/in/avelange"),
        "role": "Network Automation Engineer", "skill_1": "Python & Ansible", "skill_2": "MPLS & SD-WAN integratie",
    },
    {
        "company": ("27037520", "Creative Fabrica", "creativefabrica.com", "Design & AI Technology Platform", "Amsterdam, Nederland", 360),
        "manager": ("168228909", "Alvaro", "Caballero", "Alvaro Caballero", "Head of Human Resources", "https://www.linkedin.com/in/alvarocc"),
        "role": "Frontend Developer", "skill_1": "React & TypeScript", "skill_2": "design tool integratie & schaalbaarheid",
    },
    {
        "company": ("14423397", "Info Support", "infosupport.com", "Software Development & IT Consulting", "Veenendaal, Nederland", 691),
        "manager": ("46776398", "Lammert", "Vinke", "Lammert Vinke", "Managing Director", "https://www.linkedin.com/in/lammert-vinke-37779443"),
        "role": ".NET / C# Developer", "skill_1": "C# & Azure cloud", "skill_2": "agile software consultancy & delivery",
    },
    {
        "company": ("82183971", "SSC-ICT", "ssc-ict.nl", "Government IT Services", "Den Haag, Nederland", 1028),
        "manager": ("277635821", "Nardie", "Scharenborg", "Nardie Scharenborg", "Chief Technology Officer / Chief Information Officer", "https://www.linkedin.com/in/nardie-scharenborg-8828a311"),
        "role": "Cloud Engineer (Azure Government)", "skill_1": "Azure & overheids-cloudinfrastructuur", "skill_2": "IT werkplek & beveiligingsbeheer",
    },
    {
        "company": ("17996116", "Total Specific Solutions", "totalspecificsolutions.com", "Vertical Market Software", "Utrecht, Nederland", 443),
        "manager": ("212597224", "Maaike", "Kleingeld", "Maaike Kleingeld", "Head of Human Resources", "https://www.linkedin.com/in/maaikekleingeld"),
        "role": "Software Developer (C#/.NET)", "skill_1": "C# & .NET", "skill_2": "verticale markt software & SaaS migratie",
    },
    {
        "company": ("2935495", "Interstellar", "interstellar.nl", "IT Consulting & Software Development", "Delft, Nederland", 691),
        "manager": ("186765356", "Edwin", "Prinsen", "Edwin Prinsen", "Chief Executive Officer", "https://www.linkedin.com/in/edwinprinsen"),
        "role": "Full Stack Developer", "skill_1": "JavaScript/TypeScript & Node.js", "skill_2": "cloud-native applicaties & React",
    },
    {
        "company": ("20708590", "4PS", "4ps.nl", "Construction & Real Estate Software", "Ede, Nederland", 620),
        "manager": ("659299310", "Niels", "Blikman", "Niels Blikman", "Director of Product Technology", "https://www.linkedin.com/in/nielsblikman"),
        "role": "Dynamics 365 Developer", "skill_1": "Microsoft Dynamics 365 F&O", "skill_2": "bouw- & projectmanagementsoftware",
    },
    {
        "company": ("7719042", "Esprit ICT", "esprit-ict.nl", "IT Managed Services", "Veenendaal, Nederland", 617),
        "manager": ("472503557", "Emile", "Jongboer", "Emile Jongboer", "Chief Commercial Officer", "https://www.linkedin.com/in/emile-jongboer-b644223"),
        "role": "Cloud & Netwerk Consultant", "skill_1": "Cisco & Microsoft Azure", "skill_2": "IT managed services & monitoring",
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
            job_url=item.get("job_url", ""),
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
