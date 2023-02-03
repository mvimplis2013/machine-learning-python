import logging
import argparse

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(function) -35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class ExampleConsumer(object):
	def __init__(self):
		return

class ReconnectingExampleConsumer(object):
	def __init__(self):
		print("This is a consumer that will try to reconnect if nested connection is lost")

		self._consumer = ExampleConsumer()

		return

def asynchronous_consumer_main():
	print("! Inside main() !")

	consumer = ReconnectingExampleConsumer()

# ******  ENTRYPOINT ******
if __name__ == '__main__':
	print("Inside __MAIN__")

	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

	parser = argparse.ArgumentParser( description='Arguments for Asynchronous RabbitMQ Basic Message Consumer' )

	# Credentials
	parser.add_argument( '-u', '--user', required=True, type=str, help='Username for RabbitMQ Connection', default='tandem' )
	parser.add_argument( '-p', '--password', required=True, type=str, help='Password for RabbitMQ Connection' )
	
	# Location
	parser.add_argument( '--host', required=True, type=str, help='RabbitMQ Server IP-Address')
	parser.add_argument( '--port', required=False, type=int, help='RabbitMQ Server AMQP-Port', default=5672 )

	args = parser.parse_args()
	
	amqp_url = 'amqp://guest:guest@localhost:5672/%2F'

	asynchronous_consumer_main()