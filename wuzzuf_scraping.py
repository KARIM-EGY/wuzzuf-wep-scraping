import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

## the target link
url = 'https://wuzzuf.net/search/jobs/?q=data%20analyst&a=hpb'
job_title = []
companies_name = []
companies_location = []
skills = []
links = []
salary = []

## extracting the html code
page = requests.get(url)
content = page.content
soup = BeautifulSoup(content, 'lxml')  # clarify the html code to be readable
## extracting all jobs links from the page
jobs = soup.find_all('h2', {'class': 'css-m604qf'}) # extracting the job title
company_name = soup.find_all('a', {'class': 'css-17s97q8'}) # extracting the company name
company_location = soup.find_all('span', {'class': 'css-5wys0k'}) # extracting the job location
job_skills = soup.find_all('div', {'class': 'css-y4udm8'}) # extracting the skills required

## extracting the text from the lists above
for i in range(len(company_location)):
    job_title.append(jobs[i].text.strip())
    companies_name.append(company_name[i].text.strip())
    companies_location.append(company_location[i].text.strip())
    skills.append(job_skills[i].text.strip())
    links.append(jobs[i].find("a").attrs['href'])

## extract the data from every job
for link in links:
    job_page = requests.get(link)
    page_content = job_page.content
    page_soup = BeautifulSoup(page_content,'html.parser')
    salary.append(page_soup.find('span', {'class':'css-4xky9y'}))
## creating csv file
lists = [job_title, companies_name, companies_location, skills , salary]
data = zip_longest(*lists)
with open(r'D:\Karim\bootcamp\wuzzuf_jobs.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Job location', 'skills required', 'Salary'])
    writer.writerows(data)
