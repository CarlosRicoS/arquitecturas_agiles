export interface ErrorLog {
    timestamp: number;
    level: string;
    message: string;
    instance: string;
  }
  
  export interface ExperimentLog {
    timestamp: number;
    experimento: number;
    llamado: number;
    estado: 'disponible' | 'indispuesto';
  }
  
  export interface ExperimentStats {
    totalExperiments: number;
    totalCalls: number;
    availabilityRate: number;
    avgDetectionTime: number;
    minDetectionTime: number;
    maxDetectionTime: number;
    errorsByExperiment: { [key: number]: number };
  }