import streamlit as st

st.title(" Threat Intelligence Dashboard")

st.subheader("Latest Detection")

st.metric("Anomaly Score", "0.91")

st.error(" Suspicious Activity Detected")

st.write({
   "threat_level": "HIGH",
   "description": "Multiple failed login attempts",
   "action": "Block IP"
})