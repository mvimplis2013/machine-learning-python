from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client import BucketRetentionRules
from influxdb_client import WritePrecision

import influxdb as db 

import os

MY_TOKEN = "PFDhKbmqL3M7wAMS-YotkAS-6zF3mTABoeliBMATeSWNOyJuHXs_gwi35fAx6BKSSRujlqAj6FmTZKpQAMgj6Q=="
MY_BUCKET = "tandem"

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
		  print(f"------------- List All Buckets -------------")
		  for bucket in buckets:
		  	print(f"Existing Bucket --> {bucket}")

		  bucket_id = buckets_api.find_bucket_by_name( MY_BUCKET ) 
		  if bucket_id is not None:
		  	print(f"------------- Delete Tandem Bucket -------------")
		  	buckets_api.delete_bucket( bucket_id ) 
		  	print(f"Bucket Deleted ... {MY_BUCKET}")

		  print(f"---------- Create Bucket for Tandem Data ----------")
		  retention_rules = BucketRetentionRules( type="expire", every_seconds=3600 )
		  created_bucket = buckets_api.create_bucket( bucket_name=MY_BUCKET, retention_rules=retention_rules, org=ORG)
		  print(f"Bucket Created ... {created_bucket}")

		  """
		  Prepare Data
		  """
		  print(f"---------- Write Data to Bucket ----------")

		  write_api = client.write_api(write_options=SYNCHRONOUS)

		  _point1 = Point("eu_capitals_oC").tag("location", "Amsterdam").field("temperature", 18).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point2 = Point("eu_capitals_oC").tag("location", "Athens").field("temperature", 19).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point3 = Point("eu_capitals_oC").tag("location", "Belgrade").field("temperature", 16).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point4 = Point("eu_capitals_oC").tag("location", "Berlin").field("temperature", 16).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point5 = Point("eu_capitals_oC").tag("location", "Bern").field("temperature", 20).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point6 = Point("eu_capitals_oC").tag("location", "Bratislava").field("temperature", 20).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point7 = Point("eu_capitals_oC").tag("location", "Brussels").field("temperature", 18).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point8 = Point("eu_capitals_oC").tag("location", "Bucharest").field("temperature", 20).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point9 = Point("eu_capitals_oC").tag("location", "Copenhagen").field("temperature", 12).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point10 = Point("eu_capitals_oC").tag("location", "Dublin").field("temperature", 14).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point11 = Point("eu_capitals_oC").tag("location", "Helsinki").field("temperature", 3).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point12 = Point("eu_capitals_oC").tag("location", "Kyiv").field("temperature", 8).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point13 = Point("eu_capitals_oC").tag("location", "Lisbon").field("temperature", 19).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point14 = Point("eu_capitals_oC").tag("location", "London").field("temperature", 19).time(
		  	datetime.utcnow(), WritePrecision.MS)
		  _point15 = Point("eu_capitals_oC").tag("location", "Madrid").field("temperature", 17).time(
		  	datetime.utcnow(), WritePrecision.MS)

		  write_api.write( bucket=MY_BUCKET, record=_point1 )
		  write_api.write( bucket=MY_BUCKET, record=_point2 )
		  write_api.write( bucket=MY_BUCKET, record=_point3 )
		  write_api.write( bucket=MY_BUCKET, record=_point4 )
		  write_api.write( bucket=MY_BUCKET, record=_point5 )
		  write_api.write( bucket=MY_BUCKET, record=_point6 )
		  write_api.write( bucket=MY_BUCKET, record=_point7 )
		  write_api.write( bucket=MY_BUCKET, record=_point8 )
		  write_api.write( bucket=MY_BUCKET, record=_point9 )
		  write_api.write( bucket=MY_BUCKET, record=_point10 )
		  write_api.write( bucket=MY_BUCKET, record=_point11 )
		  write_api.write( bucket=MY_BUCKET, record=_point12 )
		  write_api.write( bucket=MY_BUCKET, record=_point13 )
		  write_api.write( bucket=MY_BUCKET, record=_point14 )
		  write_api.write( bucket=MY_BUCKET, record=_point15 )

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