import requests
import json
import os
from dotenv import load_dotenv

# 🌿 Load environment variables from .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

API_URL = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&what=developer&where=India&results_per_page=25"

def fetch_and_save_jobs():
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()

        jobs = data.get("results", [])

        formatted = [{
            "title": job.get("title", "No title"),
            "company": {
                "display_name": job.get("company", {}).get("display_name", "Unknown")
            },
            "location": {
                "display_name": job.get("location", {}).get("display_name", "India")
            },
            "created": job.get("created", ""),
            "redirect_url": job.get("redirect_url", ""),
            "description": job.get("description", "")
        } for job in jobs]

        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump({"results": formatted}, f, indent=2)

        return {"status": "success", "results": formatted}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    fetch_and_save_jobs()
