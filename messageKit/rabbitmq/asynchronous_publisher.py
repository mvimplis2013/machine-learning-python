import logging

import pika
from pika.exchange_type import ExchangeType

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class ExamplePublisher(object):
	"""
	This is an example publisher that will handle unexpected interactions with RabbitMQ
	such as channel and connection closures.

	If RabbitMQ closes the connection, it will reopen it. You should look at the output
	as there are limited reasons why the connection may be closed.

	It uses delivery confirmations and illustrates one way to keep track of messages
	that have been sent and if they have been confirmed by RabbitMQ.
	"""
	EXCHANGE = "message"
	EXCHANGE_TYPE = ExchangeType.topic
	PUBLISH_INTERVAL = 1
	QUEUE = 'text'
	ROUTING_KEY = 'example.text'

	def __init__(self, amqp_url):
		"""
		Setup the example-publisher object, passing in the URL we will use to connect to RabbitMQ
		""" 
	
		self._connection = None
		self._channel = None 
		self._url = amqp_url

		self._stopping = False
		self._url = amqp_url

	def connect(self):
		"""
		This method connects to RabbitMQ and returns the connection handle.
		When the connection is established, the on_connection_open method will be invoked by pika.

		:rtype pika.SelectConnection 
		"""
		LOGGER.info(f"Connecting to {self._url}")

		return pika.SelectConnection(
			pika.URLParameters(self._url),
			on_open_callback=self.on_connection_open
			)

	def on_connection_open(self, _unused_connection):
		"""
		This method is called by pika once the connection to RabbitMQ has been established.
		It passes the handle to the connection object in case we need it. 

		:param pika.SelectConnection _unused_connection: The connection
		"""
		LOGGER.info("Connection Opened !")

		self.open_channel()

		return

	def open_channel(self):
		"""
		This method will open a new channel with RabbitMQ by issuing the open() RPC command.
		When RabbitMQ confirms that the channel is open, the on_channel_open() method will be invoked.
		
		Since the channel is now open, we will declare the EXCHANGE to use.

		:param pika.channel.Channel channel: The channel object

		"""

		LOGGER.info("Creating a New Channe ...")

		self._connection.channel(on_open_callback=self.on_channel_open)

		return
		
	def run(self):
		"""
		Run the example code by connecting and then starting the IOLoop.
		"""
		while not self._stopping:
			self._connection = None
			self._deliveries = {}
			self._acked = 0
			self._nacked = 0
			self._message_number = 0

			try:
				self._connection = self.connect()
				self._connection.ioloop.start()
			except KeyboardInterrupt:
				self.stop()

				if (self._connection is not None and not self._connection.is_closed):
					self._connection.ioloop.start()

		LOGGER.info('Stopped !')

	def stop(self):
		"""
		Stop the example by closing the channel and connection. 
		"""

		LOGGER.info("Stopping ...")

		self._stopping = True

		self.close_channel()
		self.close_connection()

	def close_channel(self):
		"""
		Invoke this method to close the channel with RabbitMQ.
		"""
		if self._channel is not None:
			LOGGER.info("Closing the Channel !")
			self._channel.close()

		return

	def close_connection(self):
		"""
		This method closes the connection to RabbitMQ.
		"""
		if self._connection is not None:
			LOGGER.info("Closing Connection !")
			self._connection.close()

		return

def main():
	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

	LOGGER.info("Ready to Start the ASYNCHRONOUS_PUBLISHER to RabbitMQ !")

	example = ExamplePublisher(
		"amqp://tandem:tandem123@10.244.84.166:5672/%2F?connection_attempts=3&heartbeat=3600"
		)

	example.run()

