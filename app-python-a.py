import sys
import KSR as KSR


def dumpObj(obj):           # List all obj attributes and methods
    for attr in dir(obj):
        KSR.info("obj attr = %s" % attr)
        if (attr != "Status"):
            KSR.info(" type = %s\n" % type(getattr(obj, attr)))
        else:
            KSR.info("\n")
    return 1

def mod_init():
    KSR.info("===== from Python mod init\n")
    return kamailio()

class kamailio:
    def __init__(self):
        KSR.info('===== kamailio.__init__\n')
        self.usersState= ()

    def child_init(self, rank):
       # KSR.info('===== kamailio.child_init(%d)\n' % rank)
        return 0

    def ksr_request_route(self, msg):
        if  (msg.Method == "REGISTER"):
            KSR.info("REGISTER R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info("            To: " + KSR.pv.get("$tu") + " Contact:"+ KSR.hdr.get("Contact") +"\n")
            
            if(KSR.pv.get("$fd") != "acme.pt" ):
                KSR.info("Wrong domain for registration\n")
                KSR.sl.send_reply(403, "Forbidden: - Invalid domain")
                return -1
            
            self.usersState[KSR.pv.get("$fu")] = "Available"
            KSR.registrar.save('location', 0)
            KSR.info("User " + KSR.pv.get("$fu") + " is registered, saved and is available \n")
            return 1

        if (msg.Method == "INVITE"):                      
            KSR.info("INVITE R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info("        From: " + KSR.pv.get("$fu") + "\n")
            KSR.info("          To: " + KSR.pv.get("$tu") + "\n")
            
            if (KSR.pv.get("$td") == "acme.pt" & KSR.pv.get("$fd") == "acme.pt"):   # Check if To domain is a.pt
                if(KSR.registrar.lookup("location") != 1):
                    KSR.info("User " + KSR.pv.get("$fu") + " is not registered\n")
                    KSR.sl.send_reply(404, "User Not found")
                    return -1
                
                if (KSR.pv.get("$tu") == "sip:conference@acme.pt"):  # Special To-URI
                    KSR.pv.sets("$ru", "sip:conference@127.0.0.1:5090")
                    KSR.rr.record_route()
                    KSR.tm.t_relay()    # Relaying using transaction mode
                    
                    self.usersState[KSR.pv.get("$fu")] = "InConference"
                    KSR.info("User " + KSR.pv.get("$fu") + " is in conference\n")
                    return 1               
                
                if (KSR.registrar.lookup("location") == 1):  # Check if registered
                    KSR.info("  Lookup changed R-URI: " + KSR.pv.get("$ru") +"\n")
                    
                    if (self.usersState[KSR.pv.get("$tu")] == "Busy"):
                        KSR.info("User " + KSR.pv.get("$tu") + " is in call, redirecting to announcements server\n")
                        
                        self.usersState[KSR.pv.get("$fu")] = "Busy"
                        KSR.pv.sets("$ru", "sip:call_announcement@127.0.0.1:5091")
                        KSR.rr.record_route()
                        KSR.tm.t_relay()
                        KSR.info("User " + KSR.pv.get("$fu") + " is busy\n")
                        return 1
                    
                    if(self.usersState[KSR.pv.get("$tu")] == "InConference"):
                        KSR.info("User " + KSR.pv.get("$fu") + " is in conference, redirecting to announcements server\n")
                        
                        self.usersState[KSR.pv.get("$fu")] = "InConference"
                        KSR.pv.sets("$ru", "sip:conference_announcement@127.0.0.1:5092")
                        KSR.rr.record_route()
                        KSR.tm.t_relay()
                        KSR.info("User " + KSR.pv.get("$fu") + " is busy (can also join conference)\n")
                        return 1
                    
                    if(self.usersState[KSR.pv.get("$tu")] == "Available"):
                        KSR.info("User " + KSR.pv.get("$fu") + " is available, fowarding call\n")

                        self.usersState[KSR.pv.get("$fu")] = "Busy"
                        self.usersState[KSR.pv.get("$tu")] = "Busy"
                        KSR.tm.t_relay()
                        KSR.rr.record_route()
                        KSR.info("User " + KSR.pv.get("$fu") + " is in call with + " + KSR.pv.get("$tu") +"\n")
                        return 1
                    
            else:
                KSR.info("Wrong domain for invite\n")
                KSR.sl.send_reply(403, "Forbidden: - Invalid domain")
                return -1
            

        if (msg.Method == "ACK"):
            KSR.info("ACK R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.tm.t_relay()
            return 1

        if (msg.Method == "CANCEL"):
            KSR.info("CANCEL R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.registrar.lookup("location")
            KSR.tm.t_relay()
            return 1

        if (msg.Method == "BYE"):
            KSR.info("BYE R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.registrar.lookup("location")
            KSR.rr.loose_route()
            KSR.tm.t_relay()
            
            self.usersState[KSR.pv.get("$fu")] = "Available"
            self.usersState[KSR.pv.get("$tu")] = "Available"
            KSR.info("User " + KSR.pv.get("$fu") + " has ended the call with " + KSR.pv.get("$tu") + "they are both now available\n")
            
            # Additional behaviour for BYE - sending a MESSAGE Request
            if (KSR.pv.get("$fd") == "acme.pt"):
                KSR.pv.sets("$uac_req(method)", "MESSAGE")
                KSR.pv.sets("$uac_req(ruri)", KSR.pv.get("$fu")) # Send to ender
                KSR.pv.sets("$uac_req(turi)", KSR.pv.get("$fu"))
                KSR.pv.sets("$uac_req(furi)", "sip:kamailio@acme.pt")
                KSR.pv.sets("$uac_req(callid)", KSR.pv.get("$ci")) # Keep the Call-ID
                msg = "You have ended a call"
                hdr = "Content-Type: text/plain\r\n" # More headers can be added
                KSR.pv.sets("$uac_req(hdrs)", hdr)
                KSR.pv.sets("$uac_req(body)", msg)
                KSR.uac.uac_req_send()
            return 1

        if (msg.Method == "MESSAGE"):
            KSR.info("MESSAGE R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info("        From: " + KSR.pv.get("$fu") + " To:"+ KSR.pv.get("$tu") +"\n")
            if (KSR.pv.get("$rd") == "acme.pt"):
                if (KSR.registrar.lookup("location") == 1):
                    KSR.info("  lookup changed R-URI: " + KSR.pv.get("$ru") +"\n")
                    KSR.tm.t_relay()
                else:
                    KSR.sl.send_reply(404, "Not found")
            else:
                KSR.rr.loose_route()
                KSR.tm.t_relay()
            return 1
        
        if (msg.Method == "INFO"):
            if (self.usersState[KSR.pv.get("$fu")] == "InConference"):
                KSR.info("User " + KSR.pv.get("$fu") + " sent INFO message\n")
                
                dtmf_body = KSR.pv.get("$rb")
                
                print("DTMF body is: " + dtmf_body + "\n")
                
                if (dtmf_body.split()[0] == "Signal=0"):
                    KSR.info("User " + KSR.pv.get("$fu") + " is in conference_announcement server wants to join the conference, now redirecting\n")
                    KSR.pv.sets("$uac_rq(method)", "INVITE")
                    KSR.pv.sets("$uac_req(ruri)", KSR.pv.get("$fu"))
                    KSR.pv.sets("$uac_req(turi)", KSR.pv.get("$fu"))
                    KSR.pv.sets("$uac_req(furi)", "sip:conference_announcement@127.0.0.1:5092")
                    KSR.pv.sets("$uac_req(callid)", KSR.pv.get("$ci"))
                    
                    contact_value = "<sip:" + KSR.pv.get("$fu") + "@" + KSR.pv.get("$fd") + ">"
                    hdr = "Contact: " + contact_value + "\r\n"
                    KSR.pv.sets("$uac_req(hdrs)", hdr)
                    KSR.uac.uac_req_send()
                    return 1
                
                KSR.info("No action for DTMF received\n")
                return -1
            else:
                KSR.info("User " + KSR.pv.get("$fu") + " is not in conference, no available DTMF service\n")
                return -1
                

    def ksr_reply_route(self, msg):
        KSR.info("===== response - from kamailio python script\n")
        KSR.info("      Status is:"+ str(KSR.pv.get("$rs")) + "\n")
        
        code_replied = int(KSR.pv.get("$rs"))
        KSR.info("Retrieve status code is: "+ str(code_replied) + "\n")
        
        if (code_replied >= 404 and code_replied <= 499):
            KSR.info("Call didn't happen\n")
            
            self.usersState[KSR.pv.get("$fu")] = "Available"
            self.usersState[KSR.pv.get("$tu")] = "Available"
            KSR.info("User " + KSR.pv.get("$fu") + " and " + KSR.pv.get("$tu") + " are now available\n")
            
            KSR.tm.t_release()
            return 1
        
        return 1

    def ksr_onsend_route(self, msg):
        return 1

    def ksr_onreply_route_INVITE(self, msg):
        return 0
 
    def ksr_failure_route_INVITE(self, msg):
        return 1
