# Job Market Dashboard 📊

Interactive dashboard for analyzing 5000+ Data Science and IT job postings with real-time filtering and analytics.

## Quick Start

### 1. Install Dependencies
```bash
cd scraper
pip install -r requirements.txt
cd ..
```

### 2. Generate Data
```bash
cd scraper
python scraper.py          # Collects 5000+ job postings
python preprocessor.py     # Cleans to 4,626 records
cd ..
```

### 3. Prepare Dashboard Data
```bash
python convert_to_json.py
```

### 4. Run Dashboard
```bash
cd web
python -m http.server 8000
```
Visit: `http://localhost:8000/public/`

## Project Structure

```
├── scraper/
│   ├── scraper.py          # Job scraper
│   ├── preprocessor.py     # Data cleaning & enrichment
│   └── requirements.txt    # Dependencies
├── data/
│   ├── jobs_raw.csv        # Raw data
│   └── jobs_cleaned.csv    # Cleaned data
├── web/
│   ├── public/
│   │   ├── index.html      # Dashboard
│   │   └── data/           # JSON data
│   └── src/
│       ├── app.js          # App logic
│       ├── charts.js       # Visualizations
│       ├── data-loader.js  # Data handling
│       └── styles.css      # Styling
├── convert_to_json.py      # CSV → JSON converter
└── README.md
```

## Features

✨ **6 Interactive Charts** - Job titles, companies, locations, skills, salary, employment types  
🔍 **Real-time Filters** - Search, location, company, skills  
📊 **Statistics Panel** - Jobs, companies, locations, avg salary  
📋 **Job Table** - Paginated browsing with full details  
📱 **Responsive Design** - Works on desktop and mobile

## Deploy to GitHub Pages

```bash
# Initialize git
git init
git add .
git commit -m "Job Market Dashboard"
git remote add origin https://github.com/YOUR-USERNAME/job-market-dashboard.git
git push -u origin main
```

Then go to Settings → Pages → Deploy from main branch → /web/public folder

## Dataset

- **4,626** cleaned job records
- **23** companies
- **15** locations  
- **40+** skills identified
- **287K RUB** average salary

## Requirements

- Python 3.8+
- pandas, beautifulsoup4, requests
- Modern browser
- Git (for GitHub deployment)

## License

MIT License

