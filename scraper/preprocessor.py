#!/usr/bin/env python3
"""
Data Preprocessing and Cleaning Module
Cleans and preprocesses job posting data
"""

import pandas as pd
import numpy as np
import re
import json
import os
from typing import Dict, List, Tuple

class DataPreprocessor:
    """Data cleaning and preprocessing for job postings"""
    
    def __init__(self):
        self.df = None
        self.stats = {}
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load raw job data"""
        if filepath.endswith('.csv'):
            self.df = pd.read_csv(filepath, encoding='utf-8')
        elif filepath.endswith('.json'):
            self.df = pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format")
        
        print(f"Loaded {len(self.df)} records")
        return self.df
    
    def clean_salary(self, salary_str: str) -> Tuple[float, str]:
        """Extract salary value and currency from salary string"""
        if pd.isna(salary_str) or salary_str == "Not specified":
            return None, None
        
        salary_str = str(salary_str)
        
        # Try to find currency
        currency = None
        if 'RUB' in salary_str or 'руб' in salary_str.lower():
            currency = 'RUB'
        elif 'USD' in salary_str or '$' in salary_str:
            currency = 'USD'
        elif 'EUR' in salary_str or '€' in salary_str:
            currency = 'EUR'
        
        # Extract numbers
        numbers = re.findall(r'\d+', salary_str)
        
        if len(numbers) >= 1:
            # Take average if range is given
            salary = float(numbers[0])
            if len(numbers) > 1:
                salary = (float(numbers[0]) + float(numbers[1])) / 2
            return salary, currency
        
        return None, None
    
    def extract_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        if pd.isna(text):
            return 0
        
        text = str(text).lower()
        pattern = r'(\d+)\s*(?:года|лет|years?)'
        matches = re.findall(pattern, text)
        
        if matches:
            return int(matches[0])
        return 0
    
    def extract_skills(self, description: str) -> List[str]:
        """Extract technical skills from description"""
        skills_dict = {
            'Python': ['python', 'py'],
            'JavaScript': ['javascript', 'js', 'node'],
            'Java': ['java'],
            'C++': ['c++', 'cpp'],
            'SQL': ['sql', 'database'],
            'R': ['r programming', 'rlang', 'rstudio', 'r language'],
            'Go': ['golang', 'go programming', 'go language'],
            'Rust': ['rust'],
            'TypeScript': ['typescript', 'ts'],
            'React': ['react', 'reactjs'],
            'Vue': ['vue', 'vuejs'],
            'Angular': ['angular'],
            'Django': ['django'],
            'Flask': ['flask'],
            'FastAPI': ['fastapi'],
            'Spring': ['spring', 'springboot'],
            'TensorFlow': ['tensorflow'],
            'PyTorch': ['pytorch'],
            'Scikit-learn': ['scikit-learn', 'sklearn'],
            'Pandas': ['pandas'],
            'Spark': ['spark', 'apache spark'],
            'Hadoop': ['hadoop'],
            'Docker': ['docker'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'AWS': ['aws', 'amazon'],
            'Azure': ['azure'],
            'GCP': ['gcp', 'google cloud'],
            'MongoDB': ['mongodb'],
            'PostgreSQL': ['postgresql', 'postgres'],
            'MySQL': ['mysql'],
            'Redis': ['redis'],
            'Git': ['git', 'github', 'gitlab'],
            'Machine Learning': ['machine learning', 'ml'],
            'Deep Learning': ['deep learning'],
            'NLP': ['nlp', 'natural language'],
            'Computer Vision': ['computer vision', 'cv'],
            'Statistics': ['statistics', 'statistical']
        }
        
        found_skills = []
        text = str(description).lower()
        
        for skill, patterns in skills_dict.items():
            for pattern in patterns:
                if re.search(re.escape(pattern), text):
                    found_skills.append(skill)
                    break
        
        return found_skills
    
    def clean_location(self, location: str) -> Tuple[str, str]:
        """Clean and categorize location"""
        if pd.isna(location):
            return None, 'Other'
        
        location = str(location).strip()
        
        # Categorize location type
        if 'remote' in location.lower():
            return 'Remote', 'Remote'
        elif 'hybrid' in location.lower():
            return 'Hybrid', 'Hybrid'
        
        # Categorize by region
        if any(city in location for city in ['Moscow', 'Москва', 'МСК']):
            return 'Moscow', 'Russia'
        elif any(city in location for city in ['Saint Petersburg', 'Санкт-Петербург', 'СПб']):
            return 'Saint Petersburg', 'Russia'
        elif any(country in location for country in ['Russia', 'Россия']):
            return location, 'Russia'
        else:
            return location, 'International'
    
    def preprocess(self) -> pd.DataFrame:
        """Apply all preprocessing steps"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        print("Starting preprocessing...")
        
        # Remove duplicates
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=['title', 'company', 'location'], keep='first')
        print(f"Removed {initial_count - len(self.df)} duplicates")
        
        # Clean salary
        print("Cleaning salary...")
        self.df[['salary_min', 'currency']] = self.df['salary'].apply(
            lambda x: pd.Series(self.clean_salary(x))
        )
        
        # Extract experience
        print("Extracting experience...")
        if 'description' in self.df.columns:
            self.df['experience_years'] = self.df['description'].apply(self.extract_experience)
        elif 'experience_years' not in self.df.columns:
            self.df['experience_years'] = 0
        
        # Extract skills
        print("Extracting skills...")
        description_col = 'description' if 'description' in self.df.columns else 'title'
        self.df['skills'] = self.df[description_col].apply(self.extract_skills)
        self.df['skills_count'] = self.df['skills'].apply(len)
        
        # Clean location
        print("Cleaning location...")
        self.df[['location_clean', 'region']] = self.df['location'].apply(
            lambda x: pd.Series(self.clean_location(x))
        )
        
        # Standardize title
        print("Standardizing job titles...")
        self.df['title_normalized'] = self.df['title'].apply(self._normalize_title)
        
        # Remove rows with missing critical fields
        self.df = self.df.dropna(subset=['title', 'company', 'location'])
        
        print(f"Final dataset size: {len(self.df)}")
        self.stats = {
            'total_records': len(self.df),
            'companies': self.df['company'].nunique(),
            'locations': self.df['location'].nunique(),
            'avg_salary': self.df['salary_min'].mean(),
            'avg_experience': self.df['experience_years'].mean()
        }
        
        return self.df
    
    def _normalize_title(self, title: str) -> str:
        """Normalize job titles"""
        title = str(title).lower().strip()
        
        # Common replacements
        replacements = {
            r'senior\s+': 'Senior ',
            r'junior\s+': 'Junior ',
            r'lead\s+': 'Lead ',
            r'principal\s+': 'Principal ',
            r'devops': 'DevOps',
            r'fullstack|full-stack|full stack': 'Full Stack',
            r'frontend|front-end': 'Frontend',
            r'backend|back-end': 'Backend',
        }
        
        for pattern, replacement in replacements.items():
            title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
        
        return title.title()
    
    def save_cleaned_data(self, output_path: str = '../data/jobs_cleaned.csv'):
        """Save cleaned data"""
        if self.df is None:
            raise ValueError("No data to save")
        
        self.df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved cleaned data to {output_path}")
        
        # Save stats
        stats_path = output_path.replace('.csv', '_stats.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)
        print(f"Saved statistics to {stats_path}")
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of cleaned data"""
        if self.df is None:
            return {}
        
        return {
            'total_records': len(self.df),
            'unique_companies': self.df['company'].nunique(),
            'unique_locations': self.df['location'].nunique(),
            'unique_titles': self.df['title'].nunique(),
            'avg_salary': float(self.df['salary_min'].mean()) if self.df['salary_min'].notna().any() else 0,
            'max_salary': float(self.df['salary_min'].max()) if self.df['salary_min'].notna().any() else 0,
            'min_salary': float(self.df['salary_min'].min()) if self.df['salary_min'].notna().any() else 0,
            'avg_experience': float(self.df['experience_years'].mean()),
            'top_locations': self.df['location_clean'].value_counts().head(10).to_dict(),
            'top_companies': self.df['company'].value_counts().head(10).to_dict(),
            'top_titles': self.df['title_normalized'].value_counts().head(10).to_dict(),
            'top_skills': self._get_top_skills(10)
        }
    
    def _get_top_skills(self, n: int = 10) -> Dict:
        """Get top skills"""
        skill_counts = {}
        for skills in self.df['skills']:
            for skill in skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        return dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:n])

def main():
    preprocessor = DataPreprocessor()
    
    # Load raw data
    raw_data_path = '../data/jobs_raw.csv'
    if os.path.exists(raw_data_path):
        preprocessor.load_data(raw_data_path)
        preprocessor.preprocess()
        preprocessor.save_cleaned_data()
        
        # Print summary
        stats = preprocessor.get_summary_stats()
        print("\n=== Summary Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")
    else:
        print(f"Raw data not found at {raw_data_path}")

if __name__ == "__main__":
    main()
