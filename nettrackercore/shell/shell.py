import signal

from mongoengine.errors import NotUniqueError
from rich import print
from rich.console import Console
from rich.prompt import Prompt

from nettrackercore.core.controller import NettrackerDAO
from nettrackercore.core.dba import DBA
from nettrackercore.core.exceptions import *
from nettrackercore.core.results import JSONResult
from nettrackercore.core.scanner import Scanner
from nettrackercore.shell.helpers import Helper

console = Console()

PROMPT = "[underline]net-tracker[/underline]"
SCANNER_PROMPT = PROMPT + "([bold red]scanner[/bold red])"
DBA_PROMPT = PROMPT + "([bold red]dba[/bold red])"


class Shell:
    """
    La clase **Shell** representa la terminal de comandos por donde el usuario interacciona con el núcleo de la
    aplicación.
    Esta terminal está inspirada en la terminal de comandos ofrecida por
    `Kali Linux Metasploit Framework <https://www.kali.org/docs/tools/starting-metasploit-framework-in-kali/>`_.

    El usuario puede elegir varios objetos ofrecidos por el núcleo y debe de establecer los parámetros necesarios para
    ejecutar los comandos correspondientes. El diseño de la terminal está implementado con
    `rich <https://rich.readthedocs.io/en/stable/index.html>`_, un paquete escrito en Python que ayuda escribir y mostrar
    texto más complejo por la terminal de comandos de una forma más bonita.

        Rich is a Python library for writing rich text (with color and style) to the terminal, and for displaying advanced
        content such as tables, markdown, and syntax highlighted code.

        Use Rich to make your command line applications visually appealing and present data in a more readable way. Rich can
        also be a useful debugging aid by pretty printing and syntax highlighting data structures.
    """

    LOGO = """[magenta] _  _  ___  _____        _____  ___  ___   ___  _  __ ___  ___ 
| \| || __||_   _|      |_   _|| _ \/   \ / __|| |/ /| __|| _ \\
| .  || _|   | |          | |  |   /| - || (__ |   < | _| |   /
|_|\_||___|  |_|          |_|  |_|_\|_|_| \___||_|\_\|___||_|_\\
"""

    def __init__(self, translator, config):
        signal.signal(signal.SIGINT, self.handler)
        self.translator = translator
        self.config = config

    def handler(self, signum=None, frame=None):
        """
        Este método es necesario para capturar la señal de teclado `Ctrl+C`
        """
        print(self.translator.translate("goodbye"))
        exit(1)

    def set_options(self, options, option, value):
        """
        Método que se encarga de establecer un valor a la opción pasada por parámetro. Las diferentes opciones se
        establecen previamente en un diccionario.

        :param options: es el diccionario con las diferentes opciones mapeadas.
        :param option: es la **opción** dentro de las **opciones** mapeadas la cual se va a modificar.
        :param value: es el valor que se establecerá a la opción.
        :type options: dict
        :type option: str
        :type value: str

        """
        options[option] = str(value)

    def get_options(self, options, option):
        """
        Este método se encarga de obtener los valores de las distintas opciones usadas por el objeto. Dichas opciones
        están mapeadas en un diccionario para mejorar el acceso a ellas. El usuario puede obtener el valor de una opción
        o de todas las opciones mapeadas con la opción `ALL`.

        :param options: es el diccionario con las distintas opciones del objeto mapeadas
        :param option: es la opción de la cual se obtendrá el valor. Si se indica `ALL` o `all` se devuelven los valores
            de todas las opciones.
        """
        if option.upper() in options.keys():
            console.print(f"[cyan]{option.upper()}[/cyan]\t\t {options.get(option.upper())}")
        elif option.upper() == 'ALL':
            for key, value in options.items():
                console.print(f"[cyan]{key}[/cyan]\t\t {value}")

    def build_params(self, options):
        """
        Existen ciertos parámetros que corresponden a *interrogantes booleanos* y en función de su valor se deben de
        añadir más o menos valores al comando final del escáner. Estos parámetros se encuentran dentro del diccionario
        con las opciones mapeadas.

        :param options: es el diccionario con las opciones mapeadas
        :type options: dict

        :return: el valor final del parámetro `OPTIONS`
        :rtype: dict
        """
        if options["SILENT"]:
            options["OTHER"] += "-sS "
        elif options["TCP"]:
            options["OTHER"] += "-sT "
        elif options["UDP"]:
            options["OTHER"] += "-sU "
        elif options["OS"]:
            options["OTHER"] += "-O "

        return options["OTHER"]

    def __create_network(self, dao, address, netmask):
        while True:
            network_name = Prompt.ask(self.translator.translate("provide_network_name"))
            try:
                dao.new_network(name=network_name, address=address, submask=netmask)
                break  # Salir del bucle si se guarda correctamente
            except NotUniqueError:
                console.print(self.translator.translate("network_not_unique").format(network_name=network_name))
                update = Prompt.ask("¿Quieres actualizar la red actual con dicho nombre?")
                if update.lower() == "y" or update.lower() == "s":
                    dao.update_network(name=network_name, address=address, submask=netmask)
                    break

    def save_scan(self, scan_result: JSONResult, options):
        """
        Este método se encarga de guardar el resultado del escaneo en la base de datos. Ciertos parámetros corresponden
        a las opciones mapeadas del escáner.

        :param scan_result: el resultado del escaneo en forma de objeto :py:class:`~nettrackercore.core.results.JSONResult`
        :type scan_result: JSONResult
        :param options: son las opciones mapeadas del escáner
        :type options: dict

        """
        dao = NettrackerDAO(scan_result)

        if "/" in options["TARGET"]:
            console.print(self.translator.translate("network_detected"))
            address, netmask = options["TARGET"].split("/")
            self.__create_network(dao, address, netmask)

    def scanner(self):
        """
        El método :py:func:`~nettrackercore.core.shell.scanner` establece la lógica de uso del objeto. Cuando el usuario
        decide usar el escáner este método se ejecuta. Primero se crea un objeto
        :py:class:`~nettrackercore.core.scanner.Scanner` y posteriormente se crea un diccionario con las opciones
        permitidas por el escáner.

        El usuario introduce una opción dentro de las posibles:

        - **exit** Sale de la terminal
        - **help** Muestra la ayuda del escáner
        - **set <opcion> <valor>** establece el valor de una opción mapeada al introducido por el usuario
        - **get <opcion> | ALL** devuelve el valor de la opción introducida por el usuario. Si se indica `ALL` o `all` se devuelven todos los valores
        - **scan** Empieza a escanear la red con los datos establecidos por el usuario y pregunta al usuario si quiere almacenar dicha información en la base de datos.

        """
        sc = Scanner(self.config)
        # mapeo las posibles opciones y valores predeterminados
        options = {"TARGET": "localhost", "PORT": "", "OTHER": "", "SILENT": False, "TCP": False, "UDP": False,
                   "OS": True, "SUDO": True}

        while True:
            option = Prompt.ask(SCANNER_PROMPT)
            if option == "exit":
                console.print(self.translator.translate("goodbye"))
                exit(0)
            elif option.startswith("set"):
                _, key, value = option.split()
                if key.upper() in options.keys():
                    self.set_options(options, key.upper(), value)
            elif option.startswith("get"):
                option = option.split()
                self.get_options(options, option[1])
            elif option == "scan":
                try:
                    # with console.status(self.translator.translate("scanning"), spinner="aesthetic"):
                    params = self.build_params(options)
                    result = sc.scan(targets=options["TARGET"], ports=options["PORT"], params=params,
                                     sudo=bool(options["SUDO"]))

                    console.print(self.translator.translate("successful_scan"))
                    save = Prompt.ask(self.translator.translate("save_scan"))
                    if save.lower() == "y" or save.lower() == "s":
                        self.save_scan(result, options)
                except (ExecutionError, InvalidArgumentsException, IllegalArgumentException, InvalidAddressException,
                        InvalidPortsException) as e:
                    console.print(f"[red]{e}[/red]")
            elif option == "help":
                Helper.print_scan_help()
            else:
                console.print(self.translator.translate("unknown_option"))

    def dba(self):
        dba = DBA()
        while True:
            option = Prompt.ask(DBA_PROMPT).split()
            if option[0] == "exit":
                console.print(self.translator.translate("goodbye"))
                exit(0)
            elif option[0] == "get":
                if option[1] == "networks":
                    console.print(dba.get_networks())
                elif option[1] == "network" and option[2]:
                    console.print(dba.get_network(option[2]))
            elif option[0] == "list":
                if option[1] == "devices":
                    network = Prompt.ask("Nombre de la red")
                    console.print(dba.get_devices(network))
                elif option[1] == "services":
                    network = Prompt.ask("Nombre de la red")
                    device = Prompt.ask("Dirección IP del dispositivo")
                    console.print(dba.get_services(network, device))

    def main_menu(self):
        """
        Este método muestra el prompt principal del programa donde el usuario elige qué objeto quiere usar.
        """
        print(self.LOGO)
        while True:
            option = Prompt.ask(PROMPT)
            if option == "help":
                Helper.print_main_help()
            elif option == "scanner":
                self.scanner()
            elif option == "dba":
                self.dba()
            elif option == "exit":
                exit(0)
            else:
                print("Opción inválida. Pruebe otra vez")
