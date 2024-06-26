��                        �  /  �  �  -     	     *	     H	     Z	     z	  9   �	  2   �	     �	  '   �	  -   
     M
     `
     g
  "   x
  7   �
  	   �
     �
     �
     �
            K         l  "   ~  .   �     �  $   �  �    �  �  �  8  
             +     ;     U  /   ]  1   �     �  "   �  3   �          %     *     7  ,   Q     ~     �     �     �     �     �  7   �     �     �  +        H     e   
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

`get all` Obtiene todos los parámetros. 
## Comandos de uso
- **help** - Muestra este mensaje de ayuda
- **get networks** - Muestra todas las redes de la base de datos en forma de tabla.
- **get network <nombre>** - Muestra la información de una red determinada en forma de tabla.
- **list devices <nombre>** - Muestra los dispositivos de una red concreta en forma de tabla
- **list services** - Muestra los servicios de un dispositivo en una red concreta en forma de tabla. 
    La dirección y nombre de la red se piden al usuario. Dirección IP Dirección IP del dispositivo Dirección de red Disposistivos de {network_name} Dispositivos El dispositivo o dispositivos deben pertenecer a una red. El programa ha detectado el objetivo como una red. ID Introduce el nombre de una red conocida La red[red] {network_name}[/red] no es única Máscara de subred Nombre Nombre de la red Opción inválida. Pruebe otra vez Por favor introduce un nombre para identificar a la red Protocolo Puerta de enlace Puerto Red {network_name} Redes Servicios activos Servicios activos del dispositivo {device_address} dentro de {network_name} Sistema operativo [blue]Guardar escaneo [S/n][/blue] [green]Escaneo terminado correctamente[/green] [magenta][bold]¡Adiós! 👋 [yellow]Opción desconocida[/yellow] Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2024-05-27 11:31+0200
PO-Revision-Date: 2024-05-13 10:50+0200
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: en
Language-Team: en <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.15.0
 
# Command Usage
- **help** - Displays this help message
- **set <option> <value>** - Sets the network and/or device parameters to be scanned with the provided value
- **get <option> | ALL** - Gets the value of the requested parameter or all (ALL)
- **scan** - Performs the scan of the established network and/or devices.

## Valid Options

- **TARGET** - Network and/or device target corresponding to a valid IP address.
- **PORT** - Ports to be scanned on all assigned devices.
- **OTHER** - Other parameters accepted by Nmap.
- **SILENT** - Parameter that sets whether the scan is silent or not.
- **TCP** - Sets the scan protocol to TCP.
- **UDP** - Sets the scan protocol to UDP.
- **OS** - Parameter that enables the detection of the operating system of the scanned device.
- **SUDO** - Valid only for UNIX/Linux. Certain parameters require superuser permissions to execute.

## Usage Examples

`set TARGET 192.168.1.0/24` to scan a complete network or `set TARGET 192.168.1.1 192.168.1.100` to scan only two devices.

`set OS True` Options SILENT, TCP, UDP, OS, and SUDO are boolean values.

`get target` Gets only the scan target.

`get all` Gets all parameters.

 
## Command Usage
- **help** - Displays this help message
- **get networks** - Shows all networks from the database in table format.
- **get network <name>** - Shows information about a specific network in table format.
- **list devices <name>** - Shows the devices of a specific network in table format.
- **list services** - Shows the services of a device in a specific network in table format.
  The address and name of the network will be requested from the user.

 IP address Device IP address Network address Devices of {network_name} Devices The device or devices must belong to a network. The program has detected the target as a network. ID Enter the name of a known network. The network[red] {network_name}[/red] is not unique Subnet mask Name Network name Invalid option. Try again Please enter a name to identify the network. Protocol Gateway Port {network_name} network Networks Active services Active services of {device_address} from {network_name} OS [blue]Save scan [Y/n][/blue] [green]Scan successfully completed.[/green] [magenta][bold]Goodbye! 👋 [yellow]Unknown option[/yellow] 