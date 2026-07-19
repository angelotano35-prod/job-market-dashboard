import requests
from db.database import insert_job

def fetch_remoteok_jobs(keyword="qa"):
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}  # required or API returns 403
    response = requests.get(url, headers=headers)
    jobs = response.json()[1:]  # first item is metadata, skip it

    count = 0
    for job in jobs:
        title = job.get("position", "")
        if keyword.lower() in title.lower() or keyword.lower() in job.get("description", "").lower():
            insert_job({
                "source": "RemoteOK",
                "title": title,
                "company": job.get("company", ""),
                "location": job.get("location", "Remote"),
                "tags": ", ".join(job.get("tags", [])),
                "date_posted": job.get("date", ""),
                "url": job.get("url", "")
            })
            count += 1
    print(f"RemoteOK: inserted {count} jobs matching '{keyword}'")