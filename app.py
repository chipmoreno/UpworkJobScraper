# app.py
from flask import Flask, jsonify, render_template
from scraper import scraper  # Import the scrape function from scraper.py
from summarize_jobs import *
from filterjobs import *

app = Flask(__name__)

@app.route('/')
def index():
    job_list = []
    job_data = scraper()  # Call the scrape function from scraper.py
    #return jsonify(job_data)


    for job in job_data.values():
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
