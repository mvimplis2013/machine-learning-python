import argparse
import os
import pika
import redis

USER = "user"

def call_mq_server( host, password ):
	print(f"Ready to Start Sending Messages with RabbitMQ")

	try:
		#conn_params = pika.ConnectionParameters('amqp://www-data:rabbit_pwd@rabbit1/web_messages')
		#conn_params = pika.ConnectionParameters('amqp://user:@10.109.109.116:5672/%2F')

		credentials = pika.PlainCredentials( USER, password )
		conn_params = pika.ConnectionParameters( host, credentials=credentials )

		print(f"Connection String ... {conn_params}")

		connection = pika.BlockingConnection( conn_params )

		channel = connection.channel()

		channel.queue_declare(queue='hello')

		channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
		
		print(" [x] Sent 'Hello World!'")

		connection.close()

	except pika.exceptions.AMQPConnectionError as pika_e:
		print(f"Failed to Connect to RabbitMQ ... {pika_e}")
		return

	return

def follow_mq_server( host, password ):
	credentials = pika.PlainCredentials( USER, password )
	conn_params = pika.ConnectionParameters( host, credentials=credentials )

	print(f"Connection String ... {conn_params}")

	connection = pika.BlockingConnection( conn_params )

	channel = connection.channel()
	channel.queue_declare(queue='hello')

	def callback( ch, method, properties, body ):
		print(f"Recieved ... {body}")

	channel.basic_consume( queue='hello', on_message_callback=callback, auto_ack=True)

	print( f"Waiting for Messages" )

	channel.start_consuming()

	return
def call_redis_to_communicate():
	print(f"Using Redis to Send Messages")

def __main_mq_client__():
	print(f"Ready to Handle a Message ... {redis.__version__}")

	parser = argparse.ArgumentParser( description='Handle Messages Between MicroServices' )

	parser.add_argument( '-a', '--action', choices=['sent', 'receive', 'delete'], help='action for backend message-queue service', default='sent' )

	parser.add_argument( '-n', '--name', required=False, type=str, help='message-queue name', default="Message-Queue-VIBM" )
	parser.add_argument( '-p', '--port', required=False, type=int, help='listen-port', default=5672 )

	args = parser.parse_args()

	if args.action == "sent":
		print( f"SEND-Action {args.name}, {args.port}" )
	elif args.action == "receive":
		print( f"{args.name}, {args.port}, {args.action}" )
	elif args.action == "delete":
		print( f"{args.action} , {args.name}" )

	# Read Environment Variables Associated with Message-Queue Service
	try:
		mq_type = os.environ['MESSAGE_QUEUE_TYPE']

		host_port = os.environ[ "LISTENING_SERVICE" ].split(":")
		host = host_port[0]
		port = host_port[1]

		userpass = os.environ[ "USERNAME_PASSWORD" ].split("/")
		user = userpass[0]
		password = userpass[1] 
	except KeyError as e:
		print( f"Problem Reading Environment Variables for Message-Queue ... {e}" )
		return

	print( f"Listening Service = {host} && Credentials = {pass}" )
	#return

	if mq_type.casefold() == "rabbitmq".casefold():	
		call_mq_server( host , password )
	elif mq_type.casefold() == "REDIS".casefold():
		call_redis_to_communicate()
	elif mq_type.casefold() == "receive".casefold():
		try:
			follow_mq_server()
		except KeyboardInterrupt:
			return

	return