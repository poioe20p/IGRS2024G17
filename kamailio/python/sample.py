## Kamailio - equivalent of routing blocks in Python
import sys
import Router.Logger as Logger
import KSR as KSR
from concurrent import futures
import logging

import grpc

def dumpObj(obj):
    for attr in dir(obj):
        # KSR.info("obj.%s = %s\n" % (attr, getattr(obj, attr)));
        Logger.LM_INFO("obj.%s = %s\n" % (attr, getattr(obj, attr)));

# global function to instantiate a kamailio class object
# -- executed when kamailio app_python module is initialized
def mod_init():
    KSR.info("===== from Python mod init\n")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));
    return kamailio();

# -- {start defining kamailio class}
class kamailio:
    def __init__(self):
        KSR.info('===== kamailio.__init__\n');
    
    # executed when kamailio child processes are initialized
    def child_init(self, rank):
        KSR.info('===== kamailio.child_init(%d)\n' % rank);
        KSR.pv.sets("$uac_req(method)","INVITE");
        KSR.pv.sets("$uac_req(ruri)","sip:bob@127.0.0.1:6666");
        KSR.pv.sets("$uac_req(furi)","sip:kamailio.org");
        KSR.pv.sets("$uac_req(turi)","sip:bob@127.0.0.1:6666");
        KSR.pv.sets("$uac_req(callid)","my_call_id1");
        KSR.pv.sets("$uac_req(hdrs)","Contact: sip@server@127.0.0.1:5060");
        KSR.uac.uac_req_send();
        return 0

    # SIP request routing
    # -- equivalent of request_route{}
    def ksr_request_route(self, msg):
        KSR.info("===== request - from kamailio python script\n");
        KSR.info("===== method [%s] r-uri [%s]\n" % (KSR.pv.get("$rm"),KSR.pv.get("$ru")));
        #if KSR.pv.get("$rm") == "REGISTER":
        if KSR.is_REGISTER():
            KSR.registrar.save("location");		
            KSR.textops.set_reply_body("Test", "text/plain")
            KSR.sl.send_reply(200, "Great invite!")
            return 0
        KSR.sl.send_reply(200)
        return 0