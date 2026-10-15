/**
 * Online Complaint Management System (OCMS)
 * Dynamic Dashboard Chart (Resolution Trend via /admin/api/stats)
 */

document.addEventListener('DOMContentLoaded', function () {
  const trendCanvas = document.getElementById('singleTrendChart');
  if (!trendCanvas) return;

  function renderChart(labels, resolvedData, newData) {
    new Chart(trendCanvas, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Complaints Resolved',
            data: resolvedData,
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
            data: newData,
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
              precision: 0,
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

  // Attempt to fetch live statistics from backend
  fetch('/admin/api/stats')
    .then(response => {
      if (!response.ok) {
        throw new Error('Stats API returned ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      if (data && data.labels && data.labels.length > 0) {
        renderChart(data.labels, data.resolved_complaints, data.new_complaints);
      } else {
        // Fallback default sample trend
        renderChart(['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'], [4, 6, 8, 12, 10, 14], [5, 7, 9, 14, 11, 16]);
      }
    })
    .catch(() => {
      // Graceful fallback if guest or non-admin session
      renderChart(['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'], [4, 6, 8, 12, 10, 14], [5, 7, 9, 14, 11, 16]);
    });
});
