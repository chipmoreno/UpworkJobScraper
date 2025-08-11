Job Application Assistant
A Flask web application that scrapes job listings and provides tools for analysis, visualization, and making application decisions. This project serves as a personal assistant for job seekers, particularly for those looking for online freelance work.

Key Features 🤖
Job Scraping: Scrapes job data from a specified online platform (e.g., Upwork) based on predefined keywords.

Data Analysis: Provides a dashboard with descriptive statistics on job budgets, experience levels, and elapsed times.

Visualization: Renders basic visualizations of job data to help users identify trends.

Machine Learning Integration: Includes a simple machine learning model to predict which jobs are a good fit and which to skip.

Data Persistence: Saves and loads a list of "seen" jobs to avoid processing the same listings multiple times.

Debugging & Development Tools: Includes a debug mode with default data, and a basic authentication system for protected routes.

How to Run Locally 💻
Clone the repository:

Bash

git clone [your-repository-url]
cd [your-repository-name]
Install dependencies:
This project requires Flask and other libraries specified in the requirements.txt file (if one exists). Make sure to install them.

Bash

pip install -r requirements.txt
Configure environment variables:
The application uses basic authentication. Set your desired username and password.

Bash

export USERNAME="your_username"
export PASSWORD="your_password"
Run the application:

Bash

python app.py
Access the application:
Open your web browser and navigate to http://127.0.0.1:5000. You will be prompted to log in with the credentials you set.
