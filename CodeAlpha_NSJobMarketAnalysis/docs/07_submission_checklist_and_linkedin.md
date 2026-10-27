# 07 · CodeAlpha Submission Checklist & LinkedIn Post

## Your CodeAlpha requirements (from the internship instructions)

- [ ] Share your internship status on LinkedIn, **tagging @CodeAlpha**
- [ ] Complete **at least 2 or 3 tasks** (one task alone is considered incomplete and no certificate is issued). This project covers **Task 1 (Web Scraping)**, **Task 2 (EDA)** and **Task 3 (Data Visualization)**.
- [ ] GitHub repository named **`CodeAlpha_ProjectName`** → yours is `CodeAlpha_NSJobMarketAnalysis`
- [ ] Post a **video explanation** on LinkedIn **with the GitHub repo link**
- [ ] Submit through the **Submission Form** shared in your WhatsApp group (the only accepted route)

## Before you push to GitHub

- [ ] Reload the database, refresh Tableau and re-export the three PNGs ([guide](06_refreshing_the_dashboards.md))
- [ ] Open the dashboard images and check every number against the README
- [ ] Read the website's terms of use and confirm you may share the scraped data (if unsure, leave `data/` out and keep the code and docs)
- [ ] Confirm there are no passwords, database credentials or personal details in any file
- [ ] Preview `README.md` on GitHub: images show, links work, tables look right
- [ ] Repo description: *"Scraped 100 healthcare job adverts, cleaned them in Python, analysed them in PostgreSQL and visualised them in Tableau."*
- [ ] Add topics: `data-analytics`, `web-scraping`, `sql`, `tableau`, `python`, `postgresql`

## The 2-3 minute video (script outline)

1. **Hook (10 sec):** "What do healthcare data jobs actually look like? I scraped 100 job adverts to find out."
2. **The problem (20 sec):** Adverts are messy free text; salaries come as text, hourly or not at all.
3. **Scraping (30 sec):** Show the script/notebook collecting 100 adverts.
4. **Cleaning (30 sec):** Salary split, hourly vs annual, missing salaries kept as missing.
5. **SQL (30 sec):** Show the views and the median query.
6. **Dashboards (45 sec):** Walk through the three dashboards.
7. **Findings and recommendations (30 sec):** Walk through the six objectives in one line each: demand 40%, median £44,038, London only 9 adverts, 6% remote (0 for data roles), 75% permanent, and the £40k+ permanent shortlist.
8. **Limits and close (15 sec):** "It's a 100-advert sample, not the whole market. Repo link is in the post."

## LinkedIn post (draft, edit freely to sound like you)

> 🚀 Project time! I scraped, cleaned and analysed 100 healthcare job adverts to answer: *what do data and analytics jobs look like, and what should a job seeker target?*
>
> How I did it 👇
> 🕷️ Python (Requests + BeautifulSoup) to collect 100 adverts
> 🧹 Cleaning in Python and Excel: split salaries, separated hourly from annual pay, kept missing salaries as missing
> 🗄️ PostgreSQL for reusable views and medians
> 📊 Tableau for three interactive dashboards
>
> What I found (in this 100-advert sample):
> 📈 Demand: 40% were Data & Analytics roles, but only half of those are career-track (analyst, engineering, lead)
> 💷 Pay: median £44,038. Engineering and analyst roles pay roughly £45k to £57k; admin and data-quality roles roughly £27k to £28k
> 📍 Location: London leads with just 9 adverts. Hiring is scattered across 76 location labels
> 🏠 Flexibility: only 6% list home or remote working, and none of the 40 data roles do. Flexible ≠ remote!
> 📝 Contracts: 75% permanent (82% for data roles)
> 🎯 For job seekers: 18 data adverts pay £40k+, and 15 of them are permanent. Adverts were typically open for just 14 days
>
> My biggest lesson: check your filters and your units. A hidden filter once made a chart show only 33 of 100 postings, and one keyword rule quietly put "Audit" roles in IT. Catching both made me trust my numbers more.
>
> It's a sample, not the whole market, and the data doesn't say anything about visa sponsorship, so I treat these as patterns, not promises.
>
> Code, SQL, dashboards and write-up on GitHub: [paste your repo link here]
>
> Thank you @CodeAlpha for the opportunity! 💜
>
> #DataAnalytics #SQL #Tableau #Python #WebScraping #CodeAlpha #Internship #HealthcareData

## Final order of operations

1. Refresh data and dashboards (guide 06) → 2. Push to GitHub → 3. Record the video → 4. Post on LinkedIn with the repo link and the @CodeAlpha tag → 5. Submit the form from your WhatsApp group.
