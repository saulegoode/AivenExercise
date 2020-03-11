# test script
# This script tests if connections to Aiven Postgres and Kafka is OK 
# jmaupin@comcast.net

from kafka import KafkaConsumer
from kafka import KafkaClient
import psycopg2
import configparser
import sys

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

# test db connection
print("Testing connection to Postgres: %s, %s\n" % (db_host, db_name))
try:
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    print("Connection to Postgres is OK: %s, %s\n\n" % (db_host, db_name))
except:
    print("Connection to Postgres is NOT OK: %s, %s\n\n" % (db_host, db_name))
    sys.exit(-1)

# test that the table exists
print("Testing to see if ibeacon-metrics table exists: %s, %s\n" % (db_host, db_name))
try:
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM %s" % (db_table)) 
    print("Postgres table is OK:  %s, %s, %s\n\n" % (db_host, db_name, db_table))
except psycopg2.DatabaseError as error:
    print("Postgres table is NOT OK:  %s, %s, %s\n\n" % (db_host, db_name, db_table))
    print('Error %s' % error)    
    sys.exit(-1)

# test that the TimescaleDB extension is loaded 
print("Testing to see if TimescaleDB extension is loaded: %s, %s\n" % (db_host, db_name))
try:
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE") 
    print("TimescaleDB extension is OK:  %s, %s, %s\n\n" % (db_host, db_name, db_table))
except psycopg2.DatabaseError as error:
    print("TimescaleDB extension is NOT OK:  %s, %s, %s\n\n" % (db_host, db_name, db_table))
    print('Error %s' % error)    
    sys.exit(-1)
finally:
    if conn:
        conn.close()

# test kafka connection
print("Testing to see if Kafka connection is OK:  %s\n" % (bootstrap_servers))

try:
    consumer = KafkaConsumer(
         topic,
         bootstrap_servers=bootstrap_servers,
         security_protocol=security_protocol,
         ssl_cafile=ssl_cafile,
         ssl_certfile=ssl_certfile,
         ssl_keyfile=ssl_keyfile,
         value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print("Kafka connection is OK:  %s\n\n" % (bootstrap_servers))
except Exception as e:
    print("Kafka connection is NOT OK:  %s\n\n" % (bootstrap_servers))
    print("ERROR: %s" % e)
    sys.exit(-1)

# test if kafka topic exists, if not create it
print("Testing to see if Kafka topic is OK:  %s\n" % (bootstrap_servers))

try:
    topics = consumer.topics()
    if topic in topics:
        print("Kafka topic %s is OK:  %s\n\n" % (topic, bootstrap_servers))
    else:
        raise Exception("Kafka topic %s is not OK\n\nYou need to create a topic in the Aiven console named 'demo-topic'" % (topic))
except Exception as e:
    print("Kafka topic %s is NOT OK:  %s\n\nYou need to create a topic in the Aiven console named 'demo-topic'" % (topic, bootstrap_servers))
    print("ERROR: %s" % e)
    sys.exit(-1)    
