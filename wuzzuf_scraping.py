import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

# the target link
job_title = []
companies_name = []
companies_location = []
skills = []
links = []
date_posted = []
page_number = 0
while True:
    # extracting the html code
    page = requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=data%20analyst&start={page_number}')
    content = page.content
    soup = BeautifulSoup(content, 'lxml')  # clarify the html code to be readable
    # extracting all jobs links from the page
    jobs = soup.find_all('h2', {'class': 'css-m604qf'})
    company_name = soup.find_all('a', {'class': 'css-17s97q8'})
    company_location = soup.find_all('span', {'class': 'css-5wys0k'})
    job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
    date_new = soup.find_all('div', {'class': 'css-4c4ojb'})
    date_old = soup.find_all('div', {'class': 'css-do6t5g'})
    date = [*date_new, *date_old]
    jobs_count = int(soup.find('strong').text)
    if page_number > jobs_count // 15:
        print('Pages Ended')
        break

    # extracting the text from the lists above
    for i in range(len(company_location)):
        job_title.append(jobs[i].text.strip().replace('-', ''))
        companies_name.append(company_name[i].text.strip())
        companies_location.append(company_location[i].text.strip())
        skills.append(job_skills[i].text.strip())
        links.append(jobs[i].find("a").attrs['href'])
        date_posted.append(date[i].text)
    page_number += 1
    print('page switched')
# creating csv file
lists = [job_title, companies_name, companies_location, skills, date_posted]
data = zip_longest(*lists)
with open(r'D:\Karim\bootcamp\wuzzuf_jobs.csv', 'w', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Job location', 'Skills required', 'Date posted'])
    writer.writerows(data)
