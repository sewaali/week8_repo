import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_logs(n=1000):
   logs = []
   base_time = datetime.now()

   for i in range(n):
       timestamp = base_time + timedelta(seconds=i*5)

       ip = f"192.168.1.{random.randint(1,50)}"
       action = random.choice(["login", "request", "logout"])
       status = random.choice(["success", "fail"])

       # Inject anomalies
       if random.random() < 0.1:
           status = "fail"
           action = "login"

       logs.append({
           "timestamp": timestamp,
           "ip": ip,
           "action": action,
           "status": status
       })

   return pd.DataFrame(logs)

if __name__ == "__main__":
   os.makedirs("../data", exist_ok=True)
   df = generate_logs()
   df.to_csv("../data/logs.csv", index=False)
   print("Logs generated ✅")