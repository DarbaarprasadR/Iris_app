document.addEventListener('DOMContentLoaded', function () {
    // Accuracy Over Time Chart
    const accuracyOverTimeCanvas = document.getElementById('accuracyOverTimeChart');
    if (accuracyOverTimeCanvas) {
        const accuracyDataStr = accuracyOverTimeCanvas.getAttribute('data-accuracy');
        const accuracyData = JSON.parse(accuracyDataStr);
        const labels = accuracyData.map((_, index) => 'Epoch ' + (index + 1));
        const dataOverTime = {
            labels: labels,
            datasets: [{
                label: 'Accuracy Over Time',
                data: accuracyData.map(a => a * 100),
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                pointHoverBackgroundColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 3
            }]
        };
        const configOverTime = {
            type: 'line',
            data: dataOverTime,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Model Accuracy Over Epochs',
                        font: {
                            size: 18,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        labels: {
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                        mode: 'nearest',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Epoch',
                            font: {
                                size: 16,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Accuracy (%)',
                            font: {
                                size: 16,
                                weight: 'bold'
                            }
                        },
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.3)'
                        },
                        ticks: {
                            stepSize: 10,
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        };
        new Chart(accuracyOverTimeCanvas.getContext('2d'), configOverTime);
    }

    // Overall Accuracy Chart as line graph with single point
    const accuracyCanvas = document.getElementById('accuracyChart');
    if (accuracyCanvas) {
        const accuracyValue = parseFloat(accuracyCanvas.getAttribute('data-accuracy'));
        const ctx = accuracyCanvas.getContext('2d');

        const labels = ['Current Accuracy'];
        const dataPoints = [accuracyValue * 100];

        const data = {
            labels: labels,
            datasets: [{
                label: 'Model Accuracy',
                data: dataPoints,
                fill: false,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                tension: 0.4,
                pointRadius: 7,
                pointHoverRadius: 9,
                pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                pointHoverBackgroundColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 3
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Current Model Accuracy',
                        font: {
                            size: 18,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        labels: {
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.3)'
                        },
                        ticks: {
                            stepSize: 10,
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        };

        new Chart(ctx, config);
    }
});
