import logging
import asyncio
from monitor.monitor import Monitor

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s|[%(levelname)s]|%(asctime)s|%(message)s',
    handlers=[
        logging.FileHandler("logs/monitor.log"),
        logging.StreamHandler()
    ]
)

if __name__=="__main__":
    asyncio.run(Monitor().start())
