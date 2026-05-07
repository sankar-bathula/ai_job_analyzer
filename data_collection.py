import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# =========================
# STEP 1: DATA COLLECTION
# =========================

# Example: Read data from CSV
df = pd.read_csv("jobs.csv")

print("Raw Data:")
print(df.head())

# =========================
# STEP 2: DATA CLEANING
# =========================

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove null values
df.dropna(inplace=True)

# Clean text columns
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text.strip()

df['Job_Description'] = df['Job_Description'].apply(clean_text)

# =========================
# STEP 3: FEATURE ENGINEERING
# =========================

# Example: Create text length feature
df['Description_Length'] = df['Job_Description'].apply(len)

# Example: Skill matching flag
skills = ['python', 'aws', 'docker']

for skill in skills:
    df[skill] = df['Job_Description'].apply(
        lambda x: 1 if skill in x else 0
    )

# =========================
# STEP 4: WEB SCRAPING (Optional)
# =========================

url = "https://example.com/jobs"

try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.find_all("h2")

    scraped_jobs = []

    for title in titles:
        scraped_jobs.append(title.text.strip())

    print("\nScraped Jobs:")
    print(scraped_jobs)

except Exception as e:
    print("Web Scraping Error:", e)

# =========================
# STEP 5: SAVE PROCESSED DATA
# =========================

df.to_csv("processed_jobs.csv", index=False)

print("\nProcessed data saved successfully!")