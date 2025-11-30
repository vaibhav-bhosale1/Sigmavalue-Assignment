import React from 'react';

const DataTable = ({ tableData }) => {
  if (!tableData || tableData.length === 0) return null;

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="table table-hover align-middle">
        <thead className="table-light text-secondary">
          <tr style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            <th className="border-0">Year</th>
            <th className="border-0">Location</th>
            <th className="border-0">Avg Rate (Flat)</th>
            <th className="border-0">Total Sales</th>
            <th className="border-0 text-end">Supply</th>
          </tr>
        </thead>
        <tbody style={{ fontSize: '0.9rem', color: '#2c3e50' }}>
          {tableData.map((row, index) => (
            <tr key={index}>
              <td className="fw-bold">{row.year}</td>
              <td>{row.final_location}</td>
              <td>₹{row.flat_weighted_avg_rate.toLocaleString()}</td>
              <td>{row.total_sales_igr}</td>
              <td className="text-end">{row.total_units}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;