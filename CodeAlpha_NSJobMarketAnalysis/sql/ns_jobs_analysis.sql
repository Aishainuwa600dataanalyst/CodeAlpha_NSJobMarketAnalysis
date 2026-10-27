/* =====================================================================
   NS JOB MARKET ANALYSIS  |  PostgreSQL script
   Author : Aisha O. Inuwa  |  CodeAlpha Data Analytics Internship, 2026

   WHAT THIS SCRIPT DOES
   1. Creates the raw table that holds the 100 scraped job postings.
   2. Builds a "clean" foundation view (tidy locations, annual-only salary
      midpoints, closing status, role category).
   3. Builds small analysis views (salary, location, working pattern,
      contract type, role demand, jobseeker summary).
   4. Builds the row-level view that Tableau connects to.

   HOW TO RUN IT (DBeaver or psql)
   1. Create a database called  ns_data_analyst_jobs_100  (or any name).
   2. Run the CREATE TABLE section below.
   3. Load  data/ns_data_analyst_jobs_100.csv  into the table, e.g. in psql:
        \copy public.ns_data_analyst_jobs_100 FROM 'data/ns_data_analyst_jobs_100.csv' WITH (FORMAT csv, HEADER true)
      (In DBeaver: right-click the table > Import Data > CSV.)
   4. Run the rest of the script top to bottom.

   NOTE: closing_status is measured against CURRENT_DATE, so the number of
   "Closing date passed" postings keeps growing as time goes by. The
   published dashboards were refreshed on 26 Oct 2026 (93 passed / 7 not
   yet closed). Re-run it later and the split will change.
   ===================================================================== */

DROP TABLE IF EXISTS public.ns_data_analyst_jobs_100;
-----------------------------------------------------
CREATE TABLE public.ns_data_analyst_jobs_100
(
job_title VARCHAR(200),
employer TEXT,
location VARCHAR (100),	
postcode VARCHAR(100),	
salary	VARCHAR (500),
date_posted	DATE,
closing_date DATE,
contract_type TEXT,	
working_pattern	TEXT,
job_url	VARCHAR(2000),
salary_min 	NUMERIC,
salary_max	NUMERIC,
salary_midpoint NUMERIC,
salary_type	TEXT,
closing_date_clean DATE,
role_category TEXT
);
---------
SELECT * FROM public.ns_data_analyst_jobs_100;
-----------------Create the foundation view-----------------------------------

CREATE OR REPLACE VIEW public.vw_ns_jobs_clean AS
SELECT
    job_title,
    employer,

    -- Standardize spacing in location names
    TRIM(REGEXP_REPLACE(location, '\s+', ' ', 'g'))
        AS location,

    postcode,
    salary,

    date_posted,
    closing_date,
    closing_date_clean,

    contract_type,
    working_pattern,
    job_url,

    salary_min,
    salary_max,

    -- Only retain annual salary midpoints
    CASE
        WHEN LOWER(TRIM(salary_type)) = 'annual'
             AND salary_min IS NOT NULL
             AND salary_max IS NOT NULL
        THEN (salary_min + salary_max) / 2.0
        ELSE NULL
    END AS annual_salary_midpoint,

    CASE
        WHEN LOWER(TRIM(salary_type)) = 'annual'
            THEN 'Annual'
        WHEN LOWER(TRIM(salary_type)) = 'hourly'
            THEN 'Hourly'
        ELSE 'Not available'
    END AS salary_type,

    COALESCE(
        NULLIF(TRIM(role_category), ''),
        'Unclassified'
    ) AS role_category,

    -- Useful for prioritizing time-sensitive opportunities
    CASE
        WHEN closing_date_clean IS NULL
            THEN 'Closing date unavailable'
        WHEN closing_date_clean < CURRENT_DATE
            THEN 'Closing date passed'
        ELSE 'Not yet closed'
    END AS closing_status

FROM public.ns_data_analyst_jobs_100;

--------------------------------------------------------------------

SELECT *
FROM public.vw_ns_jobs_clean
LIMIT 10;
--------------------------------------------------------------------
SELECT
    COUNT(*) AS total_jobs,
    COUNT(DISTINCT job_url) AS unique_job_urls,
    COUNT(*) FILTER (
        WHERE annual_salary_midpoint IS NOT NULL
    ) AS jobs_with_annual_salary
