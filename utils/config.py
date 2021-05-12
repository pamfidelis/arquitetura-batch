import logging
import os.path

import yaml
import sys

logger = logging.getLogger(__name__)

def load_config():
    try:
        with open(os.path.abspath('config/config.yaml')) as file:
            return yaml.safe_load(file)
    except IOError as e:
            logger.exception(f"I/O error({e.errno}): {e.strerror}")
            raise e
    except: 
        logger.exception(f"Unexpected error: {sys.exc_info()[0]}")