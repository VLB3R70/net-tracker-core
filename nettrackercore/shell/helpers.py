from rich import print
from rich.markdown import Markdown


class Helper:
    @staticmethod
    def print_main_help():
        prompt = """
## Comandos de uso
        
- **help** - Muestra este menú de ayuda
- **scanner** - Crea un nuevo objeto Scanner. Es necesario para escanear la red y/o dispositivos
- **tracker** - Crea un nuevo objeto Tracker. Es necesario para monitorizar los paquetes de la red
        
"""
        print(Markdown(prompt))

    @staticmethod
    def print_scan_help():
        prompt = """
## Comandos de uso
- **help** - Muestra este mensaje de ayuda
- set [OPTION] - Establece los parámetros de la red y/o dispositivos que se escanearán
- get [OPTION] | ALL - Obtiene el valor del parámetro solicitado o de todos (ALL) 
- scan - Realiza el escaneo de la red y/o dispositivos establecidos."""

        print(Markdown(prompt))
