import logging

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

def main():
	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

	LOGGER.info("Ready to Start the ASYNCHRONOUS_PUBLISHER to RabbitMQ !")

	example = ExamplePublisher(
		"amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
		)

	example.run()

