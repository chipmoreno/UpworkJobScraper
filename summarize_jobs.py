import matplotlib.pyplot as plt
from collections import defaultdict
def summarize_jobs(job_data):
    category_counts = defaultdict(int)
    budget_by_category = defaultdict(list)
    experience_level_counts = defaultdict(int)

    for job in job_data.values():
        category = job.get('category', 'Uncategorized')  # Default if not found
        experience_level = job.get('experience_level', 'Unknown')  # Default if not found
        
        # Get the budget and attempt to convert to float
        budget_str = job.get('budget', '0')
        
        # Attempt to convert to float, handle cases where it is not a valid number
        try:
            budget = float(budget_str)  # Try to convert to float
        except ValueError:
            print(f"Invalid budget value: {budget_str} for job: {job.get('title')}")
            budget = 0  # Default to 0 if the conversion fails

        category_counts[category] += 1
        budget_by_category[category].append(budget)
        experience_level_counts[experience_level] += 1

    # Calculate average budget per category
    avg_budget_by_category = {}
    for category, budgets in budget_by_category.items():
        avg_budget_by_category[category] = sum(budgets) / len(budgets) if budgets else 0

    return category_counts, experience_level_counts, avg_budget_by_category
