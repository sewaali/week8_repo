from alerts import generate_alert

def detector_agent(result):
   return result

def analyzer_agent(result):
   if result["anomaly"]:
       return "Multiple failed login attempts detected"
   return "Normal behavior"

def reporter_agent(analysis):
   return f" ALERT: {analysis}"

def run_agents(result):
   detection = detector_agent(result)
   analysis = analyzer_agent(detection)
   report = reporter_agent(analysis)
   alert = generate_alert(analysis)

   return {
       "detection": detection,
       "analysis": analysis,
       "report": report,
       "alert": alert
   }