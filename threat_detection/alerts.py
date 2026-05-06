def generate_alert(message, threat_level):

   if threat_level == "HIGH":

       recommended_action = (
           "Block IP address and enable MFA"
       )

   else:

       recommended_action = (
           "No action needed"
       )

   return {
       "threat_level": threat_level,
       "description": message,
       "recommended_action": recommended_action
   }