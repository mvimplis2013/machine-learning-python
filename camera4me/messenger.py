import argparse

def __main_mq_client__():
	print(f"Ready to Post a Message")

	parser = argparse.ArgumentParser( description='Handle Messages Between MicroServices' )

	parser.add_argument( '-a', '--action', required=False, choices=['sent', 'receive', 'delete'], help='action for backend message-queue service' )

	#parser.add_argument( '-n', '--name', required=False, type=str, help='message-queue name', default="Message-Queue-VIBM" )
	#parser.add_argument( '-p', '--port', required=False, type=int, help='listen-port', default=5672 )

	args = parser.parse_args()

	if args.action == "sent":
	  print "SEND" #args.name, args.port, "SEND"

	'''
	elif args.action == "receive":
        print args.name, args.port, "RECEIVE"
    elif args.action == "delete":
        print args.name
    '''

	return