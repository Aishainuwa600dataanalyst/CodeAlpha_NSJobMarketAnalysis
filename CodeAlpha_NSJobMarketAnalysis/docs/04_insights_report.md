# 04 · Findings, Insights & Recommendations

**Scope:** 100 job adverts returned by a "Data Analyst" keyword search on a public UK healthcare jobs board (posted 7 Sep to 2 Oct 2026). Every figure here can be re-created with `python src/objectives_summary.py`, and the headline numbers were also checked against the SQL views and the dashboards.

## The one-paragraph summary

Data and analytics work is the largest category (40 of 100 adverts), but about half of those are support-level roles. The median advertised annual salary is **£44,038**, and pay depends heavily on role type: data engineering and analyst roles pay roughly £45,000 to £57,000 at the median, while administration and data-quality roles pay roughly £27,000 to £28,000. Jobs are scattered across 76 location labels, with London first at only 9 adverts. Most roles are permanent (75% overall, 82% in data roles). Flexibility is a minority feature: 28% of adverts list any flexible or remote option, only 6% list home or remote working, and none of the 40 data roles do. One advert in five shows no salary.

## How the six objectives fit together

| # | Objective | Short answer |
|---|---|---|
| 2 | Demand | Data & Analytics leads (40%); half of it is career-track (analyst, engineering, lead), half is administration, data quality and governance |
| 3 | Compensation | Median £44,038; engineering and analyst roles are the best paid data roles |
| 4 | Work location | Scattered: London 9, then 5, 3, 3, 3; 65 of 76 location labels appear once |
| 5 | Work flexibility | 72% no flexibility listed, 22% flexible, 6% home or remote; 0 of 40 data roles list remote |
| 6 | Employment type | 75% permanent, 23% fixed-term; data roles 82% permanent |
| 1 | Job-seeker opportunity | Best-looking profile: permanent, career-track data role paid £40,000+ (18 adverts); remote needs a wider search |

---

## Objective 2 · Demand
*Which data and analytics roles are most frequently advertised?*

### Role categories (all 100 adverts)

| Rank | Role category | Adverts | Share |
|---:|---|---:|---:|
| 1 | Data & Analytics | 40 | 40% |
| 2 | IT & Technology | 14 | 14% |
| 3 | Business & Performance | 11 | 11% |
| 4 | Other | 9 | 9% |
| 5 | Cybersecurity | 8 | 8% |
| 6 | Administration & Support | 7 | 7% |
| 7 | Clinical & Research | 7 | 7% |
| 8 | Finance & Commercial | 4 | 4% |

### Inside Data & Analytics (40 adverts)

Grouped by job title (an analysis-time grouping, not a CSV column or dashboard field; the rules are in `src/objectives_summary.py`):

| Job family | Adverts | Share | Typical titles |
|---|---:|---:|---|
| Administration, assistant & coordination | 12 | 30% | Data Administrator, Data Assistant, Data Co-ordinator, Information Assistant |
| Analyst | 11 | 28% | Senior Information Analyst, EHR Senior Analyst, Data Analyst |
| Lead / manager | 5 | 12% | Data Lead, Research Data Manager, Data and Analytical Lead |
| Data quality & validation | 5 | 12% | Data Quality Coordinator, Data Quality & RTT Validator |
| Data engineering | 4 | 10% | Senior Data Engineer, Principal Data Engineer |
| Governance & protection | 2 | 5% | Data Protection Officer, Data Security & IG Officer |
| Clinical coding | 1 | 2% | Novice Clinical Coder & HIMS Apprentice Open Day |

**So what?** The "Data & Analytics" label covers very different jobs. Analyst, engineering and lead/manager roles (20 of 40) are the career-track ones. Searching only for "data analyst" would miss much of the market, because many roles are called *information analyst*, *data engineer* or *data quality lead*.

---

## Objective 3 · Compensation
*What salary levels are associated with these opportunities?*

Based on the **79** adverts with an annual salary range (midpoint of min and max). One advert was hourly and **20** showed no salary.

| Measure | All roles | Data & Analytics |
|---|---:|---:|
| Adverts with annual salary | 79 | 30 (of 40) |
| Median | **£44,038** | **£44,038** |
| Mean | £45,513 | n/a |
| Lowest midpoint | £25,737 | £25,737 |
| Highest midpoint | £85,557 | £69,885 |

### Data & Analytics salary by job family

| Job family | Salaried adverts | Median | Range |
|---|---:|---:|---|
| Data engineering | 4 | £57,045 | £52,951 to £61,139 |
| Governance & protection | 2 | £52,588 | £44,038 to £61,139 |
| Analyst | 11 | £44,700 | £29,775 to £69,885 |
| Lead / manager | 3 | £42,670 | £35,558 to £52,951 |
| Data quality & validation | 4 | £28,196 | £26,618 to £40,922 |
| Administration, assistant & coordination | 6 | £26,618 | £25,737 to £29,775 |

