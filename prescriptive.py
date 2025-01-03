def prescribe_jobs_above_budget(job_data, budget_threshold):
    budget_threshold = float(budget_threshold)
    return [job for job in job_data.values() if float(job['budget']) > budget_threshold]
    