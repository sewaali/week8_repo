from flask import Flask, jsonify
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
# HOME PAGE
# =========================================

@app.route("/")
def home():

   return """
<h1> Threat Detection API Running ✅</h1>

<h3>Available Pages:</h3>

<ul>
<li>
<a href="/test">/test</a>
           → Run Threat Detection
</li>
</ul>
   """

# =========================================
# TEST PAGE (JSON OUTPUT)
# =========================================

@app.route("/test")
def test():

   # suspicious sample log
   sample_data = [
       {
           "timestamp": "2026-01-01 10:00:00",
           "ip": "10.0.0.1",
           "action": "login",
           "status": "fail"
       }
   ]

   # dataframe
   df = pd.DataFrame(sample_data)

   # features
   features = build_features(df)

   X = features[[
       "failed_logins",
       "request_count"
   ]]

   # prediction
   prediction = model.predict(X)[0]

   result = {
       "anomaly": bool(prediction == -1)
   }

   # agents
   output = run_agents(result)

   return jsonify(output)

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

   app.run(debug=True)