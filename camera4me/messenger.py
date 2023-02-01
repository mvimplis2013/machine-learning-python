import argparse
import os

import pika
from pika import DeliveryMode
from pika.exchange_type import ExchangeType 

import redis

import logging

logging.basicConfig(level=logging.DEBUG)

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

def basic_msg_publisher(connection, topic, channel):
	"""
	Basic Message Publisher
	"""
	print( "***********************************************************************************************" )
	print( "** RabbitMQ is a message broker ... It accepts messages from publishers, routes them and ... **" )
	print( "**  [x] IF THERE WERE QUEUES to route to ==> stores them for consumption                     **" )
	print( "**  [x] Otherwise ==> Immediately delivers to consumers if any                               **" )
	print( "***********************************************************************************************" ) 
	
	#channel.queue_declare(queue='hello')

	#def callback( ch, method, properties, body ):
	#print(f"Recieved ... {body}")

	#channel.basic_consume( queue='hello', on_message_callback=callback, auto_ack=True)

	#print( f"Waiting for Messages" )

	# The application that publishes (produces) messages.
	# Another application or insytance consumes messages at the same time.
	print( "Sending Message to Create Group-Queue" )
	channel.basic_publish(
		topic, 
		'test',
        'queue:group',
		pika.BasicProperties(
			content_type='text/plain',
			delivery_mode=DeliveryMode.Transient
			)
		)

	connection.sleep(5)

	print( "Sending Text Message to Queue:Group" )
	channel.basic_publish(
		topic,
		"group---key",
		"Message to group---key",
		pika.BasicProperties(
            content_type='text/plain',
			delivery_mode=DeliveryMode.Transient
			)
		)
	
	connection.sleep(5)

	print("Sending Text Message")
	channel.basic_publish(
		topic,
		'standard_key',
		'Message to STANDARD key')

	connection.close()

	print("Succesfully Published a Basic Message !")

	#channel.start_consuming()

	return

def basic_msg_consumer(topic, channel):
	"""
	Basic Message Consumer
	"""

	print(f"Ready to start consuming messages on Topic ... {topic}")

	return

def call_rabbit_broker( action, host, port, username, password, topic="parking-slots" ):
	"""
	RabbitMQ Broker
	"""
	print( f"Inside RabbitMQ Client .. using pika vers {pika.__version__}" )
	#return

	credentials = pika.PlainCredentials( username, password )
	conn_params = pika.ConnectionParameters( host=host, port=port, credentials=credentials )

	print( f"Connection String '{action}' ... {conn_params} && {credentials}" )

	# The TCP-Connection between the application and the broker
	connection = pika.BlockingConnection(conn_params)
	
    # Lighweight connections that share a single TCP connection
	channel = connection.channel()
	
	# A logical receiver that will route messages into a queue.
	# There are 4 different types of exchanges: Direct, Fanout, Topic and Headers.
	# You link into an exchange using a Binding (defined by a routing-key).
	# You Publish messages to an Exchange.
	# You Consume messages from a Queue.
	channel.exchange_declare(
		# Exchange name
		exchange=topic, 
		# Delivers messages to queues based on routing key
		exchange_type=ExchangeType.direct,
		passive=False,
		# Survive after broker-restart
		durable=False,
		# Is deleted when last queue is unbound
		auto_delete=False
		)

	if action == "subscribe":
		basic_msg_consumer( topic, channel )
	elif action == "publish":
		basic_msg_publisher( connection, topic, channel )
	else:
		print("Hello")

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

		print(f"Successful Connection to Redis ... {host}:{port}")
	except Exception as ex:
		print(f"{ex}")

	return


def __main_mq_client__():
	print(f"Ready to Handle a Message !!!")

	parser = argparse.ArgumentParser( description='Handle Messages Between MicroServices' )

	parser.add_argument( '-a', '--action', choices=['publish', 'subscribe', 'delete'], help='action for backend message-queue service', default='sent' )

	parser.add_argument( '-n', '--name', required=False, type=str, help='message-queue name', default="Message-Queue-VIBM" )
	parser.add_argument( '-p', '--port', required=False, type=int, help='listen-port', default=5672 )

	args = parser.parse_args()

	if args.action == "publish":
		print( f"SEND-Action {args.name}, {args.port}" )
	elif args.action == "subscribe":
		print( f"SUBSCRIBE-Action to Topic ... {args.name}, {args.port}, {args.action}" )
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
		print(f"Need to Contact a RABBITMQ message queue @ Backend")

		call_rabbit_broker( args.action, host , port, username, password )
	elif mq_type.casefold() == "REDIS".casefold():
		print(f"Need to Contact REDIS message queue @ Backend")
		#return

		call_redis_to_communicate(host, port, username, password)
		return
	#elif mq_type.casefold() == "receive".casefold():
	#	try:
	#		follow_mq_server()
	#	except KeyboardInterrupt:
	#		return

	return