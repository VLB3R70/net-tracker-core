from rich import print
from rich.console import Console
from rich.prompt import Prompt

console = Console()


class Shell:
    LOGO = """[bold][magenta] _  _  ___  _____        _____  ___  ___   ___  _  __ ___  ___ 
| \| || __||_   _|      |_   _|| _ \/   \ / __|| |/ /| __|| _ \\
| .  || _|   | |          | |  |   /| - || (__ |   < | _| |   /
|_|\_||___|  |_|          |_|  |_|_\|_|_| \___||_|\_\|___||_|_\\
"""

    def help(self):
        pass

    def run(self, args):
        pass

    def scanner(self):
        pass

    def tracker(self):
        pass

    def main_menu(self):
        option = ""
        print(self.LOGO)
        while True:
            option = Prompt.ask(f"[underline]net-tracker[/underline] ([bold][red]{option}[/red][/bold]) ")
            if option == "help":
                self.help()
            elif option == "scanner":
                self.scanner()
            elif option == "tracker":
                self.tracker()


shell = Shell()
shell.main_menu()
