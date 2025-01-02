from flask import Flask, render_template, request, redirect, Response, g
from scraper import scraper
from descriptive import *
from prescriptive import *
from featurizing import *
from data_exploration import *
from flask import jsonify
import json
from model import *
from evaluate_accuracy import *
from time import time


app = Flask(__name__)

# The following lines are tools to monitor and maintain the product 

@app.before_request
def log_request():
    g.start = time()

@app.after_request
def log_response(response):
    if hasattr(g, 'start'):
        duration = time() - g.start
        print(f"Request took {duration:.2f} seconds")
    return response

# The following lines are a basic security feature
USERNAME = "admin"
PASSWORD = "password"

# Basic Authentication function
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Authenticate function
def authenticate():
    return Response(
    'Unauthorized access. Please provide a valid username and password.',
    401,
    {'WWW-Authenticate': 'Basic realm="Login required"'}
)

# Basic security check for each request
@app.before_request
def before_request():
    if not request.authorization or not check_auth(request.authorization.username, request.authorization.password):
        return authenticate()


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

current_job_data = default_job_data.copy()

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
        if budget != 'Not available':
            budgetCategory = categorize_budget((budget))
        else: 
            budgetCategory = "Unknown"
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
        summary = summarize_data(job_data)
    return render_template('index.html', jobs=job_list, summary=summary)

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

@app.route('/visualize', methods=['GET'])
def visualize():
    if USE_DEFAULTS:
        job_data = default_job_data
    else:
        job_data = scraper()
    
    # Convert job data into a string that JavaScript can use
    jobs_str = ""
    for job in job_data.values():
        jobs_str += f"{job['title']}:{job['budget']}|"
    
    return render_template('visualize.html', jobs_data=jobs_str)

class SimpleML:
    def predict(self, job):
        budget = float(job["budget"])
        elapsed = sum(int(x) * 60 ** i for i, x in enumerate(reversed(job["elapsed"].split(":"))))
        experience = 2 if job["experience_level"] == "Expert" else 1
        return "Apply" if budget + experience > 60 else "Skip"

@app.route('/ml', methods=['GET', 'POST'])
def ml_visualize():
    predictions = {job_id: SimpleML().predict(job) for job_id, job in default_job_data.items()} if request.method == "POST" else {}
    return render_template("ml.html", jobs=default_job_data, predictions=predictions)


@app.route('/accuracy', methods=['GET'])
def accuracy():
    # Fetch the job data
    if USE_DEFAULTS:
        job_data = default_job_data
    else:
        job_data = scraper()

    # Render the accuracy page and pass the job data for inspection
    return render_template('accuracy.html', job_data=job_data)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    global default_job_data
    scraped_data = scraper()
    if request.method == 'POST':
        overwrite = request.form.get('overwrite')  # 'yes' or 'no'
        if overwrite == "no":
            return redirect('/')
        if overwrite == "yes":
            # Loop through scraped data and update the dictionary
            for i, job_data in enumerate(scraped_data, start=1):
                job_key = f"job{i}"  # Dynamically create job keys like job1, job2, etc.
                # Add or overwrite job data in the dictionary
                default_job_data[job_key] = {
                    "title": job_data["title"],
                    "description": job_data["description"],
                    "budget": job_data["budget"],
                    "elapsed": job_data["elapsed"],
                    "link": job_data["link"],
                    "experience_level": job_data["experience_level"]
                }
            
            print("Job data has been overwritten.")
        else:
            print("Job data has not been overwritten.")
        return redirect('/')  # Redirect to index
    return render_template('scrape.html', scraped_data=scraped_data, default_data=default_job_data)

@app.route('/dashboard')
def dashboard():
    if USE_DEFAULTS:
        job_data = default_job_data
    else:
        job_data = scraper()  # Assuming scraper() provides job data
    experience_levels = {'Beginner': 0, 'Intermediate': 0, 'Expert': 0}
    beginnerCount = 0
    intermediateCount = 0
    expertCount = 0
    for job in job_data.values():
        if(job['experience_level']) == 'Beginner':
            beginnerCount += 1
        elif(job['experience_level']) == 'Intermediate':
            intermediateCount += 1
        elif(job['experience_level']) == 'Expert':
            expertCount +=1
    budgets = [float(job["budget"]) for job in job_data.values()]
    elapsed_times = [
        sum(int(x) * 60 ** i for i, x in enumerate(reversed(job["elapsed"].split(":"))))
        for job in job_data.values()
    ]   

    lessThan1Hour=0
    greaterThan1Hour=0
    for job in job_data.values():
        elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(job["elapsed"].split(":"))))
        
        # Categorize elapsed time into ranges
        if elapsed_seconds < 3600:
            lessThan1Hour += 1
        elif 3600 <= elapsed_seconds:
            greaterThan1Hour += 1
        
    return render_template('dashboard.html', job_data=job_data, budgets=budgets, experience_levels=experience_levels, elapsed_times=elapsed_times, beginnerCount = beginnerCount, intermediateCount = intermediateCount, expertCount = expertCount, lessThan1Hour = lessThan1Hour, greaterThan1Hour=greaterThan1Hour)

if __name__ == '__main__':
    app.run(debug=True)