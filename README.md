# AivenExercise

Aiven exercise using Kafka, PostgreSQL, and optionally Grafana. 

This exercise was built around work done by John Hammink (https://gist.github.com/Jammink2). It simulates an iBeacon device streaming data using Aiven hosted Kafka and written to a Aiven hosted PostgreSQL instance for further analysis and optionally analysed in a Aiven hosted Grafana instance.

## Pre-requisites
Python > 3x with psycopg2 and kafka-python modules loaded

PostgreSQL client such as psql or PGAdmin

GitHub client

## Server Setup
Create a Aiven hosted Kafka service. <https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka> 

Create a Aiven hosted PostgreSQL service <https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql>

[Optional] Create a Aiven hosted Grafana service <https://help.aiven.io/en/articles/489587-getting-started-with-aiven-grafana>

Clone this Github repository using `git clone https://github.com/saulegoode/AivenExercise.git`.

## Kafka setup:

Download the Access Key, Access Certificate, and CA Certificate from the Overview into the same directory as ibeacon_producer.py.

Edit the ibeacon.properties with appropriate values from console overview.

**Note** Create a Kafka topic in the Aiven console using the Topics tab. The topic should be named demo-topic.

## PostgreSQL setup:
	
Edit ibeacon.properties with appropriate values from console overview.

Connect to the Aiven hosted PostgreSQL instance with your favorite PostgreSQL client such as psql or PGAdmin.

Load the TimescaleDB Apache 2.0 extension  with:

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
``` 

Create the ibeacon-metrics table with:

```sql
CREATE TABLE IF NOT EXISTS ibeacon_metrics (
        timestamp TIMESTAMP,
        uuid uuid NOT NULL,
        major NUMERIC,
        measured_power NUMERIC,
        rssi NUMERIC,
        accuracy NUMERIC,
        proximity TEXT);
```

Convert the table into a TimescaleDB hypertable with:

```sql
SELECT create_hypertable('ibeacon_metrics', 'timestamp');
```

## Testing

Run the ibeacon-test.py script to make sure all is setup correctly. Correct any problems found.

`python ./ibeacon-test.py`

## Run the Kafka producer and Kafka consumer (in separate consoles)

Run ibeacon_producer.py in a console. ibeacon_producer.py requires one argument: the number of records to generate and send.

`python ./ibeacon_producer 10000`

Run ibeacon_consumer.py in a console

`python ./ibeacon_consumer`

## Analyze the data in Aiven hosted PostgreSQL

Connect to the PostgreSQL instance with your favorite client tool such as psql or PGAdmin and issues queries.

Example queries:

```sql
SELECT
        time_bucket('1 minute', timestamp) AS time,
        uuid,
        avg(measured_power) as power,
        avg(rssi) as rssi
  FROM 
        ibeacon_metrics
  GROUP BY
        time, uuid
  ORDER BY
        time;
``` 

## Credits: John Hammink https://gist.github.com/Jammink2
