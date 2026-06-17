document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('activityChart').getContext('2d');
    
    // ایجاد گرادینت برای زیر نمودار خطی
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, 'rgba(14, 165, 233, 0.25)'); // رنگ آبی ملایم با شفافیت
    gradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');  // محو شدن به سمت پایین

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'],
            datasets: [{
                label: 'درخواست‌ها',
                data: [2, 5, 3, 7, 4, 6, 8],
                borderColor: '#0ea5e9', // رنگ آبی مدرن (Sky 500)
                backgroundColor: gradient,
                tension: 0.4, // نرمی خط
                fill: true,
                borderWidth: 3,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#0ea5e9',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointHoverBackgroundColor: '#0ea5e9',
                pointHoverBorderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false // مخفی کردن لیجن چون فقط یک نمودار داریم
                },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    padding: 10,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.04)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: { size: 11 }
                    }
                },
                x: {
                    grid: {
                        display: false // حذف خطوط عمودی برای تمیزی کار
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: { size: 11 }
                    }
                }
            }
        }
    });
});