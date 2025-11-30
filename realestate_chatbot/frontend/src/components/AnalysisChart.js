import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler // Import Filler for area effects if desired
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const AnalysisChart = ({ chartData }) => {
  if (!chartData || chartData.length === 0) return null;

  const data = {
    labels: chartData.map((item) => item.year),
    datasets: [
      {
        label: 'Avg Price (₹/sqft)',
        data: chartData.map((item) => item.price),
        // Monochromatic: Dark Slate for Price
        borderColor: '#2c3e50', 
        backgroundColor: 'rgba(44, 62, 80, 0.1)',
        borderWidth: 2,
        tension: 0.4, // Smooth curves
        pointRadius: 4,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#2c3e50',
        yAxisID: 'y',
        fill: true,
      },
      {
        label: 'Total Sales',
        data: chartData.map((item) => item.sales),
        // Monochromatic: Light Grey/Silver for Sales
        borderColor: '#95a5a6',
        backgroundColor: 'rgba(149, 165, 166, 0.1)', 
        borderWidth: 2,
        borderDash: [5, 5], // Dashed line for contrast
        tension: 0.4,
        pointRadius: 3,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          font: { family: '-apple-system, sans-serif', size: 12 }
        }
      },
      tooltip: {
        backgroundColor: '#2c3e50',
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        padding: 10,
        cornerRadius: 8,
        displayColors: false,
      }
    },
    scales: {
      x: {
        grid: { display: false }, // Cleaner look
        ticks: { font: { size: 11 } }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        grid: { color: '#f0f0f0' },
        ticks: { 
          callback: (value) => '₹' + value/1000 + 'k' // Shorten numbers
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: { display: false },
      },
    },
  };

  return (
    <div className="modern-card p-4">
      <h6 className="text-uppercase text-secondary mb-3" style={{letterSpacing: '1px', fontSize: '0.75rem'}}>Market Trend Analysis</h6>
      <Line options={options} data={data} />
    </div>
  );
};

export default AnalysisChart;