import gettext
import json
from pathlib import Path


class Configuration:
    """
    La clase **Configuration** representa la configuración del programa. Este objeto obtiene la información de la
    lectura de un fichero de tipo JSON donde se almacena toda la información para el correcto funcionamiento del programa.

    Se establecen tres constantes que determinan el directorio principal donde se almacena el fichero de configuración,
    el directorio de las traducciones y la ruta del propio fichero de configuración.

    Se ha creado el objeto mediante el patrón de diseño Singleton para así tener instanciado solo un objeto durante toda
    la vida del programa.
    """
    _instance = None

    MAIN_DIR = Path.home().joinpath('.nettracker')
    LOCALES_DIR = Path(__file__).parent.joinpath('locales')
    CONFIG_FILE = MAIN_DIR.joinpath('config.json')

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, lang='es'):
        if self._initialized:
            return
        self._initialized = True
        self.data = self.load_config(lang)

    def load_config(self, lang):
        """
        Este método es el encargado de cargar la configuración del programa. Los datos que el programa necesita son:

        - El idioma del mismo. Por ahora solo permite español o inglés.
        - El directorio donde se almacenarán los ficheros de traducción.
        - El directorio donde se almacenarán los ficheros de log.
        - El directorio donde se almacenará el fichero temporal necesario para la lógica del programa.

        Antes de cargar esta configuración primero se deben de crear los directorios si no existen haciendo una llamada
        al método :py:func:`~nettrackercore.config.load_config`.

        Si el fichero de configuración existe previamente se carga la configuración y si no existe se crea y se escribe
        una configuración predeterminada.

        :param lang: Es el idioma elegido por el usuario. De forma predeterminada el idioma es el español.
        :type lang: str
        """
        self.create_directories()
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            self.CONFIG_FILE.touch()
            data = {'lang': lang, 'locales_dir': str(self.LOCALES_DIR), 'log_dir': str(self.MAIN_DIR.joinpath('logs')),
                    'temp_dir': str(self.MAIN_DIR.joinpath('temp'))}
            with open(self.CONFIG_FILE, 'w') as f:
                return json.dump(data, f)

    def create_directories(self):
        """
        Este método se encarga de crear los directorios necesarios para el programa si no existen.
        """
        self.MAIN_DIR.mkdir(exist_ok=True)
        log_dir = Path(self.MAIN_DIR.joinpath('logs'))
        temp_dir = Path(self.MAIN_DIR.joinpath('temp'))
        log_dir.mkdir(exist_ok=True)
        temp_dir.mkdir(exist_ok=True)


class Translator:
    """
    El objeto **Translator** carga la configuración del idioma elegido por el usuario para el programa e instala dicho
    idioma en el contexto de la aplicación usando el módulo
    `gettext <https://docs.python.org/3/library/gettext.html#module-gettext>`_. Una vez instalado el idioma simplemente
    se debe de hacer una llamada al método :py:func:`~nettrackercore.translator.translate`.

    Este objeto se crea mediante el patrón de diseño Singleton para así asegurar que solo existe un objeto durante toda
    la vida del programa.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Configuration):
        if self._initialized:
            return
        self._initialized = True
        self.config = config
        self.translations = gettext.translation('messages', localedir=self.config.data["locales_dir"],
                                                languages=[self.config.data['lang']])
        self.translations.install()

    def translate(self, string):
        """
        Este método devuelve la traducción del mensaje pasado como parámetro.
        :param string: Identificador del mensaje que debe ser traducido.
        :type string: str
        :return: Se devuelve el mensaje traducido.
        :rtype: str
        """
        return self.translations.gettext(string)
