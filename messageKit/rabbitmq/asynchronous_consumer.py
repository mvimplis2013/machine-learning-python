import logging
import argparse

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class ExampleConsumer(object):
	def __init__(self):
		return

class ReconnectingExampleConsumer(object):
	def __init__(self):
		print("This is a consumer that will try to reconnect if nested connection is lost")

		self._consumer = ExampleConsumer()

		return

	def connect(self):
		"""
		This method connects to RabbitMQ, returning the connection handle.
		When the connection is established, the on_connection_open method will be invoked by pika.

		:rtype: pika.SelectConnection
		"""

		return pika.SelectConnection()
		
	def run(self):
		"""
		Run the ExampleConsumer by connecting to RabbitMQ and then starting the IOLoop to block.
		"""
		self.connection = self.connect()
		self._connection.ioloop.start()


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
	
	consumer = ReconnectingExampleConsumer()

# ******  ENTRYPOINT ******
if __name__ == '__main__':
	print("Inside __MAIN__")

	asynchronous_consumer_main()