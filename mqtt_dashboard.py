import streamlit as st
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Conveyor Belt Dashboard", layout="wide")
st.title("🛠️ Conveyor Belt Live Digital Twin Dashboard")

data_store = []

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    client.subscribe("conveyor/belt/data")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    payload['timestamp'] = datetime.now()
    data_store.append(payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

placeholder = st.empty()

while True:
    if len(data_store) > 0:
        df = pd.DataFrame(data_store[-50:])  # show last 50
        with placeholder.container():
            st.subheader("Live Sensor Metrics (Last 50)")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Vibration (mm/s)", df['vibration_mm_s'].iloc[-1])
            col2.metric("Temperature (°C)", df['temperature_C'].iloc[-1])
            col3.metric("Load (%)", df['load_percent'].iloc[-1])
            col4.metric("Speed (m/s)", df['speed_m_s'].iloc[-1])
            st.line_chart(df.set_index('timestamp')[['vibration_mm_s', 'temperature_C', 'load_percent', 'speed_m_s']])
