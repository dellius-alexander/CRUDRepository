import json
import os
import logging.config
import logging
from src.__config__ import log_config

# Load the logging configuration
try:
    # check if logging.json has been loaded
    ROOT_DIR = os.getenv("ROOT_DIR")
    LOG_DIR = os.getenv("LOG_DIR")
    if len(logging.root.handlers) == 0:
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        data = json.loads(json.dumps(log_config))
        # read initial config file
        logging.config.dictConfig(config=data)
        # Update globals with new logger
        globals().update(locals())
except Exception as e:
    logging.error(f"An error occurred: {e}")
    exit(1)


def get_logger(name: str, level: int = logging.INFO):
    logging.addLevelName(levelName=logging.getLevelName(level), level=level)
    return logging.getLogger(name)