FROM public.vw_ns_jobs_clean;
---------------------------------------------------------------------
SELECT
    salary_type,
    COUNT(*) AS job_count
FROM public.vw_ns_jobs_clean
GROUP BY salary_type
ORDER BY job_count DESC;
---------------------------------------------------------------------
SELECT
    role_category,
    COUNT(*) AS job_count
FROM public.vw_ns_jobs_clean
GROUP BY role_category
ORDER BY job_count DESC;
-----------------------Create the salary-analysis view---------------------------------------------

CREATE OR REPLACE VIEW public.vw_ns_salary_analysis AS
SELECT
    COUNT(*) AS jobs_with_annual_salary,
    ROUND(AVG(annual_salary_midpoint), 2) AS average_annual_salary,
    ROUND(
        (PERCENTILE_CONT(0.5)
         WITHIN GROUP (ORDER BY annual_salary_midpoint))::NUMERIC,
        2
    ) AS median_annual_salary,
    MIN(annual_salary_midpoint) AS lowest_annual_salary_midpoint,
    MAX(annual_salary_midpoint) AS highest_annual_salary_midpoint
FROM public.vw_ns_jobs_clean
WHERE annual_salary_midpoint IS NOT NULL;
--------------------------------------------------------------
SELECT *
FROM public.vw_ns_salary_analysis;
-------------------------------------------------------------

SELECT
    role_category,
    COUNT(*) AS jobs_with_annual_salary,
    ROUND(AVG(annual_salary_midpoint), 2) AS average_annual_salary,
    ROUND(
        (PERCENTILE_CONT(0.5)
         WITHIN GROUP (ORDER BY annual_salary_midpoint))::NUMERIC,
        2
    ) AS median_annual_salary
FROM public.vw_ns_jobs_clean
WHERE annual_salary_midpoint IS NOT NULL
GROUP BY role_category
HAVING COUNT(*) >= 2
ORDER BY median_annual_salary DESC;

-------Phase 4: Location, flexibility and contract analysis
---Step 11️⃣ Create the location-demand view
---This shows where the sampled job postings are concentrated.

CREATE OR REPLACE VIEW public.vw_ns_location_demand AS
SELECT
    COALESCE(NULLIF(TRIM(location), ''), 'Not available')
        AS location,
    COUNT(*) AS job_count,
    ROUND(
        COUNT(*) * 100.0 /
        NULLIF(SUM(COUNT(*)) OVER (), 0),
        2
    ) AS percentage_of_jobs
FROM public.vw_ns_jobs_clean
GROUP BY COALESCE(NULLIF(TRIM(location), ''), 'Not available');

---Step 12️⃣ Display the top 10 locations

SELECT *
FROM public.vw_ns_location_demand
ORDER BY job_count DESC, location
LIMIT 10;

--Step 13️⃣ Create the working-arrangements view
--This helps us investigate work flexibility, which matters when evaluating international opportunities.

CREATE OR REPLACE VIEW public.vw_ns_working_arrangements AS
SELECT
    COALESCE(
        NULLIF(TRIM(working_pattern), ''),
        'Not available'
    ) AS working_pattern,
    COUNT(*) AS job_count,
    ROUND(
        COUNT(*) * 100.0 /
        NULLIF(SUM(COUNT(*)) OVER (), 0),
        2
    ) AS percentage_of_jobs
FROM public.vw_ns_jobs_clean
GROUP BY COALESCE(
    NULLIF(TRIM(working_pattern), ''),
    'Not available'
);
--Step 14️⃣ Display working-arrangement results
SELECT *
FROM public.vw_ns_working_arrangements
ORDER BY job_count DESC, working_pattern;

--Step 15️⃣ Create the contract-analysis view
--This shows the types of employment contracts advertised.

CREATE OR REPLACE VIEW public.vw_ns_contract_analysis AS
SELECT
    COALESCE(
        NULLIF(TRIM(contract_type), ''),
        'Not available'
    ) AS contract_type,
    COUNT(*) AS job_count,
    ROUND(
        COUNT(*) * 100.0 /
        NULLIF(SUM(COUNT(*)) OVER (), 0),
        2
    ) AS percentage_of_jobs
