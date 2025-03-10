'use client'

import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Bar,
  BarChart,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';
import type { ErrorLog, ExperimentLog, ExperimentStats } from '@/types/logs';

const LogAnalyzer = () => {
  const [errorLogs, setErrorLogs] = useState<ErrorLog[]>([]);
  const [experimentLogs, setExperimentLogs] = useState<ExperimentLog[]>([]);
  const [stats, setStats] = useState<ExperimentStats | null>(null);
  const [detectionTimes, setDetectionTimes] = useState<any[]>([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const [errorResponse, experimentResponse] = await Promise.all([
        fetch('/api/logs/error'),
        fetch('/api/logs/experimento')
      ]);

      const errors = await errorResponse.json();
      const experiments = await experimentResponse.json();

      setErrorLogs(errors);
      setExperimentLogs(experiments);
      
      const detectionData = experiments
        .filter((exp: ExperimentLog) => exp.estado === 'indispuesto')
        .map((exp: ExperimentLog) => {
          const matchingError = errors.find((e: ErrorLog) => 
            Math.abs(e.timestamp - exp.timestamp) < 2000
          );
          
          if (matchingError) {
            const errorTime = exp.timestamp;
            const detectionTime = Math.max(errorTime, matchingError.timestamp);

            return {
              experimento: exp.experimento,
              llamado: exp.llamado,
              errorTime: exp.timestamp,
              detectionTime: matchingError.timestamp,
              detectionDelay: Math.abs(detectionTime - errorTime) / 1000,
              errorId: matchingError.instanceId
            };
          }
          return null;
        })
        .filter(Boolean);

      setDetectionTimes(detectionData);
      calculateStats(errors, experiments, detectionData);
    };

    fetchLogs();
  }, []);

  const calculateStats = (errors: ErrorLog[], experiments: ExperimentLog[], detectionData: any[]) => {
    const stats: ExperimentStats = {
      totalExperiments: Math.max(...experiments.map(e => e.experimento)),
      totalCalls: experiments.length,
      availabilityRate: experiments.filter(e => e.estado === 'disponible').length / experiments.length * 100,
      avgDetectionTime: detectionData.reduce((acc, curr) => acc + curr.detectionDelay, 0) / detectionData.length,
      errorsByExperiment: {},
      minDetectionTime: Math.min(...detectionData.map(d => d.detectionDelay)),
      maxDetectionTime: Math.max(...detectionData.map(d => d.detectionDelay))
    };

    experiments.forEach(exp => {
      if (exp.estado === 'indispuesto') {
        stats.errorsByExperiment[exp.experimento] = (stats.errorsByExperiment[exp.experimento] || 0) + 1;
      }
    });

    setStats(stats);
  };

  const timelineData = experimentLogs.map(log => ({
    time: log.timestamp,
    estado: log.estado === 'disponible' ? 1 : 0,
    experimento: log.experimento,
    erroresDetectados: errorLogs.filter(e => 
      Math.abs(e.timestamp - log.timestamp) < 2000
    ).length
  }));

  const errorsByExperiment = stats?.errorsByExperiment ? 
    Object.entries(stats.errorsByExperiment).map(([exp, count]) => ({
      experimento: parseInt(exp),
      errores: count
    })) : [];

  return (
    <div className="space-y-8 p-4">
      {stats && (
        <div className="grid grid-cols-6 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Total Experimentos</h3>
            <p className="text-2xl">{stats.totalExperiments}</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Total Llamadas</h3>
            <p className="text-2xl">{stats.totalCalls}</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Disponibilidad</h3>
            <p className="text-2xl">{stats.availabilityRate.toFixed(1)}%</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Tiempo Promedio Detección</h3>
            <p className="text-2xl">{stats.avgDetectionTime.toFixed(3)}s</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Detección Más Rápida</h3>
            <p className="text-2xl">{stats.minDetectionTime.toFixed(3)}s</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">Detección Más Lenta</h3>
            <p className="text-2xl">{stats.maxDetectionTime.toFixed(3)}s</p>
          </div>
        </div>
      )}

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Tiempos de Detección por Error</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="errorTime" 
                type="number"
                domain={['dataMin', 'dataMax']}
                name="Tiempo"
                tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString()}
              />
              <YAxis 
                dataKey="detectionDelay" 
                name="Tiempo de Detección (s)"
                label={{ value: 'Tiempo de Detección (s)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                formatter={(value: any, name: string) => {
                  if (name === 'Tiempo') return new Date(value).toLocaleString();
                  return `${Number(value).toFixed(3)}s`;
                }}
              />
              <Legend />
              <Scatter 
                name="Tiempo de Detección" 
                data={detectionTimes} 
                fill="#8884d8"
              />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-100 p-4 rounded">
            {detectionTimes.slice(0, Math.ceil(detectionTimes.length / 2)).map((item, index) => (
              <pre key={index}>{JSON.stringify(item, null, 2)}</pre>
            ))}
          </div>
          <div className="bg-gray-100 p-4 rounded">
            {detectionTimes.slice(Math.ceil(detectionTimes.length / 2)).map((item, index) => (
              <pre key={index}>{JSON.stringify(item, null, 2)}</pre>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Línea de Tiempo de Estados y Errores</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="time" 
                type="number"
                domain={['dataMin', 'dataMax']}
                tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString()}
              />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip 
                labelFormatter={(timestamp) => new Date(timestamp).toLocaleString()}
              />
              <Legend />
              <Line 
                yAxisId="left"
                type="stepAfter"
                dataKey="estado"
                stroke="#8884d8"
                name="Estado (1=Disponible)"
              />
              <Line 
                yAxisId="right"
                type="monotone"
                dataKey="erroresDetectados"
                stroke="#82ca9d"
                name="Errores Detectados"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Detalle de Tiempos de Detección</h2>
        <div className="h-64 overflow-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left p-3">Experimento</th>
                <th className="text-left p-3">Llamada</th>
                <th className="text-left p-3">Tiempo Error</th>
                <th className="text-left p-3">Tiempo Detección</th>
                <th className="text-left p-3">Retraso (s)</th>
                <th className="text-left p-3">ID Error</th>
              </tr>
            </thead>
            <tbody>
              {detectionTimes.map((detection, idx) => (
                <tr key={idx} className="border-t hover:bg-gray-50">
                  <td className="p-3">{detection.experimento}</td>
                  <td className="p-3">{detection.llamado}</td>
                  <td className="p-3">{new Date(detection.errorTime).toLocaleString()}</td>
                  <td className="p-3">{new Date(detection.detectionTime).toLocaleString()}</td>
                  <td className="p-3">{detection.detectionDelay.toFixed(3)}</td>
                  <td className="p-3">{detection.errorId}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default LogAnalyzer;