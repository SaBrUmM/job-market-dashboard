#!/usr/bin/env python3
"""
Job Postings Scraper
Collects job postings from HH.ru API
"""

import requests
import pandas as pd
import time
import json
import os
import re
from datetime import datetime
from typing import List, Dict
import random

class JobScraper:
    """Main scraper class for job postings"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'job-market-dashboard/1.0 (educational project)'
        }
        self.jobs = []
        self.api_base = 'https://api.hh.ru'

    def scrape_hh_api(self, search_term: str = "Data Science", max_pages: int = 20) -> List[Dict]:
        """Scrape job postings from HH.ru public API (no auth required)"""
        print(f"Fetching HH.ru API for '{search_term}'...")
        jobs = []

        for page in range(max_pages):
            try:
                params = {
                    'text': search_term,
                    'page': page,
                    'per_page': 100,
                    'area': 113,
                    'search_field': 'name'
                }
                response = requests.get(
                    f'{self.api_base}/vacancies',
                    params=params,
                    headers=self.headers,
                    timeout=15
                )

                if response.status_code != 200:
                    print(f"  Page {page+1}: HTTP {response.status_code}, stopping")
                    break

                data = response.json()
                items = data.get('items', [])
                total_pages = data.get('pages', 0)

                if not items:
                    break

                for item in items:
                    try:
                        salary_str = "Not specified"
                        salary_min = None
                        currency = None
                        sal = item.get('salary')
                        if sal:
                            lo = sal.get('from')
                            hi = sal.get('to')
                            currency = sal.get('currency', '')
                            if lo and hi:
                                salary_str = f"{lo} - {hi} {currency}"
                                salary_min = (lo + hi) / 2
                            elif lo:
                                salary_str = f"from {lo} {currency}"
                                salary_min = float(lo)
                            elif hi:
                                salary_str = f"up to {hi} {currency}"
                                salary_min = float(hi)
                            if salary_min and currency == 'RUR':
                                salary_min = salary_min / 1000

                        area = item.get('area', {})
                        location = area.get('name', 'N/A')

                        employment = item.get('employment', {})
                        emp_type = employment.get('name', 'Full-time')

                        snippet = item.get('snippet', {})
                        requirement = snippet.get('requirement', '') or ''
                        responsibility = snippet.get('responsibility', '') or ''
                        requirement = re.sub(r'<[^>]+>', ' ', requirement)
                        responsibility = re.sub(r'<[^>]+>', ' ', responsibility)
                        description = f"{requirement} {responsibility}".strip()

                        jobs.append({
                            'title': item.get('name', 'N/A'),
                            'company': (item.get('employer') or {}).get('name', 'N/A'),
                            'salary': salary_str,
                            'salary_min': salary_min,
                            'currency': currency,
                            'location': location,
                            'url': item.get('alternate_url', ''),
                            'source': 'HH.ru',
                            'description': description,
                            'employment_type': emp_type,
                            'experience_years': 0,
                            'scraped_date': datetime.now().isoformat()
                        })
                    except Exception as e:
                        print(f"  Error parsing item: {e}")
                        continue

                print(f"  Page {page+1}/{total_pages}: +{len(items)} jobs (total {len(jobs)})")

                if page >= total_pages - 1:
                    break

                time.sleep(0.3)

            except Exception as e:
                print(f"  Error on page {page+1}: {e}")
                break

        print(f"HH.ru API collected {len(jobs)} jobs for '{search_term}'")
        return jobs

    def scrape_mock_data(self, count: int = 1000) -> List[Dict]:
        """Generate realistic mock job data with proper descriptions for skill extraction"""
        print(f"Generating {count} mock job postings...")

        titles = [
            "Data Scientist", "Senior Data Scientist", "Junior Data Scientist",
            "Machine Learning Engineer", "ML Engineer", "Data Analyst",
            "Python Developer", "Backend Developer", "Full Stack Developer",
            "DevOps Engineer", "Cloud Engineer", "Software Engineer",
            "Data Engineer", "Analytics Engineer", "Business Analyst",
            "Systems Administrator", "Database Administrator", "QA Engineer"
        ]

        companies = [
            "Yandex", "Mail.ru", "VKontakte", "Sberbank", "Gazprom",
            "Rostelecom", "MegaFon", "Beeline", "Aviasales", "Booking.com",
            "Google", "Amazon", "Microsoft", "Apple", "Meta",
            "Airbnb", "Uber", "Spotify", "Netflix", "Stripe"
        ]

        locations = [
            "Moscow", "Saint Petersburg", "Ekaterinburg", "Novosibirsk",
            "New York", "San Francisco", "London", "Berlin", "Amsterdam",
            "Singapore", "Dubai", "Remote", "Hybrid"
        ]

        levels = ["Junior", "Middle", "Senior", "Lead", "Principal"]

        skill_sets = [
            {
                'desc': "We are looking for a specialist with strong python programming skills. "
                        "Requirements: experience with sql databases, pandas for data manipulation, "
                        "machine learning algorithms. Knowledge of tensorflow or pytorch is a plus."
            },
            {
                'desc': "Required: javascript development experience, react framework, "
                        "node.js for backend. Database: postgresql. Docker and kubernetes knowledge preferred."
            },
            {
                'desc': "Java developer needed. Must know spring framework, microservices architecture. "
                        "Experience with docker containers and kubernetes orchestration required. git version control."
            },
            {
                'desc': "ML engineer for deep learning projects. Skills: python, tensorflow or pytorch, "
                        "natural language processing (nlp), computer vision. "
                        "Statistics and mathematics background required."
            },
            {
                'desc': "Cloud engineer position. Requirements: aws services (ec2, s3, lambda), "
                        "docker and kubernetes, python scripting. CI/CD, infrastructure as code."
            },
            {
                'desc': "Data engineer role. Must have: sql, python, apache spark, hadoop ecosystem. "
                        "Experience with big data processing, ETL pipelines, postgresql or mongodb."
            },
            {
                'desc': "Backend developer with golang experience. "
                        "Requirements: golang, docker, kubernetes, postgresql database, microservices, git."
            },
            {
                'desc': "Data analyst position. Required: python, statistics and statistical analysis, "
                        "sql for data extraction, machine learning basics. Tableau or data visualization tools."
            },
            {
                'desc': "Frontend developer. Skills: typescript, react or angular framework. "
                        "DevOps basics: docker, aws deployment, git and github."
            },
            {
                'desc': "Junior data scientist. Required: python, scikit-learn, pandas, "
                        "sql databases. Knowledge of machine learning, statistics. Jupyter notebooks."
            },
            {
                'desc': "DevOps engineer. Must have: kubernetes, docker, ci/cd pipelines, "
                        "aws or azure cloud, python scripting, git, monitoring and logging."
            },
            {
                'desc': "Full stack developer. Skills: javascript, react frontend, "
                        "node.js or python backend, postgresql or mongodb, docker, git."
            },
        ]

        jobs = []
        for i in range(count):
            skill_set = random.choice(skill_sets)
            level = random.choice(levels)
            title = random.choice(titles)
            salary_lo = random.randint(80, 250)
            salary_hi = salary_lo + random.randint(50, 150)
            has_salary = random.random() > 0.25

            jobs.append({
                'title': f"{level} {title}",
                'company': random.choice(companies),
                'salary': f"{salary_lo} - {salary_hi} K RUB" if has_salary else "Not specified",
                'salary_min': (salary_lo + salary_hi) / 2 if has_salary else None,
                'currency': 'RUB' if has_salary else None,
                'location': random.choice(locations),
                'url': f"https://example.com/job/{i}",
                'source': 'Mock',
                'description': skill_set['desc'],
                'experience_years': random.randint(0, 10),
                'employment_type': random.choice(['Full-time', 'Contract', 'Part-time']),
                'scraped_date': datetime.now().isoformat()
            })

        return jobs

    def save_to_csv(self, jobs: List[Dict], filename: str = 'jobs_raw.csv'):
        df = pd.DataFrame(jobs)
        os.makedirs('../data', exist_ok=True)
        filepath = os.path.join('../data', filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Saved {len(jobs)} jobs to {filepath}")
        return filepath

    def save_to_json(self, jobs: List[Dict], filename: str = 'jobs_raw.json'):
        os.makedirs('../data', exist_ok=True)
        filepath = os.path.join('../data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(jobs)} jobs to {filepath}")
        return filepath


def main():
    scraper = JobScraper()

    search_terms = [
        "Data Science", "Machine Learning", "Python developer",
        "Data Engineer", "DevOps", "Backend developer",
        "Frontend developer", "Data Analyst", "Software Engineer"
    ]

    all_jobs = []
    for term in search_terms:
        jobs = scraper.scrape_hh_api(term, max_pages=20)
        all_jobs.extend(jobs)
        time.sleep(1)

    # Deduplicate by URL
    seen_urls = set()
    unique_jobs = []
    for job in all_jobs:
        if job['url'] not in seen_urls:
            seen_urls.add(job['url'])
            unique_jobs.append(job)
    all_jobs = unique_jobs
    print(f"\nUnique jobs from HH.ru API: {len(all_jobs)}")

    # Supplement with mock if needed
    if len(all_jobs) < 2000:
        needed = 2000 - len(all_jobs)
        print(f"Supplementing with {needed} mock jobs...")
        all_jobs.extend(scraper.scrape_mock_data(needed))

    scraper.save_to_csv(all_jobs, 'jobs_raw.csv')
    scraper.save_to_json(all_jobs, 'jobs_raw.json')
    print(f"\nTotal jobs collected: {len(all_jobs)}")


if __name__ == "__main__":
    main()
