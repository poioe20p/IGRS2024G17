import KSR as KSR

def mod_init():
    KSR.info("===== from Python mod init\n")
    return kamailio()

class kamailio:
    def __init__(self):
        KSR.info('===== kamailio.__init__\n')

    def child_init(self, rank):
        KSR.info('===== kamailio.child_init(%d)\n' % rank)
        return 0

    def ksr_request_route(self, msg):
        # Bloquear pedidos cuja origem não pertence ao domínio acme.pt
        if KSR.pv.get("$fd") != "acme.pt":
            KSR.info("Bloqueando origem fora do domínio acme.pt\n")
            KSR.sl.send_reply(403, "Forbidden: Invalid Source Domain")
            return 1

        # Garantir que o domínio do destino é acme.pt
        if KSR.pv.get("$td") != "acme.pt":
            KSR.info("Destino fora do domínio acme.pt\n")
            KSR.sl.send_reply(403, "Forbidden: Invalid Destination Domain")
            return 1

        # Processamento de REGISTER
        if msg.Method == "REGISTER":
            KSR.info("REGISTER R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.registrar.save('location', 0)
            return 1

        # Processamento de INVITE
        if msg.Method == "INVITE":
            KSR.info("INVITE R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.info(" From: " + KSR.pv.get("$fu") + " To: " + KSR.pv.get("$tu") + "\n")

            # Verificar se o destino está registado
            if KSR.registrar.lookup("location") == 1:
                KSR.info("Destino registado. Reencaminhando o pedido.\n")
                KSR.tm.t_relay()
            else:
                KSR.info("Destino não registado. Respondendo ao remetente.\n")
                KSR.sl.send_reply(404, "User Not Registered")
            return 1

        # Outros métodos como ACK, BYE, CANCEL são apenas reencaminhados
        if msg.Method in ["ACK", "BYE", "CANCEL"]:
            KSR.info(f"{msg.Method} R-URI: " + KSR.pv.get("$ru") + "\n")
            KSR.tm.t_relay()
            return 1

        # Mensagem não tratada
        KSR.info("Método não suportado: " + msg.Method + "\n")
        KSR.sl.send_reply(405, "Method Not Allowed")
        return 1

    def ksr_reply_route(self, msg):
        KSR.info("===== response - from kamailio python script\n")
        KSR.info(" Status is:" + str(KSR.pv.get("$rs")) + "\n")
        return 1

    def ksr_onsend_route(self, msg):
        KSR.info("===== onsend route - from kamailio python script\n")
        return 1