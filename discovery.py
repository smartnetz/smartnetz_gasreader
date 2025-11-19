import os, json, time
import paho.mqtt.client as mqtt

MQTT_HOST=os.environ.get("MQTT_HOST","localhost")
MQTT_PORT=int(os.environ.get("MQTT_PORT","1883"))
MQTT_USER=os.environ.get("MQTT_USER") or None
MQTT_PASSWORD=os.environ.get("MQTT_PASSWORD") or None

DISCOVERY_PREFIX=(os.environ.get("DISCOVERY_PREFIX") or "homeassistant").rstrip("/")
DEVICE_ID=os.environ.get("DEVICE_ID") or "smartnetz_gas"
STATE_TOPIC=os.environ.get("STATE_TOPIC") or "tele/Gaszaehler/json"
LWT_TOPIC=os.environ.get("LWT_TOPIC") or "tele/Gaszaehler/LWT"
DEVICE_NAME=os.environ.get("DEVICE_NAME") or "Smartnetz Gaszähler"

DEVICE={
    "identifiers":[DEVICE_ID],
    "manufacturer":"Smartnetz",
    "model":"Gasreader",
    "name":DEVICE_NAME,
}

def client():
    c=mqtt.Client()
    if MQTT_USER:
        c.username_pw_set(MQTT_USER, MQTT_PASSWORD or "")
    c.connect(MQTT_HOST, MQTT_PORT, 60)
    return c

def publish(client, suffix, name, uid, tpl, unit=None, dev_cla=None, stat_cla=None):
    topic=f"{DISCOVERY_PREFIX}/sensor/{DEVICE_ID}_{suffix}/config"
    payload={
        "name":name,
        "uniq_id":uid,
        "stat_t":STATE_TOPIC,
        "val_tpl":tpl,
        "device":DEVICE,
        "avty_t":LWT_TOPIC,
        "pl_avail":"Online",
        "pl_not_avail":"Offline",
    }
    if unit: payload["unit_of_meas"]=unit
    if dev_cla: payload["dev_cla"]=dev_cla
    if stat_cla: payload["stat_cla"]=stat_cla
    client.publish(topic, json.dumps(payload), qos=1, retain=True)

def main():
    c=client()
    c.loop_start()
    time.sleep(0.3)

    publish(c,"zaehlerstand","Zählerstand",f"{DEVICE_ID}_zaehlerstand","{{ value_json.gastotal | float(0) }}","m³","gas","total_increasing")
    publish(c,"zaehlung_seit_nullung","Zählung seit Nullung",f"{DEVICE_ID}_zaehlung_seit_nullung","{{ value_json.value | float(0) }}","m³","gas","total_increasing")
    publish(c,"verbrauch_volumen_heute","Verbrauch Volumen heute",f"{DEVICE_ID}_verbrauch_volumen_heute","{{ value_json.today_m3 | float(0) }}","m³","gas","total")
    publish(c,"verbrauch_energie_heute","Verbrauch Energie heute",f"{DEVICE_ID}_verbrauch_energie_heute","{{ value_json.today_kwh | float(0) }}","kWh","energy","total")
    publish(c,"verbrauch_volumen_gestern","Verbrauch Volumen gestern",f"{DEVICE_ID}_verbrauch_volumen_gestern","{{ value_json.yesterday_m3 | float(0) }}","m³","gas")
    publish(c,"verbrauch_energie_gestern","Verbrauch Energie gestern",f"{DEVICE_ID}_verbrauch_energie_gestern","{{ value_json.yesterday_kwh | float(0) }}","kWh","energy")
    publish(c,"verbrauch_volumen_vorgestern","Verbrauch Volumen vorgestern",f"{DEVICE_ID}_verbrauch_volumen_vorgestern","{{ value_json.db_yesterday_m3 | float(0) }}","m³","gas")
    publish(c,"verbrauch_energie_vorgestern","Verbrauch Energie vorgestern",f"{DEVICE_ID}_verbrauch_energie_vorgestern","{{ value_json.db_yesterday_kwh | float(0) }}","kWh","energy")

    time.sleep(1)
    c.loop_stop()
    c.disconnect()

if __name__=="__main__":
    main()
