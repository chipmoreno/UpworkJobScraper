def summarize_data(job_data):
    summary = 0.0
    for job in job_data.values():  # Loop over the job data (it is a dictionary of dictionaries)
        try:
            summary += float(job['budget'])  # Convert the 'budget' from string to float
        except ValueError:
            # In case the budget value is invalid, skip that job (or handle it as needed)
            continue
    summary = summary / len(job_data) if job_data else 0
    return summary