import os
from sys import argv
from termcolor import colored
from cmdarg import CmdArg


class Menu():
    
    #def __init__(self):
        #arg == self.men(arg)

    def men(self, arg):
        if len(argv) == 1 or len(argv) <= 1:
            mandatoryArg = colored("?", "green", attrs=["bold"])
            print(colored("                            Mode d'emploi :                                \n\n", "red", attrs=['bold', 'reverse'])
            + colored(os.getcwd(), "red", attrs=["bold"])+ 
            " [" + colored("-a", "red") + "=" + colored("\"yes/no\"", "yellow") +"]"+ 
            " [" + colored("-s", "red") + "=" + colored("\"yes/no\"", "yellow") +"]"+ 
            " [" + colored("-j", "red") + "=" + colored("\"job name\"", "yellow" ) + "]"+
            " [" + colored("-c", "red") + "=" + colored("\"city name\"", "yellow" ) + "]\n\n" 

            + colored("Arguments : \n\n", "green")
            
            + colored("  -a  / --all", "cyan") + "              : get all in config.json " + colored("(string) \n", "blue")
            + colored("  -s  / --specific", "cyan") + "         : specific if you wan't only one " + colored("(string) \n", "blue")
            + colored("  -j / --job_name", "cyan") + "          : job name you want " + colored("(string) \n", "blue")
            + colored("  -c / --city_name", "cyan") + "         : city name you want " + colored("(string) \n", "blue")
            )
            exit()
        error = []
        cmdarg = CmdArg(argv, arg)
        args = cmdarg.check(error)
        if len(error) > 0:
            for e in error:
                print(colored("The argument " +e+" is incorect", "red"))
            exit()
        return args[0]
