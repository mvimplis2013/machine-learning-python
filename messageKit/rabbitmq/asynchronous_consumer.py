import logging
import argparse

import pika
from pika.exchange_type import ExchangeType

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class ExampleConsumer(object):
	"""
	This is an example consumer that will handle unexpected interactions with RabbitMQ such as channel and
	connection closure.

	If RabbitMQ closes the connection, thi class will stop and indicate that reconnection is necessary. 
	You should look at the output, as there are limited reasons why the connection may be closed.
	"""
	EXCHANGE = "message"
	EXCHANGE_TYPE=ExchangeType.topic
	QUEUE = 'text'
	ROUTING_KEY = 'example.text'

	def __init__(self, amqp_url):
		"""
		Create a new instance of the consumer class, passing it the AMQP URL used to connect to RabbitMQ.
		
		:param str amqp_url: The AMQP URL to connect with RabbitMQ
		"""
		self.should_reconnect = False
		self.was_consuming = False 

		self._connection = None
		self._channel = None

		self._closing = False
		self._consumer_tag = None
		self._consuming = False 
		self._url = amqp_url

		# In Production, experiment with higher prefetch values for higher consumer throughput
		self._prefetch_count = 1

		return

	def connect(self):
		"""
		This method connects to RabbitMQ, returning the connection handle.
		When the connection is established, the on_connection_open method will be invoked by pika.

		rtype: pika.SelectConnection
		"""

		LOGGER.info("Connection to %s", self._url)

		return pika.SelectConnection(
		)

	def run(self):
		"""
		Run the ExampleConsumer by connecting to RabbitMQ and then starting the IOLoop to block and 
		allow the SelectedConnection to operate.
		"""		

class ReconnectingExampleConsumer(object):
	def __init__(self, amqp_url):
		print("This is a consumer that will try to reconnect if nested connection is lost")

		self._reconnect_delay = 0 

		self._amqp_url = amqp_url

		self._consumer = ExampleConsumer(self._amqp_url)

		return

	def _maybe_reconnect(self):
	"""
	"""
		if self._consumer.should_reconnect:
			self._consumer.stop()
			reconnect_delay = self._get_reconnect_delay()

			LOGGER.info("Reconnecting after %d seconds", reconnect_delay)
			time.sleep(reconnect_delay)

			self._consumer = ExampleConsumer(self._amqp_url)

		return

	def connect(self):
		"""
		This method connects to RabbitMQ, returning the connection handle.
		When the connection is established, the on_connection_open method will be invoked by pika.

		:rtype: pika.SelectConnection
		"""

		return pika.SelectConnection()

	def run(self):
		while True:
			try:
				self._consumer.run()
			except KeyboardInterrupt:
				self._consumer.stop()
				break

			self._maybe_reconnect()

def asynchronous_consumer_main():
	print("! Inside main() !")

	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

	parser = argparse.ArgumentParser( description='Arguments for Asynchronous RabbitMQ Basic Message Consumer' )

	# Credentials
	parser.add_argument( '-u', '--user', required=True, type=str, help='Username for RabbitMQ Connection', default='tandem' )
	parser.add_argument( '-p', '--password', required=True, type=str, help='Password for RabbitMQ Connection' )
	
	# Location
	parser.add_argument( '--host', required=True, type=str, help='RabbitMQ Server IP-Address')
	parser.add_argument( '--port', required=False, type=int, help='RabbitMQ Server AMQP-Port', default=5672 )

	args = parser.parse_args()

	amqp_url = f'amqp://{args.user}:{args.password}@{args.host}:{args.port}/%2F'
	LOGGER.info(amqp_url)
	#print( args.user )
	
	example_consumer = ReconnectingExampleConsumer(amqp_url)
	example_consumer.run()

# ******  ENTRYPOINT ******
if __name__ == '__main__':
	print("Inside __MAIN__")

	asynchronous_consumer_main()