import logging
from utils.config import logs_dir
import os

log_file = os.path.join(logs_dir, 'runtime.log')

"""logger functionas"""
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
