import logging
import logging.config
import os
import yaml

logger = logging.getLogger('setup_logging')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_CONFIG_PATH = os.path.join(BASE_DIR, 'resources', 'logging.yml')

def setup_logging():
    """
    Sets up logging configuration from a YAML config file.

    Ensures the logs directory exists and applies the configuration.
    Logs an error if setup fails.
    """
    try:
        with open(LOG_CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f.read())
            os.makedirs('./logs', exist_ok=True)
            logging.config.dictConfig(config)
            logger.debug('setup done for logging')
    except Exception as e:
        logger.error(e)