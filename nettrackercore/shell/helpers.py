from rich import print
from rich.markdown import Markdown

from nettrackercore.config import Translator

translator = Translator()

class Helper:
    """
    La clase **Helper** se encarga de añadir funciones para mostrar las ayudas de los comandos disponibles en la
    terminal. Usando :py:class:`rich.markdown.Markdown` se pueden mostrar las ayudas en formato
    `Markdown <https://www.markdownguide.org/getting-started/>`_ para que las ayudas sean más legibles.
    """

    @staticmethod
    def print_main_help():
        """
        Este método muestra la ayuda principal del programa en formato Markdown. A esta ayuda se accede en el principio
        del programa. Esta ayuda muestra los 3 comandos principales: **scanner** para acceder al escáner, **dba** para
        acceder al administrador de base de datos y **help** para mostrar el propio mensaje de ayuda.
        """
        prompt = translator._("""
# Comandos de uso
        
- **help** - Muestra este menú de ayuda
- **scanner** - Crea un nuevo objeto Scanner. Es necesario para escanear la red y/o dispositivos
- **dba** - Crea un nuevo objeto DBA. Es necesario para consultar la base de datos
        
""")
        print(Markdown(prompt))

    @staticmethod
    def print_scan_help():
        """
        Este método muestra la ayuda sobre el escáner en formato Markdown. A esta ayuda se accede desde el escáner y
        muestra los comandos posibles. Los comandos posibles son: **set** para establecer el valor de una opción, **get**
        para obtener los valores de una opción, **scan** para realizar el escaneo con las opciones asignadas y **help**
        para mostrar el mensaje de ayuda.
        """
        prompt = translator._("""
# Comandos de uso
- **help** - Muestra este mensaje de ayuda
- **set <opción> <valor>**- Establece los parámetros de la red y/o dispositivos que se escanearán con el valor introducido
- **get <opción> | ALL** - Obtiene el valor del parámetro solicitado o de todos (ALL) 
- **scan** - Realiza el escaneo de la red y/o dispositivos establecidos.

## Opciones válidas

- **TARGET** - Objetivo de la red y/o dispositivos que corresponde a una dirección IP válida.
- **PORT** - Puertos que se escanearán en todos los dispositivos asignados.
- **OTHER** - Otros parámetros aceptados por Nmap.
- **SILENT** - Parámetro que establece si el escaneo es silencioso o no.
- **TCP** - Establece el protocolo de escaneo en TCP.
- **UDP** - Establece el protocolo de escaneo en UDP.
- **OS** - Parámetro que permite la obtención del sistema operativo del dispositivo escaneado.
- **SUDO** - Válido solo para UNIX/Linux. Ciertos parámetros necesitan permisos de superusuario para poder ejecutarse

## Ejemplos de uso

`set TARGET 192.168.1.0/24` Para escanear una red completa o `set TARGET 192.168.1.1 192.168.1.100` para escanear solo 
dos dispositivos

`set OS True` Las opciones SILENT, TCP, UDP, OS y SUDO son valores booleanos.

`get target` Obtiene solo el objetivo del escaneo.

`get all` Obtiene todos los parámetros.""")

        print(Markdown(prompt))

    @staticmethod
    def print_dba_help():
        """
        Este método muestra la ayuda sobre el DBA en formato Markdown. A esta ayuda se accede desde el objeto **DBA** y
        muestra los comandos posibles del objeto.
        """
        prompt = translator._("""
## Comandos de uso
- **help** - Muestra este mensaje de ayuda
- **get networks** - Muestra todas las redes de la base de datos en forma de tabla.
- **get network <nombre>** - Muestra la información de una red determinada en forma de tabla.
- **list devices <nombre>** - Muestra los dispositivos de una red concreta en forma de tabla
- **list services** - Muestra los servicios de un dispositivo en una red concreta en forma de tabla. 
    La dirección y nombre de la red se piden al usuario.""")
        print(Markdown(prompt))
