import logging
import asyncio
from monitor.monitor import Monitor

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s|[%(levelname)s]|%(asctime)s|%(message)s',
    handlers=[
        logging.FileHandler("logs/monitor.log", mode="w"),
        logging.StreamHandler()
    ]
)

# Set pika logger to WARNING level to suppress INFO logs
logging.getLogger("pika").setLevel(logging.WARNING)

if __name__=="__main__":
    asyncio.run(Monitor().start())
