import datetime
import os
import subprocess
from pathlib import Path

import xmltodict

from .exceptions import ExecutionError
from .parsers import NmapParser
from .results import JSONResult

DATE = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
MAIN_DIR = Path.home().joinpath('.nettracker')
LOG_DIR = Path.joinpath(MAIN_DIR, 'logs')
TEMP_DIR = Path.joinpath(MAIN_DIR, 'temp')

MAIN_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)


class Logger:
    """
    La clase **Logger** se encarga de escribir mensajes en los ficheros designados. Existen dos ficheros: uno de `log` y
    otro de errores. Estos ficheros se crean previamente.
    """

    @staticmethod
    def log(message, command):
        """
        Este método se encarga escribir un mensaje concreto en el log. Para añadir más información se escribe la fecha
        del día en el momento de la ejecución del programa.

        :param message: Mensaje a escribir dentro del log.
        """
        log_file = LOG_DIR.joinpath('scanner.log')
        with open(log_file, 'a') as log:
            log.write(f'[{DATE}]\n{command}\n{message}')

    @staticmethod
    def error(message):
        """
        Este método se encarga de escribir los mensajes de error en un log. Cuando ha ocurrido un error o se ha lanzado
        una excepción, la traza de dicho error o la salida estándar de error de un proceso se guarda en el log. En este
        formato también se guarda la fecha.
        """
        error_file = LOG_DIR.joinpath('err.log')
        with open(error_file, 'a') as log:
            log.write(f'[{DATE}]\n' + message + '\n')


class Scanner:
    """
    Objeto que representa un escáner. Este escáner se encarga de usar el paquete de Nmap previamente instalado en la
    máquina. El usuario establece ciertos parámetros que posteriormente serán usados por el paquete Nmap. Dichos
    parámetros son:

    - **targets**: puede ser una dirección de red en formato CIDR, una dirección o varias direcciones IP, etc.

    - **ports**: es un parámetro que establece los puertos que se escanearán, si no se establece nada se escanean todos.

    El formato de los puertos es:

        - `80` -> Solo se escanea el puerto 80
        - `80,443` -> Se escanean los puertos 80 y 443 únicamente
        - `1-1024` -> Solo se escanean los puertos comprendidos entre el 1 y el 1024

    - **params**: son otros parámetros permitidos por Nmap.

    """

    def __init__(self):
        self.temp_file = TEMP_DIR.joinpath('scanner.xml')
        self.temp_file.touch()  # Creo el fichero temporal vacío
        self.parser = NmapParser()

    def scan(self, targets=None, ports=None, params=None, sudo=False):
        """
        El método `scan` realiza el escaneo sobre los objetivos asignados usando el paquete Nmap. La salida estándar del
        comando se almacena de un fichero de log y el resultado del escaneo se encapsula en un objeto
        :py:class:`~nettrackercore.core.results.JSONResult`

        :param targets: Es la dirección IP hacia donde se hará el escaneo. Puede ser una dirección de red o una
            dirección de equipo.

        :param ports: Son los puertos hacia donde se hará el escaneo. Los puertos deben estar comprendidos entre el 1 y
            el 65535, ambos incluidos.

        :param params: Son parámetros opcionales introducidos por el usuario y aceptados por Nmap.

        :param sudo: Ciertos parámetros necesitan permisos de superusuario para ejecutarse.

        :type targets: str
        :type ports: str
        :type params: str
        :type sudo: bool
        :return: El resultado del escaneo se encapsula en un objeto :py:class:`~nettrackercore.core.results.JSONResult`.
        :rtype: JSONResult
        """
        command = self.parser.create_command(targets, ports, params, sudo, str(self.temp_file))
        print(command)
        output, err, code = self.execute_command(command)
        if err:
            Logger.error(err)
            raise ExecutionError(err)
        Logger.log(output, command)

        with open(self.temp_file, 'r') as file:
            json_data = xmltodict.parse(file.read())

        result = JSONResult(json_data)

        return result

    def execute_command(self, command):
        """
        Este método es el encargado de crear un subproceso y ejecutar el comando configurado por el usuario. La salida
        estándar y la salida de error se obtienen mediante un `pipe`; el código de retorno también se obtiene.

        :param command: El comando configurado por el usuario en forma de lista.
        :type command: list
        :return: La salida estándar, la salida de error y el código de retorno.
        :rtype: tuple
        """
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            output = process.stdout.read().decode('utf-8')
            err = process.stderr.read().decode('utf-8')
            code = process.returncode
            return output, err, code

    def cleanup(self):
        """
        Este método se encarga de eliminar el fichero temporal necesario para la lógica del programa.
        """
        os.remove(self.temp_file)

# sc = Scanner()
# sc.scan(targets='192.168.1.0/24')
# resultado = sc.scan(targets='192.168.1.0/24', params='-sV ')
# host = resultado.get_host()
# rich.print(host)
# rich.print(resultado.get_address(host))
# rich.print(resultado.get_os(host))
# rich.print(resultado.get_services(host))
# rich.print(resultado.get_hostname(host))
