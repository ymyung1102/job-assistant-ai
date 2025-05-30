# main.py
import logging
from app.handler.handler import app
from app.utils.setup_logging import setup_logging

logger = logging.getLogger('main')

if __name__ == '__main__':
    setup_logging()
    logger.info('Starting Job Assistant AI')
    app.run(host="0.0.0.0", port=5000, debug=True)
