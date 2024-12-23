# app.py
from flask import Flask, jsonify, render_template
from scraper import scraper  # Import the scrape function from scraper.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    job_list = []
    job_data = scraper()  # Call the scrape function from scraper.py
    #return jsonify(job_data)
    for job in job_data.values():
        title = job.get('title')
        time_posted = job.get('time_posted')
        description = job.get('description')[:100]  # Get the first 100 characters
        link = job.get('link')

        job_list.append({
                'title': title,
                'time_posted': time_posted,
                'description': description,
                'link': link
            })
        
    return job_list

if __name__ == '__main__':
    app.run(debug=True)
