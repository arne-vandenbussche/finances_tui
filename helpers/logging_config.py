# -*- coding: utf-8 -*-
import logging.config

# define a dictionary with our logging settings
# we will reuse this configuration throughout our application
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            },
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'financial.log',
            'mode': 'a',
            }
        },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
        },
    
    }

logging.config.dictConfig(LOGGING)