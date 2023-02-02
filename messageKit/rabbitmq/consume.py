"""
Basic Message Consumer Example
"""

import functools
import logging
import pika
from pika.exchange_type import ExchangeType

LOG_FORMAT = (("%(levelname)"))
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

 
def main():
	"""Main Method"""

	print("Basic Message Consumer for RabbitMQ")

	return