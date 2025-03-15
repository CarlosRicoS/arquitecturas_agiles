import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, ResponsiveContainer } from 'recharts';

const EventsByIPChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip formatter={(value) => [`${value} eventos`, 'Cantidad']} />
        <Legend />
        <Bar dataKey="value" name="Eventos" fill="#8884d8">
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={entry.name === "172.20.0.8" ? "#FF8042" : "#0088FE"} 
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default EventsByIPChart;