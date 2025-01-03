import time

def get_recent_jobs(job_data):
    recent_jobs = []
    for job in job_data.values():
        elapsed_str = job.get('elapsed', '')
        hours, minutes, seconds = map(int, elapsed_str.split(':'))
        elapsed_seconds = hours * 3600 + minutes * 60 + seconds
        if elapsed_seconds <= 600:
            recent_jobs.append(job)
        return recent_jobs
