from influxdb import InfluxDBClient

import os

def write_events():
	return

def __influx_main__():
	print(f"Ready to Connect to InfluxDB")

	host = os.environ[ "INFLUXDB_SERVICE" ]

	username = os.environ[ "INFLUXDB_USER" ]
	password = os.environ[ "INFLUXDB_PASSWORD" ]
	
	database = os.environ[ "INFLUXDB_NAME" ]

	client = InfluxDBClient( host=host, port=8086, username="tandem", password="tandem" )

	version = client.ping()
	#client.get_list_database()

	#client.close()

	return