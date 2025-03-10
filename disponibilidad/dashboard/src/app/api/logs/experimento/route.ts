import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

export async function GET() {
  try {
    const logPath = path.join(process.cwd(), 'logs', 'run_experimento.log');
    const data = await fs.readFile(logPath, 'utf8');
    
    const experiments = data.split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [timestamp, exp, call, status] = line.split('|').map(s => s.trim());
        const fixedTimestamp = timestamp.replace(",", ".");

        return {
          timestamp: new Date(fixedTimestamp).getTime(),
          experimento: parseInt(exp.replace('Experimento ', '')),
          llamado: parseInt(call.replace('Call ', '')),
          estado: status.replace(/"/g, '')
        };
      });

    return NextResponse.json(experiments);
  } catch (error) {
    console.error('Error reading experiment log:', error);
    return NextResponse.json({ error: 'Failed to read experiment log' }, { status: 500 });
  }
}