import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os
from feature_engineering import build_features

def train():
   df = pd.read_csv("../data/logs.csv")

   features = build_features(df)

   X = features[["failed_logins", "request_count"]]

   model = IsolationForest(contamination=0.1, random_state=42)
   model.fit(X)

   features["anomaly"] = model.predict(X)

   os.makedirs("../model", exist_ok=True)
   joblib.dump(model, "../model/model.pkl")

   print("Model trained & saved ✅")
   print(features.head())

if __name__ == "__main__":
   train()