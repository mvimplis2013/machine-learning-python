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

	asynchronous_consumer_main()