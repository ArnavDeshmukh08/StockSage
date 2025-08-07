// Chart.js configuration and initialization for Stock Trading Assistant

// Chart instances
let priceChart = null;
let rsiChart = null;

// Chart colors
const chartColors = {
    primary: '#0d6efd',
    success: '#198754',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#0dcaf0',
    secondary: '#6c757d',
    dark: '#212529',
    light: '#f8f9fa'
};

// Initialize price chart
function initializePriceChart(chartData, symbol) {
    const ctx = document.getElementById('priceChart');
    if (!ctx || !chartData) return;

    // Destroy existing chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }

    // Prepare datasets
    const datasets = [
        {
            label: 'Close Price',
            data: chartData.prices.close,
            borderColor: chartColors.primary,
            backgroundColor: chartColors.primary + '20',
            borderWidth: 2,
            fill: false,
            tension: 0.1,
            yAxisID: 'y'
        }
    ];

    // Add moving averages if available
    if (chartData.indicators.ema_9 && chartData.indicators.ema_9.length > 0) {
        datasets.push({
            label: 'EMA 9',
            data: chartData.indicators.ema_9,
            borderColor: chartColors.success,
            backgroundColor: 'transparent',
            borderWidth: 1,
            fill: false,
            tension: 0.1,
            yAxisID: 'y'
        });
    }

    if (chartData.indicators.ema_21 && chartData.indicators.ema_21.length > 0) {
        datasets.push({
            label: 'EMA 21',
            data: chartData.indicators.ema_21,
            borderColor: chartColors.warning,
            backgroundColor: 'transparent',
            borderWidth: 1,
            fill: false,
            tension: 0.1,
            yAxisID: 'y'
        });
    }

    if (chartData.indicators.sma_50 && chartData.indicators.sma_50.length > 0) {
        datasets.push({
            label: 'SMA 50',
            data: chartData.indicators.sma_50,
            borderColor: chartColors.info,
            backgroundColor: 'transparent',
            borderWidth: 1,
            fill: false,
            tension: 0.1,
            yAxisID: 'y'
        });
    }

    if (chartData.indicators.sma_200 && chartData.indicators.sma_200.length > 0) {
        datasets.push({
            label: 'SMA 200',
            data: chartData.indicators.sma_200,
            borderColor: chartColors.danger,
            backgroundColor: 'transparent',
            borderWidth: 1,
            fill: false,
            tension: 0.1,
            yAxisID: 'y'
        });
    }

    // Add Bollinger Bands if available
    if (chartData.indicators.bb_upper && chartData.indicators.bb_upper.length > 0) {
        datasets.push({
            label: 'BB Upper',
            data: chartData.indicators.bb_upper,
            borderColor: chartColors.secondary,
            backgroundColor: 'transparent',
            borderWidth: 1,
            fill: false,
            borderDash: [5, 5],
            yAxisID: 'y'
        });

        datasets.push({
            label: 'BB Lower',
            data: chartData.indicators.bb_lower,
            borderColor: chartColors.secondary,
            backgroundColor: chartColors.secondary + '10',
            borderWidth: 1,
            fill: '+1',
            borderDash: [5, 5],
            yAxisID: 'y'
        });
    }

    // Add volume as bar chart
    if (chartData.prices.volume && chartData.prices.volume.length > 0) {
        datasets.push({
            label: 'Volume',
            data: chartData.prices.volume,
            type: 'bar',
            backgroundColor: chartColors.secondary + '40',
            borderColor: chartColors.secondary,
            borderWidth: 1,
            yAxisID: 'y1'
        });
    }

    // Chart configuration
    const config = {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Price (₹)'
                    },
                    grid: {
                        drawOnChartArea: true,
                    },
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Volume'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    max: Math.max(...(chartData.prices.volume || [0])) * 4
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `${symbol} - Price Chart with Technical Indicators`
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.dataset.label === 'Volume') {
                                return `${context.dataset.label}: ${formatNumber(context.raw)}`;
                            } else {
                                return `${context.dataset.label}: ₹${context.raw.toFixed(2)}`;
                            }
                        }
                    }
                }
            },
            elements: {
                point: {
                    radius: 0,
                    hoverRadius: 4
                }
            }
        }
    };

    // Create chart
    priceChart = new Chart(ctx, config);
}

// Initialize RSI chart (separate chart for better visualization)
function initializeRSIChart(rsiData, dates) {
    const ctx = document.getElementById('rsiChart');
    if (!ctx || !rsiData) return;

    // Destroy existing chart if it exists
    if (rsiChart) {
        rsiChart.destroy();
    }

    const config = {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'RSI',
                    data: rsiData,
                    borderColor: chartColors.primary,
                    backgroundColor: chartColors.primary + '20',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'RSI'
                    },
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 10
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'RSI (Relative Strength Index)'
                },
                legend: {
                    display: false
                },
                annotation: {
                    annotations: {
                        overbought: {
                            type: 'line',
                            yMin: 70,
                            yMax: 70,
                            borderColor: chartColors.danger,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                enabled: true,
                                content: 'Overbought (70)',
                                position: 'end'
                            }
                        },
                        oversold: {
                            type: 'line',
                            yMin: 30,
                            yMax: 30,
                            borderColor: chartColors.success,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                enabled: true,
                                content: 'Oversold (30)',
                                position: 'end'
                            }
                        }
                    }
                }
            },
            elements: {
                point: {
                    radius: 0,
                    hoverRadius: 4
                }
            }
        }
    };

    rsiChart = new Chart(ctx, config);
}

// Initialize candlestick chart (if needed)
function initializeCandlestickChart(ohlcData, symbol) {
    const ctx = document.getElementById('candlestickChart');
    if (!ctx || !ohlcData) return;

    // This would require a candlestick chart plugin
    // For now, we'll use the line chart approach
    console.log('Candlestick chart would be initialized here');
}

// Update chart with new data
function updateChart(chartInstance, newData) {
    if (!chartInstance || !newData) return;

    chartInstance.data.labels = newData.dates;
    chartInstance.data.datasets.forEach((dataset, index) => {
        if (newData.datasets && newData.datasets[index]) {
            dataset.data = newData.datasets[index].data;
        }
    });

    chartInstance.update();
}

// Export chart as image
function exportChartAsPNG(chartInstance, filename = 'chart.png') {
    if (!chartInstance) return;

    const url = chartInstance.toBase64Image();
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
}

// Resize chart
function resizeChart(chartInstance) {
    if (chartInstance) {
        chartInstance.resize();
    }
}

// Format number for chart tooltips
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Handle window resize
window.addEventListener('resize', function() {
    resizeChart(priceChart);
    resizeChart(rsiChart);
});

// Export chart functions
window.ChartManager = {
    initializePriceChart,
    initializeRSIChart,
    initializeCandlestickChart,
    updateChart,
    exportChartAsPNG,
    resizeChart
};
