/**
 * Data Loader Module
 * Handles loading and caching job data
 */

class DataLoader {
    constructor() {
        this.data = null;
        this.filteredData = null;
        this.dataUrl = '/data/jobs_cleaned.json'; // Change to your data source
        this.cache = new Map();
    }

    async loadData() {
        try {
            // Try to load from generated JSON file
            const response = await fetch('/data/jobs_cleaned.json');
            if (response.ok) {
                const jsonData = await response.json();
                // Ensure data is an array
                this.data = Array.isArray(jsonData) ? jsonData : [jsonData];
                this.filteredData = [...this.data];
                console.log(`✓ Loaded ${this.data.length} jobs from JSON`);
                return this.data;
            }
        } catch (error) {
            console.warn('Could not load from /data/jobs_cleaned.json:', error);
        }

        // Fallback to mock data if real data not available
        console.log('Generating mock data as fallback...');
        this.data = this.generateMockData(5000);
        this.filteredData = [...this.data];
        return this.data;
    }

    generateMockData(count = 5000) {
        const titles = [
            "Data Scientist", "Senior Data Scientist", "Junior Data Scientist",
            "Machine Learning Engineer", "ML Engineer", "Data Analyst",
            "Python Developer", "Backend Developer", "Full Stack Developer",
            "DevOps Engineer", "Cloud Engineer", "Software Engineer",
            "Data Engineer", "Analytics Engineer", "Business Analyst",
            "Systems Administrator", "Database Administrator", "QA Engineer"
        ];

        const companies = [
            "Yandex", "Mail.ru", "VKontakte", "Sberbank", "Gazprom", "Lukoil",
            "Rostelecom", "MegaFon", "Beeline", "Aviasales", "Booking.com",
            "Google", "Amazon", "Microsoft", "Apple", "Meta", "LinkedIn",
            "Airbnb", "Uber", "Spotify", "Netflix", "Stripe", "Notion"
        ];

        const locations = [
            "Moscow", "Saint Petersburg", "Ekaterinburg", "Novosibirsk", "Vladivostok",
            "New York", "San Francisco", "London", "Berlin", "Amsterdam",
            "Taipei", "Singapore", "Dubai", "Remote", "Hybrid"
        ];

        const levels = ["Junior", "Middle", "Senior", "Lead", "Principal"];

        const skills = [
            ["Python", "SQL", "Pandas"],
            ["Python", "TensorFlow", "Deep Learning"],
            ["SQL", "Tableau", "Excel"],
            ["Java", "Spring", "Microservices"],
            ["Go", "Kubernetes", "Docker"],
            ["JavaScript", "React", "Node.js"],
            ["Python", "Apache Spark", "Hadoop"],
            ["C++", "CUDA", "GPU Computing"],
            ["R", "Statistics", "Data Visualization"],
            ["AWS", "Lambda", "S3"],
            ["Kubernetes", "Docker", "CI/CD"],
            ["PostgreSQL", "MongoDB", "Redis"]
        ];

        const employmentTypes = ["Full-time", "Contract", "Part-time"];

        const jobs = [];
        for (let i = 0; i < count; i++) {
            const selectedSkills = skills[Math.floor(Math.random() * skills.length)];
            jobs.push({
                id: i,
                title: `${levels[Math.floor(Math.random() * levels.length)]} ${titles[Math.floor(Math.random() * titles.length)]}`,
                company: companies[Math.floor(Math.random() * companies.length)],
                salary: Math.random() > 0.3 ? `${Math.floor(Math.random() * 250) + 50} - ${Math.floor(Math.random() * 250) + 300} K RUB` : "Not specified",
                location: locations[Math.floor(Math.random() * locations.length)],
                location_clean: locations[Math.floor(Math.random() * locations.length)],
                region: Math.random() > 0.5 ? "Russia" : "International",
                url: `https://example.com/job/${i}`,
                source: ["HH.ru", "Indeed", "LinkedIn", "HeadHunter"][Math.floor(Math.random() * 4)],
                description: `We are looking for a professional. Required skills: ${selectedSkills.join(", ")}`,
                experience_years: Math.floor(Math.random() * 15),
                employment_type: employmentTypes[Math.floor(Math.random() * employmentTypes.length)],
                skills: selectedSkills,
                skills_count: selectedSkills.length,
                title_normalized: `${levels[Math.floor(Math.random() * levels.length)]} ${titles[Math.floor(Math.random() * titles.length)]}`,
                salary_min: Math.random() > 0.3 ? Math.floor(Math.random() * 250) + 50 : null,
                currency: "RUB"
            });
        }
        return jobs;
    }

