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

def call_rabbit_broker( host, port, username, password ):
	print( f"Inside RabbitMQ Client .. using pika vers {pika.__version__}" )

	credentials = pika.PlainCredentials( username, password )
	conn_params = pika.ConnectionParameters( host=host, port=port, credentials=credentials )

	print(f"Connection String ... {conn_params} && {credentials}")

	connection = pika.BlockingConnection( conn_params )

	channel = connection.channel()
	#channel.queue_declare(queue='hello')

	#def callback( ch, method, properties, body ):
		#print(f"Recieved ... {body}")

	#channel.basic_consume( queue='hello', on_message_callback=callback, auto_ack=True)

	#print( f"Waiting for Messages" )

	channel.basic_publish(exchange='test', routing_key='test', body=b'Test Message')
	connection.close()

	#channel.start_consuming()

	return

def call_redis_to_communicate( host, port, username, password ):
	print( f"Using Redis to Send Messages ... Python-Client ver. {redis.__version__}" )
	#return

	#r = redis.Redis(host=host, port=port, username=username, password=password)
	#r = redis.Redis(host=host, port=port, username="redis", password=password)
	#r = redis.Redis(host=host, port=port, username="redis", password="")

    # It works with user.auth=FALSE 
	r = redis.Redis(host=host, port=port, socket_timeout=4, socket_connect_timeout=4)
	#return

	try:
		r.ping()
	except Exception as ex:
		print(f"{ex}")

	return


def __main_mq_client__():
	print(f"Ready to Handle a Message !!!")

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

		print(f"Message Queue Type ... {mq_type}")

		host_port = os.environ[ "LISTENING_SERVICE" ].split(":")
		host = host_port[0]
		if len(host_port) == 1:
			port = 6379
		else:
			port = host_port[1]

		userpass = os.environ[ "USERNAME_PASSWORD" ].split("/")
		username = userpass[0]
		password = userpass[1] 
	except KeyError as e:
		print( f"Problem Reading Environment Variables for Message-Queue ... {e}" )
		return

	print( f"Listening Service = {host} && Credentials = {password}" )
	#return

	if mq_type.casefold() == "rabbitmq".casefold():	
		call_rabbit_broker( host , port, username, password )
	elif mq_type.casefold() == "REDIS".casefold():
		print(f"Need to Contact REDIS message queue")
		#return

		call_redis_to_communicate(host, port, username, password)
		return
	#elif mq_type.casefold() == "receive".casefold():
	#	try:
	#		follow_mq_server()
	#	except KeyboardInterrupt:
	#		return

	return