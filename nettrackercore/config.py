import gettext
import json
from pathlib import Path


class Configuration:
    MAIN_DIR = Path.home().joinpath('.nettracker')
    LOCALES_DIR = Path(__file__).parent.joinpath('locales')
    CONFIG_FILE = MAIN_DIR.joinpath('config.json')

    def __init__(self, lang='es'):
        self.load_config(lang)

    def load_config(self, lang):
        self.create_directories()
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                self.data = json.load(f)
        else:
            self.CONFIG_FILE.touch()
            data = {'lang': lang, 'locales_dir': str(self.LOCALES_DIR), 'log_dir': str(self.MAIN_DIR.joinpath('logs')),
                    'temp_dir': str(self.MAIN_DIR.joinpath('temp'))}
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f)

    def create_directories(self):
        self.MAIN_DIR.mkdir(exist_ok=True)
        log_dir = Path(self.MAIN_DIR.joinpath('logs'))
        temp_dir = Path(self.MAIN_DIR.joinpath('temp'))
        log_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)


class Translator:
    def __init__(self, config: Configuration = None):
        self.config = config
        self.translations = gettext.translation('messages', localedir=self.config.data['locales_dir'],
                                                languages=[self.config.data['lang']])
        self.translations.install()

    def translate(self, string):
        return self.translations.gettext(string)
