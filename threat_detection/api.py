from flask import Flask, request, render_template_string
import pandas as pd
import joblib
import os

from feature_engineering import build_features
from agents import run_agents

app = Flask(__name__)

# =========================================
# PATHS
# =========================================

BASE_DIR = os.path.dirname(
   os.path.dirname(
       os.path.abspath(__file__)
   )
)

model_path = os.path.join(
   BASE_DIR,
   "model",
   "model.pkl"
)

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load(model_path)

# =========================================
# MAIN PAGE
# =========================================

@app.route("/", methods=["GET", "POST"])
def home():

   output = None

   if request.method == "POST":

       ip = request.form["ip"]
       action = request.form["action"]
       status = request.form["status"]

       # =====================================
       # SAMPLE LOG
       # =====================================

       sample_data = [
           {
               "timestamp": "2026-01-01 10:00:00",
               "ip": ip,
               "action": action,
               "status": status
           }
       ]

       # dataframe
       df = pd.DataFrame(sample_data)

       # feature engineering
       features = build_features(df)

       X = features[[
           "failed_logins",
           "request_count"
       ]]

       # model prediction
       prediction = model.predict(X)[0]

       # =====================================
       # THREAT LOGIC
       # =====================================

       suspicious_ips = [
           "10.0.0.1",
           "10.0.0.2",
           "10.0.0.3"
       ]

       is_anomaly = False

       # failed login attack
       if action == "login" and status == "fail":
           is_anomaly = True

       # suspicious IP
       if ip in suspicious_ips:
           is_anomaly = True

       result = {
           "anomaly": is_anomaly
       }

       # agents
       output = run_agents(result)

   # =====================================
   # HTML UI
   # =====================================

   html = f"""

<html>

<head>

<title>Threat Detection Dashboard</title>

<style>

           body {{
               background-color: #0f172a;
               color: white;
               font-family: Arial;
               padding: 40px;
           }}

           .container {{
               width: 70%;
               margin: auto;
           }}

           .card {{
               background: #1e293b;
               padding: 25px;
               border-radius: 10px;
               margin-bottom: 20px;
           }}

           input, select {{
               width: 100%;
               padding: 12px;
               margin-top: 10px;
               margin-bottom: 20px;
               border-radius: 5px;
               border: none;
           }}

           button {{
               background: #ef4444;
               color: white;
               padding: 12px 20px;
               border: none;
               border-radius: 5px;
               cursor: pointer;
               font-size: 16px;
           }}

           button:hover {{
               background: #dc2626;
           }}

           .danger {{
               color: #ff4d4d;
               font-size: 22px;
               font-weight: bold;
           }}

           .safe {{
               color: #22c55e;
               font-size: 22px;
               font-weight: bold;
           }}

</style>

</head>

<body>

<div class="container">

<h1>🛡 Threat Intelligence Dashboard</h1>

<div class="card">

<h2>🔍 Detect Threat</h2>

<form method="POST">

<label>IP Address</label>

<input
                       type="text"
                       name="ip"
                       placeholder="Enter IP Address"
                       required
>

<label>Action</label>

<select name="action">

<option value="login">
                           login
</option>

<option value="request">
                           request
</option>

<option value="logout">
                           logout
</option>

</select>

<label>Status</label>

<select name="status">

<option value="success">
                           success
</option>

<option value="fail">
                           fail
</option>

</select>

<button type="submit">
                       🚨 Detect Threat
</button>

</form>

</div>

   """

   # =====================================
   # RESULTS
   # =====================================

   if output:

       if output["detection"]["anomaly"]:

           alert_class = "danger"

       else:

           alert_class = "safe"

       html += f"""

<div class="card">

<h2>Detection Result</h2>

<p class="{alert_class}">
               {output["report"]}
</p>

<p>
<strong>Threat Level:</strong>
               {output["alert"]["threat_level"]}
</p>

<p>
<strong>Recommended Action:</strong>
               {output["alert"]["recommended_action"]}
</p>

</div>

       """

   html += """

</div>

</body>

</html>
   """

   return render_template_string(html)

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

   app.run(debug=True)