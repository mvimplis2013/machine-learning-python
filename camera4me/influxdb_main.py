from influxdb import InfluxDBClient

import os

def write_events():
	return

def __influx_main__():
	print(f"Ready to Connect to InfluxDB")

	#host = os.environ[ "INFLUXDB_SERVICE" ]
	#print(f"Host = {host}")

	#username = os.environ[ "INFLUXDB_USER" ]
	#password = os.environ[ "INFLUXDB_PASSWORD" ]
	
	#database = os.environ[ "INFLUXDB_NAME" ]
	
	try:
		#client = InfluxDBClient( host="vibm-influxdb-influxdb2", port=8086, username="admin", password="mnzLrGbCpH89okUbSzpLHuPKC8iFXbXJ" )

		#version = client.ping()
		#print(f"Database Version = {version}")
        
        print("Inside Try-Catch")
		
		#client.switch_user("admin", "")

		#users = client.get_list_users()
		#print(f"Users = {users}")
	except Exception as e:
		print(f"Exception is Raised ... {e}")

	#client.get_list_database()

	#client.close()

	return