from jobspy import scrape_jobs
import pandas as pd
from typing import List, Optional

def search_portal_jobs(
    search_term: str, 
    location: str = "India", 
    sites: List[str] = ["linkedin", "indeed", "glassdoor"], 
    results_wanted: int = 10,
    hours_old: int = 72
) -> pd.DataFrame:
    """
    Search for jobs on various portals using jobspy.
    """
    try:
        jobs = scrape_jobs(
            site_name=sites,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_around=location.lower() if location else "india"
        )
        
        if jobs.empty:
            return pd.DataFrame()
            
        # Select relevant columns and handle potential missing ones
        columns_to_keep = [
            'id', 'site', 'job_url', 'title', 'company', 
            'location', 'job_type', 'date_posted', 'description'
        ]
        
        # Ensure description exists
        if 'description' not in jobs.columns:
            jobs['description'] = ""
            
        return jobs[jobs.columns.intersection(columns_to_keep)]
        
    except Exception as e:
        print(f"Error scraping jobs: {e}")
        return pd.DataFrame()

def get_job_details(job_id: str, df: pd.DataFrame) -> Optional[dict]:
    """
    Get details of a specific job from the dataframe.
    """
    job = df[df['id'] == job_id]
    if not job.empty:
        return job.iloc[0].to_dict()
    return None
