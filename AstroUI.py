import streamlit as st
import requests
from datetime import date

# ===============================
# BACKEND CONFIGURATION
# ===============================
BASE_URL = "http://localhost:8000"  # 🔴 Change this if needed


def get_today_events(event_type=None):
    try:
        params = {}
        if event_type and event_type != "All Events":
            params["type"] = event_type
        response = requests.get(f"{BASE_URL}/events/today", params=params)
        return response.json()
    except:
        return []


def get_events_by_date(selected_date, event_type=None):
    try:
        params = {"date": selected_date}
        if event_type and event_type != "All Events":
            params["type"] = event_type
        response = requests.get(f"{BASE_URL}/events", params=params)
        return response.json()
    except:
        return []


def subscribe_user(email):
    try:
        response = requests.post(f"{BASE_URL}/subscribe", json={"email": email})
        return response.status_code == 200
    except:
        return False


# ===============================
# STREAMLIT UI CONFIG
# ===============================
st.set_page_config(
    page_title="Astronomical Event Predictor", page_icon="🔭", layout="wide"
)

st.title("🔭 Astronomical Event Predictor & Notifier")

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("🧭 Controls")

# 🔽 EVENT DROPDOWN
event_type = st.sidebar.selectbox(
    "🌌 Select Astronomical Event",
    [
        "All Events",
        "Solar Eclipse",
        "Lunar Eclipse",
        "Meteor Shower",
        "Planetary Alignment",
        "Comet Appearance",
        "Supermoon",
    ],
)

option = st.sidebar.radio("📍 View Mode", ["Today's Events", "Search by Date"])

st.sidebar.divider()

# 🔔 NOTIFICATION
st.sidebar.header("🔔 Get Notifications")
email = st.sidebar.text_input("Enter your email")

if st.sidebar.button("Subscribe"):
    if email:
        if subscribe_user(email):
            st.sidebar.success("Subscribed successfully!")
        else:
            st.sidebar.error("Subscription failed.")
    else:
        st.sidebar.warning("Please enter a valid email.")

# ===============================
# MAIN CONTENT
# ===============================
if option == "Today's Events":
    st.subheader("🌠 Today's Astronomical Events")

    events = get_today_events(event_type)

    if events:
        for event in events:
            st.markdown(f"## ✨ {event.get('event', 'Unknown Event')}")
            st.write(f"📅 **Date:** {event.get('date', 'N/A')}")
            st.write(f"📍 **Visibility:** {event.get('visibility', 'N/A')}")
            with st.expander("🔍 Event Description"):
                st.write(event.get("description", "No description available"))
            st.divider()
    else:
        st.info("No events found for selected category.")

elif option == "Search by Date":
    st.subheader("📅 Search Astronomical Events")

    selected_date = st.date_input("Select a date", date.today())

    if st.button("Search"):
        events = get_events_by_date(selected_date, event_type)

        if events:
            for event in events:
                st.markdown(f"## 🌌 {event.get('event', 'Unknown Event')}")
                st.write(f"📅 **Date:** {event.get('date', 'N/A')}")
                st.write(f"📍 **Visibility:** {event.get('visibility', 'N/A')}")
                with st.expander("🔍 Event Description"):
                    st.write(event.get("description", "No description available"))
                st.divider()
        else:
            st.warning("No events found for selected date and category.")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("🚀 Astronomical Event Predictor | Streamlit UI")