### All role categories

| Role category | Salaried adverts | Median midpoint |
|---|---:|---:|
| Cybersecurity | 8 | £54,121 |
| Business & Performance | 9 | £52,951 |
| Clinical & Research | 7 | £44,038 |
| Data & Analytics | 30 | £44,038 |
| Finance & Commercial | 4 | £43,798 |
| Other | 8 | £42,670 |
| IT & Technology | 10 | £39,798 |
| Administration & Support | 3 | £29,775 |

### Pay levels (79 salaried adverts)

| Salary band (midpoint) | Adverts |
|---|---:|
| £25,000 to £29,999 | 20 |
| £30,000 to £34,999 | 1 |
| £35,000 to £39,999 | 8 |
| £40,000 to £44,999 | 18 |
| £45,000 to £49,999 | 1 |
| £50,000 to £54,999 | 14 |
| £55,000 to £59,999 | 1 |
| £60,000 to £64,999 | 10 |
| £65,000 to £69,999 | 2 |
| £70,000 to £74,999 | 2 |
| £85,000 to £89,999 | 2 |

Pay clusters around a few fixed pay points (employers advertise set pay-scale ranges), which is why some bands hold only one advert.

**Caveats**
- Cybersecurity's median is lifted by four adverts from one national employer sharing one salary band (the advert text says it includes a 20% recruitment and retention premium).
- Administration has only 3 salaried adverts, and the data-engineering and governance families have 4 and 2. Treat those medians as hints.
- Advertised pay is not take-home pay or an actual offer.

---

## Objective 4 · Work location
*Where are these opportunities concentrated?*

| Location | Adverts (all 100) | Share |
|---|---:|---:|
| London | 9 | 9% |
| Leeds / Exeter | 5 | 5% |
| Cardiff | 3 | 3% |
| Cheltenham | 3 | 3% |
| Sheffield | 3 | 3% |
| Birmingham, Bradford, Bristol Gloucester, Liverpool, Manchester | 2 each | 2% each |

- The top 10 locations cover **33** adverts. The sample has **76** different location labels, and **65** appear only once.
- Among the 40 data roles: London 4, then Bradford, Cardiff and Cheltenham with 2 each. The 40 roles come from **35 employers**; only 5 employers have two or more.

**So what?** There is no single hub. The location field is free text typed by employers (e.g. `Leeds / Exeter`, `Bristol Gloucester`, `TBC`), so grouping is approximate, and the real picture is even more scattered than a tidy "top 10" suggests.

---

## Objective 5 · Work flexibility
*How prevalent are remote, hybrid/flexible and on-site working arrangements?*

The advert's working-pattern field is a list of options (e.g. `Full-time, Flexible working, Home or remote working`). I grouped it in order of strength: remote, then flexible, then none.

| Working arrangement | All 100 | Data & Analytics (40) |
|---|---:|---:|
| Home or remote working listed | 6 (6%) | 0 (0%) |
| Flexible working listed (no remote) | 22 (22%) | 7 (18%) |
| No flexibility listed (standard hours, assumed on-site) | 72 (72%) | 33 (82%) |

Other facts: **54** adverts are plain *Full-time*, **28** mention *Part-time* as an option, and 25 adverts use the exact phrase *Flexible working* (some of them also list remote).

The 6 adverts listing home or remote working: Performance Analyst, Senior Finance Analyst, Senior Business Analyst, Remote Senior Clinical Coding Analyst, and two Clinical Audit Assistant roles.

**So what?**
- **Remote is rare** and, in this sample, **absent from the data & analytics category**.
- **"Hybrid" and "on-site" are not options on the advert form.** Flexible working is the nearest proxy for hybrid, and "no flexibility listed" is the nearest proxy for on-site. Neither tells you where you'll actually sit; check the full advert.
- Flexible ≠ remote.

---

## Objective 6 · Employment type
*What contract structures are employers offering?*

| Contract type | All 100 | Data & Analytics (40) |
|---|---:|---:|
| Permanent | 75 (75%) | 33 (82%) |
| Fixed term | 23 (23%) | 7 (18%) |
| Secondment | 1 | 0 |
| Apprenticeship | 1 | 0 |

**So what?** Permanent contracts dominate, and data roles are slightly *more* likely to be permanent than the sample as a whole. Fixed-term adverts (about one in five) can still be a route into an organisation.

---

## Objective 1 · Job-seeker opportunity
*What characteristics of data and analytics jobs can help job seekers target promising international opportunities?*

### What "promising" means here
The adverts record pay, contract, flexibility, location and timing. They do **not** record visa sponsorship, whether overseas applicants are welcome, or whether work can be done from another country. So "promising" means **favourable characteristics visible in the data**: career-track role, solid pay, permanent contract, and as much flexibility as the advert lists. A shortlist built this way still has to be checked against each full advert and official guidance.

