import React, { useState } from 'react';
import { analyzeLogs } from './LogParser';
import { Search, Filter } from 'lucide-react';

const EventsTable = ({ logs }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [sortField, setSortField] = useState('timestamp');
  const [sortDirection, setSortDirection] = useState('desc');
  
  const logAnalysis = analyzeLogs(logs);
  
  // Combinar todos los eventos de inventario
  let allEvents = [...logAnalysis.inventoryEvents];
  
  // Aplicar filtro por tipo
  if (filterType !== 'all') {
    allEvents = allEvents.filter(event => {
      if (filterType === 'GET' && event.jsonData?.message?.detail?.accion === 'GET') return true;
      if (filterType === 'POST' && event.jsonData?.message?.detail?.accion === 'POST') return true;
      if (filterType === 'DELETE' && event.jsonData?.message?.detail?.accion === 'DELETE') return true;
      if (filterType === 'intruso' && event.jsonData?.message?.detail?.usuario === 'usuario_intruso') return true;
      if (filterType === 'legitimo' && event.jsonData?.message?.detail?.usuario === 'usuario_legitimo') return true;
      return false;
    });
  }
  
  // Aplicar búsqueda
  if (searchTerm) {
    const searchLower = searchTerm.toLowerCase();
    allEvents = allEvents.filter(event => {
      const jsonString = JSON.stringify(event.jsonData).toLowerCase();
      return jsonString.includes(searchLower);
    });
  }
  
  // Ordenar eventos
  allEvents.sort((a, b) => {
    let aValue, bValue;
    
    if (sortField === 'timestamp') {
      aValue = new Date(a.timestamp || 0);
      bValue = new Date(b.timestamp || 0);
    } else if (sortField === 'usuario') {
      aValue = a.jsonData?.message?.detail?.usuario || '';
      bValue = b.jsonData?.message?.detail?.usuario || '';
    } else if (sortField === 'accion') {
      aValue = a.jsonData?.message?.detail?.accion || '';
      bValue = b.jsonData?.message?.detail?.accion || '';
    } else if (sortField === 'ip') {
      aValue = a.jsonData?.message?.host_ip || '';
      bValue = b.jsonData?.message?.host_ip || '';
    }
    
    if (aValue === bValue) return 0;
    
    const comparison = aValue > bValue ? 1 : -1;
    return sortDirection === 'desc' ? -comparison : comparison;
  });
  
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };
  
  const SortIcon = ({ field }) => {
    if (sortField !== field) return null;
    return <span className="ml-1">{sortDirection === 'asc' ? '▲' : '▼'}</span>;
  };
  
  return (
    <div className="space-y-4">
      <div className="bg-white shadow rounded-lg p-5">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Registro de Eventos</h2>
        
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <Search className="w-5 h-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full pl-10 p-2.5"
              placeholder="Buscar en eventos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg p-2.5"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="all">Todos</option>
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="DELETE">DELETE</option>
              <option value="intruso">Usuario Intruso</option>
              <option value="legitimo">Usuario Legítimo</option>
            </select>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('timestamp')}
                >
                  Timestamp <SortIcon field="timestamp" />
                </th>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('usuario')}
                >
                  Usuario <SortIcon field="usuario" />
                </th>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('accion')}
                >
                  Acción <SortIcon field="accion" />
                </th>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('ip')}
                >
                  IP <SortIcon field="ip" />
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Datos
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {allEvents.map((event, index) => {
                const isIntruso = event.jsonData?.message?.detail?.usuario === 'usuario_intruso';
                const timestamp = event.jsonData?.message?.timestamp;
                const usuario = event.jsonData?.message?.detail?.usuario;
                const accion = event.jsonData?.message?.detail?.accion;
                const ip = event.jsonData?.message?.host_ip;
                const data = event.jsonData?.message?.detail?.data;
                
                return (
                  <tr key={index} className={isIntruso ? 'bg-red-50' : ''}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {timestamp}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        isIntruso ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                      }`}>
                        {usuario}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {accion}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {ip}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {Array.isArray(data) ? data.join(', ') : data}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 text-sm text-gray-500">
          Mostrando {allEvents.length} eventos
        </div>
      </div>
    </div>
  );
};

export default EventsTable;