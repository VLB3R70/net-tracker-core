import datetime
import os
import subprocess
import traceback
from pathlib import Path

import rich

from .parsers import NmapParser, JSONNmapParser

DATE = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
MAIN_DIR = Path.home().joinpath('.nettracker')
LOG_DIR = Path.joinpath(MAIN_DIR, 'logs')
TEMP_DIR = Path.joinpath(MAIN_DIR, 'temp')

MAIN_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)


class Logger:

    @staticmethod
    def log(message):
        log_file = LOG_DIR.joinpath('scanner.log')
        with open(log_file, 'a') as log:
            log.write(f'[{DATE}]\n' + message + '\n')

    @staticmethod
    def error():
        error_file = LOG_DIR.joinpath('err.log')
        with open(error_file, 'a') as log:
            log.write(f'[{DATE}]\n' + traceback.format_exc() + '\n')


class Scanner:
    """
    Objeto que representa un escáner. Este escáner se encarga de usar el paquete de Nmap previamente instalado en la máquina.

    El usuario establece ciertos parámetros que posteriormente serán usados por el paquete Nmap. Dichos parámetros son:

    - **Objetivos**: puede ser una dirección de red en formato CIDR, una dirección IP o varias direcciones IP separadas por comas.

    - **Puertos**: es un parámetro que establece los puertos que se escanearán, si no se establece nada se escanean todos.
    El formato de los puertos es:
        - '80' -> Solo se escanea el puerto 80
        - '80,443' -> Se escanean los puertos 80 y 443 únicamente
        - '1-1024' -> Solo se escanean los puertos comprendidos entre el 1 y el 1024

    - **Parámetros**: son otros parámetros permitidos por Nmap

    :param targets: Dirección IP o varias direcciones IP separadas por comas.
    :param ports: Puertos que se escanearán.
    :param params: Parámetros adicionales permitidos por el paquete Nmap. **Ejemplo:** -O, -sV, -sS, etc.

    :return: Se devuelve un objeto que representa el resultado de la ejecución de Nmap.
    :rtype: ScannerResult
    """

    def __init__(self):
        self.temp_file = TEMP_DIR.joinpath('scanner.xml')
        self.temp_file.touch()  # Creo el fichero temporal vacío
        self.parser = NmapParser()
        self.json_parser = None

    def scan(self, targets=None, ports=None, params=None, sudo=False):
        command = self.parser.create_command(targets, ports, params, sudo, str(self.temp_file))
        output, err, code = self.execute_command(command)
        Logger.log(output)
        Logger.error()

        # pruebas
        self.json_parser = JSONNmapParser(self.temp_file)
        # rich.print(self.json_parser.data)
        rich.print(self.json_parser.get_host_address(self.json_parser.get_hosts()))
        rich.print(type(self.json_parser.get_hosts()))

    def execute_command(self, command):
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            output = process.stdout.read().decode('utf-8')
            err = process.stderr.read().decode('utf-8')
            code = process.returncode
            return output, err, code

    def cleanup(self):
        os.remove(self.temp_file)


# sc = Scanner()
# sc.scan(targets='192.168.1.0/24')
# sc.scan(targets='192.168.1.132-140')
