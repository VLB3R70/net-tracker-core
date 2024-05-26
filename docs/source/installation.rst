Instalación
===========

Debido a su naturaleza inestable, Net-Tracker necesita seguir ciertos pasos específicos para la instalación. A continuación,
se detallan los pasos recomendados que se han seguido para realizar la correcta instalación de la aplicación.

Entorno virtual
---------------

Se recomienda usar un entorno virtual para mantener la aplicación encapsulada del resto del sistema. Para instalar y
configurar un entorno virtual en un entorno UNIX/Linux, se deben seguir los siguientes pasos:

.. code-block:: bash

    $ sudo apt install python3-venv

Con el paquete instalado, se debe ejecutar el siguiente comando para crear el entorno:

.. note::
    Es recomendable crear un directorio separado para el entorno virtual.

.. code-block:: bash

    $ python3 -m venv venv

Donde el último ``venv`` corresponde al nombre que tendrá el directorio del entorno virtual. Con el entorno virtual
instalado y creado, solo es necesario activarlo con el siguiente comando:

.. code-block:: bash

    $ source venv/bin/activate

Windows
^^^^^^^

Si tu entorno es Windows, los pasos a seguir son diferentes. Cuando se instala `Python <https://www.python.org/downloads/>`_,
también se instalan las herramientas para crear entornos virtuales. Para crear el entorno virtual, ejecuta el siguiente comando:

.. code-block:: bash

    $ python -m venv venv

.. warning::

    Para poder ejecutar el comando ``python`` desde la terminal de Windows, este debe ser accesible desde el **PATH**.

Para activar el entorno virtual, debemos ejecutar el siguiente comando:

.. code-block:: bash

    $ .\venv\Scripts\activate

Instalación de la aplicación
----------------------------

Con el entorno virtual instalado y activado, queda instalar la aplicación. Actualmente, al ser una versión inestable,
se debe instalar desde el repositorio oficial de `Github <https://github.com/VLB3R70/net-tracker-core>`_. A continuación,
se muestran los comandos que deben ejecutarse:

.. code-block:: bash

    $ git clone https://github.com/VLB3R70/net-tracker-core.git
    $ cd net-tracker-core
    $ pip install -r requirements.txt --upgrade
    $ pip install .

.. note::

    También es posible encapsular la construcción del proyecto y luego instalarlo con los siguientes comandos:

    .. code-block:: bash

        $ python -m build
        $ pip install .

    Este método es recomendable usarlo en entornos de desarrollo y nunca en el entorno del sistema.

Después de la instalación, simplemente deberemos ejecutar el comando ``net-tracker`` para iniciar la aplicación.

Despliegue
----------

La aplicación necesita, además, una conexión a una base de datos MongoDB y Docker correctamente instalado para poder
desplegar la API en un contenedor. Es posible crear un contenedor para la base de datos si no se quiere tener una
instalación completa de MongoDB. Dentro del directorio del proyecto, ejecutamos el siguiente comando:

.. code-block:: bash

    $ docker compose up -d

Con este comando, se procede a crear la imagen de la aplicación establecida en el fichero Dockerfile y posteriormente se
crea el contenedor con la imagen creada. Si además queremos crear un contenedor para la base de datos, debemos indicar
el perfil de este contenedor:

.. code-block:: bash

    $ docker compose --profile db up -d

Una vez creados los contenedores y desplegada la API, podemos comprobarlo abriendo un navegador y visitando
`<http://localhost:5000>`_. También es posible acceder a la API desde ``http://<IP>:5000``.
