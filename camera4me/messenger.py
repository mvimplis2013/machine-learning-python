import argparse

def __main_mq_client__():
	print(f"Ready to Post a Message")

	parser = argparse.ArgumentParser( description='Handle Messages Between MicroServices' )

	parser.add_argument(
        '-a', '--action', choices=['sent', 'receive', 'delete'], help='action for backend message-queue service')

	parser.add_argument(
        '-n', '--name', required=True, type=str, help='message-queue name')
    parser.add_argument(
        '-p', '--port', required=False, type=int, help='listen-port')

    args = parser.parse_args()

    if args.action == "sent":
        print args.name, args.port, "SEND"
    elif args.action == "receive":
        print args.name, args.port, "RECEIVE"
    elif args.action == "delete":
        print args.name