import React from 'react';
import { analyzeLogs } from './LogParser';
import { AlertTriangle, Clock, RefreshCw } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const IntrusionsView = ({ logs }) => {
    const logAnalysis = analyzeLogs(logs);
  
    const intrusionEvents = logAnalysis.intrusionEvents;
    
    const auditorEvents = logs.auditor.filter(log => 
        log.jsonData?.message?.detail?.usuario === 'usuario_intruso'
    );
    
    const suspiciousEvents = logs.inventario.filter(log => 
        log.jsonData?.message?.detail?.usuario === 'usuario_intruso'
    );
    
    const detectionTimes = [];
    
    suspiciousEvents.forEach(event => {
        if (!event.jsonData?.message?.timestamp) return;
        
        const eventTime = new Date(event.jsonData.message.timestamp);
        const eventUUID = event.jsonData.message.uuid;
        
        let auditEvent = auditorEvents.find(audit => 
            audit.jsonData?.message?.uuid === eventUUID
        );
        
        if (!auditEvent) {
            auditEvent = auditorEvents.find(audit => {
                if (!audit.jsonData?.message?.detail) return false;
                
                const sameUser = audit.jsonData.message.detail.usuario === event.jsonData.message.detail.usuario;
                const sameAction = audit.jsonData.message.detail.accion === event.jsonData.message.detail.accion;
                
                if (sameUser && sameAction && audit.jsonData.message.timestamp) {
                    const auditTime = new Date(audit.jsonData.message.timestamp);
                    const timeDiff = Math.abs(auditTime.getTime() - eventTime.getTime()) / 1000;
                    return timeDiff < 5;
                }
                
                return false;
            });
        }
        
        let detectionEvent = null;
        if (!auditEvent) {
            detectionEvent = intrusionEvents.find(detection => {
                const messageContent = detection.message || '';
                const jsonStartIdx = messageContent.indexOf('{');
                let detectionJsonData = null;
                
                if (jsonStartIdx !== -1) {
                    try {
                        const jsonStr = messageContent.substring(jsonStartIdx);
                        detectionJsonData = JSON.parse(jsonStr);
                    } catch (e) {
                        console.error("Error parsing JSON in detection message:", e);
                    }
                }
                
                const detectionIpMatch = messageContent.includes(event.jsonData.message.host_ip);
                
                let timeMatch = false;
                if (detection.timestamp) {
                    try {
                        const detectionTimeParts = detection.timestamp.split(',');
                        if (detectionTimeParts.length >= 2) {
                            const dateStr = detectionTimeParts[0].trim();
                            const timeStr = detectionTimeParts[1].trim();
                            const isoTimestamp = dateStr.replace(' ', 'T') + '.' + timeStr;
                            
                            const detectionDate = new Date(isoTimestamp);
                            const timeDiff = Math.abs(detectionDate.getTime() - eventTime.getTime()) / 1000;
                            
                            if (timeDiff < 10) {
                                timeMatch = true;
                            }
                        }
                    } catch (e) {
                        console.error("Error parsing detection timestamp:", e);
                    }
                }
                
                return detectionIpMatch || 
                       (detectionJsonData && detectionJsonData.message?.uuid === eventUUID) ||
                       timeMatch;
            });
        }
        
        const finalEvent = auditEvent || detectionEvent;
        
        if (finalEvent) {
            let detectionTime;
            
            if (finalEvent.timestamp) {
                try {
                    const timeParts = finalEvent.timestamp.split(',');
                    if (timeParts.length >= 2) {
                        const dateStr = timeParts[0].trim();
                        const timeStr = timeParts[1].trim();
                        const isoTimestamp = dateStr.replace(' ', 'T') + '.' + timeStr;
                        detectionTime = new Date(isoTimestamp);
                    } else {
                        detectionTime = new Date(finalEvent.timestamp);
                    }
                } catch (e) {
                    console.error("Error parsing timestamp:", e);
                }
            } else if (finalEvent.jsonData?.message?.timestamp) {
                detectionTime = new Date(finalEvent.jsonData.message.timestamp);
            }
            
            if (detectionTime && !isNaN(detectionTime.getTime())) {
                const diff = (detectionTime.getTime() - eventTime.getTime()) / 1000;
                
                detectionTimes.push({
                    evento: eventUUID || 'Unknown',
                    origen: event.jsonData.message.host_ip || 'Unknown',
                    tiempo: Math.abs(diff).toFixed(2),
                    timestamp: event.jsonData.message.timestamp,
                    fuente: auditEvent ? 'auditor' : 'detector'
                });
            }
        } else {
            detectionTimes.push({
                evento: eventUUID || 'Unknown',
                origen: event.jsonData.message.host_ip || 'Unknown',
                tiempo: '0.00',
                timestamp: event.jsonData.message.timestamp,
                fuente: 'no_detectado'
            });
        }
    });
    
    console.log("Tiempos de detección:", detectionTimes);
    
    const timelineData = suspiciousEvents.map(event => {
        const timestamp = new Date(event.jsonData?.message?.timestamp);
        return {
            time: timestamp.toLocaleTimeString(),
            accion: event.jsonData?.message?.detail?.accion,
            usuario: event.jsonData?.message?.detail?.usuario,
            ip: event.jsonData?.message?.host_ip,
            data: event.jsonData?.message?.detail?.data,
            timestamp: timestamp.getTime(),
            uuid: event.jsonData?.message?.uuid
        };
    }).sort((a, b) => a.timestamp - b.timestamp);
    
    const chartData = detectionTimes.map(time => ({
        name: time.evento.substring(0, 8) + '...',
        tiempo: parseFloat(time.tiempo),
        fuente: time.fuente
    }));
    
    if (chartData.length === 0) {
        chartData.push({
            name: 'No hay datos',
            tiempo: 0,
            fuente: 'none'
        });
    }
  
    return (
        <div className="space-y-6">
            <div className="bg-white shadow rounded-lg p-5">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Análisis de Intrusiones</h2>
                
                <div className="grid grid-cols-3 gap-4">
                    <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                        <div className="flex items-center">
                            <AlertTriangle className="h-8 w-8 text-red-500 mr-3" />
                            <div>
                                <h3 className="text-sm font-medium text-red-800">Intrusiones Detectadas</h3>
                                <p className="text-2xl font-bold text-red-900">{intrusionEvents.length}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                        <div className="flex items-center">
                            <RefreshCw className="h-8 w-8 text-yellow-500 mr-3" />
                            <div>
                                <h3 className="text-sm font-medium text-yellow-800">Acciones Sospechosas</h3>
                                <p className="text-2xl font-bold text-yellow-900">{suspiciousEvents.length}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <div className="flex items-center">
                            <Clock className="h-8 w-8 text-blue-500 mr-3" />
                            <div>
                                <h3 className="text-sm font-medium text-blue-800">Tiempo Promedio Detección</h3>
                                <p className="text-2xl font-bold text-blue-900">
                                    {detectionTimes.length > 0 && detectionTimes.some(t => t.fuente !== 'no_detectado')
                                        ? (detectionTimes
                                            .filter(t => t.fuente !== 'no_detectado')
                                            .reduce((sum, time) => sum + parseFloat(time.tiempo), 0) / 
                                            detectionTimes.filter(t => t.fuente !== 'no_detectado').length
                                        ).toFixed(2) + 's'
                                        : 'N/A'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div className="mt-6">
                    <h3 className="text-md font-medium text-gray-700 mb-3">Tiempos de Detección de Intrusiones</h3>
                    <div className="h-64">
                        {chartData.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart
                                    data={chartData}
                                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                                >
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis 
                                        label={{ value: 'Segundos', angle: -90, position: 'insideLeft' }}
                                        domain={[0, 'dataMax + 1']} 
                                    />
                                    <Tooltip 
                                        formatter={(value) => [`${value} segundos`, 'Tiempo de detección']}
                                        labelFormatter={(value) => `Evento: ${value}`} 
                                    />
                                    <Line 
                                        type="monotone" 
                                        dataKey="tiempo" 
                                        stroke="#FF8042" 
                                        activeDot={{ r: 8 }} 
                                        name="Tiempo de detección"
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="flex h-full items-center justify-center text-gray-500">
                                No hay datos de detección para visualizar
                            </div>
                        )}
                    </div>
                </div>
            </div>
            
            <div className="bg-white shadow rounded-lg p-5">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Detalles de Intrusiones</h2>
                
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Timestamp
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Origen (IP)
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Acción
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Datos
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Tiempo Detección
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {timelineData.map((event, index) => {
                                const detectionTime = detectionTimes.find(dt => dt.evento === event.uuid);
                                
                                return (
                                    <tr key={index} className="bg-red-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {event.time}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                                {event.ip}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {event.accion}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {Array.isArray(event.data) ? event.data.join(', ') : event.data}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {detectionTime && detectionTime.fuente !== 'no_detectado' ? (
                                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                                    {detectionTime.tiempo}s
                                                </span>
                                            ) : (
                                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                                                    No detectado
                                                </span>
                                            )}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default IntrusionsView;