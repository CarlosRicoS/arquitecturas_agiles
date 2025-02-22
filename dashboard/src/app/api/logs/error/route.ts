import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

export async function GET() {
  try {
    const logPath = path.join(process.cwd(), 'logs', 'logger.log');
    const data = await fs.readFile(logPath, 'utf8');
    
    const errors = data.split('\n')
        .slice(1)
        .filter(line => line.trim())
        .map(line => {
            const [x, level, timestamp, message, instance] = line.split('|').map(s => s.trim());
            const fixedTimestamp = timestamp.replace(",", ".");
            
            return {
                timestamp: new Date(fixedTimestamp).getTime(),
                level,
                message,
                instance
            };
        });

    return NextResponse.json(errors);
  } catch (error) {
    console.error('Error reading error log:', error);
    return NextResponse.json({ error: 'Failed to read error log' }, { status: 500 });
  }
}