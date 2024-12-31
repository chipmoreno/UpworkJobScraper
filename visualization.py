import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_category_counts(category_counts):
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color='skyblue')
    plt.title('Job Distribution by Category')
    plt.xlabel('Job Categories')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_experience_level_distribution(experience_level_counts):
    labels = list(experience_level_counts.keys())
    sizes = list(experience_level_counts.values())
    colors = ['lightcoral', 'lightgreen', 'lightblue', 'gold']
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Job Distribution by Experience Level')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def plot_jobs_over_time(job_data):
    from collections import defaultdict
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    # Create a dictionary to hold the count of jobs per date
    date_counts = defaultdict(int)
    for job in job_data:
        posted_date = job.get('posted')
        date_counts[posted_date] += 1

    # Sort by date
    dates = sorted(date_counts.keys())
    counts = [date_counts[date] for date in dates]

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o', color='b')
    plt.title('Number of Jobs Posted Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.tight_layout()
    plt.show()

def plot_salary_vs_budget(job_data):
    budgets = []
    salaries = []
    categories = []
    for job in job_data:
        budget = job.get('budget')
        salary = job.get('salary')
        category = job.get('category')

        if budget and salary:  # Ensure no missing data
            budgets.append(budget)
            salaries.append(salary)
            categories.append(category)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(budgets, salaries, c=categories, cmap='viridis', alpha=0.7)
    plt.title('Salary vs. Budget for Different Job Categories')
    plt.xlabel('Budget')
    plt.ylabel('Salary')
    plt.colorbar(scatter, label='Job Categories')
    plt.show()

def plot_heatmap(job_data):
    # Convert job data into a DataFrame for easier manipulation
    df = pd.DataFrame(job_data)

    # Use seaborn to create a heatmap of correlation between budget and salary
    correlation_matrix = df[['budget', 'salary', 'experience_level']].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap of Job Features')
    plt.show()

def save_and_render_plot():
    # Plotting logic (e.g., bar chart)
    plt.figure(figsize=(10, 6))
    plt.bar(['A', 'B', 'C'], [10, 20, 30])
    plt.title('Simple Bar Chart')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    
    # Save the plot
    plot_path = 'static/plot.png'
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path