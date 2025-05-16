import time
import json
import random
import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt

# Generate one sensor record
def generate_sensor_data():
    return {
        'timestamp': str(pd.Timestamp.now()),
        'vibration_mm_s': round(np.random.normal(3.0, 0.5), 2),
        'temperature_C': round(np.random.normal(40.0, 2.0), 1),
        'load_percent': round(random.uniform(50, 100), 1),
        'speed_m_s': round(np.random.normal(1.2, 0.1), 2)
    }

# MQTT setup
broker = "broker.hivemq.com"
port = 1883
topic = "conveyor/belt/data"

client = mqtt.Client()
client.connect(broker, port, 60)

print(f"Publishing to MQTT broker at {broker}:{port} on topic '{topic}'")

try:
    while True:
        data = generate_sensor_data()
        payload = json.dumps(data)
        client.publish(topic, payload)
        print("Published:", payload)
        time.sleep(2)  # simulate real-time stream
except KeyboardInterrupt:
    print("Stopped publishing.")
    client.disconnect()
