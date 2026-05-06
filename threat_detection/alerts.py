def generate_alert(analysis):
   if "failed login" in analysis.lower():
       level = "HIGH"
   else:
       level = "LOW"

   return {
       "threat_level": level,
       "description": analysis,
       "recommended_action": "Block IP or enable MFA" if level == "HIGH" else "No action needed"
   }