/**
 * Dashboard Charts – fetches data from the dashboard_data API endpoint
 * and renders Chart.js charts.
 */
document.addEventListener('DOMContentLoaded', function () {
    const dataUrl = document.querySelector('[data-dashboard-url]');
    // Build URL from known path
    const url = '/dashboard/data/';

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            renderCategoryChart(data.stock_by_category);
            renderMonthlyChart(data.monthly_transactions);
        })
        .catch(err => {
            console.error('Failed to load dashboard data:', err);
        });

    function renderCategoryChart(chartData) {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;

        const colors = [
            '#0d6efd', '#198754', '#ffc107', '#dc3545', '#0dcaf0',
            '#6f42c1', '#fd7e14', '#20c997', '#d63384', '#6c757d'
        ];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Total Stock',
                    data: chartData.data,
                    backgroundColor: colors.slice(0, chartData.labels.length),
                    borderRadius: 6,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    function renderMonthlyChart(chartData) {
        const ctx = document.getElementById('monthlyChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Transactions',
                    data: chartData.data,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#0d6efd',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }
});
