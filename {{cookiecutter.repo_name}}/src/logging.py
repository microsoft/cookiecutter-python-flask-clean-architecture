import logging.config

from flask import request

from src.domain import LOG_LEVEL


def setup_logging(app):
    log_level = app.config.get(LOG_LEVEL)
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': log_level,
                'propagate': False
            },
        }
    }

    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s %s %s %s %s",
            request.method,
            request.path,
            response.status,
            request.referrer,
            request.user_agent,
        )
        return response

    logging.config.dictConfig(logging_config)
    return app
