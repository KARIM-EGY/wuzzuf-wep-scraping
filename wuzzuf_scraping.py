import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import time

job_title = []
companies_name = []
companies_location = []
skills = []
links = []
date_posted = []
page_number = 0

while True:
    # Extracting the HTML code
    try:
        page = requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=data%20analyst&start={page_number}')
        page.raise_for_status()
        content = page.content
        soup = BeautifulSoup(content, 'lxml')  # Clarify the HTML code to be readable
    except requests.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        break

    # Extracting all jobs links from the page
    jobs = soup.find_all('h2', {'class': 'css-m604qf'})
    company_name = soup.find_all('a', {'class': 'css-17s97q8'})
    company_location = soup.find_all('span', {'class': 'css-5wys0k'})
    job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
    date_new = soup.find_all('div', {'class': 'css-4c4ojb'})
    date_old = soup.find_all('div', {'class': 'css-do6t5g'})
    date = [*date_new, *date_old]

    # Check if there are no more jobs
    if not jobs or not company_name or not company_location or not job_skills:
        print('No more jobs found.')
        break

    # Extracting the text from the lists above
    for i in range(len(jobs)):
        job_title.append(jobs[i].text.strip().replace('-', ''))
        companies_name.append(company_name[i].text.strip().replace('-', ''))
        companies_location.append(company_location[i].text.strip())
        skills.append(job_skills[i].text.strip())
        links.append(jobs[i].find("a").attrs['href'])
        date_posted.append(date[i].text if i < len(date) else 'N/A')

    # Increment page number and check if we have reached the end
    page_number += 1
    jobs_count = int(soup.find('strong').text)
    if page_number > jobs_count // 15:
        print('Pages Ended')
        break

    print('Page switched')

    # Be polite and wait a bit before the next request
    time.sleep(1)

# Creating CSV file
lists = [job_title, companies_name, companies_location, skills, date_posted]
data = zip_longest(*lists)

with open(r'D:\Karim\bootcamp\wuzzuf_jobs.csv', 'w', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Job Location', 'Skills Required', 'Date Posted'])
    writer.writerows(data)

print('CSV file created successfully')
