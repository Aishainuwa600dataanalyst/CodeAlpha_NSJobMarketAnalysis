# 01 · Methodology

How the data went from "100 web pages" to "three dashboards", and *why* each decision was made.

## 1. Data collection

| Item | Detail |
|---|---|
| Source | A public UK healthcare job-search website |
| Search | Keyword: `Data Analyst`, search-result pages 1 to 10 |
| Volume | 100 unique adverts (100 unique URLs, 76 distinct employers) |
| Posting dates | 7 Sep 2026 to 2 Oct 2026 |
| Closing dates | 4 Oct 2026 to 30 Nov 2026 |
| Tools | Python, `requests`, `BeautifulSoup`, `pandas` |

**How the scraper works**

1. Loop through search-result pages 1 to 10 and collect every link containing `/candidate/jobadvert/`.
2. De-duplicate the links.
3. Visit each advert and read fixed HTML elements by id (`heading`, `employer_name`, `employer_town`, `employer_postcode`, `range_salary`, `date_posted`, `closing_date`, `contract_type`, and the paragraph after `working_pattern_heading`).
4. If a field is missing, store `Not available` instead of crashing.
5. Wait 1 second between requests, so the server isn't hammered.

## 2. Cleaning

| Problem | What I did | Why |
|---|---|---|
| Stray whitespace and line breaks in text | Collapsed repeated spaces and trimmed ends | Otherwise `London` and `London ` count as different places |
| Salary is free text (`£32,073 to £39,043 a year per annum`) | Pulled out the numbers with a pattern for `£` amounts → `salary_min`, `salary_max` | Numbers can be analysed; text can't |
| Some pay is hourly | Labelled each salary **Annual**, **Hourly** or **Not available** (`salary_type`) | Mixing £15/hour with £40,000/year ruins any average |
| Salary missing | Left blank (NULL), never 0 | A zero would drag averages down and create fake "£0 jobs" |
| Dates stored as text | Converted `date_posted` and `closing_date` to real dates | Lets SQL and Tableau compare them |
| No role information | Created `role_category` from the job title | Lets us compare groups of similar roles |
| Location spacing | Standardised spaces in SQL (`REGEXP_REPLACE`) | Consistent grouping |

**Midpoint:** For annual ranges, `salary_midpoint = (min + max) / 2`. It stands in for "the typical pay of this advert". It is only calculated for **Annual** salaries.

## 3. Role categories

A simple rule-based classifier checks the lowercase job title for keywords. **Order matters**: the first group that matches wins.

1. **Cybersecurity**: "cyber security", "information security"
2. **Finance & Commercial**: "finance", "financial", "commercial"
3. **Business & Performance**: "business analyst", "performance analyst", "portfolio analyst", "commissioning", "service improvement", …
4. **Data & Analytics**: "data analyst", "data engineer", "data quality", "information analyst", "EHR", …
5. **IT & Technology**: "IT" (as a whole word), "ICT", "application support", "network", "digital", "service desk", …
6. **Clinical & Research**: "research", "clinical audit", "clinical coding", …
7. **Administration & Support**: "administrator", "receptionist", "call handler", …
8. **Other**: everything else

These are **my own** categories for this project, not official job families. I started with a first version, listed every title that fell into "Other", and refined the rules until the groups made sense.

## 4. SQL layer (PostgreSQL)

| View | Purpose |
|---|---|
| `vw_ns_jobs_clean` | Foundation. Tidy location, annual-only midpoint, salary type, role category, closing status |
| `vw_ns_salary_analysis` | Count, average, **median**, min and max of annual salary midpoints |
| `vw_ns_role_demand` | Postings and share by role category |
| `vw_ns_location_demand` | Postings and share by location |
| `vw_ns_working_arrangements` | Postings and share by working pattern |
| `vw_ns_contract_analysis` | Postings and share by contract type |
| `vw_ns_jobseeker_summary` | One-row headline summary |
| `vw_ns_jobs_tableau` | Row-level view that Tableau connects to |

Design choices:
- **Median over mean** for salary, because a handful of high salaries can't distort it.
- **`HAVING COUNT(*) >= 2`** when comparing role medians, so one advert can't *be* a category's median.
- **Closing status** (`Closing date passed` / `Not yet closed` / `Closing date unavailable`) is computed from `CURRENT_DATE`, so it changes over time.

## 5. Visualisation

Tableau dashboards connect to `vw_ns_jobs_tableau`. Design principles I followed:

- One clear question per dashboard.
- Horizontal bars for long category names (easy to read).
- A consistent navy palette so attention goes to the *data*.
- Direct data labels on bars.
- Filters on the things a jobseeker would actually want to change.

## 6. Validation

Before writing this repo I re-checked the headline numbers three ways: directly from the CSV with pandas, by running the SQL script end to end on a fresh PostgreSQL database, and against the dashboard screenshots. All three agree (100 postings, 79 annual salaries, median £44,038, role counts 40/14/11/9/8/7/7/4).

## 7. Objective analysis (`src/objectives_summary.py`)

The six project objectives are answered with the CSV plus two **analysis-time groupings** that are *not* columns in the dataset and not fields in the dashboards:

**Job family (inside Data & Analytics only).** First matching rule on the lowercase title wins: *engineer* → Data engineering; *analyst/analytical* → Analyst; *protection/security* → Governance & protection; *lead/manager* → Lead / manager; *quality/validator/failsafe* → Data quality & validation; *administrator/assistant/coordinator/data input/secretary* → Administration, assistant & coordination; *coder* → Clinical coding.

**Flexibility group (all adverts).** Based on the advertised working-pattern text, strongest signal first: contains *remote* → "Home or remote working listed"; contains *flexible*, *compressed* or *job share* → "Flexible working listed (no remote)"; otherwise "No flexibility listed". The advert form has no "hybrid" or "on-site" option, so flexible working is the closest proxy for hybrid, and no flexibility listed is the closest proxy for on-site.

**Shortlist (Objective 1).** Data & Analytics adverts with an annual salary midpoint of £40,000 or more, then summarised by contract type and flexibility.

Re-run `python src/objectives_summary.py` to reproduce every table in `docs/04_insights_report.md`.
