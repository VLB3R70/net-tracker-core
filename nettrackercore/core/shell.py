import signal

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

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

    def scanner(self):
        sc = Scanner()
        # mapeo las posibles opciones y valores predeterminados
        options = {"TARGET": "localhost", "PORT": None, "OTHER": None, "SILENT": False, "TCP": False, "UDP": False,
                   "OS": False, "SUDO": False}

        while True:
            option = Prompt.ask(PROMPT + "([bold red]scanner[/bold red])")
            if option == "exit":
                console.print("\n[magenta][bold]Goodbye! 👋")
                exit(0)
            elif option == "tracker":
                self.tracker()
            elif option.startswith("set"):
                option = option.split()
                if option[1] in options.keys():
                    options[option[1]] = str(option[2])
            elif option.startswith("get"):
                option = option.split()
                if option[1] in options.keys():
                    print(f"[cyan]{option[1]}[/cyan]\t\t {options.get(option[1])}")
                elif option[1] == 'ALL':
                    for key, value in options.items():
                        print(f"[cyan]{key}[/cyan]\t\t {value}")
            elif option == "scan":
                if options["SILENT"]:
                    options["OTHER"] += "-sS "
                elif options["TCP"]:
                    options["OTHER"] += "-sT "
                elif options["UDP"]:
                    options["OTHER"] += "-sU "
                elif options["OS"]:
                    options["OTHER"] += "-O "

                with console.status("[bold green]Scanning[/bold green]"):
                    sc.scan(targets=options["TARGET"], ports=options["PORT"], params=options["OTHER"],
                            sudo=options["SUDO"])

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
