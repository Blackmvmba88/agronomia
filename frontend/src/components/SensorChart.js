import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function SensorChart({ data, dataKey, dataKey2, color = '#8884d8', color2 = '#82ca9d', legend1, legend2 }) {
  // Preparar datos para el gráfico
  const chartData = data.map(item => ({
    time: new Date(item.timestamp || item.createdAt?.seconds * 1000).toLocaleTimeString(),
    [dataKey]: item[dataKey],
    ...(dataKey2 && { [dataKey2]: item[dataKey2] })
  })).reverse();

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey={dataKey} 
          stroke={color} 
          name={legend1 || dataKey}
          strokeWidth={2}
          dot={false}
        />
        {dataKey2 && (
          <Line 
            type="monotone" 
            dataKey={dataKey2} 
            stroke={color2} 
            name={legend2 || dataKey2}
            strokeWidth={2}
            dot={false}
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
}

export default SensorChart;
