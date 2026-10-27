"""
NS Jobs scraping + cleaning pipeline
=====================================
Author : Aisha O. Inuwa  |  CodeAlpha Data Analytics Internship, 2026

This is the tidy, re-runnable version of the exploration I did in
notebooks/01_ns_jobs_scraping_and_cleaning.ipynb. The notebook shows the
messy "figuring it out" journey; this script is the clean final route.

What it does
------------
1. Collects job-advert links from the jobs-board search results (pages 1-N).
2. Visits each advert and pulls out title, employer, location, postcode,
   salary, dates, contract type and working pattern.
3. Cleans the text, splits salary into min / max / midpoint, labels the
   salary as Annual / Hourly / Not available, and assigns a role category.
4. Saves everything to a CSV.

Usage
-----
    python src/ns_jobs_pipeline.py                      # scrape 10 pages
    python src/ns_jobs_pipeline.py --pages 3 --out data/test.csv
    python src/ns_jobs_pipeline.py --clean-only data/raw.csv --out data/clean.csv

Be kind to the website: the script waits between requests. Please check the
site's terms of use before scraping and only redistribute data you are
allowed to share.
"""

from __future__ import annotations

import argparse
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.jobs.nhs.uk"
SEARCH_URL = (
    BASE_URL + "/candidate/search/results"
    "?searchFormType=main&keyword=Data%20Analyst&language=en&page={page}"
)
HEADERS = {"User-Agent": "Mozilla/5.0 (student project: CodeAlpha NS job analysis)"}
DELAY_SECONDS = 1  # pause between requests


# --------------------------------------------------------------------------
# 1. SCRAPING
# --------------------------------------------------------------------------
def collect_job_urls(pages: int = 10) -> list[str]:
    """Walk through the search-result pages and collect unique advert URLs."""
    urls: list[str] = []
    for page in range(1, pages + 1):
        print(f"Collecting links from page {page}/{pages}...")
        response = requests.get(SEARCH_URL.format(page=page), headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=lambda h: h and "/candidate/jobadvert/" in h):
            full_url = urljoin(BASE_URL, link["href"])
            if full_url not in urls:
                urls.append(full_url)
        time.sleep(DELAY_SECONDS)
    print(f"Unique job URLs collected: {len(urls)}")
    return urls


def _text(soup: BeautifulSoup, element_id: str) -> str:
    """Safely read the text of an element by id (or 'Not available')."""
    element = soup.find(id=element_id)
    return element.get_text(" ", strip=True) if element else "Not available"


