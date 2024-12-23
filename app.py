# app.py
from flask import Flask, jsonify, render_template
from scraper import scraper  # Import the scrape function from scraper.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    job_data = scraper()  # Call the scrape function from scraper.py
    return jsonify(job_data)

if __name__ == '__main__':
    app.run(debug=True)
