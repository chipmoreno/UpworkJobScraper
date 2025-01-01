from flask import Flask, render_template, request
from scraper import scraper
from descriptive import *
from prescriptive import *
from featurizing import *

app = Flask(__name__)

USE_DEFAULTS = True  # Set this to True to use default data, False to scrape

# Default job data for debugging
default_job_data = {
    "job1": {
        "title": "Sample Job 1",
        "description": "This is a sample description for Job 1.",
        "budget": "50",
        "elapsed": "00:10:00",
        "link": "https://www.upwork.com/job1",
        "experience_level": "Intermediate"
    },
    "job2": {
        "title": "Sample Job 2",
        "description": "This is a sample description for Job 2.",
        "budget": "75",
        "elapsed": "33:00:10",
        "link": "https://www.upwork.com/job2",
        "experience_level": "Expert"
    },
    # Add more sample jobs if needed
}

@app.route('/', methods=['GET', 'POST'])
def index():
    job_list = []
    if USE_DEFAULTS:
        # Use default data for debugging
        job_data = default_job_data
    else:
        # Scrape the data if USE_DEFAULTS is set to False
        job_data = scraper()
    for job in job_data.values():
        title = job.get('title', '')
        description = job.get('description', '')
        budget = job.get('budget', '0')
        budgetCategory = categorize_budget((budget))
        experience_level = job.get('experience_level', 'Unknown')
        elapsed = job.get('elapsed')
        link = job.get('link')
        job_list.append({
                'title': title,
                'elapsed': elapsed,
                'description': description,
                'link': link,
                'budget': budget,
                'experience_level': experience_level,
                'budgetCategory': budgetCategory
            })
    return render_template('index.html', jobs=job_list)

@app.route('/recent_jobs')
def recent_jobs_page():
    if USE_DEFAULTS:
        # Use default data for debugging
        job_data = default_job_data
    else:
        # Scrape the data if USE_DEFAULTS is set to False
        job_data = scraper()
    recent_jobs = get_recent_jobs(job_data)  # Filter jobs from last 10 minutes
    return render_template('recent_jobs.html', recent_jobs=recent_jobs)

@app.route('/jobs_above_budget/', methods=['GET'])
def jobs_above_budget():
    if USE_DEFAULTS:
        # Use default data for debugging
        job_data = default_job_data
    else:
        # Scrape the data if USE_DEFAULTS is set to False
        job_data = scraper()
    # Get the budget threshold from the URL query parameter
    budget_threshold = request.args.get('budget', default=0, type=int)

    # Get the jobs above the threshold using the prescribed function
    jobs = prescribe_jobs_above_budget(job_data, budget_threshold)

    return render_template('jobs_above_budget.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)