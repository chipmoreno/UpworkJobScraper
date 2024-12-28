from flask import Flask, render_template, request
from summarize_jobs import summarize_jobs
from scraper import scraper
from filterjobs import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    job_list = []
    job_data = scraper()  # Call the scraping function from scraper.py

    # Default criteria (if no form input)
    keywords = []
    min_budget = None
    max_budget = None
    experience_levels = []

    # If the form is submitted (POST request), get the user-defined criteria
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        min_budget = request.form.get('min_budget', type=float)
        max_budget = request.form.get('max_budget', type=float)
        experience_levels = request.form.getlist('experience_levels')

    # Filter and prioritize the jobs based on the criteria
    filtered_jobs = filter_and_prioritize_jobs(job_data, keywords, min_budget, max_budget, experience_levels)

    # Prepare the job details for rendering
    for job in filtered_jobs:
        title = job.get('title')
        time_posted = job.get('time_posted')
        description = job.get('description')
        link = job.get('link')

        job_list.append({
                'title': title,
                'time_posted': time_posted,
                'description': description,
                'link': link
            })

    category_counts, experience_level_counts, avg_budget_by_category = summarize_jobs(job_data)

    return render_template('index.html', jobs=job_list, category_counts=category_counts, 
                           experience_level_counts=experience_level_counts, avg_budget_by_category=avg_budget_by_category)

if __name__ == '__main__':
    app.run(debug=True)