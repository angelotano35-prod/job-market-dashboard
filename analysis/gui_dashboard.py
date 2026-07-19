"""
Run this with: python analysis/gui_dashboard.py
(run it from the job-market-dashboard root folder)

Opens a filter window. Set your filters, click "Show Charts",
and a set of chart windows will pop up based on your selections.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "data/jobs.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    df["tags"] = df["tags"].fillna("")
    df["company"] = df["company"].fillna("").str.strip()
    df["location"] = df["location"].fillna("")
    df = df.drop_duplicates(subset=["url"])
    return df


def show_charts(filtered_df):
    if len(filtered_df) == 0:
        messagebox.showinfo("No results", "No jobs match those filters. Try loosening them.")
        return

    # Top companies
    top_companies = filtered_df["company"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_companies.values, y=top_companies.index)
    plt.title(f"Top Companies Hiring ({len(filtered_df)} jobs matched)")
    plt.xlabel("Number of Postings")
    plt.tight_layout()
    plt.show()

    # Top tags/skills
    all_tags = filtered_df["tags"].str.split(", ").explode()
    all_tags = all_tags[all_tags != ""]
    if len(all_tags) > 0:
        top_tags = all_tags.value_counts().head(15)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_tags.values, y=top_tags.index)
        plt.title("Most In-Demand Skills/Tags")
        plt.xlabel("Frequency")
        plt.tight_layout()
        plt.show()

    # Jobs by source
    plt.figure(figsize=(6, 6))
    filtered_df["source"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Jobs by Source")
    plt.ylabel("")
    plt.show()

    # Top locations
    top_locations = filtered_df["location"].value_counts().head(10)
    if len(top_locations) > 0:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_locations.values, y=top_locations.index)
        plt.title("Top Job Locations")
        plt.tight_layout()
        plt.show()


def apply_filters():
    df = load_data()

    # Filter by source
    source = source_var.get()
    if source != "All":
        df = df[df["source"] == source]

    # Filter by keyword in title
    keyword = keyword_entry.get().strip()
    if keyword:
        df = df[df["title"].str.contains(keyword, case=False, na=False)]

    # Filter by location
    location = location_entry.get().strip()
    if location:
        df = df[df["location"].str.contains(location, case=False, na=False)]

    show_charts(df)


# ---------- Build the GUI window ----------
root = tk.Tk()
root.title("Job Market Dashboard - Filters")
root.geometry("400x300")

tk.Label(root, text="Job Market Dashboard", font=("Segoe UI", 14, "bold")).pack(pady=10)

# Source dropdown
tk.Label(root, text="Source:").pack(anchor="w", padx=20)
source_var = tk.StringVar(value="All")
source_dropdown = ttk.Combobox(root, textvariable=source_var, values=["All", "RemoteOK", "Arbeitnow"], state="readonly")
source_dropdown.pack(fill="x", padx=20, pady=5)

# Keyword filter
tk.Label(root, text="Job title keyword (e.g. QA, developer):").pack(anchor="w", padx=20, pady=(10, 0))
keyword_entry = tk.Entry(root)
keyword_entry.pack(fill="x", padx=20, pady=5)

# Location filter
tk.Label(root, text="Location (e.g. Remote, Philippines):").pack(anchor="w", padx=20, pady=(10, 0))
location_entry = tk.Entry(root)
location_entry.pack(fill="x", padx=20, pady=5)

# Note about salary
tk.Label(
    root,
    text="(Salary filtering not available yet — free APIs don't\nreliably provide salary data)",
    font=("Segoe UI", 8), fg="gray"
).pack(pady=(5, 0))

# Button
tk.Button(root, text="Show Charts", command=apply_filters, bg="#4CAF50", fg="white", font=("Segoe UI", 11)).pack(pady=20)

root.mainloop()
