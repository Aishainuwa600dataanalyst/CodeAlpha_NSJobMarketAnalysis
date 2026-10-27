# 03 · SQL Guide (a plain-English tour)

The script is [`sql/ns_jobs_analysis.sql`](../sql/ns_jobs_analysis.sql). It was written for **PostgreSQL** and tested end to end on PostgreSQL 16 (it loads the 100 rows and every query and view runs without errors).

## Running order

1. **Create the table** `public.ns_data_analyst_jobs_100` (16 columns matching the CSV).
2. **Load the CSV** into it.
   - psql: `\copy public.ns_data_analyst_jobs_100 FROM 'data/ns_data_analyst_jobs_100.csv' WITH (FORMAT csv, HEADER true)`
   - DBeaver: right-click the table → *Import Data* → CSV.
3. **Run the rest top to bottom.**

## The building blocks

### `vw_ns_jobs_clean`: the foundation
Everything else is built on this view. It:
- tidies spaces in `location`,
- keeps a salary midpoint **only** for annual salaries with both a min and a max,
- turns `salary_type` into `Annual` / `Hourly` / `Not available`,
- replaces blank role categories with `Unclassified`,
- adds `closing_status` by comparing `closing_date_clean` to today.

```sql
CASE
    WHEN LOWER(TRIM(salary_type)) = 'annual'
         AND salary_min IS NOT NULL AND salary_max IS NOT NULL
    THEN (salary_min + salary_max) / 2.0
    ELSE NULL
END AS annual_salary_midpoint
```

### Analysis views
| View | Question it answers |
|---|---|
| `vw_ns_salary_analysis` | What's the average, median, lowest and highest annual salary? |
| `vw_ns_role_demand` | Which role categories are advertised most? |
| `vw_ns_location_demand` | Where are the jobs (with % share)? |
| `vw_ns_working_arrangements` | How are jobs structured: full-time, part-time, flexible…? |
| `vw_ns_contract_analysis` | Permanent vs fixed-term vs other? |
| `vw_ns_jobseeker_summary` | The headline numbers in a single row |
| `vw_ns_jobs_tableau` | Row-level data for Tableau |

### SQL techniques used
- `CREATE OR REPLACE VIEW`: re-runnable, reusable building blocks
- `FILTER (WHERE …)`: conditional counts without extra subqueries
- `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY …)`: the median
- `SUM(COUNT(*)) OVER ()`: a window function to turn counts into percentages
- `COALESCE` / `NULLIF` / `TRIM` / `REGEXP_REPLACE`: cleaning inside the query
- `HAVING COUNT(*) >= 2`: avoids one-advert medians

## Expected results (a quick self-check)

```sql
SELECT * FROM public.vw_ns_jobseeker_summary;
```

| total_jobs | unique_job_postings | jobs_with_annual_salary | jobs_without_salary | average_annual_salary | median_annual_salary |
|---:|---:|---:|---:|---:|---:|
| 100 | 100 | 79 | 20 | 45,512.92 | 44,038.00 |

`postings_with_future_closing_dates` and `postings_with_past_closing_dates` depend on the day you run it. On 26 Oct 2026 they were **7** and **93**, and on 27 Oct 2026 **6** and **94**.

## One thing I fixed while packaging this repo
My original script queried `vw_ns_role_demand` (Step 18) without ever creating it, so it would have errored for anyone running it fresh. I added the missing `CREATE VIEW` just before Step 18 and marked it with a comment.
