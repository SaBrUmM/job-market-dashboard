/**
 * Main Application Logic
 * Handles UI interactions and data binding
 */

let currentPage = 1;
const pageSize = 20;
let currentFilters = {};

// Initialize the dashboard
async function initializeDashboard() {
    try {
        // Show loading state
        showLoadingState();

        // Load data
        await dataLoader.loadData();

        // Initialize UI
        initializeCharts();
        populateFilterOptions();
        updateStatistics();
        renderJobsTable();

        // Hide loading state
        hideLoadingState();

        // Attach event listeners
        attachEventListeners();

    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showErrorState('Failed to load dashboard data');
    }
}

function populateFilterOptions() {
    const options = dataLoader.getFilterOptions();

    // Populate locations
    const locationSelect = document.getElementById('location-filter');
    options.locations.forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.textContent = location;
        locationSelect.appendChild(option);
    });

    // Populate companies
    const companySelect = document.getElementById('company-filter');
    options.companies.slice(0, 30).forEach(company => {
        const option = document.createElement('option');
        option.value = company;
        option.textContent = company;
        companySelect.appendChild(option);
    });

    // Populate skills
    const skillsSelect = document.getElementById('skills-filter');
    options.skills.forEach(skill => {
        const option = document.createElement('option');
        option.value = skill;
        option.textContent = skill;
        skillsSelect.appendChild(option);
    });
}

function updateStatistics() {
    const stats = dataLoader.getStatistics();

    document.getElementById('total-jobs').textContent = stats.totalJobs.toLocaleString();
    document.getElementById('total-companies').textContent = stats.uniqueCompanies;
    document.getElementById('total-locations').textContent = stats.uniqueLocations;
    document.getElementById('avg-salary').textContent = `$${Math.round(stats.avgSalary).toLocaleString()}K`;
    document.getElementById('avg-experience').textContent = `${Math.round(stats.avgExperience)} years`;
}

function applyFilters() {
    currentFilters = {
        search: document.getElementById('search-filter').value,
        location: document.getElementById('location-filter').value,
        company: document.getElementById('company-filter').value,
        skills: document.getElementById('skills-filter').value
    };

    // Remove empty filter values
    Object.keys(currentFilters).forEach(key => {
        if (!currentFilters[key]) {
            delete currentFilters[key];
        }
    });

    dataLoader.filterData(currentFilters);

    // Reset to first page
    currentPage = 1;

    // Update UI
    updateStatistics();
    destroyAllCharts();
    initializeCharts();
    renderJobsTable();
}

function resetFilters() {
    document.getElementById('search-filter').value = '';
    document.getElementById('location-filter').value = '';
    document.getElementById('company-filter').value = '';
    document.getElementById('skills-filter').value = '';

    currentFilters = {};
    dataLoader.filterData({});

    currentPage = 1;

    updateStatistics();
    destroyAllCharts();
    initializeCharts();
    renderJobsTable();
}

function renderJobsTable() {
    const pagination = dataLoader.paginateData(currentPage, pageSize);
    const tbody = document.getElementById('jobs-table-body');
    tbody.innerHTML = '';

    pagination.data.forEach(job => {
        const row = document.createElement('tr');
        row.className = 'fade-in';

        const skillsHtml = job.skills
            ? job.skills.map(skill => `<span class="skills-badge">${skill}</span>`).join('')
            : '<span class="text-light">N/A</span>';

        row.innerHTML = `
            <td><strong>${job.title}</strong></td>
            <td>${job.company}</td>
            <td>${job.location_clean}</td>
            <td>${job.salary || 'Not specified'}</td>
            <td>${job.employment_type || 'N/A'}</td>
            <td>${skillsHtml}</td>
        `;

        tbody.appendChild(row);
    });

    // Update pagination info
    document.getElementById('showing-start').textContent = pagination.startIndex;
    document.getElementById('showing-end').textContent = pagination.endIndex;
    document.getElementById('showing-total').textContent = pagination.totalItems;
    document.getElementById('page-info').textContent = `Page ${pagination.currentPage} of ${pagination.totalPages}`;

    // Update button states
    document.getElementById('prev-page').disabled = pagination.currentPage === 1;
    document.getElementById('next-page').disabled = pagination.currentPage === pagination.totalPages;
}

function attachEventListeners() {
    // Filter inputs
    document.getElementById('search-filter').addEventListener('input', () => {
        currentPage = 1;
        applyFilters();
    });

    document.getElementById('location-filter').addEventListener('change', () => {
        currentPage = 1;
        applyFilters();
    });

    document.getElementById('company-filter').addEventListener('change', () => {
        currentPage = 1;
        applyFilters();
    });

    document.getElementById('skills-filter').addEventListener('change', () => {
        currentPage = 1;
        applyFilters();
    });

    // Reset filters button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);

    // Pagination
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderJobsTable();
            window.scrollTo(0, 0);
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        const pagination = dataLoader.paginateData(currentPage + 1, pageSize);
        if (currentPage < pagination.totalPages) {
            currentPage++;
            renderJobsTable();
            window.scrollTo(0, 0);
        }
    });
}

function showLoadingState() {
    const container = document.querySelector('.container');
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.id = 'loading-state';
    loading.innerHTML = '<div class="spinner"></div><p>Loading job data...</p>';
    container.appendChild(loading);
}

function hideLoadingState() {
    const loading = document.getElementById('loading-state');
    if (loading) {
        loading.remove();
    }
}

function showErrorState(message) {
    const container = document.querySelector('.container');
    const error = document.createElement('div');
    error.className = 'loading';
    error.innerHTML = `<p style="color: red;">❌ ${message}</p>`;
    container.appendChild(error);
}

// Export data as CSV
function exportToCsv() {
    const data = dataLoader.filteredData;
    let csv = 'Title,Company,Location,Salary,Employment Type,Skills\n';

    data.forEach(job => {
        const skills = job.skills ? job.skills.join('; ') : '';
        const salary = job.salary || 'Not specified';
        csv += `"${job.title}","${job.company}","${job.location_clean}","${salary}","${job.employment_type}","${skills}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `jobs_export_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+F focus search
    if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        document.getElementById('search-filter').focus();
    }

    // Escape reset filters
    if (e.key === 'Escape') {
        resetFilters();
    }
});

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}
