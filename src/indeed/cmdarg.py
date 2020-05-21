import os, re
from termcolor import colored



class CmdArg():
    USR_ERROR = -1
    ARG_ERROR = -2
    global usrArg
    global cmdArg

    def __init__(self, usrArg, cmdArg):
        self.usrArg = usrArg[1:]
        self.cmdArg = cmdArg

    def check(self, error):
        ret = self.printUserError()
        if ret == -1:
            return ret
        values = []
        ret = self.getValues(error, values)
        #self.setBools(values)
        return values if len(ret) <= 0 else ret

    def setBools(self, values):
        for short in self.usrArg:
            #print(short)
            found = False
            if len(short) == 1:
                for (arg, val) in values:
                    if re.search("^"+short+"$", arg):
                        found = True
                        break
                if found == False:
                    values[short] = False

    def getValues(self, error, values):
        values = {}
        for arg in self.usrArg:
            _el = [usrShort for usrShort in self.cmdArg]
            values[re.search("^[^=]*", arg)[0]] = re.search("[^=]+$",arg)[0]
            if re.search("^[^=]*", arg)[0] in _el:
                continue
            else:
                #print(colored("KO " + arg, "red"))
                error.append(re.search("^[^=]*", arg)[0])

        return values, [-2, error]
        """for arg in self.cmdArg:
            print(arg)
            arg_found = False
            for usrShort in self.usrArg:
                #print(colored(usrShort, 'blue'))
                if re.search("#\+.$#", usrShort):
                    _del = re.search("#^.\+#", usrShort)
                if re.search("^.", arg)[0] == self.cmdArg.index(arg):
                    arg_found = True
                    print("is T", arg_found)
                    if arg.find("="):
                        val = re.search("[^=]*$", arg)[0]
                        #print(val)
                    break
            #if arg_found == False:
            #    print("is F",arg_found)
            #    notFoundArg = arg
        try:
            error = notFoundArg
            return error
        except:
            return -2"""

    def printUserError(self):
        e = False
        for longArg in self.usrArg:
            """if re.search("^[a-zA-Z](:|(\+.))?$",longArg):
                e = True
                print(colored("Caretere illicite argument court ", "red"), longArg)"""
            if re.search("#^(\#|[a-zA-Z]+)$#", longArg):
                e = True
                print(colored("Caretere illicite argument long ", "red"), longArg)
            if e:
                return USR_ERROR
            return True
