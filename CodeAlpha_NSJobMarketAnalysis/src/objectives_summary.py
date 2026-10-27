"""
Objectives summary
==================
Re-computes, straight from the cleaned CSV, every number used to answer the six
project objectives (see README). Run it to check any figure in the docs:

    python src/objectives_summary.py

It also defines two *analysis-time* groupings that are NOT columns in the CSV
or the Tableau dashboards:
  * job family (inside Data & Analytics), taken from the job title
  * flexibility group, taken from the advertised working pattern
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CSV = Path(__file__).resolve().parents[1] / "data" / "ns_data_analyst_jobs_100.csv"


def job_family(title: str) -> str:
    """Group Data & Analytics job titles. First matching rule wins."""
    t = title.lower()
    if "engineer" in t:
        return "Data engineering"
    if "analyst" in t or "analytical" in t:
        return "Analyst"
    if "protection" in t or "security" in t:
        return "Governance & protection"
    if "lead" in t or "manager" in t:
        return "Lead / manager"
    if "quality" in t or "validator" in t or "failsafe" in t:
        return "Data quality & validation"
    if any(w in t for w in ["administrator", "assistant", "coordinator", "co-ordinator",
                            "data input", "secretary"]):
        return "Administration, assistant & coordination"
    if "coder" in t:
        return "Clinical coding"
    return "Other"


def flexibility(pattern: str) -> str:
    """Remote > flexible > standard. 'Hybrid' is not a value on the advert form."""
    p = pattern.lower()
    if "remote" in p:
        return "Home or remote working listed"
    if any(w in p for w in ["flexible", "compressed", "job share"]):
        return "Flexible working listed (no remote)"
    return "No flexibility listed"


def table(title: str, df: pd.DataFrame) -> None:
    print(f"\n### {title}\n")
    print(df.to_markdown())


def main() -> None:
    d = pd.read_csv(CSV, parse_dates=["date_posted", "closing_date_clean"])
    d["location"] = d["location"].str.replace(r"\s+", " ", regex=True).str.strip()
    d["flexibility"] = d["working_pattern"].apply(flexibility)
    d["open_days"] = (d["closing_date_clean"] - d["date_posted"]).dt.days
    da = d[d["role_category"] == "Data & Analytics"].copy()
    da["family"] = da["job_title"].apply(job_family)
    annual = d["salary_type"].eq("Annual")
    da_annual = da["salary_type"].eq("Annual")
    n, nda = len(d), len(da)

    print(f"Sample: {n} adverts | Data & Analytics: {nda} ({nda / n:.0%})")

    # ---- Objective 2: demand ------------------------------------------------
    t = d["role_category"].value_counts().rename("adverts").to_frame()
    t["share"] = (t["adverts"] / n).map("{:.0%}".format)
    table("Obj 2a: role categories (all 100)", t)
    t = da["family"].value_counts().rename("adverts").to_frame()
    t["share_of_DA"] = (t["adverts"] / nda).map("{:.0%}".format)
    table("Obj 2b: families inside Data & Analytics (40)", t)

    # ---- Objective 3: compensation -----------------------------------------
    s = d[annual]["salary_midpoint"]
    print(f"\nObj 3: annual salary n={len(s)} median={s.median():,.0f} mean={s.mean():,.0f} "
          f"min={s.min():,.0f} max={s.max():,.0f}")
    s2 = da[da_annual]["salary_midpoint"]
    print(f"Obj 3: Data & Analytics annual n={len(s2)} median={s2.median():,.0f} "
          f"min={s2.min():,.0f} max={s2.max():,.0f}; no salary shown: {(~da_annual).sum()}")
    g = da[da_annual].groupby("family")["salary_midpoint"].agg(["count", "median", "min", "max"])
    table("Obj 3a: Data & Analytics salary by family", g.sort_values("median", ascending=False).round(0))
    bands = pd.cut(s, [0, 30000, 50000, 1e9], right=False, labels=["<30k", "30-49.9k", "50k+"])
    table("Obj 3b: pay levels (all annual)", bands.value_counts().sort_index().to_frame("adverts"))

    # ---- Objective 4: location ---------------------------------------------
    loc = d["location"].value_counts()
    t = loc.head(10).rename("adverts").to_frame()
    t["share"] = (t["adverts"] / n).map("{:.0%}".format)
    table("Obj 4a: top 10 locations", t)
    print(f"\nObj 4: top-10 total={loc.head(10).sum()} ; distinct locations={loc.size}; "
          f"locations with 1 advert={(loc == 1).sum()}")
    table("Obj 4b: Data & Analytics top locations", da["location"].value_counts().head(6).to_frame("adverts"))

    # ---- Objective 5: flexibility ------------------------------------------
    t = d["flexibility"].value_counts().rename("adverts").to_frame()
    t["share"] = (t["adverts"] / n).map("{:.0%}".format)
    table("Obj 5a: flexibility (all 100)", t)
    t = da["flexibility"].value_counts().rename("adverts").to_frame()
    t["share_of_DA"] = (t["adverts"] / nda).map("{:.0%}".format)
    table("Obj 5b: flexibility (Data & Analytics)", t)
    print(f"\nObj 5: mention 'Part-time' = {d['working_pattern'].str.contains('Part-time').sum()}; "
          f"full-time only = {(d['working_pattern'] == 'Full-time').sum()}")
    rem = d[d["flexibility"].str.startswith("Home")][["job_title", "role_category", "contract_type"]]
    table("Obj 5c: adverts listing home or remote working", rem)

    # ---- Objective 6: employment type --------------------------------------
    t = d["contract_type"].value_counts().rename("adverts").to_frame()
    t["share"] = (t["adverts"] / n).map("{:.0%}".format)
    table("Obj 6a: contract type (all 100)", t)
    t = da["contract_type"].value_counts().rename("adverts").to_frame()
    t["share_of_DA"] = (t["adverts"] / nda).map("{:.0%}".format)
    table("Obj 6b: contract type (Data & Analytics)", t)

    # ---- Objective 1: characteristics for job-seekers ----------------------
    print(f"\nObj 1: advert open (posting to closing) median={d['open_days'].median():.0f} days; "
          f"within 21 days={(d['open_days'] <= 21).sum()}")
    prof = da[da_annual & (da["salary_midpoint"] >= 40000)]
    print(f"Obj 1: D&A with annual salary >= 40k: {len(prof)} "
          f"(permanent: {(prof['contract_type'] == 'Permanent').sum()}, "
          f"flexible or remote listed: {(prof['flexibility'] != 'No flexibility listed').sum()}, "
          f"remote listed: {prof['flexibility'].str.startswith('Home').sum()})")
    table("Obj 1: D&A adverts with salary >= 40k",
          prof[["job_title", "salary_midpoint", "contract_type", "flexibility"]]
          .sort_values("salary_midpoint", ascending=False))
    emp = da["employer"].value_counts()
    print(f"\nObj 1: D&A employers={emp.size}; employers with 2+ D&A adverts={(emp >= 2).sum()}")

    # ---- Closing status as of today ----------------------------------------
    today = pd.Timestamp.today().normalize()
    print(f"\nClosing status as of {today.date()}: passed={(d['closing_date_clean'] < today).sum()}, "
          f"not yet closed={(d['closing_date_clean'] >= today).sum()}")


if __name__ == "__main__":
    sys.exit(main())
