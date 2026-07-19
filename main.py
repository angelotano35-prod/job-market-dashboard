from db.database import init_db
from scraper.fetch_remoteok import fetch_remoteok_jobs
from scraper.fetch_arbeitnow import fetch_arbeitnow_jobs

if __name__ == "__main__":
    init_db()

    keywords = ["qa", "software", "developer", "support"]
    for kw in keywords:
        fetch_remoteok_jobs(kw)
        fetch_arbeitnow_jobs(kw)

    print("Done. Data saved to data/jobs.db")