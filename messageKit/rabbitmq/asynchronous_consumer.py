import functools

import logging
import argparse

import time

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
			parameters = pika.URLParameters(self._url),
			on_open_callback=self.on_connection_open,
			on_open_error_callback=self.on_connection_open_error,
			on_close_callback=self.on_connection_closed
		)

		return

	def on_connection_open(self, _unused_connection):
		"""
		This method is called by pika if the connection to RabbitMQ
		has been established.

		:param pika.SelectConnection _unused_connection: The connection
		"""

		LOGGER.info("Connection is opened")

		self.open_channel()

		return

	def open_channel(self):
		"""
		Open a new channel with RabbitMQ by issuing the Channel.Open command.
		When RabbitMQ responds that the channel is open, the on_channel_open callback will be invoked by pika.
		"""

		LOGGER.info("Creating a New Channel")

		self._connection.channel(on_open_callback=self.on_channel_open)

		return

	def on_channel_open(self, channel):
		"""
		This method is invoked by pika when the channel has been opened.
		The channel object is passedin so we can make use of it.

		Since the channel is now open, we will declare the exchange to use.

		:param pika.channel.Channel channel: The channel object
		"""

		LOGGER.info('Channel is Open !')

		self._channel = channel

		self.add_on_channel_close_callback()
		self.setup_exchange(self.EXCHANGE)

		return

	def add_on_channel_close_callback(self):
		"""
		This method tells pika to call the on_channel_closed method if 
		RabbitMQ unexpectedly closes the channel.

		:param pika.channel.Channel channel: The channel object
		"""
		LOGGER.info("Adding channel close callback")

		self._channel.add_on_close_callback(self.on_channel_closed)

		return

	def on_channel_closed(self, channel, reason):
		"""
		Invoked by pika when RabbitMQ unexpectedly closes the channel.
		Channels are usually closed if you attempt to do something that 
		violates the protocol, such as re-declare an exchange or queue with 
		different parameters. In this case we will close the connection to 
		shutdown the object.

		:param pika.channel.Channel channel: The closed channel
		:param Exception reason: Why the channel was closed
		"""
		LOGGER.warning("Channel %i was closed: %s", channel, reason)

		self.close_connection()

		return

	def close_connection(self):
		self._consuming = False

		if self._connection.is_closing or self._connection.is_closed:
			LOGGER.info("Connection is closing or already closed")
		else:
			LOGGER.info("Closing Connection")

			self._connection.close()

		return

	def on_connection_open_error(self):
		return

	def on_connection_closed(self, _unused_connection, reason):
		"""
		This method is invokedby pika when the connection to RabbitMQ is closed unexpectedly.
		Since it is unexpected, we will try to reconnect to RabbitMQ.

		:param pika.connection.Connection connection: The closed connection obj
		:param Exception reason: exception representing reason for loss of connection
		"""

		self._channel = None 

		if self._closing:
			self._connection.ioloop.stop()
		else:
			LOGGER.warning("Connection is closed, reconnect is necessary: %s", reason)

			self.reconnect()

		return

	def setup_exchange(self, exchange_name):
		"""
		Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC command.
		When it is complete, the on_exchange_declareok method will be invoked by pika.

		:param str|unicode exchange_name: The name of EXCHANGE to declare
		"""
		LOGGER.info(f"Declaring Exchange: {exchange_name}")

		cb = functools.partial(
			self.on_exchange_declareok, userdata=exchange_name)

		self._channel.exchange_declare(
			exchange=exchange_name,
			exchange_type=self.EXCHANGE_TYPE,
			callback=cb)

		return

	def on_exchange_declareok(self, _unused_frame, userdata):
		LOGGER.info(f"Exchange declared: {userdata}")

		self.setup_queue(self.QUEUE)

		return

	def setup_queue(self, queue_name):
		LOGGER.info(f"Declaring Queue: {queue_name}")

		cb = functools.partial(self.on_queue_declareok, userdata=queue_name)

		self._channel.queue_declare(queue=queue_name, callback=cb)

		return

	def on_queue_declareok(self, _unused_frame, userdata):
		queue_name = userdata

		LOGGER.info(f"Binding {self.EXCHANGE} to {queue_name} with {self.ROUTING_KEY}")

		cb = functools.partial(self.on_bindok, userdata=queue_name)

		self._channel.queue_bind(
			queue_name,
			self.EXCHANGE,
			routing_key=self.ROUTING_KEY,
			callback=cb)

		return

	def on_bindok(self, _unused_frame, userdata):
		LOGGER.info(f"Queue Bound: {userdata}")

		self.set_qos()

		return

	def set_qos(self):

		self._channel.basic_qos(
			prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

		return

	def on_basic_qos_ok(self, _unused_frame):
		LOGGER.info(f"QOS set to: {self._prefetch_count}")

		self.start_consuming()

		return

	def start_consuming(self):
		LOGGER.info("Issuing consumer")

		self._consumer_tag = self._channel.basic_consume(
			self.QUEUE, self.on_message)

		return

	def on_message(self, _unused_channel, basic_deliver, properties, body):
		LOGGER.info(f"Received Message #{basic_deliver.delivery_tag} from {properties.app_id} : {body}")

		return
		
	def reconnect(self):
		"""
		Will be invoked if the connection is lost. Indicates that a reconnection is necessary and stops the ioloop
		"""

		self.should_reconnect = True 

		self.stop() 

		return

	def run(self):
		"""
		Run the ExampleConsumer by connecting to RabbitMQ and then starting the IOLoop to block and 
		allow the SelectedConnection to operate.
		"""		
		# LOGGER.debug(f"Try to Connect to RabbitMQ and then Start the IOLoop to Block Code Execution ... {self._url}")

		self._connection = self.connect()
		self._connection.ioloop.start()

	def stop(self):
		"""
		Cleanly shutdown the connection to RabbitMQ by stopping the consumer with RabbitMQ.
		When RabbitMQ confirms the cancellation, on_cancelok will be invoked by pika, 
		which will then close the channel and connection.
		This method is invoked when CTRL-C is pressed raising a KeyboardInterrupt Exception.
		"""
		if not self._closing:
			self._closing = True 
			LOGGER.info("Stopping")
			if self._consuming:
				self.stop_consuming()
				self._connection.ioloop.start()
			else:
				self._connection.ioloop.stop()

			LOGGER.info("Stopped !")

		return

class ReconnectingExampleConsumer(object):
	def __init__(self, amqp_url):
		print("This is a consumer that will try to reconnect if nested connection is lost")

		self._reconnect_delay = 0 

		self._amqp_url = amqp_url

		self._consumer = ExampleConsumer(self._amqp_url)

		return

	def _maybe_reconnect(self):
		"""
		Try to reconnect after XX seconds.
		"""
		if self._consumer.should_reconnect:
			self._consumer.stop()
			reconnect_delay = self._get_reconnect_delay()

			LOGGER.info("Reconnecting after %d seconds", reconnect_delay)
			time.sleep(reconnect_delay)

			self._consumer = ExampleConsumer(self._amqp_url)

		return

	def _get_reconnect_delay(self):
		if self._consumer.was_consuming:
			self._reconnect_delay = 0
		else:
			self._reconnect_delay += 1

		if self._reconnect_delay > 30:
			self._reconnect_delay = 30

		return self._reconnect_delay

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
	
	#example_consumer = ReconnectingExampleConsumer(amqp_url)
	#example_consumer.run()

# ******  ENTRYPOINT ******
if __name__ == '__main__':
	print("Inside __MAIN__")

	asynchronous_consumer_main()