### The shortlist profile: data & analytics adverts paid £40,000 or more
**18 of the 40** data adverts qualify. **15** are permanent, **3** list flexible working, and **0** list remote.

| Advert title | Salary midpoint | Contract | Flexibility listed |
|---|---:|---|---|
| EHR Senior Analyst (×2) | £69,885 | Permanent | None |
| Senior Analyst - HIM | £61,697 | Permanent | None |
| Senior Data Engineer (secure data environment) | £61,139 | Permanent | None |
| EPR Data Engineering Manager | £61,139 | Permanent | None |
| Data Protection Officer | £61,139 | Permanent | Flexible working |
| Data and Analytical Lead | £61,139 | Permanent | None |
| Advanced Information Analyst | £53,747 | Permanent | None |
| Senior Data Engineer | £52,951 | Permanent | None |
| Principal Data Engineer | £52,951 | Fixed term | None |
| Senior Clinical Research Data Manager | £52,951 | Permanent | Flexible working |
| Bioinformatician (Information Analyst Specialist) | £44,700 | Permanent | None |
| Senior Information Analyst (×2) | £44,700 | 1 permanent, 1 fixed term | None |
| Senior Information Analyst, Band 6 | £44,038 | Permanent | None |
| Data Security & IG Officer | £44,038 | Permanent | Flexible working |
| Research Data Manager | £42,670 | Fixed term | None |
| Procedure Coder & Data Quality Co-ordinator | £40,922 | Permanent | None |

### Characteristics that help a job seeker target roles

| Characteristic | Evidence | Practical meaning |
|---|---|---|
| Role level | Engineering, analyst and lead roles pay about £43,000 to £57,000 at the median; administration and data quality about £27,000 to £28,000 | Target career-track titles: *analyst*, *engineer*, *lead*, *manager*, *senior* |
| Pay | 18 of 40 data adverts at £40,000+ | A clear tier to aim for |
| Contract | 15 of the 18 are permanent; 82% of data roles are permanent | Expect stability |
| Flexibility | 3 of the 18 list flexible working; none list remote | Don't count on remote from higher-paid data roles |
| Where remote does appear | 4 analyst-titled roles (performance, finance, business, clinical coding) | Add these to a remote-focused search |
| Employers | 35 employers for 40 roles; 5 hire more than once | Apply widely, not to one "hub" |
| Timing | Median advert open **14 days**; 86 of 100 closed within 3 weeks | Prepare CV and applications in advance |

### Not answerable from this data
- Visa sponsorship, overseas applicants, or work from another country.
- Whether a role is genuinely on-site, hybrid or remote beyond the listed pattern.
- Whether a vacancy is still open (a future closing date is not proof).

---

## Timing and data-quality check: closing dates

- Posted: 7 Sep to 2 Oct 2026. Closing: 4 Oct to 30 Nov 2026.
- The median advert was open **14 days**; 86 of 100 closed within 3 weeks of posting.
- On the dashboard refresh date (27 Oct 2026): **94 passed, 6 not yet closed**. This changes every day.
- Every advert has a closing date, so the SQL category `Closing date unavailable` has **0** adverts.

---

## Recommendations

Who this is for: job seekers exploring data and analytics careers. Every recommendation is tied to a number from the sample.

| # | Recommendation | Evidence (objective) |
|---|---|---|
| 1 | **Aim for career-track roles** (analyst, engineer, lead, manager). | Median £43,000 to £57,000 vs £27,000 to £28,000 for admin and data-quality roles (2, 3) |
| 2 | **Prioritise permanent roles, but keep fixed-term in view.** | 82% of data roles permanent; 18% fixed-term (6) |
| 3 | **Don't expect remote work from data-category roles; widen the search if remote matters.** | 0 of 40 data roles list remote; 4 analyst-titled adverts elsewhere do (5) |
| 4 | **Search several job titles.** | Only 28% of data roles are titled analyst; others are engineer, lead, quality, administrator (2) |
| 5 | **Open the advert when no salary is shown.** | 20 of 100 (10 of 40 data roles) show none (3) |
| 6 | **Apply early.** | Median advert open 14 days (1) |
| 7 | **Look beyond London.** | London 9 adverts; 65 of 76 location labels appear once (4) |
| 8 | **Check eligibility yourself.** | Sponsorship and overseas eligibility are not in the data (1) |

## Recommendations for improving the analysis
- Scrape several keywords and compare, to reduce the keyword bias.
- Re-scrape monthly to see trends rather than a single snapshot.
- Extract skills and sponsorship wording from the full advert text, which would let Objective 1 say much more about international opportunities.

*These are patterns in a sample of 100 adverts, not guarantees about the whole UK healthcare job market.*
