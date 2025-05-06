document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard charts initializing...');

    // Category Chart
    const categoryChart = document.getElementById('expenseCategoryChart');
    if (categoryChart) {
        console.log('Category chart element found');

        try {
            // Access data attributes directly
            const categoriesStr = categoryChart.getAttribute('data-categories');
            const amountsStr = categoryChart.getAttribute('data-amounts');

            console.log('Raw data attributes:', {
                categories: categoriesStr,
                amounts: amountsStr
            });

            // Parse JSON
            const categories = JSON.parse(categoriesStr || '[]');
            const amounts = JSON.parse(amountsStr || '[]');

            console.log('Parsed data:', {
                categories: categories,
                amounts: amounts
            });

            if (categories.length > 0 && amounts.length > 0) {
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
                console.log('Category chart created successfully');
            } else {
                console.warn('No data for category chart');
                categoryChart.innerHTML = '<div style="text-align:center;padding:50px;">No data available</div>';
            }
        } catch (error) {
            console.error('Error creating category chart:', error);
            categoryChart.innerHTML = '<div style="text-align:center;padding:50px;">Error: ' + error.message + '</div>';
        }
    } else {
        console.error('Category chart element not found');
    }

    // Budget Progress Chart
    const budgetChart = document.getElementById('budgetProgressChart');
    if (budgetChart) {
        console.log('Budget chart element found');

        try {
            // Access data attributes directly
            const budgetNamesStr = budgetChart.getAttribute('data-budget-names');
            const budgetAmountsStr = budgetChart.getAttribute('data-budget-amounts');
            const spentAmountsStr = budgetChart.getAttribute('data-spent-amounts');

            console.log('Raw budget data attributes:', {
                budgetNames: budgetNamesStr,
                budgetAmounts: budgetAmountsStr,
                spentAmounts: spentAmountsStr
            });

            // Parse JSON
            const budgetNames = JSON.parse(budgetNamesStr || '[]');
            const budgetAmounts = JSON.parse(budgetAmountsStr || '[]');
            const spentAmounts = JSON.parse(spentAmountsStr || '[]');

            console.log('Parsed budget data:', {
                budgetNames: budgetNames,
                budgetAmounts: budgetAmounts,
                spentAmounts: spentAmounts
            });

            if (budgetNames.length > 0 && budgetAmounts.length > 0 && spentAmounts.length > 0) {
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
                console.log('Budget chart created successfully');
            } else {
                console.warn('No data for budget chart');
                budgetChart.innerHTML = '<div style="text-align:center;padding:50px;">No data available</div>';
            }
        } catch (error) {
            console.error('Error creating budget chart:', error);
            budgetChart.innerHTML = '<div style="text-align:center;padding:50px;">Error: ' + error.message + '</div>';
        }
    } else {
        console.error('Budget chart element not found');
    }

    // Expense Trend Chart
    const trendChart = document.getElementById('expenseTrendChart');
    if (trendChart) {
        console.log('Trend chart element found');

        try {
            // Access data attributes directly
            const datesStr = trendChart.getAttribute('data-dates');
            const amountsStr = trendChart.getAttribute('data-amounts');

            console.log('Raw trend data attributes:', {
                dates: datesStr,
                amounts: amountsStr
            });

            // Parse JSON
            const dates = JSON.parse(datesStr || '[]');
            const amounts = JSON.parse(amountsStr || '[]');

            console.log('Parsed trend data:', {
                dates: dates,
                amounts: amounts
            });

            if (dates.length > 0 && amounts.length > 0) {
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
                console.log('Trend chart created successfully');
            } else {
                console.warn('No data for trend chart');
                trendChart.innerHTML = '<div style="text-align:center;padding:50px;">No data available</div>';
            }
        } catch (error) {
            console.error('Error creating trend chart:', error);
            trendChart.innerHTML = '<div style="text-align:center;padding:50px;">Error: ' + error.message + '</div>';
        }
    } else {
        console.error('Trend chart element not found');
    }

    console.log('Dashboard charts initialization complete');
});
