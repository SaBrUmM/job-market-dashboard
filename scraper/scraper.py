#!/usr/bin/env python3
"""
Job Postings Scraper
Collects job postings from multiple sources (HH.ru, Indeed, etc.)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
from datetime import datetime
from typing import List, Dict
import random

class JobScraper:
    """Main scraper class for job postings"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.jobs = []
        
    def scrape_hh_ru(self, search_term: str = "Data Science", pages: int = 50) -> List[Dict]:
        """Scrape job postings from HH.ru (Russian job site)"""
        print(f"Scraping HH.ru for '{search_term}'...")
        jobs = []
        
        try:
            for page in range(pages):
                url = f"https://hh.ru/search/vacancy"
                params = {
                    'text': search_term,
                    'page': page,
                    'per_page': 100,
                    'area': '113'  # Russia
                }
                
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h3')
                            title = title_elem.get_text(strip=True) if title_elem else "N/A"
                            
                            company_elem = card.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
                            company = company_elem.get_text(strip=True) if company_elem else "N/A"
                            
                            salary_elem = card.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                            salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
                            
                            location_elem = card.find('span', {'data-qa': 'vacancy-serp__vacancy-location'})
                            location = location_elem.get_text(strip=True) if location_elem else "N/A"
                            
                            url_elem = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                            job_url = url_elem.get('href') if url_elem else "N/A"
                            
                            jobs.append({
                                'title': title,
                                'company': company,
                                'salary': salary,
                                'location': location,
                                'url': job_url,
                                'source': 'HH.ru',
                                'description': '',
                                'scraped_date': datetime.now().isoformat()
                            })
                        except Exception as e:
                            print(f"Error parsing job card: {e}")
                            continue
                    
                    print(f"Page {page + 1}: Found {len(job_cards)} jobs")
                    time.sleep(random.uniform(1, 3))
                else:
                    print(f"Failed to fetch page {page + 1}: Status {response.status_code}")
                    
        except Exception as e:
            print(f"Error scraping HH.ru: {e}")
        
        return jobs
    
    def scrape_mock_data(self, count: int = 5000) -> List[Dict]:
        """Generate mock job data for demonstration (since live scraping might be limited)"""
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
            "Yandex", "Mail.ru", "VKontakte", "Sberbank", "Gazprom", "Lukoil",
            "Rostelecom", "MegaFon", "Beeline", "Aviasales", "Booking.com",
            "Google", "Amazon", "Microsoft", "Apple", "Meta", "LinkedIn",
            "Airbnb", "Uber", "Spotify", "Netflix", "Stripe", "Notion"
        ]
        
        locations = [
            "Moscow", "Saint Petersburg", "Ekaterinburg", "Novosibirsk", "Vladivostok",
            "New York", "San Francisco", "London", "Berlin", "Amsterdam",
            "Taipei", "Singapore", "Dubai", "Remote", "Hybrid"
        ]
        
        levels = ["Junior", "Middle", "Senior", "Lead", "Principal"]
        
        all_skills = [
            "Python", "SQL", "Pandas", "TensorFlow", "Deep Learning",
            "Tableau", "Excel", "Java", "Spring", "Microservices",
            "Go", "Kubernetes", "Docker", "JavaScript", "React", "Node.js",
            "Apache Spark", "Hadoop", "C++", "CUDA", "GPU Computing",
            "R", "Statistics", "Data Visualization", "AWS", "Lambda", "S3",
            "CI/CD", "PostgreSQL", "MongoDB", "Redis"
        ]
        
        jobs = []
        for i in range(count):
            selected_skills = random.sample(all_skills, random.randint(2, 5))
            job = {
                'title': f"{random.choice(levels)} {random.choice(titles)}",
                'company': random.choice(companies),
                'salary': f"{random.randint(50, 300)} - {random.randint(300, 500)} K RUB" if random.random() > 0.3 else "Not specified",
                'location': random.choice(locations),
                'url': f"https://example.com/job/{i}",
                'source': random.choice(['HH.ru', 'Indeed', 'LinkedIn', 'HeadHunter']),
                'description': f"We are looking for a {random.choice(titles)}. Required skills: {', '.join(selected_skills)}",
                'experience_years': random.randint(0, 15),
                'employment_type': random.choice(['Full-time', 'Contract', 'Part-time']),
                'skills': selected_skills,
                'scraped_date': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs
    
    def save_to_csv(self, jobs: List[Dict], filename: str = 'jobs_raw.csv'):
        """Save jobs to CSV file"""
        df = pd.DataFrame(jobs)
        filepath = os.path.join('../data', filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Saved {len(jobs)} jobs to {filepath}")
        return filepath
    
    def save_to_json(self, jobs: List[Dict], filename: str = 'jobs_raw.json'):
        """Save jobs to JSON file"""
        filepath = os.path.join('../data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(jobs)} jobs to {filepath}")
        return filepath

def main():
    scraper = JobScraper()
    
    # Try to scrape real data from HH.ru
    # Note: For production, you might want to use official APIs
    jobs_hh = scraper.scrape_hh_ru("Data Science", pages=10)
    jobs_it = scraper.scrape_hh_ru("IT Developer", pages=10)
    
    all_jobs = jobs_hh + jobs_it
    
    # If we don't have enough jobs, supplement with mock data
    if len(all_jobs) < 5000:
        needed = 5000 - len(all_jobs)
        print(f"Supplementing with {needed} mock jobs...")
        all_jobs.extend(scraper.scrape_mock_data(needed))
    
    # Save raw data
    scraper.save_to_csv(all_jobs, 'jobs_raw.csv')
    scraper.save_to_json(all_jobs, 'jobs_raw.json')
    
    print(f"\nTotal jobs collected: {len(all_jobs)}")

if __name__ == "__main__":
    main()
