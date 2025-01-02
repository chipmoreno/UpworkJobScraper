from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pprint import pprint

def scraper():
    driver = webdriver.Chrome()
    driver.get('https://www.upwork.com/nx/search/jobs/?q=copywriting')
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    job_tiles = soup.find_all('article', {'data-test': 'JobTile'})[:5]
    job_data = []
    for job_tile in job_tiles:
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
        if budget_element == 'Hourly':
            budget = 0
        if budget_element:
            # Extract fixed-price budget
            budget = budget_element.find_all('strong')[1].get_text(strip=True)
        else:
            # If no fixed-price budget, check for hourly budget
            hourly_element = job_tile.find('li', {'data-test': 'job-type-label'})
            if hourly_element and 'Hourly' in hourly_element.get_text(strip=True):
                # Extract hourly budget
                budget_text = hourly_element.find('strong').get_text(strip=True)
                # Remove 'Hourly: ' from the text and split the range if needed
                budget_text = budget_text.replace('Hourly: ', '')
                # If it's a range, calculate the midpoint
                if '-' in budget_text:
                    budget_values = [float(num.replace('$', '').replace(',', '').strip()) for num in budget_text.split('-')]
                    if len(budget_values) == 2:
                        budget = sum(budget_values) / 2  # Calculate midpoint for hourly range
                else:
                    # If it's a single value, just clean and convert it
                    print(budget)
                    #budget = float(budget_text.replace('$', '').replace(',', '').strip())
                    budget = 0

        # Convert budget to float if it's a valid numeric value
        try:
            if isinstance(budget, str) and budget != "Not available":
                # Remove any non-numeric characters (like '$' and ',') before converting to float
                budget = float(budget.replace('$', '').replace(',', ''))
        except ValueError:
            budget = "Not available"  # If conversion fails, assign "Not available"

        elapsed = job_tile.find('small', {'data-test': 'job-pubilshed-date'})
        print (f"Elapsed Step 1, raw dump from scrape: {elapsed}")
        elapsed = elapsed.text.strip()  # Get the text from the first element
        print(f"Elapsed step 2 stripping from raw dump: {elapsed}")
        hours, minutes, seconds = 0, 0, 0
        if 'second' in elapsed:
            seconds = int([word for word in elapsed.split() if word.isdigit()][0])
            print (f"Seconds:  {seconds}")
            elapsed = f"{hours:02}:{minutes:02}:{seconds:02}"
        if 'minute' in elapsed:
            minutes = int([word for word in elapsed.split() if word.isdigit()][0])
            (f"Minutes:  {minutes}")
            elapsed = f"{hours:02}:{minutes:02}:{seconds:02}"
        if 'hour' in elapsed:
            hours = int([word for word in elapsed.split() if word.isdigit()][0])
            (f"Hours:  {hours}")
            elapsed = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"Elapsed Step 4 After Final Assignment: {elapsed}")

        link = f"https://upwork.com{title_element['href']}" if title_element else None
        experience_level = job_tile.find('li', {'data-test': 'experience-level'}).get_text(strip=True) if job_tile.find('li', {'data-test': 'experience-level'}) else None
        
        job_data.append({
            'title':title,
            'description': description,
            'budget': budget,
            'elapsed': elapsed,
            'link': link,
            'experience_level': experience_level,
                            })
    return job_data
