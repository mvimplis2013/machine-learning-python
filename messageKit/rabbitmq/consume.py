"""
Basic Message Consumer Example
"""
import argparse

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

	parser = argparse.ArgumentParser( description='Arguments for RabbitMQ Basic Message Consumer' )

	# Credentials
	parser.add_argument( '-u', '--user', required=True, type=str, help='Username for RabbitMQ Connection', default='tandem' )
	parser.add_argument( '-p', '--password', required=True, type=str, help='Password for RabbitMQ Connection' )
	
	# Location
	parser.add_argument( '-h', '--host', required=True, type=str, help='RabbitMQ Server IP-Address')
	parser.add_argument( '-p', '--port', required=False, type=int, help='RabbitMQ Server AMQP-Port', default=5672 )

	args = parser.parse_args()

	LOGGER.info("Delivery properties: %s / %s", args.user, args.password)

	return