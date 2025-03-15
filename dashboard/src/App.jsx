import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import EventsTable from './components/EventsTable';
import IntrusionsView from './components/IntrusionsView';
import { parseLogFile } from './components/LogParser';
import { RefreshCw } from 'lucide-react';

function App() {
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState({
    auditor: [],
    autorizador: [],
    detector: [],
    inventario: []
  });
  
  const [activeTab, setActiveTab] = useState('dashboard');
  
  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        const auditorResponse = await fetch('/logs/auditor.log');
        const autorizadorResponse = await fetch('/logs/autorizador.log');
        const detectorResponse = await fetch('/logs/detector_intrusos.log');
        const inventarioResponse = await fetch('/logs/inventario.log');
        
        const auditorText = await auditorResponse.text();
        const autorizadorText = await autorizadorResponse.text();
        const detectorText = await detectorResponse.text();
        const inventarioText = await inventarioResponse.text();
        
        setLogs({
          auditor: parseLogFile(auditorText, 'auditor'),
          autorizador: parseLogFile(autorizadorText, 'autorizador'),
          detector: parseLogFile(detectorText, 'detector'),
          inventario: parseLogFile(inventarioText, 'inventario')
        });
      } catch (error) {
        console.error('Error fetching logs:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchLogs();
  }, []);
  
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <RefreshCw className="w-12 h-12 text-blue-500 animate-spin" />
        <h2 className="mt-4 text-xl font-semibold text-gray-700">Cargando datos de seguridad...</h2>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard de Seguridad</h1>
            <div className="flex space-x-2">
              <button 
                className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600 flex items-center"
                onClick={() => window.location.reload()}
              >
                <RefreshCw className="w-4 h-4 mr-1" /> Actualizar
              </button>
            </div>
          </div>
        </div>
      </header>
      
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex space-x-8">
            <button 
              className={`py-3 px-1 border-b-2 font-medium text-sm ${activeTab === 'dashboard' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`py-3 px-1 border-b-2 font-medium text-sm ${activeTab === 'events' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('events')}
            >
              Eventos
            </button>
            <button 
              className={`py-3 px-1 border-b-2 font-medium text-sm ${activeTab === 'intrusions' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('intrusions')}
            >
              Intrusiones
            </button>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6">
        {activeTab === 'dashboard' && <Dashboard logs={logs} />}
        {activeTab === 'events' && <EventsTable logs={logs} />}
        {activeTab === 'intrusions' && <IntrusionsView logs={logs} />}
      </main>
    </div>
  );
}

export default App;