/**
 * Función para analizar archivos de log y convertirlos en objetos estructurados
 * @param {string} logText - Texto del archivo de log
 * @param {string} source - Fuente del log (auditor, autorizador, etc.)
 * @returns {Array} - Array de objetos de log estructurados
 */
export const parseLogFile = (logText, source) => {
    const lines = logText.split('\n').filter(line => line.trim());
    return lines.map(line => {
      try {
        const parts = line.split('|');
        const timestamp = parts[2] || '';
        let message = parts[3] || '';
        
        const jsonStart = message.indexOf('{');
        let jsonData = null;
        if (jsonStart !== -1) {
          try {
            jsonData = JSON.parse(message.substring(jsonStart));
          } catch (e) {
            console.log(e);
          }
        }
        
        return {
          source,
          component: parts[0] || '',
          level: parts[1] || '',
          timestamp,
          message: message.trim(),
          jsonData,
          raw: line
        };
      } catch (e) {
        console.log(e);
        return { source, raw: line };
      }
    });
  };
  
  /**
   * Analiza los logs para extraer información relevante
   * @param {Object} logs - Objeto con los logs por fuente
   * @returns {Object} - Análisis de los logs
   */
  export const analyzeLogs = (logs) => {
    const authEvents = logs.autorizador.filter(log => 
      log.message && log.message.includes('[Autorizador]')
    );
    
    const intrusionEvents = logs.detector.filter(log => 
      log.level === '[WARNING]' && log.message && log.message.includes('origen no válido')
    );
    
    const inventoryEvents = logs.inventario.filter(log => 
      log.jsonData && log.jsonData.message && log.jsonData.message.event_type === 'CAMBIO-INVENTARIO'
    );
    
    const authorizedUsers = {};
    authEvents.forEach(event => {
      if (event.message) {
        const match = event.message.match(/usuario='([^']+)'/);
        if (match) {
          const user = match[1];
          authorizedUsers[user] = (authorizedUsers[user] || 0) + 1;
        }
      }
    });
    
    const eventsByIp = {};
    inventoryEvents.forEach(event => {
      if (event.jsonData && event.jsonData.message && event.jsonData.message.host_ip) {
        const ip = event.jsonData.message.host_ip;
        eventsByIp[ip] = (eventsByIp[ip] || 0) + 1;
      }
    });
    
    const actionTypes = {};
    inventoryEvents.forEach(event => {
      if (event.jsonData && event.jsonData.message && event.jsonData.message.detail && event.jsonData.message.detail.accion) {
        const action = event.jsonData.message.detail.accion;
        actionTypes[action] = (actionTypes[action] || 0) + 1;
      }
    });
    
    return {
      authEvents,
      intrusionEvents,
      inventoryEvents,
      authorizedUsers: Object.entries(authorizedUsers).map(([name, value]) => ({ name, value })),
      eventsByIp: Object.entries(eventsByIp).map(([name, value]) => ({ name, value })),
      actionTypes: Object.entries(actionTypes).map(([name, value]) => ({ name, value }))
    };
  };