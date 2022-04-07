import argparse
import os
import pika

def call_mq_server():
	print(f"Ready to Start Sending Messages with RabbitMQ")

	try:
		#conn_params = pika.ConnectionParameters('amqp://www-data:rabbit_pwd@rabbit1/web_messages')
		#conn_params = pika.ConnectionParameters('amqp://user:@10.109.109.116:5672/%2F')

		credentials = pika.PlainCredentials( "user", "voMjPY74Ui" )
		conn_params = pika.ConnectionParameters( "my-rabbitmq.default.svc", credentials=credentials )

		print(f"Connection String ... {conn_params}")

		connection = pika.BlockingConnection( conn_params )
	except pika.exceptions.AMQPConnectionError as pika_e:
		print(f"Failed to Connect to RabbitMQ ... {pika_e}")
		return

	return

def __main_mq_client__():
	print(f"Ready to Post a Message")

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
	except KeyError as e:
		print( f"Problem Reading Environment Variables for Message-Queue ... {e}" )
		return

	if mq_type.casefold() == "rabbitmq".casefold():	
		call_mq_server()

	return