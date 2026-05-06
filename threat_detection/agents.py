from alerts import generate_alert

# =========================================
# DETECTOR AGENT
# =========================================

def detector_agent(result):

   return result

# =========================================
# ANALYZER AGENT
# =========================================

def analyzer_agent(result):

   if result["anomaly"]:

       return {
           "message": "🚨 Suspicious activity detected",
           "threat_level": "HIGH"
       }

   else:

       return {
           "message": "✅ Normal activity detected",
           "threat_level": "LOW"
       }

# =========================================
# REPORTER AGENT
# =========================================

def reporter_agent(analysis):

   return analysis["message"]

# =========================================
# RUN ALL AGENTS
# =========================================

def run_agents(result):

   detection = detector_agent(result)

   analysis = analyzer_agent(detection)

   report = reporter_agent(analysis)

   alert = generate_alert(
       analysis["message"],
       analysis["threat_level"]
   )

   return {
       "detection": detection,
       "analysis": analysis["message"],
       "report": report,
       "alert": alert
   }