    filterData(filters = {}) {
        let filtered = [...this.data];

        if (filters.search) {
            const searchTerm = filters.search.toLowerCase();
            filtered = filtered.filter(job =>
                job.title.toLowerCase().includes(searchTerm) ||
                job.company.toLowerCase().includes(searchTerm) ||
                job.description.toLowerCase().includes(searchTerm)
            );
        }

        if (filters.location) {
            filtered = filtered.filter(job => job.location_clean === filters.location);
        }

        if (filters.company) {
            filtered = filtered.filter(job => job.company === filters.company);
        }

        if (filters.skills) {
            filtered = filtered.filter(job => job.skills.includes(filters.skills));
        }

        this.filteredData = filtered;
        return filtered;
    }

    getStatistics() {
        const data = this.filteredData;

        const stats = {
            totalJobs: data.length,
            uniqueCompanies: new Set(data.map(j => j.company)).size,
            uniqueLocations: new Set(data.map(j => j.location_clean)).size,
            avgSalary: data
                .filter(j => j.salary_min)
                .reduce((sum, j) => sum + (j.salary_min || 0), 0) / data.filter(j => j.salary_min).length || 0,
            avgExperience: data.reduce((sum, j) => sum + (j.experience_years || 0), 0) / data.length || 0
        };

        return stats;
    }

    getTopItems(field, limit = 10) {
        const counts = {};
        this.filteredData.forEach(job => {
            const value = job[field];
            counts[value] = (counts[value] || 0) + 1;
        });

        return Object.entries(counts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {});
    }

    getTopSkills(limit = 10) {
        const skillCounts = {};
        this.filteredData.forEach(job => {
            if (job.skills && Array.isArray(job.skills)) {
                job.skills.forEach(skill => {
                    skillCounts[skill] = (skillCounts[skill] || 0) + 1;
                });
            }
        });

        return Object.entries(skillCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {});
    }

    getSalaryDistribution() {
        const distribution = {};
        const salaries = this.filteredData
            .filter(j => j.salary_min)
            .map(j => j.salary_min);

        if (salaries.length === 0) return distribution;

        const maxSalary = Math.max(...salaries);
        const binSize = 50; // 50K bins

        for (let i = 0; i <= Math.ceil(maxSalary / binSize); i++) {
            const binStart = i * binSize;
            const binEnd = (i + 1) * binSize;
            const label = `${binStart}-${binEnd}K`;
            distribution[label] = salaries.filter(s => s >= binStart && s < binEnd).length;
        }

        return distribution;
    }

    getEmploymentTypeDistribution() {
        const distribution = {};
        this.filteredData.forEach(job => {
            const type = job.employment_type || 'Unknown';
            distribution[type] = (distribution[type] || 0) + 1;
        });
        return distribution;
    }

    getFilterOptions() {
        return {
            locations: [...new Set(this.data.map(j => j.location_clean))].sort(),
            companies: [...new Set(this.data.map(j => j.company))].sort(),
            skills: this.getUniqueSkills()
        };
    }

    getUniqueSkills() {
        const skills = new Set();
        this.data.forEach(job => {
            if (job.skills && Array.isArray(job.skills)) {
                job.skills.forEach(skill => skills.add(skill));
            }
        });
        return [...skills].sort();
    }

    paginateData(page = 1, pageSize = 20) {
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        const totalPages = Math.ceil(this.filteredData.length / pageSize);

        return {
            data: this.filteredData.slice(start, end),
            currentPage: page,
            totalPages: totalPages,
            totalItems: this.filteredData.length,
            pageSize: pageSize,
            startIndex: start + 1,
            endIndex: Math.min(end, this.filteredData.length)
        };
    }
}

// Global data loader instance
const dataLoader = new DataLoader();
