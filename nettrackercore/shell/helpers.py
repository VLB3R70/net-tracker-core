from rich import print
from rich.markdown import Markdown

from nettrackercore.config import Translator, Configuration

config = Configuration()
translator = Translator(config)

class Helper:
    @staticmethod
    def print_main_help():
        prompt = translator._("""
## Comandos de uso
        
- **help** - Muestra este menú de ayuda
- **scanner** - Crea un nuevo objeto Scanner. Es necesario para escanear la red y/o dispositivos
- **dba** - Crea un nuevo objeto DBA. Es necesario para consultar la base de datos
        
""")
        print(Markdown(prompt))

    @staticmethod
    def print_scan_help():
        prompt = translator._("""
## Comandos de uso
- **help** - Muestra este mensaje de ayuda
- set [OPTION] - Establece los parámetros de la red y/o dispositivos que se escanearán
- get [OPTION] | ALL - Obtiene el valor del parámetro solicitado o de todos (ALL) 
- scan - Realiza el escaneo de la red y/o dispositivos establecidos.""")

        print(Markdown(prompt))
