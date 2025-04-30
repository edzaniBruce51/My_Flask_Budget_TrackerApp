document.addEventListener('DOMContentLoaded', function() {
    // Category Chart
    const categoryChart = document.getElementById('expenseCategoryChart');
    if (categoryChart) {
        const categories = JSON.parse(categoryChart.dataset.categories);
        const amounts = JSON.parse(categoryChart.dataset.amounts);
        
        new Chart(categoryChart, {
            type: 'pie',
            data: {
                labels: categories,
                datasets: [{
                    data: amounts,
                    backgroundColor: [
                        '#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981',
                        '#3B82F6', '#6366F1', '#8B5CF6', '#D946EF', '#F97316'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Budget Progress Chart
    const budgetChart = document.getElementById('budgetProgressChart');
    if (budgetChart) {
        const budgetNames = JSON.parse(budgetChart.dataset.budgetNames);
        const budgetAmounts = JSON.parse(budgetChart.dataset.budgetAmounts);
        const spentAmounts = JSON.parse(budgetChart.dataset.spentAmounts);

        new Chart(budgetChart, {
            type: 'bar',
            data: {
                labels: budgetNames,
                datasets: [{
                    label: 'Budget Amount',
                    data: budgetAmounts,
                    backgroundColor: '#4F46E5'
                }, {
                    label: 'Spent Amount',
                    data: spentAmounts,
                    backgroundColor: '#F59E0B'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Expense Trend Chart
    const trendChart = document.getElementById('expenseTrendChart');
    if (trendChart) {
        const dates = JSON.parse(trendChart.dataset.dates);
        const amounts = JSON.parse(trendChart.dataset.amounts);

        new Chart(trendChart, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Daily Expenses',
                    data: amounts,
                    borderColor: '#4F46E5',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
