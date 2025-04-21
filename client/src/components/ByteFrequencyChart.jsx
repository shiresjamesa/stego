import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function ByteFrequencyChart({ byteCounts, title }) {
  const allByteCounts = Array(256).fill(0);

  // Populate byte counts
  for (const [byte, count] of Object.entries(byteCounts)) {
    allByteCounts[parseInt(byte)] = count;
  }

  // Data for the chart
  const data = {
    labels: Array.from({ length: 256 }, (_, i) => i),
    datasets: [
      {
        label: title,
        data: allByteCounts,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Chart options to make it look pretty
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
      },
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: title,
        font: {
          size: 16
        },
        padding: {
          top: 10,
          bottom: 10
        }
      },
    },
  };
  

  return (
    <div style={{ height: '300px', width: '95%' }}>
      <Bar data={data} options={options} />
    </div>
  );
}
