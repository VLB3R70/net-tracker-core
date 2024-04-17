import signal

from nettrackercore.core.results import JSONResult
from rich import print
from rich.console import Console
from rich.prompt import Prompt

from .helpers import Helper
from ..core.scanner import Scanner

console = Console()

PROMPT = "[underline]net-tracker[/underline]"
SCANNER_PROMPT = PROMPT + "([bold red]scanner[/bold red])"
TRACKER_PROMPT = PROMPT + "([bold red]tracker[/bold red])"


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

    def set_options(self, options, option, value):
        options[option] = str(value)

    def get_options(self, options, option):
        if option.upper() in options.keys():
            print(f"[cyan]{option.upper()}[/cyan]\t\t {options.get(option)}")
        elif option.upper() == 'ALL':
            for key, value in options.items():
                print(f"[cyan]{key}[/cyan]\t\t {value}")

    def build_params(self, options):
        if options["SILENT"]:
            options["OTHER"] += "-sS "
        elif options["TCP"]:
            options["OTHER"] += "-sT "
        elif options["UDP"]:
            options["OTHER"] += "-sU "
        elif options["OS"]:
            options["OTHER"] += "-O "

        return options["OTHER"]

    def save_scan(self, scan_result: JSONResult, options):
        if "/" in options["TARGET"]:
            console.print("The system detected the target as a network.")
            address, netmask = options["TARGET"].split("/")
            network_name = Prompt.ask("Please provide a name to identify your network")
            console.print(scan_result)
            console.print(f"[cyan]{address}[/cyan]")
            console.print(f"[cyan]{netmask}[/cyan]")
            console.print(f"[cyan]{network_name}[/cyan]")

    def scanner(self):
        sc = Scanner()
        # mapeo las posibles opciones y valores predeterminados
        options = {"TARGET": "localhost", "PORT": "", "OTHER": "", "SILENT": False, "TCP": False, "UDP": False,
                   "OS": False, "SUDO": False}

        while True:
            option = Prompt.ask(SCANNER_PROMPT)
            if option == "exit":
                console.print("\n[magenta][bold]Goodbye! 👋")
                exit(0)
            elif option == "tracker":
                self.tracker()
            elif option.startswith("set"):
                _, key, value = option.split()
                if key.upper() in options.keys():
                    self.set_options(options, key.upper(), value)
            elif option.startswith("get"):
                option = option.split()
                self.get_options(options, option[1])
            elif option == "scan":
                with console.status("[bold green]Scanning[/bold green]", spinner="aesthetic"):
                    params = self.build_params(options)
                    result = sc.scan(targets=options["TARGET"], ports=options["PORT"], params=params,
                                     sudo=options["SUDO"])

                console.print("[green]Successfully scanned target[/green]")
                save = Prompt.ask("[blue]Save scan [Y/n][/blue]")
                if save.lower() == "y":
                    self.save_scan(result, options)
            elif option == "help":
                Helper.print_scan_help()

    def tracker(self):
        while True:
            option = Prompt.ask(TRACKER_PROMPT)
            if option == "exit":
                exit(0)
            elif option == "scanner":
                self.scanner()

    def main_menu(self):
        print(self.LOGO)
        while True:
            option = Prompt.ask(PROMPT)
            if option == "help":
                Helper.print_main_help()
            elif option == "scanner":
                self.scanner()
            elif option == "tracker":
                self.tracker()
            elif option == "exit":
                exit(0)
