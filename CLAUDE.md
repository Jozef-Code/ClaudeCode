# Next-Hire Outreach Pipeline

## What this project does
Automated B2B outreach for Next-Hire (IT recruitment agency). Each day Claude builds a batch of 20 Dutch IT companies that are actively hiring, finds the right contact person, and sends a personalised Dutch-language email via Gmail SMTP.

---

## Daily workflow

```
1. "Draai vandaag's batch" → Claude builds today_batch.json (see below)
2. python generate_today.py          → generates CSV, saves to SQLite
   python generate_today.py --send   → generate + preview + send emails
   python generate_today.py --dry-run → preview only, no SMTP
```

---

## Batch-building process (Claude's interactive steps)

For each role in `config.INDEED_ROLES`:

### Step 1 — Find jobs on Indeed
```
WebSearch: site:nl.indeed.com "{role}" OR site:indeed.com "{role}" Nederland
```

### Step 2 — Fetch & validate each job page
`WebFetch` the Indeed job URL and check:
- "niet meer beschikbaar" / "no longer available" → **skip** (closed listing)
- Parse JSON-LD `datePosted`, or regex "X dagen geleden" → **skip** if > 21 days old
- Extract from JSON-LD: `hiringOrganization.name` (company), `hiringOrganization.url` or `sameAs` (domain)
- **Also extract any inline contact** from the posting:
  - `applicationContact` in JSON-LD (name + email)
  - Email addresses in body text
  - Name paired with "vragen", "contact", "solliciteer via" phrases
  - → If found: use as contact, set `contact_source = "job_posting"`, **skip steps 4a and 5**

### Step 3 — Filter agencies & dedup
- Skip if company name matches any keyword in `config.AGENCY_KEYWORDS`
- Skip if company already in SQLite contacted list (`outreach/storage.py:get_contacted_company_ids`)

### Step 4a — Check company career page (only if no contact from step 2)
Using the domain extracted in step 2, try in order:
```
WebFetch {domain}/careers
WebFetch {domain}/vacatures
WebFetch {domain}/werken-bij
WebFetch {domain}/jobs
```
Look for: HR/Talent/Recruitment section, name + email pairs, contact mailto links.
Fallback: `WebSearch site:{domain} HR recruiter talent contact`
→ If contact found: set `contact_source = "career_page"`, **skip step 5**

### Step 5 — Lusha (only if steps 2 and 4a found no contact)
```
contacts_search(company_name, enrich=True)
```
Filter by `config.HIRING_MANAGER_DEPARTMENTS` and `config.HIRING_MANAGER_SENIORITY_IDS`.
Set `contact_source = "lusha"`.

### Step 6 — Write today_batch.json
Stop at 20 entries.

---

## today_batch.json schema

```json
{
  "date": "2026-06-19",
  "entries": [
    {
      "company": {
        "lusha_id": "v1.xxx",
        "name": "Acme BV",
        "domain": "acme.nl",
        "industry": "Technology, Information & Media",
        "location": "Amsterdam, Netherlands",
        "employee_count": null
      },
      "manager": {
        "lusha_id": "v1.yyy",
        "first_name": "Anna",
        "last_name": "Smit",
        "full_name": "Anna Smit",
        "title": "HR Manager",
        "linkedin_url": "https://www.linkedin.com/in/anna-smit",
        "email": "anna.smit@acme.nl"
      },
      "role": "DevOps Engineer",
      "skill_1": "Kubernetes",
      "skill_2": "CI/CD",
      "job_url": "https://nl.indeed.com/...",
      "contact_source": "lusha"
    }
  ]
}
```

`contact_source`: `"job_posting"` | `"career_page"` | `"lusha"`

When `contact_source` is `"job_posting"` or `"career_page"`, `lusha_id` fields may be empty strings — that is fine.

---

## Key files

| File | Purpose |
|------|---------|
| `generate_today.py` | Reads `today_batch.json`, builds records, sends emails |
| `outreach/config.py` | Role lists, agency keywords, Lusha filter IDs, email template |
| `outreach/storage.py` | SQLite dedup & status tracking |
| `outreach/gmail_sender.py` | Gmail SMTP send with preview + confirmation |
| `outreach/models.py` | `Company`, `HiringManager`, `OutreachRecord` dataclasses |
| `outreach/message_generator.py` | Claude-powered role/skill inference fallback |

---

## Environment variables (`.env`)

```
ANTHROPIC_API_KEY=...
GMAIL_USER=jozef@next-hire.nl
GMAIL_APP_PASSWORD=xxxx_xxxx_xxxx_xxxx
GMAIL_FROM_NAME=Next-Hire
```
