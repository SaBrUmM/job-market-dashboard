#!/usr/bin/env python3
"""
Convert cleaned CSV data to JSON for dashboard
Used by GitHub Actions workflow
"""

import pandas as pd
import json
import os

def convert_csv_to_json():
    """Convert cleaned CSV to JSON format"""
    csv_path = 'data/jobs_cleaned.csv'
    json_path = 'web/public/data/jobs_cleaned.json'
    
    # Create output directory
    os.makedirs('web/public/data', exist_ok=True)
    
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Convert skills column if needed
    if 'skills' in df.columns:
        try:
            df['skills'] = df['skills'].apply(
                lambda x: json.loads(x) if isinstance(x, str) and x.startswith('[') else []
            )
        except Exception as e:
            print(f"Warning: Could not parse skills: {e}")
            df['skills'] = df['skills'].apply(lambda x: [])
    
    # Save to JSON
    df.to_json(json_path, orient='records', force_ascii=False)
    print(f'✓ Converted {len(df)} records to JSON')
    print(f'✓ Output: {json_path}')

if __name__ == "__main__":
    convert_csv_to_json()
