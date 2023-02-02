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
	parser.add_argument( '--host', required=True, type=str, help='RabbitMQ Server IP-Address')
	parser.add_argument( '--port', required=False, type=int, help='RabbitMQ Server AMQP-Port', default=5672 )

	args = parser.parse_args()

	#LOGGER.info("Delivery properties: %s / %s", args.user, args.password)

	credentials = pika.PlainCredentials( args.user, args.password )

	parameters = pika.ConnectionParameters( host=args.host, port=args.port, credentials=credentials )

	pika.BlockingConnection(parameters)

	channel = connection.channel()

	channel.exchange_declare(
		exchange='test_exchange',
		exchange_type=ExchangeType.direct,
		passive=False,
		durable=False,
		auto_delete=False)

	channel.queue_declare(
		queue='standard',
		auto_delete=True)

	channel.queue_bind(
		queue='standard',
		exchange='test_exchange',
		routing_key='standard_key')

	channel.basic_qos(prefetch_count=1)

	on_message_callback = functools.partial(
		on_message, userdata='on_message_userdata')

	channel.basic_consume('standard', on_message_callback)

	try:
		channel.start_consuming()
	except KeyboardInterrupt:
		channel.stop_consuming()

	connection.close()
	
	return