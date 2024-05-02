from nettrackercore.config import Translator, Configuration
from nettrackercore.shell.shell import Shell


def main():
    config = Configuration()
    translator = Translator(config)
    shell = Shell(translator)
    shell.main_menu()


if __name__ == '__main__':
    main()
