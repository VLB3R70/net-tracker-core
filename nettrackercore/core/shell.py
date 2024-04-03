import signal

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

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

    def handler(self, signum=None, frame=None):
        console.print("\n[magenta][bold]Goodbye! 👋")
        exit(1)

    def help(self):
        markdown = Markdown(HELP)
        print(markdown)
        self.main_menu()

    def run(self, args):
        pass

    def scanner(self):
        while True:
            option = Prompt.ask(PROMPT + "([bold][red]scanner[/red][/bold])")
            if option == "exit":
                exit(0)
            elif option == "tracker":
                self.tracker()

    def tracker(self):
        while True:
            option = Prompt.ask(PROMPT + "([bold][red]tracker[/red][/bold])")
            if option == "exit":
                exit(0)
            elif option == "scanner":
                self.scanner()

    def main_menu(self):
        signal.signal(signal.SIGINT, self.handler)

        print(self.LOGO)
        option = Prompt.ask(PROMPT)
        if option == "help":
            self.help()
        elif option == "scanner":
            self.scanner()
        elif option == "tracker":
            self.tracker()
        elif option == "exit":
            exit(0)


shell = Shell()
shell.main_menu()
