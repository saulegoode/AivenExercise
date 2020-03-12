# AivenExercise

Aiven exercise using Kafka, PostgreSQL, and optionally Grafana. 

This exercise was built around work done by John Hammink (https://gist.github.com/Jammink2). It simulates an iBeacon device streaming data using Aiven Kafka and written to a Aiven PostgreSQL instance for further analysis and optionally analysed in a Aiven Grafana instance.

## Pre-requisites
Python > 3x with psycopg2 and kafka-python modules loaded

PostgreSQL client such as psql or PGAdmin

GitHub client

## Server Setup
Create a Aiven Kafka service. 

Create a Aiven PostgreSQL service

[Optional] Create a Aiven Grafana service

Clone this Github repository using git clone https://github.com/saulegoode/AivenExercise.git.

## Kafka setup:

Download the Access Key, Access Certificate, and CA Certificate from the Overview into the same directory as ibeacon_producer.py.

Edit the ibeacon.properties with appropriate values from console overview.

## PostgreSQL setup:
	
Edit ibeacon.properties with appropriate values from console overview.

Connect to the Aiven PostgreSQL instance with your favorite PostgreSQL client such as psql or PGAdmin.

Load the TimescaleDB Apache 2.0 extension  with:

`CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;` 

Create the ibeacon-metrics table with:

`CREATE TABLE IF NOT EXISTS ibeacon_metrics (`

  `timestamp TIMESTAMP,`

  `uuid uuid NOT NULL,`

  `major NUMERIC,`

  `measured_power NUMERIC,`

  `rssi NUMERIC,`

  `accuracy NUMERIC,`

  `proximity TEXT);`

Convert the table into a TimescaleDB hypertable with:

`SELECT create_hypertable('ibeacon_metrics', 'timestamp');` 

## Testing

Run the ibeacon-test.py script to make sure all is setup correctly. Correct any problems found.

## Run the Kafka producer and Kafka consumer (in seperate consoles)

Run ibeacon_producer.py

Run ibeacon_consumer.py

## Analyze the data in Aiven PostgreSQL

Connect to the PostgreSQL instance with your favorite client tool such as psql or PGAdmin and issues queries.

Example queries:

  `SELECT`
 
        `time_bucket('1 minute', timestamp) AS time,`
        `uuid,`
        `avg(measured_power) as power,`
        `avg(rssi) as rssi`
  `FROM 
        `ibeacon_metrics`
  `GROUP BY`
        `time, uuid`
  `ORDER BY`
        `time;` ` 

## Credits: John Hammink https://gist.github.com/Jammink2