def scrape_job(job_url: str) -> dict:
    """Pull the fields we care about from one job advert page."""
    response = requests.get(job_url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    heading = soup.find(id="working_pattern_heading")
    paragraph = heading.find_next_sibling("p") if heading else None
    working_pattern = paragraph.get_text(" ", strip=True) if paragraph else "Not available"

    return {
        "job_title": _text(soup, "heading"),
        "employer": _text(soup, "employer_name"),
        "location": _text(soup, "employer_town"),
        "postcode": _text(soup, "employer_postcode"),
        "salary": _text(soup, "range_salary"),
        "date_posted": _text(soup, "date_posted"),
        "closing_date": _text(soup, "closing_date").replace("The closing date is ", ""),
        "contract_type": _text(soup, "contract_type"),
        "working_pattern": working_pattern,
        "job_url": job_url,
    }


def scrape_all(pages: int = 10) -> pd.DataFrame:
    rows = []
    urls = collect_job_urls(pages)
    for i, url in enumerate(urls, start=1):
        print(f"Scraping job {i}/{len(urls)}...", end="\r")
        try:
            rows.append(scrape_job(url))
        except Exception as error:  # keep going if one advert misbehaves
            print(f"\nCould not scrape job {i}: {error}")
        time.sleep(DELAY_SECONDS)
    print(f"\nJobs scraped: {len(rows)}")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# 2. CLEANING
# --------------------------------------------------------------------------
TEXT_COLUMNS = [
    "job_title", "employer", "location", "postcode",
    "salary", "closing_date", "contract_type", "working_pattern",
]
MONEY = re.compile(r"£([\d,]+(?:\.\d+)?)")


def salary_numbers(salary: str) -> tuple[float | None, float | None]:
    """'£32,073 to £39,043 a year' -> (32073.0, 39043.0)."""
    found = [float(m.replace(",", "")) for m in MONEY.findall(salary)]
    if not found:
        return None, None
    return found[0], (found[-1] if len(found) >= 2 else None)


def salary_kind(salary: str) -> str:
    """Label the salary so hourly pay never gets mixed into annual pay."""
    text = salary.lower()
    if "an hour" in text or "per hour" in text:
        return "Hourly"
    if "a year" in text or "per annum" in text:
        return "Annual"
    return "Not available"


def classify_role(title: str) -> str:
    """Group job titles into broad role categories (my own, not official ones).

    Order matters: the first matching group wins.
    """
    title = title.lower()

    if any(w in title for w in ["cyber security", "cybersecurity", "information security"]):
        return "Cybersecurity"

    if any(w in title for w in ["finance", "financial", "commercial"]):
        return "Finance & Commercial"

    if any(w in title for w in [
        "business analyst", "business and performance", "performance analyst",
        "performance manager", "portfolio analyst", "commissioning",
        "monitoring, evaluation", "merl", "service improvement", "operations lead",
    ]):
        return "Business & Performance"

    if any(w in title for w in [
        "data analyst", "data engineer", "data scientist", "data lead", "data manager",
        "data quality", "data administrator", "data coordinator", "data co-ordinator",
        "data assistant", "data officer", "data entry", "data development",
        "data protection", "data security", "information analyst", "information manager",
        "information assistant", "ehr", "him", "data input", "data care",
        "analyst - him", "analytical", "research data",
    ]):
        return "Data & Analytics"

    # "IT" must be matched as a whole word: a plain "it " test wrongly matched
    # the end of words like "Audit" (fixed Oct 2026).
    if re.search(r"\bit\b", title) or any(w in title for w in [
        "ict", "im&t", "application support", "applications support",
        "network", "technology", "digital", "systems administrator",
        "service desk", "application analyst",
    ]):
        return "IT & Technology"

    if any(w in title for w in [
        "research", "clinical audit", "bioinformatic", "clinical coding",
        "clinical psychologist", "radiology",
    ]):
        return "Clinical & Research"

    if any(w in title for w in [
        "administrator", "administration", "secretary", "receptionist",
        "support officer", "call handler", "coordinator",
    ]):
        return "Administration & Support"

    return "Other"


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Turn the raw scrape into the analysis-ready dataset."""
    df = df.copy()

    # tidy text: fill gaps, squash repeated spaces, trim ends
    for col in TEXT_COLUMNS:
        df[col] = (
            df[col].fillna("Not available")
            .astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
        )

    # salary -> min / max, then a label so hourly is never averaged with annual
    pairs = df["salary"].apply(salary_numbers)
    df["salary_min"] = pairs.str[0]
    df["salary_max"] = pairs.str[1]
    df["salary_type"] = df["salary"].apply(salary_kind)

    # midpoint is only calculated for ANNUAL ranges
    is_annual = df["salary_type"].eq("Annual")
    df["salary_midpoint"] = ((df["salary_min"] + df["salary_max"]) / 2).where(is_annual)

    # dates
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["closing_date_clean"] = pd.to_datetime(df["closing_date"], errors="coerce")

    df["role_category"] = df["job_title"].apply(classify_role)

    return df[[
        "job_title", "employer", "location", "postcode", "salary",
        "date_posted", "closing_date", "contract_type", "working_pattern", "job_url",
        "salary_min", "salary_max", "salary_midpoint", "salary_type",
        "closing_date_clean", "role_category",
    ]]


# --------------------------------------------------------------------------
# 3. COMMAND LINE
# --------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape and clean NS Jobs postings.")
    parser.add_argument("--pages", type=int, default=10, help="search-result pages to scrape")
    parser.add_argument("--out", default="data/ns_data_analyst_jobs_100.csv", help="output CSV")
    parser.add_argument("--clean-only", metavar="RAW_CSV",
                        help="skip scraping and just clean an existing raw CSV")
    args = parser.parse_args()

    raw = pd.read_csv(args.clean_only) if args.clean_only else scrape_all(args.pages)
    cleaned = clean(raw)
    cleaned.to_csv(args.out, index=False)
    print(f"Saved {len(cleaned)} rows x {cleaned.shape[1]} columns to {args.out}")


if __name__ == "__main__":
    main()
