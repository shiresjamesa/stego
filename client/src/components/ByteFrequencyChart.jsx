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

export default function ByteFrequencyChart({ byteCounts }) {

  const allByteCounts = Array(256).fill(0);

  for (const [byte, count] of Object.entries(byteCounts)) {
    allByteCounts[parseInt(byte)] = count;
  }

  const data = {
    labels: Array.from({ length: 256 }, (_, i) => i),
    datasets: [
      {
        label: 'Byte Frequency',
        data: allByteCounts,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        ticks: {
          maxTicksLimit: 20,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div style={{ height: '20vw', width: '35vw' }}>
      <Bar data={data} options={options} />
    </div>
  );
}
