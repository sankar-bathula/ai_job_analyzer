from jobspy import scrape_jobs
import pandas as pd

def test_search():
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term="software engineer",
        location="India",
        results_wanted=5,
        hours_old=72,
        country_around="india"
    )
    print(f"Found {len(jobs)} jobs")
    print(jobs.head())

if __name__ == "__main__":
    try:
        test_search()
    except Exception as e:
        print(f"Error: {e}")
