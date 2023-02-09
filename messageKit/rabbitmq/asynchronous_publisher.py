import logging

import pika
from pika.exchange_type import ExchangeType

import functools

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
			on_open_callback=self.on_connection_open,
			on_open_error_callback=self.on_connection_open_error,
			on_close_callback=self.on_connection_closed
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

	def on_connection_open_error(self, _unused_connection, err):
		"""
		This method is called by pika if the connection to RabbitMQ cannot be established.

		:param pika.SelectConnection _unused_connection: The connection
		:param Exception err: The error
		"""

		LOGGER.error("Connection open failed, reopening in 5 seconds: %s", err)

		self._connection.ioloop.call_later(5, self.ioloop.stop)

		return

	def on_connection_closed(self, _unused_connection, reason):
		"""
		This method is invoked by pika when the connection to RabbitMQ is closed unexpectedly.
		We will try to reconnect.
		"""

		self._channel = None

		if self._stopping:
			self._connection.ioloop.stop()
		else:
			LOGGER.warning("Connection is closed, reopening in 5 seconds: %s", reason)

			self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

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

	def on_channel_open(self, channel):
		"""
		This method is invoked by pika when the channel has been opened.
		The channel object is passed in so we can make use of it.

		:param pika.channel.Channel: The channel object
		"""
		LOGGER.info("Channel is Opened !")

		self._channel = channel

		self.add_on_channel_close_callback()

		self.setup_exchange(self.EXCHANGE)

		return

	def add_on_channel_close_callback(self):
		"""
		This method tells pika to call the on_channel_closed method if RabbitMQ unexpectedly closes the channel.
		"""
		LOGGER.info("Adding channel close callback ...")

		self._channel.add_on_close_callback(self.on_channel_closed)

		return

	def on_channel_closed(self, channel, reason):
		"""
		Invoked by pika when RabbitMQ unexpectedly closes the channel.
		Channels are usually closed if you attempt to do something that violates the protocol.

		In this case, we will close the connection to shutdown the object.
		
		:param pika.channel.Channel: The closed channel object
		:param Exception reason: reason for loosing connection
		"""
		self._channel = None

		if self._stopping:
			self._connection.ioloop.stop()
		else:
			LOGGER.warning(f"Connection is closed, reopening in 5 seconds: {reason}")

			self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

		return

	def setup_exchange(self, exchange_name):
		"""
		Setup the exchange on RabbitMQ by invoking the ExchangeDeclare command.
		When it is COMPLETE, the ON_EXCHANGE_DECLAREOK method will be invoked by pika.
		
		:param str|unicode exchange_name: The nane of the exchange to declare
		"""

		LOGGER.info("Declaring exchange %s", exchange_name)

		# Using functools.partial is NOT required
		# It is demonstrating how arbitrary data can be passed to the callback when it is called.
		cb = functools.partial(self.on_exchange_declareok, userdata=exchange_name)

		self._channel.exchange_declare(exchange=exchange_name,
			exchange_type=self.EXCHANGE_TYPE, callback=cb)

		return

	def on_exchange_declareok(self, _unused_frame, userdata):
		"""
		Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC command.

		:param pika.Frame.Method unused_frame: Exchange.DelareOK response frame
		:param str|unicode userdata: Extra user data (exchange name)
		"""
		LOGGER.info("Exchange declare %s", userdata)

		self.setup_queue(self.QUEUE)

		return

	def setup_queue(self, queue_name):
		"""
		Setup the queue on RabbitMQ by invoking the Queue.Declare rpc-command.
		"""
		LOGGER.info("Declaring queue %s", queue_name)

		self._channel.queue_declare(queue=queue_name, callback=self.on_queue_declareok) 

	def on_queue_declareok(self, _unused_frame):
		"""
		Method invoked by pika when the Queue.Declare rpc-method is completed. 
		In this method we will bind the queue and exchange together with the routing-key by issuing the Queue.Bind

		When this command is complete, the on_bindok method will be invoked by pika.

		:param pika.frame.Method method_frame
		"""

		LOGGER.info('Binding %s to %s with %s', self.EXCHANGE, self.QUEUE, self.ROUTING_KEY)

		self._channel.queue_bind(self.QUEUE, self.EXCHANGE, routing_key=self.ROUTING_KEY,
			callback=self.on_bindok)

		return

	def on_bindok(self, _unused_frame):
		"""
		This method is invoked by pika when it recieves the Queue.BindON response from RabbitMQ.

		Since we are now setup and bound, it is time to start publishing.
		"""
		LOGGER.info("Queue is bound !")

		self.start_publishing()

	def start_publishing(self):
		"""
		This method will enable delivery confirmations and schedule the first message to be sent to RabbitMQ
		"""
		LOGGER.info("Issuing Consumer related RPC commands")

		self.enable_delivery_confirmations()

		self.schedule_next_message()

		return

	def enable_delivery_confirmations(self):
		"""
		Send the Confirm.Select rpc-method to RabbitMQ to enable delivery confirmations on the channel.
		The only way to turn this off is to close the channel and create a new one.

		When the message is confirmed from RabbitMQ, the on_delivery_confirmation method will be invoked 
		passing in a Basic.Ack or Basic.Nack method from RabbitMQ that will indicate which messages it is 
		confirming or rejecting.
		"""

		LOGGER.info("Issuing Confirm.Select RPC command")

		self._channel.confirm_delivery(self.on_delivery_confirmation)
    
	def on_delivery_confirmation(self, method_frame):
		"""
		Invoked by pika when RabbitMQ responds to a Basic.Publish RPC command ==>
		Passing in either a Basic.Ack or Basic.Nack frame With the delivery tag of the message that was published.

		The delivery tag is an integer counter indicating the message number that was sent on the channel via Basic.

		Here we are just doing house keeping to keep track of stats and remove message numbers from the list of pending.

		:param pika.frame.Method  method_frame: Basic.Ack or Basic.Nack frame
		"""  

		confirmation_type = method_frame.method.NAME.split('.')[1].lower()
		ack_multiple = method_frame.method.multiple
		delivery_tag = method_frame.method.delivery_tag

		LOGGER.info("Received %s for delivery tag: %d (multiple: %s)", confirmation_type, delivery_tag, ack_multiple)
		if confirmation_type == 'ack':
			self._acked += 1
		elif confirmation_type == 'nack':
			self._nacked += 1

		del delf._deliveries[delivery_tag]


		if ack_multiple:
			for tmp_tag in list(self._deliveries.keys()):
				if tmp_tag <= delivery_tag:
					self._acked += 1
					del self._deliveries[tmp_tag]

		"""
		NOTE: at some point you would check self._deliveries for stale entries and decide to attempt re-delivery
		"""

		LOGGER.info(
			"Published %i messages/ %i have yet to be confirmed/ %i were acked and %i were nacked",
			len(self._deliveries), self._acked, self._nacked
			)

		return

	def schedule_next_message(self):
		"""
		If we are not closing our connection to RabbitMQ, schedule another message to be delivered 
		in PUBLISH_INTERVAL seconds.
		"""

		LOGGER.info("Scheduling Next Message for %0.1f seconds.", self.PUBLISH_INTERVAL)

		self._connection.ioloop.call_later(self.PUBLISH_INTERVAL, self.publish_message)

		return 

	def publish_message(self):
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

