def filter_and_prioritize_jobs(job_data, keywords=None, min_budget=None, max_budget=None, experience_levels=None):
    filtered_jobs = []

    # Loop through the job data and apply the user-defined filters
    for job in job_data.values():
        title = job.get('title', '')
        description = job.get('description', '')
        budget_str = job.get('budget', '0')
        experience_level = job.get('experience_level', 'Unknown')

        # Try to convert the budget to a float
        try:
            budget = float(budget_str)
        except ValueError:
            budget = 0  # Default to 0 if budget conversion fails

        # Check if the job matches the user-defined criteria
        if keywords and not any(keyword.lower() in (title + description).lower() for keyword in keywords):
            continue  # Skip this job if it doesn't match any of the keywords

        if min_budget and budget < min_budget:
            continue  # Skip this job if it doesn't meet the minimum budget

        if max_budget and budget > max_budget:
            continue  # Skip this job if it exceeds the maximum budget

        if experience_levels and experience_level not in experience_levels:
            continue  # Skip if the experience level doesn't match the user's criteria

        # Add the job to the filtered list if it passes all the criteria
        filtered_jobs.append(job)

    return filtered_jobs