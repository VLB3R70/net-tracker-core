import signal

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print

from .scanner import Scanner

console = Console()

HELP = """
# Comandos de uso

- `help` - Muestra este menú de ayuda
- `scanner` - Crea un nuevo objeto Scanner. Es necesario para escanear la red y/o dispositivos
- `tracker` - Crea un nuevo objeto Tracker. Es necesario para monitorizar los paquetes de la red

"""

PROMPT = "[underline]net-tracker[/underline]"


class Shell:
    LOGO = """[magenta] _  _  ___  _____        _____  ___  ___   ___  _  __ ___  ___ 
| \| || __||_   _|      |_   _|| _ \/   \ / __|| |/ /| __|| _ \\
| .  || _|   | |          | |  |   /| - || (__ |   < | _| |   /
|_|\_||___|  |_|          |_|  |_|_\|_|_| \___||_|\_\|___||_|_\\
"""

    def __init__(self):
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, signum=None, frame=None):
        console.print("\n[magenta][bold]Goodbye! 👋")
        exit(1)

    def help(self):
        markdown = Markdown(HELP)
        print(markdown)

    # se necesita optimizar esta parte del código
    def scanner(self):
        sc = Scanner()
        target = ""
        ports = ""
        other = ""
        silent = False
        tcp = False
        udp = False
        os = False
        sudo = False

        while True:
            option = Prompt.ask(PROMPT + "([bold red]scanner[/bold red])")
            if option == "exit":
                exit(0)
            elif option == "tracker":
                self.tracker()
            elif option.startswith("set"):
                option = option.split()
                if option[1] == "target":
                    target = str(option[2])
                elif option[1] == "ports":
                    ports = str(option[2])
                elif option[1] == "other":
                    other = str(option[2])
                elif option[1] == "silent":
                    silent = option[2]
                elif option[1] == "tcp":
                    tcp = option[2]
                elif option[1] == "udp":
                    udp = option[2]
                elif option[1] == "os":
                    os = option[2]
            elif option == "scan":
                if silent:
                    other += "-sS "
                elif tcp:
                    other += "-sT "
                elif udp:
                    other += "-sU "
                elif os:
                    other += "-O "
                    sudo = True

                sc.scan(targets=target, ports=ports, params=other, sudo=sudo)

    def tracker(self):
        while True:
            option = Prompt.ask(PROMPT + "([bold red]tracker[/bold red])")
            if option == "exit":
                exit(0)
            elif option == "scanner":
                self.scanner()

    def main_menu(self):
        print(self.LOGO)
        while True:
            option = Prompt.ask(PROMPT)
            if option == "help":
                self.help()
            elif option == "scanner":
                self.scanner()
            elif option == "tracker":
                self.tracker()
            elif option == "exit":
                exit(0)


# shell = Shell()
# shell.main_menu()
