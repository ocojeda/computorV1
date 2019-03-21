import logging


logger = logging.getLogger(__file__)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s :: %(message)s", "%H:%M:%S"))

logger.addHandler(handler)
