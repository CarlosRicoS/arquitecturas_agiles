import React from 'react';
import { analyzeLogs } from './LogParser';
import StatCard from './StatCard';
import UserActivityPieChart from './charts/UserActivityPieChart';
import EventsByIPChart from './charts/EventsByIPChart';
import ActionTypesPieChart from './charts/ActionTypesPieChart';
import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';

const Dashboard = ({ logs }) => {
  const logAnalysis = analyzeLogs(logs);
  
  return (
    <div className="space-y-6">
      <div className="flex flex-row gap-6">
        <StatCard 
          icon={<Activity className="h-6 w-6 text-blue-600" />}
          title="Total Eventos"
          value={logAnalysis.inventoryEvents.length}
          bgColor="bg-blue-100"
        />
        
        <StatCard 
          icon={<AlertTriangle className="h-6 w-6 text-red-600" />}
          title="Intrusiones Detectadas"
          value={logAnalysis.intrusionEvents.length}
          bgColor="bg-red-100"
        />
        
        <StatCard 
          icon={<CheckCircle className="h-6 w-6 text-green-600" />}
          title="Autorizaciones Exitosas"
          value={logAnalysis.authEvents.filter(e => e.message && e.message.includes('autorizado=True')).length}
          bgColor="bg-green-100"
        />
      </div>
      
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribución de Actividad por Usuario</h3>
          <div className="h-64">
            <UserActivityPieChart data={logAnalysis.authorizedUsers} />
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Eventos por IP de Origen</h3>
          <div className="h-64">
            <EventsByIPChart data={logAnalysis.eventsByIp} />
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribución por Tipo de Acción</h3>
          <div className="h-64">
            <ActionTypesPieChart data={logAnalysis.actionTypes} />
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Análisis de Actividad por Usuario</h3>
          <div className="space-y-4 overflow-y-auto max-h-64">
            {logAnalysis.authorizedUsers.map((user, index) => (
              <div key={index} className="flex items-center">
                <div className={`w-3 h-3 rounded-full mr-2 ${user.name.includes('intruso') ? 'bg-red-500' : 'bg-green-500'}`}></div>
                <div className="flex-1">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{user.name}</span>
                    <span className="text-sm text-gray-500">{user.value} acciones</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <div 
                      className={`h-2 rounded-full ${user.name.includes('intruso') ? 'bg-red-500' : 'bg-green-500'}`}
                      style={{ width: `${(user.value / logAnalysis.authorizedUsers.reduce((sum, u) => sum + u.value, 0)) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;