"""
Basic Message Consumer Example
"""

import functools
import logging
import pika
from pika.exchange_type import ExchangeType

LOG_FORMAT = (("%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s"))
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def main():
	"""Main Method"""

	print("*******************************************")
	print("*** Basic Message Consumer for RabbitMQ ***")
	print("*******************************************")

	LOGGER.info("Delivery properties: %s", "@DUMMY@")
	return