document.addEventListener("DOMContentLoaded", function () {
  const chartCanvas = document.getElementById('priceChart');
  if (!chartCanvas) return;

  const ctx = chartCanvas.getContext('2d');
  
  // Read price data passed from the HTML data attribute (fallback if missing)
  const rawData = chartCanvas.dataset.prices;
  const priceData = rawData 
    ? JSON.parse(rawData) 
    : [9990, 9800, 10200, 9990, 10100, 9700, 9990, 10400, 9990, 10000, 
       9800, 9990, 10300, 10100, 9990, 9600, 9990, 10200, 10100, 9990, 
       9800, 9990, 10100, 10300, 9990, 9700, 9850, 9990, 10000,9500];

  // Generate day labels [1, 2, ..., 30]
  const labels = Array.from({ length: priceData.length }, (_, i) => i + 1);

  // Smooth green gradient fill matching WonderCamp theme
  const gradient = ctx.createLinearGradient(0, 0, 0, 200);
  gradient.addColorStop(0, 'rgba(59, 96, 37, 0.45)');
  gradient.addColorStop(1, 'rgba(59, 96, 37, 0.05)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Price (Rs)',
        data: priceData,
        borderColor: '#3b6025',
        borderWidth: 2.5,
        backgroundColor: gradient,
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 6,
        pointBackgroundColor: '#3b6025'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return ' Rs ' + context.parsed.y.toLocaleString() + ' / day';
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#3b6025', font: { weight: 'bold' } }
        },
        y: {
          grid: { color: 'rgba(200, 211, 184, 0.3)' },
          ticks: { color: '#3b6025' }
        }
      }
    }
  });
});