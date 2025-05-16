import streamlit as st
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Conveyor Belt Dashboard", layout="wide")
st.title("🛠️ Conveyor Belt Live Digital Twin Dashboard")

# Initialize session state
if 'data_store' not in st.session_state:
    st.session_state.data_store = []

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    client.subscribe("conveyor/belt/data")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload['timestamp'] = str(datetime.now())
        st.session_state.data_store.append(payload)
    except:
        pass

# Connect to MQTT only once
if 'mqtt_connected' not in st.session_state:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()
    st.session_state.mqtt_connected = True
    st.info("Connected to MQTT broker at broker.hivemq.com")

# Refresh manually or on timer
st.button("Refresh Dashboard")

# Display data
if len(st.session_state.data_store) > 0:
    df = pd.DataFrame(st.session_state.data_store[-50:])  # last 50 records
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vibration (mm/s)", df['vibration_mm_s'].iloc[-1])
    col2.metric("Temperature (°C)", df['temperature_C'].iloc[-1])
    col3.metric("Load (%)", df['load_percent'].iloc[-1])
    col4.metric("Speed (m/s)", df['speed_m_s'].iloc[-1])

    st.line_chart(df.set_index('timestamp')[['vibration_mm_s', 'temperature_C', 'load_percent', 'speed_m_s']])
else:
    st.warning("Waiting for sensor data from MQTT...")
