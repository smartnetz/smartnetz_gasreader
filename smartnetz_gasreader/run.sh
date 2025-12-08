#!/usr/bin/with-contenv bashio
set -e
bashio::log.info "Starte Smartnetz Gaszähler MQTT Discovery Add-on..."



MQTT_HOST=$(bashio::services mqtt "host")
MQTT_PORT=$(bashio::services mqtt "port")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

DISCOVERY_PREFIX=$(bashio::config 'discovery_prefix')
DEVICE_ID=$(bashio::config 'device_id')
STATE_TOPIC=$(bashio::config 'state_topic')
LWT_TOPIC=$(bashio::config 'lwt_topic')
DEVICE_NAME=$(bashio::config 'device_name')

export MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD
export DISCOVERY_PREFIX DEVICE_ID STATE_TOPIC LWT_TOPIC DEVICE_NAME

python3 /app/discovery.py
bashio::log.info "Fertig."
