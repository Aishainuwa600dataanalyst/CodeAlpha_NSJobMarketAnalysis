# 02 · Data Dictionary

**File:** `data/ns_data_analyst_jobs_100.csv` · **Rows:** 100 (one per job advert) · **Columns:** 16

Columns 1 to 10 come straight from the website (lightly tidied). Columns 11 to 16 were created during cleaning.

| # | Column | Type | Example | What it means |
|---|---|---|---|---|
| 1 | `job_title` | text | `Senior Information Analyst` | Title exactly as advertised |
| 2 | `employer` | text | `Cardiff and Vale University Health Board` | Organisation advertising the job (not always a health trust: GP practices, charities and private providers appear too) |
| 3 | `location` | text | `Leeds / Exeter` | Town or place as typed by the employer. Free text, so it can be messy (e.g. `Bristol Gloucester`, `TBC`, `Any`) |
| 4 | `postcode` | text | `LS1 4AP` | Employer postcode (formats vary slightly) |
| 5 | `salary` | text | `£32,073 to £39,043 a year per annum` | Advertised pay, original wording. `Not available` if none was shown |
| 6 | `date_posted` | date | `2026-09-24` | Date the advert was posted |
| 7 | `closing_date` | date | `2026-10-15` | Date applications close, as scraped |
| 8 | `contract_type` | text | `Permanent` | One of: Permanent, Fixed term, Secondment, Apprenticeship |
| 9 | `working_pattern` | text | `Full-time, Flexible working` | Patterns the employer lists. Several can be combined in one string |
| 10 | `job_url` | text | `https://…/candidate/jobadvert/…` | Link to the advert. Unique per row |
| 11 | `salary_min` | number | `32073` | Lower end of the advertised range (£). Blank if no salary. **Hourly figure if salary type is Hourly** |
| 12 | `salary_max` | number | `39043` | Upper end of the advertised range (£). Blank if no salary |
| 13 | `salary_midpoint` | number | `35558` | `(min + max) / 2`. **Annual salaries only**; blank for hourly and missing |
| 14 | `salary_type` | text | `Annual` | `Annual`, `Hourly` or `Not available` |
| 15 | `closing_date_clean` | date | `2026-10-15` | `closing_date` converted to a proper date |
| 16 | `role_category` | text | `Data & Analytics` | My grouping of the job title: Data & Analytics, IT & Technology, Business & Performance, Cybersecurity, Finance & Commercial, Clinical & Research, Administration & Support, Other |

## Missing values

| Field | Blank / "Not available" | Why |
|---|---:|---|
| Salary (`salary_type` = Not available) | 20 | Many GP practices and some employers don't show pay |
| Hourly salary | 1 | Advertised per hour, so it has no annual midpoint |
| `salary_midpoint` | 21 | The 20 above + the 1 hourly advert |
| Annual salary available | **79** | The base for every salary statistic |

## Things to know before you use it

- **Dates in the CSV** use `M/D/YYYY` (e.g. `10/15/2026`). PostgreSQL's default date style reads this correctly. In other tools, tell the importer the format.
- **Salary text can include extras** (e.g. "includes an RRP payment of 20%", "incl HCAS (Inner)"). The min and max pick up only the first and last `£` amounts.
- **`role_category` is subjective.** See [methodology](01_methodology.md) and [known issues](05_known_issues_and_next_steps.md).
