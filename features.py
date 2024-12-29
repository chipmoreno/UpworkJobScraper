def extract_features(job_data):
    features = []
    for job in job_data:
        # Extracting necessary details from each job
        budget = job.get('budget')
        category = job.get('category', 'Unknown')
        experience_level = job.get('experience_level', 'Unknown')
        time_posted = job.get('time_posted', 'Unknown')

        # Append the extracted features
        features.append({
            'budget': budget,
            'category': category,
            'experience_level': experience_level,
            'time_posted': time_posted
        })
    return features



def calculate_average_budget(features):
    budgets = [f['budget'] for f in features if f['budget'] > 0]
    return sum(budgets) / len(budgets) if budgets else 0


def normalize_budgets(features):
    # Get all valid budgets
    valid_budgets = [f['budget'] for f in features if f['budget'] > 0]
    max_budget = max(valid_budgets) if valid_budgets else 1  # Prevent division by 0

    # Normalize budgets based on the maximum budget
    for f in features:
        f['normalized_budget'] = f['budget'] / max_budget if f['budget'] > 0 else 0

    return features
