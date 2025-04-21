import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, Title);

export default function RGBHistogramChart({ histograms, title = "RGB Histogram" }) {
  const labels = Array.from({ length: 256 }, (_, i) => i);

  const data = {
    labels,
    datasets: [
      {
        label: 'Red',
        data: Object.values(histograms.R),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        stack: 'stack1',
      },
      {
        label: 'Green',
        data: Object.values(histograms.G),
        backgroundColor: 'rgba(0, 255, 34, 0.6)',
        borderColor: 'rgba(0, 255, 34, 1)',
        borderWidth: 1,
        stack: 'stack1',
      },
      {
        label: 'Blue',
        data: Object.values(histograms.B),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        stack: 'stack1',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        ticks: {
          maxTicksLimit: 40,
          callback: function (val, index) {
            return index % 16 === 0 ? val : '';
          },
        },
        barPercentage: 1,
        categoryPercentage: 1.0,
      },
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      title: {
        display: true,
        text: title,
        font: { size: 16 },
        padding: { top: 10, bottom: 10 },
      },
      legend: {
        display: true,
        position: 'top',
      },
    },
  };

  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
}
