-- Add the TimescaleDB Apache 2.0 extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create table
CREATE TABLE IF NOT EXISTS ibeacon_metrics (
  timestamp TIMESTAMP,
  uuid uuid NOT NULL,
  major NUMERIC,
  measured_power NUMERIC,
  rssi NUMERIC,
  accuracy NUMERIC,
  proximity TEXT);

-- Create the TimescaleDB hypertable
SELECT create_hypertable('ibeacon_metrics', 'timestamp')