FROM public.vw_ns_jobs_clean
GROUP BY COALESCE(
    NULLIF(TRIM(contract_type), ''),
    'Not available'
);

-------Step 16️⃣ Create the executive-summary view----------------------
-------Open a new SQL editor in DBeaver and run:
CREATE OR REPLACE VIEW public.vw_ns_jobseeker_summary AS
SELECT
    COUNT(*) AS total_jobs,

    COUNT(DISTINCT job_url) AS unique_job_postings,

    COUNT(*) FILTER (
        WHERE annual_salary_midpoint IS NOT NULL
    ) AS jobs_with_annual_salary,

    COUNT(*) FILTER (
        WHERE salary_type = 'Not available'
    ) AS jobs_without_salary,

    ROUND(
        AVG(annual_salary_midpoint),
        2
    ) AS average_annual_salary,

    ROUND(
        (
            PERCENTILE_CONT(0.5)
            WITHIN GROUP (
                ORDER BY annual_salary_midpoint
            )
        )::NUMERIC,
        2
    ) AS median_annual_salary,

    COUNT(*) FILTER (
        WHERE closing_status = 'Not yet closed'
    ) AS postings_with_future_closing_dates,

    COUNT(*) FILTER (
        WHERE closing_status = 'Closing date passed'
    ) AS postings_with_past_closing_dates

FROM public.vw_ns_jobs_clean;

--------Step 17️⃣ Display the summary------------------------------------
SELECT *
FROM public.vw_ns_jobseeker_summary;
---You'll get one row with the headline indicators for your project.
--Important: A future closing date doesn't guarantee that a vacancy remains available. Treat these as advertised closing-date indicators, not verified live vacancies.
-------- Role-demand view (added while packaging the repo) ---------------
-- The original script queried vw_ns_role_demand in Step 18 without ever
-- creating it. This view fixes that, so the script runs cleanly top to bottom.
CREATE OR REPLACE VIEW public.vw_ns_role_demand AS
SELECT
    role_category,
    COUNT(*) AS job_count,
    ROUND(
        COUNT(*) * 100.0 /
        NULLIF(SUM(COUNT(*)) OVER (), 0),
        2
    ) AS percentage_of_jobs
FROM public.vw_ns_jobs_clean
GROUP BY role_category;

--Step 18️⃣ Find the most frequently advertised role category
SELECT
    role_category,
    job_count,
    percentage_of_jobs
FROM public.vw_ns_role_demand
ORDER BY job_count DESC
LIMIT 5;

--This gives us the five most common role categories in your sample.
--Step 19️⃣ Identify categories with the highest median salaries

SELECT
    role_category,
    jobs_with_annual_salary,
    median_annual_salary
FROM (
    SELECT
        role_category,
        COUNT(*) AS jobs_with_annual_salary,
        ROUND(
            (
                PERCENTILE_CONT(0.5)
                WITHIN GROUP (
                    ORDER BY annual_salary_midpoint
                )
            )::NUMERIC,
            2
        ) AS median_annual_salary
    FROM public.vw_ns_jobs_clean
    WHERE annual_salary_midpoint IS NOT NULL
    GROUP BY role_category
) AS salary_by_role
WHERE jobs_with_annual_salary >= 2
ORDER BY median_annual_salary DESC
LIMIT 5;
--This helps us compare pay across role categories without letting a single posting determine a category's result.
--Step 20️⃣ Create a job-postings dataset for Tableau
--Tableau needs row-level data to create charts and filters. This view gives it the cleaned job records and relevant analytical fields.
CREATE OR REPLACE VIEW public.vw_ns_jobs_tableau AS
SELECT
    job_title,
    employer,
    location,
    postcode,
    date_posted,
    closing_date_clean AS closing_date,
    contract_type,
    working_pattern,
    role_category,
    salary_type,
    annual_salary_midpoint,
    closing_status,
    job_url
FROM public.vw_ns_jobs_clean;
--Test it:
SELECT *
FROM public.vw_ns_jobs_tableau
LIMIT 10;
