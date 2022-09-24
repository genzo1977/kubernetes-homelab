#!/usr/bin/env python

# See https://github.com/lisenet/kubernetes-homelab

import speedtest
from influxdb import InfluxDBClient
import os

# Retrieve environment variables
influx_user = os.environ['INFLUXDB_USERNAME']
influx_pass = os.environ['INFLUXDB_PASSWORD']
influx_db   = os.environ['INFLUXDB_DATABASE']
influx_host = os.environ['INFLUXDB_HOST']
influx_port = os.environ['INFLUXDB_PORT']

# Client config
influx_client = InfluxDBClient(influx_host,influx_port,influx_user,influx_pass,influx_db)

print ("Dummy request to test influxdb connection")
influx_client.get_list_database()

print ("Running a speedtest using default server")
s = speedtest.Speedtest(secure=True)
s.get_best_server()
s.download()
s.upload()
results = s.results.dict()

print ("Printing raw results to stdout")
print (results)

# Format the data
influx_data = [
    {
        "measurement": "speedtest",
        "time": results["timestamp"],
        "fields": {
            "download": results["download"],
            "upload": results["upload"],
            "bytes_received": results["bytes_received"],
            "bytes_sent": results["bytes_sent"],
            "ping": results["ping"]
        }
    }
]

print ("Writing to influxdb")
influx_client.write_points(influx_data)
