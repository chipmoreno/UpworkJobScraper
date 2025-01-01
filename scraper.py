from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pprint import pprint
from RandGen import *

def scraper():
    driver = webdriver.Chrome()
    driver.get('https://www.upwork.com/nx/search/jobs/?q=copywriting')
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    # Parse the page source
    soup = BeautifulSoup(html, 'html.parser')
    job_tiles = soup.find_all('article', {'data-test': 'JobTile'})
    job_data = {}
    for job_tile in job_tiles:
        job_id = generate_id()
        title_element = job_tile.find('a', {'data-test': 'job-tile-title-link UpLink'})
        title = title_element.get_text(strip=True) if title_element else None

        description = job_tile.find('p', {'class': 'mb-0 text-body-sm'})
        if description:
            description = description.get_text(strip=True)
        else:
            description = job_tile.find('div', {'class': 'text-body-sm'})
            description = description.get_text(strip=True) if description else None
        
        budget = "Not available"

        # Try to get the fixed-price budget
        budget_element = job_tile.find('li', {'data-test': 'is-fixed-price'})
        if budget_element:
            # Extract fixed-price budget
            budget = budget_element.find_all('strong')[1].get_text(strip=True)
        else:
            # If no fixed-price budget, check for hourly budget
            hourly_element = job_tile.find('li', {'data-test': 'job-type-label'})
            if hourly_element and 'Hourly' in hourly_element.get_text(strip=True):
                # Extract hourly budget
                budget_text = hourly_element.find('strong').get_text(strip=True)
                budget = budget_text.replace('Hourly: ', '')  # Remove 'Hourly: ' part

        # Convert budget to float if it's a valid numeric value
        try:
            if budget != "Not available":
                # Remove any non-numeric characters (like '$') before converting to float
                budget = float(budget.replace('$', '').replace(',', ''))
        except ValueError:
            budget = "Not available"  # If conversion fails, assign "Not available"

        posted_times = soup.find_all('small', {'data-test': 'job-pubilshed-date'})
        def convert_to_seconds(posted_time):
            if 'minute' in posted_time:
                minutes = int(posted_time.split(' ')[0])  # Get the number of minutes
                return minutes * 60  # Convert minutes to seconds
            elif 'hour' in posted_time:
                hours = int(posted_time.split(' ')[0])  # Get the number of hours
                return hours * 3600  # Convert hours to seconds
            return 0  # Return 0 if the time format is unrecognized

        def format_time(seconds):
            """Format seconds to HH:MM:SS format."""
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        for time_element in posted_times:
            time_text = time_element.find_all('span')[1].text.strip()  # Get the "X minutes ago" or "X hour ago" text
            seconds = convert_to_seconds(time_text)  # Convert to seconds
            elapsed = format_time(seconds)  # Format the time to HH:MM:SS

        category_element = job_tile.find('button', {'data-test': 'token'})
        if category_element:
            category = category_element.get_text(strip=True)
        else:
            category = "Not available"
        link = f"https://upwork.com{title_element['href']}" if title_element else None
        type = job_tile.find('div', {'class': 'job-type-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'job-type-label'}) else None
        experience_level = job_tile.find('li', {'data-test': 'experience-level'}).get_text(strip=True) if job_tile.find('li', {'data-test': 'experience-level'}) else None
        duration = job_tile.find('div', {'class': 'duration-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'duration-label'}) else None
        total_spent = job_tile.find('div', {'class': 'total-spent'}).get_text(strip=True) if job_tile.find('div', {'class': 'total-spent'}) else None
        
        job_data[job_id] = {
            'title':title,
            'description': description,
            'budget': budget,
            'elapsed': elapsed,
            'category': category,
            'link': link,
            'type': type,
            'experience_level': experience_level,
            'duration': duration,
            'total_spent': total_spent,
                            }
        print(f"{job_id}: {job_data[job_id]['title']}\n")
    return job_data
'''
Ideas:

- Deploy data to UI/Feed Outside Of Terminal
- Automate recurring program runs/updating of dictionary
- Accept front-end input for search query(s) 

'''