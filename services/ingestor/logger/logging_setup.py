import logging
from pathlib import Path

log_dir = Path("/app/logs/ingestor")
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'ingestor.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def setup_logging():
    logging.basicConfig(
    filename=log_dir / 'ingestor.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)