import pandas as pd

def build_features(df):
   df['timestamp'] = pd.to_datetime(df['timestamp'])

   # Failed logins per IP
   failed = df[df['status'] == 'fail'].groupby('ip').size()

   # Total requests per IP
   requests = df.groupby('ip').size()

   features = pd.DataFrame({
       "failed_logins": failed,
       "request_count": requests
   }).fillna(0)

   return features.reset_index()