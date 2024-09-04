import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Timely")
st.info("Your very own personalized scheduler")

if 'events' not in st.session_state:
    st.session_state.events = []

def add_event(name, date, time):
    event_datetime = datetime.combine(date, time)
    event = {
        'name': name,
        'datetime': event_datetime
    }
    st.session_state.events.append(event)

def delete_event(index):
    if 0 <= index < len(st.session_state.events):
        st.session_state.events.pop(index)
    st.rerun()

def display_events():
    if st.session_state.events:
        events_df = pd.DataFrame(st.session_state.events)
        events_df['datetime'] = events_df['datetime'].dt.strftime("%Y-%m-%d %H:%M")
        st.write("### Scheduled Events")
        
        for i, event in events_df.iterrows():
            col1, col2 = st.columns([4, 1])
            col1.write(f"{event['name']} - {event['datetime']}")
            if col2.button("Delete", key=f"del_{i}"):
                delete_event(i)
                st.success(f"Event '{event['name']}' deleted!")
    else:
        st.write("No events scheduled.")

now = datetime.now()

with st.form("event_form"):
    name = st.text_input("Event Name")
    date = st.date_input("Event Date", min_value=now.date())
    time = st.time_input("Event Time", now,step=1800)
    submitted = st.form_submit_button("Add Event")

    if submitted:
        event_datetime = datetime.combine(date, time)
        if event_datetime <= now:
            st.error("Please select a future date and time.")
        elif name:
            add_event(name, date, time)
            st.success(f"Event '{name}' added on {date} at {time}!")

display_events()