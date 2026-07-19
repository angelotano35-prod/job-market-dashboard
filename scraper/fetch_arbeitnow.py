import requests
from db.database import insert_job

def fetch_arbeitnow_jobs(keyword="qa"):
    url = "https://www.arbeitnow.com/api/job-board-api"
    response = requests.get(url)
    data = response.json()

    count = 0
    for job in data.get("data", []):
        title = job.get("title", "")
        if keyword.lower() in title.lower():
            insert_job({
                "source": "Arbeitnow",
                "title": title,
                "company": job.get("company_name", ""),
                "location": job.get("location", ""),
                "tags": ", ".join(job.get("tags", [])),
                "date_posted": str(job.get("created_at", "")),
                "url": job.get("url", "")
            })
            count += 1
    print(f"Arbeitnow: inserted {count} jobs matching '{keyword}'")