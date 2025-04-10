// Utility functions for creating charts in the Climate-Smart Agriculture Platform

/**
 * Create a line chart for NDVI trends
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} dates - Array of date strings
 * @param {Array} ndviValues - Array of NDVI values
 */
function createNDVITrendChart(canvasId, dates, ndviValues) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'NDVI',
                data: ndviValues,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0,
                    max: 1,
                    title: {
                        display: true,
                        text: 'NDVI Value'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `NDVI: ${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create a doughnut chart for crop health distribution
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} healthData - Array of health percentage values [excellent, good, fair, poor]
 */
function createCropHealthDoughnut(canvasId, healthData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Excellent', 'Good', 'Fair', 'Poor'],
            datasets: [{
                data: healthData,
                backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#dc3545'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Create a soil moisture trend chart
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} timestamps - Array of timestamp strings
 * @param {Array} moistureData - Array of soil moisture values
 */
function createSoilMoistureChart(canvasId, timestamps, moistureData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    // Format timestamps to show only time
    const formattedTimes = timestamps.map(timestamp => {
        const date = new Date(timestamp);
        return date.getHours() + ':' + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes();
    });
    
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: formattedTimes,
            datasets: [{
                label: 'Soil Moisture (%)',
                data: moistureData,
                borderColor: '#17a2b8',
                backgroundColor: 'rgba(23, 162, 184, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 25
                    }
                },
                x: {
                    display: true,
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

/**
 * Create a multi-line chart for weather forecast
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} times - Array of time strings
 * @param {Array} temperatures - Array of temperature values
 * @param {Array} precipProbabilities - Array of precipitation probability values
 */
function createWeatherForecastChart(canvasId, times, temperatures, precipProbabilities) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: times,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    yAxisID: 'y',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Precipitation Probability (%)',
                    data: precipProbabilities,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false,
                    },
                    title: {
                        display: true,
                        text: 'Precipitation Probability (%)'
                    },
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

/**
 * Create a bar chart for soil nutrient levels
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} nutrients - Array of nutrient labels
 * @param {Array} values - Array of nutrient values
 * @param {Array} optimalValues - Array of optimal nutrient values
 */
function createNutrientBarChart(canvasId, nutrients, values, optimalValues) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: nutrients,
            datasets: [
                {
                    label: 'Current Levels',
                    data: values,
                    backgroundColor: 'rgba(13, 110, 253, 0.7)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Optimal Levels',
                    data: optimalValues,
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1,
                    type: 'line',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Level (ppm)'
                    }
                }
            }
        }
    });
}

/**
 * Create a gauge chart for a single value
 * @param {string} canvasId - The ID of the canvas element
 * @param {number} value - The value to display (0-100)
 * @param {string} label - The label for the gauge
 * @param {Array} thresholds - Thresholds for color changes [t1, t2] (0-100)
 */
function createGaugeChart(canvasId, value, label, thresholds = [33, 66]) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    // Determine color based on thresholds
    let color;
    if (value < thresholds[0]) {
        color = '#dc3545'; // Red - low/bad
    } else if (value < thresholds[1]) {
        color = '#ffc107'; // Yellow - medium/warning
    } else {
        color = '#28a745'; // Green - high/good
    }
    
    // Calculate the remaining portion (gray)
    const remainingValue = 100 - value;
    
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: [label, ''],
            datasets: [{
                data: [value, remainingValue],
                backgroundColor: [color, 'rgba(200, 200, 200, 0.2)'],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: 270,
            cutout: '80%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        },
        plugins: [{
            id: 'valueInCenter',
            afterDraw: (chart) => {
                const {ctx, chartArea: {left, top, width, height}} = chart;
                ctx.save();
                
                // Value text
                ctx.font = '24px Arial';
                ctx.fillStyle = color;
                ctx.textAlign = 'center';
                ctx.fillText(`${value}%`, left + width / 2, top + height - 10);
                
                // Label text
                ctx.font = '14px Arial';
                ctx.fillStyle = 'white';
                ctx.fillText(label, left + width / 2, top + height + 20);
                
                ctx.restore();
            }
        }]
    });
}

/**
 * Create a radar chart for farm health
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} labels - Array of category labels
 * @param {Array} values - Array of current values (0-100)
 */
function createFarmHealthRadar(canvasId, labels, values) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Farm Health',
                data: values,
                backgroundColor: 'rgba(23, 162, 184, 0.2)',
                borderColor: 'rgba(23, 162, 184, 1)',
                pointBackgroundColor: 'rgba(23, 162, 184, 1)',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(23, 162, 184, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            }
        }
    });
}
