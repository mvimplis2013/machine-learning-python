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

	client = InfluxDBClient( host=host, username=username, password=password )

	client.create_database( database )

	client.close()

	return