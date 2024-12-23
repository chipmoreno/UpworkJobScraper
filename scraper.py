from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pprint import pprint
from RandGen import *

driver = webdriver.Chrome()
driver.get('https://www.upwork.com/nx/search/jobs/?q=copywriting')
time.sleep(5)
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')
job_tiles = soup.find_all('article', {'data-test': 'JobTile'})
job_data_list = []
job_tiles = soup.find_all('article', {'data-test': 'JobTile'})
job_data = {}

def scraper():
    for job_tile in job_tiles:
        job_id = generate_id()
        title_element = job_tile.find('a', {'data-test': 'job-tile-title-link UpLink'})
        title = title_element.get_text(strip=True) if title_element else None
        description = job_tile.find('p', {'class': 'mb-0 text-body-sm'}).get_text(strip=True)
        budget = job_tile.find('li', {'data-test': 'job-type-label'}).get_text(strip=True)
        posted = job_tile.find('small', {'data-test': 'job-pubilshed-date'}).get_text(strip=True)
        category = job_tile.find('button', {'data-test': 'token'}).get_text(strip=True)
        link = f"https://upwork.com{title_element['href']}" if title_element else None
        type = job_tile.find('div', {'class': 'job-type-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'job-type-label'}) else None
        experience_level = job_tile.find('div', {'class': 'experience-level'}).get_text(strip=True) if job_tile.find('div', {'class': 'experience-level'}) else None
        duration = job_tile.find('div', {'class': 'duration-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'duration-label'}) else None
        total_spent = job_tile.find('div', {'class': 'total-spent'}).get_text(strip=True) if job_tile.find('div', {'class': 'total-spent'}) else None
        description = job_tile.find('div', {'class': 'text-body-sm'}).get_test(strip=True) if job_tile.find('div', {'classl': 'text-body-sm'}) else None
        
        job_data[job_id] = {
            'title':title,
            'description': description,
            'budget': budget,
            'posted': posted,
            'category': category,
            'link': link,
            'type': type,
            'experience_level': experience_level,
            'duration': duration,
            'total_spent': total_spent,
                            }
        print(f"{job_id}: {job_data[job_id]['title']}\n")
    return job_data
scraper()
'''Ideas:


- Program needs deploy data from each run into a user interface or feed application. 
- Accept front-end input for search query(s) 


'''