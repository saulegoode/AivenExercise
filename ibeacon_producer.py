# iBeacon Producer simulator for Aiven Kafka
# This script was based on work done by John Hammink https://gist.github.com/Jammink2.
# This script takes, as an argument, the number of messages you want to iterate on.
# example usage: python ibeacon.py 50000
# to run continuously, try: clear && python ibeacon_producer.py 5000000

import sys, random, string, os, json
import configparser
from datetime import datetime
from time import sleep
from kafka import KafkaProducer

# use for forward compatibility 
try:
    # Python 2 forward compatibility
    xrange = range
except NameError:
    pass

# read in properties
config = configparser.RawConfigParser()
config.read('ibeacon.properties')
kafka_dict = dict(config.items('KAFKA'))

bootstrap_servers = kafka_dict['bootstrap_servers']
security_protocol = kafka_dict['security_protocol']
ssl_cafile = kafka_dict['ssl_cafile']
ssl_certfile = kafka_dict['ssl_certfile']
ssl_keyfile = kafka_dict['ssl_keyfile']

chars = '1234567890'

# get number of iterations from commandline
if len(sys.argv) != 2:
    print("Usage: python ibeacon.py <number of iterations>")
    sys.exit(-1)
     
iterator = int(sys.argv[1])

def generate_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%Y-%b-%d %H:%M:%S.%f")

def generate_uuid(length):
    #arrange numbers in chars into random string of length = length
    #uuid = ''.join([random.choice(chars) for n in xrange(length)])

    uuid = random.choice(
        ['40e6215d-b5c6-4896-987c-f30f3678f608',
         '6ecd8c99-4036-403d-bf84-cf8400f67836',
         '3f333df6-90a4-4fda-8dd3-9485d27cee36',
         '3f333df6-90a4-4fda-8dd3-9485d2734234'])
    return uuid

def generate_major(length):
    major = ''.join([random.choice(chars) for n in xrange(length)])
    return major


def generate_measuredPower():
    measured_power = random.choice([-39, -40, -41, -42, -43, -44, -45, -46, -47, -48, -49, -51, -53, -55, -57, -59, -61, -63, -65])
    return measured_power

def generate_rssi():
    rssi = random.choice([ -21, -27, -28, -29, -30, -31, -37, -41, -47, -51, -57, -61, -67, -77, -89, -95, -100])
    return rssi
    
def generate_accuracy_substring(length):
    accuracy_substring = ''.join([random.choice(chars) for n in xrange(length)])
    return accuracy_substring

def choose_proximity():
    proximity_choice = random.choice(['near', 'immediate', 'far', 'distant'])
    return proximity_choice

# method that sends the message
# be sure to copy your ca.pem, service.cert and service.key to local directory from your Aiven Kafka instance.

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    security_protocol=security_protocol,
    ssl_cafile=ssl_cafile,
    ssl_certfile=ssl_certfile,
    ssl_keyfile=ssl_keyfile,
    value_serializer=lambda m: json.dumps(m).encode('utf-8'),
)

for i in range(iterator):
    #slow down / throttle produce calls somewhat
    sleep(1)
    # get values
    uuid = str(generate_uuid(length=27))
    timestamp = generate_timestamp()
    major = str(generate_major(length=5))
    measured_power = str(generate_measuredPower())
    rssi = str(generate_rssi())
    accuracy_substring = str(generate_accuracy_substring(length=16))
    proximity_choice = str(choose_proximity())

    message = {"timestamp":timestamp,
            "uuid":uuid,
            "major":major,
            "measured_power":measured_power,
            "rssi":rssi,
            "accuracy":accuracy_substring,
            "proximity":proximity_choice}
    print("Sending: {}".format(message))
    producer.send("demo-topic", message)
    producer.flush()
