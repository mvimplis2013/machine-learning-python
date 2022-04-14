from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client import BucketRetentionRules

import influxdb as db 

import os

MY_TOKEN = "PFDhKbmqL3M7wAMS-YotkAS-6zF3mTABoeliBMATeSWNOyJuHXs_gwi35fAx6BKSSRujlqAj6FmTZKpQAMgj6Q=="
MY_BUCKET = "tandem_2"

ORG = "influxdata"

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
		print("Inside Try-Catch for InfluxDB")
		
		# *************
		# Version 2.1.1
		# *************
		with InfluxDBClient( url="http://vibm-influxdb-influxdb2:80", token=MY_TOKEN, org=ORG, debug=True ) as client: 
		  version = client.ping()
		  print( f"Database Ping = {version}" )

		  buckets_api = client.buckets_api()

		  buckets = buckets_api.find_buckets( org=ORG ).buckets
		  for bucket in buckets:
		  	print(f"Existing Bucket ... {bucket}")

		  buckets_api.delete_bucket(
		  	buckets_api.find_bucket_by_name( MY_BUCKET)) 
		  print(f"Bucket Deleted ... {MY_BUCKET}")

		  print(f"---------- Create Bucket for Tandem Data ----------")
		  retention_rules = BucketRetentionRules( type="expire", every_seconds=3600 )
		  created_bucket = buckets_api.create_bucket( bucket_name=MY_BUCKET, retention_rules=retention_rules, org=ORG)
		  print(f"Bucket Created ... {created_bucket}")

		# Only for v1.0
		#client = db.InfluxDBClient(
		#	host="vibm-influxdb-influxdb2",
		#	port=80,
		#	username="admin",
		#	password=None,
		#	database=MY_DBNAME,
		#	headers={"Authorization": MY_TOKEN})

		#bucket_api = client.buckets_api()

		#bucket_api.create_bucket( bucket_name="tandem" )

		#write_api = client.write_api()

		#p = Point("h2o_level").tag("location", "coyote_creek").field("water_level", 1)
		#write_api.write(bucket="tandem", org="influxdata", record=p)
		#write_api.write( "tandem", "influxdata", ["h2o_feet,location=coyote_creek water_level=1"])

		#query_api = client.query_api()

		#query = 'from(bucket:"tandem")\
		#|> range(start: -10m)\
		#|> filter(fn:(r) => r._measurement == “h2o_level”)\
		#|> filter(fn:(r) => r.location == "coyote_creek")\
		#|> ilter(fn:(r) => r._field == "water_level" )'

		#result = query_api.query( org="influxdata", query=query )

		results = []

		#for table in result:
		#	for record in table.records:
		#		results.append((record.get_value(), record.get_field()))

		print(f"My Results = {results}")
		
		#client.switch_user("admin", "")

		#users = client.get_list_users()
		#print(f"Users = {users}")

		client.close()
	except Exception as e:
		print(f"Exception is Raised ... {e}")

	#client.get_list_database()

	#client.close()

	return