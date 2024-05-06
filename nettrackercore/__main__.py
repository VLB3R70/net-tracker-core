from nettrackercore.config import Translator, Configuration
from nettrackercore.shell.shell import Shell


def main():
    config = Configuration()
    translator = Translator(config)
    sh = Shell(translator, config)
    sh.main_menu()


if __name__ == '__main__':
    main()
