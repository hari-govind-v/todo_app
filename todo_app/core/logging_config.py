import logging
from .context_vars import *

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True

def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(levelname)s request_id=%(request_id)s %(message)s"
    )

    handler.setFormatter(formatter)

    handler.addFilter(RequestIdFilter())
    logger.addHandler(handler)