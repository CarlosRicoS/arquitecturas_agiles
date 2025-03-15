import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const UserActivityPieChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={entry.name.includes('intruso') ? '#FF8042' : COLORS[index % COLORS.length]} 
            />
          ))}
        </Pie>
        <Tooltip formatter={(value) => [`${value} acciones`, 'Cantidad']} />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default UserActivityPieChart;