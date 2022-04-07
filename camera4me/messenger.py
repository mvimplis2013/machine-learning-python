import argparse
import os

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
    	printf(f"Ready to Start Sending Messages with RabbitMQ")

	return