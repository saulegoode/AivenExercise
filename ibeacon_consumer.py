# iBeacon Consumer simulator for Aiven Kafka
# This script was based on work done by John Hammink https://gist.github.com/Jammink2.
# This script receives messages from a Kafka topic
# usage: python ibeacon_consumer.py

import psycopg2
import json
import configparser
from kafka import KafkaConsumer
from time import sleep

# read in properties
config = configparser.RawConfigParser()
config.read('ibeacon.properties')

kafka_dict = dict(config.items('KAFKA'))
postgres_dict = dict(config.items('POSTGRESQL'))

# variables for db connection
db_name = postgres_dict['db_name'] 
db_user = postgres_dict['db_user']
db_password = postgres_dict['db_password'] 
db_host = postgres_dict['db_host'] 
db_port = postgres_dict['db_port'] 
db_table = postgres_dict['db_table']

# variables for kafka connection
topic = kafka_dict['topic']
bootstrap_servers = kafka_dict['bootstrap_servers']
security_protocol = kafka_dict['security_protocol']
ssl_cafile = kafka_dict['ssl_cafile']
ssl_certfile = kafka_dict['ssl_certfile']
ssl_keyfile = kafka_dict['ssl_keyfile']

class PGConnection():

    def __init__(self,db_name,db_user,db_password,db_host,db_port):
        # setup connection to postgres
        try: 
            self.database = psycopg2.connect (database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
            self.database.autocommit = True
            self.cursor = self.database.cursor() 
            
            print("Connection to Postgres server success: %s, %s" % (db_host, db_name))
        except:
            print("Connection to Postgres server failed: %s, %s" % (db_host, db_name))

    def execute(self, sql):
        self.cursor.execute(sql)

    def __enter__(self):
        return self
 
    def __exit__(self, *args):
        self.cursor.close()
        self.database.close()
        print("Connection closed to Postgres server: %s" % (db_host))

# method that receives the message
# be sure to copy your ca.pem, service.cert and service.key to local directory from your Aiven Kafka instance.

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    security_protocol=security_protocol,
    ssl_cafile=ssl_cafile,
    ssl_certfile=ssl_certfile,
    ssl_keyfile=ssl_keyfile,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

with PGConnection(db_name,db_user,db_password,db_host,db_port) as database:
    while True:
        raw_msgs = consumer.poll(timeout_ms=10000)
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                # build insert string
                sql = 'INSERT INTO {} '.format(db_table)
                sql += '('
                sql += ','.join(msg.value.keys()) 
                sql += ') VALUES ('
                valuelist = []
                for s in msg.value.values():
                    valuelist.append("'" + s +  "'")  
                sql += ','.join(valuelist)
                sql += ')'
                print(sql)
                database.execute(sql)
