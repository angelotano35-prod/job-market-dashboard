# Job Market Dashboard

Scrapes live IT/QA/software job postings from RemoteOK and Arbeitnow APIs,
stores them in SQLite, and visualizes hiring trends with pandas + matplotlib.

## What it answers
- Which companies are hiring most right now?
- What skills/tags appear most often in postings?
- Where are most remote jobs located?

## Tech Stack
Python, requests, SQLite, pandas, matplotlib, seaborn, Jupyter

## How to run
```bash
pip install -r requirements.txt
python main.py
jupyter notebook analysis/gui_dashboard.py
```
