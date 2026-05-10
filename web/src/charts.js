/**
 * Charts Module
 * Creates and manages all chart visualizations
 */

let charts = {};

function initializeCharts() {
    // Chart.js color palette
    const colors = [
        'rgba(102, 126, 234, 1)',
        'rgba(240, 147, 251, 1)',
        'rgba(72, 219, 251, 1)',
        'rgba(224, 112, 112, 1)',
        'rgba(126, 214, 126, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255, 193, 7, 1)',
        'rgba(156, 39, 176, 1)',
        'rgba(0, 188, 212, 1)',
        'rgba(255, 87, 34, 1)'
    ];

    const bgColors = colors.map(c => c.replace('1)', '0.7)'));

    // Top Titles Chart
    const titlesCtx = document.getElementById('titles-chart');
    if (titlesCtx) {
        const topTitles = dataLoader.getTopItems('title_normalized', 10);
        charts.titles = new Chart(titlesCtx, {
            type: 'barChart',
            data: {
                labels: Object.keys(topTitles),
                datasets: [{
                    label: 'Number of Jobs',
                    data: Object.values(topTitles),
                    backgroundColor: bgColors,
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Top Companies Chart
    const companiesCtx = document.getElementById('companies-chart');
    if (companiesCtx) {
        const topCompanies = dataLoader.getTopItems('company', 10);
        charts.companies = new Chart(companiesCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(topCompanies),
                datasets: [{
                    data: Object.values(topCompanies),
                    backgroundColor: bgColors,
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Location Distribution Chart
    const locationCtx = document.getElementById('location-chart');
    if (locationCtx) {
        const locations = dataLoader.getTopItems('location_clean', 15);
        charts.location = new Chart(locationCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(locations),
                datasets: [{
                    label: 'Number of Jobs',
                    data: Object.values(locations),
                    backgroundColor: bgColors,
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Top Skills Chart
    const skillsCtx = document.getElementById('skills-chart');
    if (skillsCtx) {
        const topSkills = dataLoader.getTopSkills(15);
        charts.skills = new Chart(skillsCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(topSkills),
                datasets: [{
                    label: 'Mentions',
                    data: Object.values(topSkills),
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Salary Distribution Chart
    const salaryCtx = document.getElementById('salary-chart');
    if (salaryCtx) {
        const salaryDist = dataLoader.getSalaryDistribution();
        charts.salary = new Chart(salaryCtx, {
            type: 'line',
            data: {
                labels: Object.keys(salaryDist),
                datasets: [{
                    label: 'Number of Jobs',
                    data: Object.values(salaryDist),
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Employment Type Distribution
    const employmentCtx = document.getElementById('employment-chart');
    if (employmentCtx) {
        const employmentDist = dataLoader.getEmploymentTypeDistribution();
        charts.employment = new Chart(employmentCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(employmentDist),
                datasets: [{
                    data: Object.values(employmentDist),
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(240, 147, 251, 0.8)',
                        'rgba(72, 219, 251, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(240, 147, 251, 1)',
                        'rgba(72, 219, 251, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

function updateCharts() {
    // Update all charts with filtered data
    const colors = [
        'rgba(102, 126, 234, 1)',
        'rgba(240, 147, 251, 1)',
        'rgba(72, 219, 251, 1)',
        'rgba(224, 112, 112, 1)',
        'rgba(126, 214, 126, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255, 193, 7, 1)',
        'rgba(156, 39, 176, 1)',
        'rgba(0, 188, 212, 1)',
        'rgba(255, 87, 34, 1)'
    ];

    const bgColors = colors.map(c => c.replace('1)', '0.7)'));

    // Update Titles
    if (charts.titles) {
        const topTitles = dataLoader.getTopItems('title_normalized', 10);
        charts.titles.data.labels = Object.keys(topTitles);
        charts.titles.data.datasets[0].data = Object.values(topTitles);
        charts.titles.update();
    }

    // Update Companies
    if (charts.companies) {
        const topCompanies = dataLoader.getTopItems('company', 10);
        charts.companies.data.labels = Object.keys(topCompanies);
        charts.companies.data.datasets[0].data = Object.values(topCompanies);
        charts.companies.update();
    }

    // Update Location
    if (charts.location) {
        const locations = dataLoader.getTopItems('location_clean', 15);
        charts.location.data.labels = Object.keys(locations);
        charts.location.data.datasets[0].data = Object.values(locations);
        charts.location.update();
    }

    // Update Skills
    if (charts.skills) {
        const topSkills = dataLoader.getTopSkills(15);
        charts.skills.data.labels = Object.keys(topSkills);
        charts.skills.data.datasets[0].data = Object.values(topSkills);
        charts.skills.update();
    }

    // Update Salary
    if (charts.salary) {
        const salaryDist = dataLoader.getSalaryDistribution();
        charts.salary.data.labels = Object.keys(salaryDist);
        charts.salary.data.datasets[0].data = Object.values(salaryDist);
        charts.salary.update();
    }

    // Update Employment
    if (charts.employment) {
        const employmentDist = dataLoader.getEmploymentTypeDistribution();
        charts.employment.data.labels = Object.keys(employmentDist);
        charts.employment.data.datasets[0].data = Object.values(employmentDist);
        charts.employment.update();
    }
}

function destroyAllCharts() {
    Object.keys(charts).forEach(key => {
        if (charts[key]) {
            charts[key].destroy();
        }
    });
    charts = {};
}
