from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Set up WebDriver (make sure 'chromedriver' is in your PATH)
driver = webdriver.Chrome()

# Open the Upwork jobs page
driver.get('https://www.upwork.com/nx/search/jobs/?q=copywriting')

# Wait for the page to load (adjust as necessary)
time.sleep(5)

# Get the page content
html = driver.page_source

# Close the browser
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

# Initialize a list to store job data
job_data_list = []

# Find all job tiles
job_tiles = soup.find_all('article', {'data-test': 'JobTile'})


# Loop through each job tile and extract required information
for job_tile in job_tiles:
    job_data = {}

    # Extract job title link
    title_element = job_tile.find('a', {'data-test': 'job-tile-title-link UpLink'})
    job_data['job_title'] = title_element.get_text(strip=True) if title_element else None
    job_data['description'] = job_tile.find('p', {'class': 'mb-0 text-body-sm'}).get_text(strip=True)
    job_data['budget'] = job_tile.find('li', {'data-test': 'job-type-label'}).get_text(strip=True)
    job_data['posted'] = job_tile.find('small', {'data-test': 'job-pubilshed-date'}).get_text(strip=True)
    job_data['category'] = job_tile.find('button', {'data-test': 'token'}).get_text(strip=True)
    #job_data['link'] = job_tile.find( {'h5 mb-0 mr-2 job-tile-title': 'data-v-489be0f1><a href='}).get_text(strip=True)

    print(job_data['job_title'])
    print(job_data['description'])
    print(job_data['budget'])
    print((job_data['posted'])[6:])
    print(job_data['category'])
    #print(job_data['link'])

    #job_data['job_link'] = f"https://upwork.com{title_element['href']}" if title_element else None

    # Extract additional data
    job_data['job_type'] = job_tile.find('div', {'class': 'job-type-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'job-type-label'}) else None
    job_data['experience_level'] = job_tile.find('div', {'class': 'experience-level'}).get_text(strip=True) if job_tile.find('div', {'class': 'experience-level'}) else None
    job_data['duration'] = job_tile.find('div', {'class': 'duration-label'}).get_text(strip=True) if job_tile.find('div', {'class': 'duration-label'}) else None
    job_data['total_spent'] = job_tile.find('div', {'class': 'total-spent'}).get_text(strip=True) if job_tile.find('div', {'class': 'total-spent'}) else None
    job_data['description'] = job_tile.find('div', {'class': 'text-body-sm'}).get_test(strip=True) if job_tile.find('div', {'classl': 'text-body-sm'}) else None
    
    # Token container
    job_data['token_container'] = ' '.join([token.get_text(strip=True) for token in job_tile.find_all('div', {'class': 'air3-token-container'})])
    
    # Proposals Tier
    job_data['proposals_tier'] = job_tile.find('div', {'class': 'proposals-tier'}).get_text(strip=True) if job_tile.find('div', {'class': 'proposals-tier'}) else None
    
    # Add the job data to the list
    job_data_list.append(job_data)

# Print the extracted job data in a pretty format
for job in job_data_list:
    print("Job Details:")
    print(f"Published Date: {job['published_date']}")
    print(f"Job Title: {job['job_title']}")
    #print(f"Job Link: {job['job_link']}")
    print(f"Job Type: {job['job_type']}")
    print(f"Experience Level: {job['experience_level']}")
    print(f"Duration: {job['duration']}")
    print(f"Total Spent: {job['total_spent']}")
    print(f"Tokens: {job['token_container'] if job['token_container'] else 'None'}")
    print(f"Proposals Tier: {job['proposals_tier']}")
    print(f"Description: {job['description']}")
    print("\n" + "-"*40 + "\n")  # Separator for each job
