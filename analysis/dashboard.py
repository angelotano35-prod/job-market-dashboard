"""
Run this with: python analysis/dashboard.py
(run it from the job-market-dashboard root folder, not from inside analysis/)

Each chart will pop up in its own window. Close a window to move to the next one.
Charts are also saved as PNG files inside data/ automatically.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data
conn = sqlite3.connect("data/jobs.db")
df = pd.read_sql_query("SELECT * FROM jobs", conn)
print(f"Loaded {len(df)} rows from database.")
print(df.head())

# 2. Clean the data
df["tags"] = df["tags"].fillna("")
df["company"] = df["company"].str.strip()
df = df.drop_duplicates(subset=["url"])
print(f"Total unique jobs: {len(df)}")

if len(df) == 0:
    print("No data found. Run 'python main.py' first to scrape jobs.")
    exit()

# 3. Top hiring companies
top_companies = df["company"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_companies.values, y=top_companies.index)
plt.title("Top 10 Companies Hiring")
plt.xlabel("Number of Postings")
plt.tight_layout()
plt.savefig("data/top_companies.png")
plt.show()

# 4. Most common skills/tags
all_tags = df["tags"].str.split(", ").explode()
top_tags = all_tags.value_counts().head(15)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_tags.values, y=top_tags.index)
plt.title("Most In-Demand Skills/Tags")
plt.xlabel("Frequency")
plt.tight_layout()
plt.savefig("data/top_skills.png")
plt.show()

# 5. Jobs by source
plt.figure(figsize=(6, 6))
df["source"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Jobs by Source")
plt.ylabel("")
plt.savefig("data/jobs_by_source.png")
plt.show()

# 6. Top locations
top_locations = df["location"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_locations.values, y=top_locations.index)
plt.title("Top Job Locations")
plt.tight_layout()
plt.savefig("data/top_locations.png")
plt.show()

print("Done. Charts saved as PNG files inside the data/ folder.")
