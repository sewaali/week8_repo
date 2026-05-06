import streamlit as st
import pandas as pd
import random

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
   page_title="Threat Intelligence Dashboard",
   layout="wide"
)

# =========================================
# TITLE
# =========================================

st.title("🛡 Threat Intelligence Dashboard")

st.markdown("---")

# =========================================
# TOP METRICS
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
   st.metric(
       label="Detected Threats",
       value="12",
       delta="+3"
   )

with col2:
   st.metric(
       label="Anomaly Score",
       value="0.91"
   )

with col3:
   st.metric(
       label="Threat Level",
       value="HIGH"
   )

st.markdown("---")

# =========================================
# ALERT MESSAGE
# =========================================

st.error(
   "🚨 Multiple failed login attempts detected from suspicious IP addresses"
)

# =========================================
# SUSPICIOUS IPS TABLE
# =========================================

st.subheader("📌 Suspicious IP Activity")

data = {
   "IP Address": [
       "10.0.0.1",
       "10.0.0.2",
       "192.168.1.55"
   ],
   "Failed Logins": [
       15,
       11,
       7
   ],
   "Request Count": [
       120,
       98,
       76
   ],
   "Threat Level": [
       "HIGH",
       "HIGH",
       "MEDIUM"
   ]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.markdown("---")

# =========================================
# LIVE THREAT LOGS
# =========================================

st.subheader("📡 Live Threat Logs")

logs = []

for i in range(10):

   logs.append({
       "Timestamp": f"2026-01-01 10:{i}:00",
       "IP": f"10.0.0.{random.randint(1,5)}",
       "Action": "login",
       "Status": "fail"
   })

logs_df = pd.DataFrame(logs)

st.table(logs_df)

st.markdown("---")

# =========================================
# THREAT SCORE CHART
# =========================================

st.subheader("📈 Threat Scores")

chart_data = pd.DataFrame({
   "Threat Score": [
       0.1,
       0.2,
       0.4,
       0.7,
       0.9,
       0.95
   ]
})

st.line_chart(chart_data)

st.markdown("---")

# =========================================
# FOOTER
# =========================================

st.success("✅ Threat Detection System Running Successfully")