from influxdb import InfluxDBClient

import os

def __influx_main__():
	print(f"Ready to Connect to InfluxDB")

	host = os.environ[ "INFLUXDB_SERVICE" ]
	password = os.environ[ "INFLUXDB_PASSWORD" ]

	client = InfluxDBClient( host, user="admin", password )

	client.close()

	return