import logging

LOG_FORMAT = (%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s)
LOGGER = logging.getLogger(__name__)

def main():
	logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

	logging.INFO("Ready to Start the ASYNCHRONOUS_PUBLISHER to RabbitMQ !")

