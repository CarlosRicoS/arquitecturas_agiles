import asyncio
import logging

from detector import Detector

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s|[%(levelname)s]|%(asctime)s|%(message)s',
    handlers=[
        logging.FileHandler("logs/monitor.log", mode="w"),
        logging.StreamHandler()
    ]
)

if __name__=="__main__":
    asyncio.run(Detector().start())