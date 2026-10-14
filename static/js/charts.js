/**
 * Online Complaint Management System (OCMS)
 * Single Clean Dashboard Chart (Resolution Trend)
 */

document.addEventListener('DOMContentLoaded', function () {
  const trendCtx = document.getElementById('singleTrendChart');
  if (trendCtx) {
    new Chart(trendCtx, {
      type: 'line',
      data: {
        labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
        datasets: [
          {
            label: 'Complaints Resolved',
            data: [28, 41, 52, 68, 60, 78],
            borderColor: '#0d9488', // Soft Teal
            backgroundColor: 'rgba(13, 148, 136, 0.08)',
            fill: true,
            tension: 0.35,
            borderWidth: 2.5,
            pointBackgroundColor: '#0d9488',
            pointRadius: 4
          },
          {
            label: 'New Complaints',
            data: [32, 45, 58, 72, 64, 85],
            borderColor: '#4338ca', // Deep Indigo
            backgroundColor: 'transparent',
            tension: 0.35,
            borderWidth: 2.5,
            pointBackgroundColor: '#4338ca',
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              font: {
                family: "'Inter', sans-serif",
                size: 12,
                weight: '500'
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: '#f1f5f9'
            },
            ticks: {
              font: {
                family: "'Inter', sans-serif"
              }
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: {
                family: "'Inter', sans-serif"
              }
            }
          }
        }
      }
    });
  }
});
