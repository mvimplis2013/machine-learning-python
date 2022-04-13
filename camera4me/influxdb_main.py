from influxdb_client import InfluxDBClient

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
		print("Inside Try-Catch")
		
		client = InfluxDBClient( url="http://vibm-influxdb-influxdb2:80", 
		  token="PFDhKbmqL3M7wAMS-YotkAS-6zF3mTABoeliBMATeSWNOyJuHXs_gwi35fAx6BKSSRujlqAj6FmTZKpQAMgj6Q==",  
		  org="influxdata" ) #password="mnzLrGbCpH89okUbSzpLHuPKC8iFXbXJ" )

		bucket_api = client.buckets_api()

		#bucket_api.create_bucket( bucket_name="tandem" )

		write_api = client.write_api()

		write_api.write( "tandem", "influxdata", ["h2o_feet,location=coyote_creek water_level=1"])

		#client.create_database( "tandem" )

		#version = client.ping()
		#print(f"Database Version = {version}")
        
		#client.switch_user("admin", "")

		#users = client.get_list_users()
		#print(f"Users = {users}")

		client.close()
	except Exception as e:
		print(f"Exception is Raised ... {e}")

	#client.get_list_database()

	#client.close()

	return