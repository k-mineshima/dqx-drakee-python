from config.config import logging_config
from config.application import environment

config = logging_config[environment]
levels = config['level']
output = config['output']

config_dict = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': levels['console'],
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'timed_rotating_file': {
            'level': levels['timed_rotating_file'],
            'formatter': 'standard',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/logger.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 30
        }
    },
    'root': {
        'handlers': output,
        'level': 'INFO'
    }
}
