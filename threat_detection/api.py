from flask import Flask, render_template_string
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

@app.route("/")
def home():

   # Sample suspicious log
   sample_data = [
       {
           "timestamp": "2026-01-01 10:00:00",
           "ip": "10.0.0.1",
           "action": "login",
           "status": "fail"
       }
   ]

   # Convert to dataframe
   df = pd.DataFrame(sample_data)

   # Feature engineering
   features = build_features(df)

   X = features[[
       "failed_logins",
       "request_count"
   ]]

   # Prediction
   prediction = model.predict(X)[0]

   result = {
       "anomaly": bool(prediction == -1)
   }
   output = run_agents(result)

   # =====================================
   # HTML PAGE
   # =====================================

   html = f"""
<html>

<head>
<title>Threat Detection Dashboard</title>

<style>

           body {{
               font-family: Arial;
               background-color: #0f172a;
               color: white;
               padding: 40px;
           }}

           .card {{
               background: #1e293b;
               padding: 20px;
               border-radius: 10px;
               margin-bottom: 20px;
           }}

           .danger {{
               color: red;
               font-size: 22px;
               font-weight: bold;
           }}

           table {{
               width: 100%;
               border-collapse: collapse;
           }}

           th, td {{
               border: 1px solid gray;
               padding: 10px;
               text-align: center;
           }}

           th {{
               background-color: #334155;
           }}

</style>

</head>

<body>

<h1>🛡 Threat Intelligence Dashboard</h1>

<div class="card">
<h2>Threat Detection Result</h2>

<p class="danger">
               🚨 {output["analysis"]}
</p>

<p>
               Threat Level:
<strong>
                   {output["alert"]["threat_level"]}
</strong>
</p>

<p>
               Recommended Action:
<strong>
                   {output["alert"]["recommended_action"]}
</strong>
</p>
</div>

<div class="card">

<h2>📡 Suspicious Activity</h2>

<table>

<tr>
<th>IP Address</th>
<th>Action</th>
<th>Status</th>
</tr>

<tr>
<td>10.0.0.1</td>
<td>login</td>
<td>fail</td>
</tr>

</table>

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