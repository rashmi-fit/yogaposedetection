
class MSGBUILDER:
    def __init__(self, system_msg):
        self.system_msg = system_msg

    def construct_msg(self,user_msg):
        message = [{"role":"system","content":self.system_msg},
                   {"role":"user","content":user_msg}]

        return message