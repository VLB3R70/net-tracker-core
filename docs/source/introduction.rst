Introducción
============

**Net-Tracker** es una aplicación que busca ayudar a los administradores de sistemas informáticos monitorizar redes
haciendo uso de distintas herramientas existentes.
La herramienta principal que se usa para esta monitorización es `Nmap <https://nmap.org/>`_. Con **Nmap** se realizan
escaneos sobre una red con los valores que el usuario introduzca y estos valores deben ser aceptados por **Nmap**.

Posteriormente, la información obtenida se manipula y almacena en una base de datos `MongoDB <https://www.mongodb.com>`_
a la que el usuario puede consultar si es necesario.

Todo esto junto a una **API REST** desarrollada con `Flask <https://flask.palletsprojects.com/en/3.0.x/>`_ hace posible
que la aplicación sea accesible desde un terminal móvil. Para ver más sobre ese proyecto basta con visitar su página en
GitHub (`Net-Tracker-App <https://github.com/VLB3R70/net-tracker-app>`_).

Requisitos
----------

- Python 3.7 o superior (Última versión recomendada)
- MongoDB 7.0 o superior

La aplicación funciona tanto en Linux como en Windows. Para Windows se recomienda el uso de la nueva terminal `Windows Terminal <https://github.com/microsoft/terminal/releases>`_.

.. warning::
    Aunque se han realizado pruebas en entornos Windows y la aplicación ha funcionado correctamente se pueden experimentar
    fallos en la conexión con la base de datos o a la hora de desplegar la API REST.

Contribuciones
--------------

Debido a que la aplicación está en construcción y todavía no es estable ni contiene todas las funcionalidades pensadas,
todas las contribuciones y ayuda posible será bienvenida. El código fuente está disponible en `Github <https://github.com/VLB3R70/net-tracker-core>`_.

Enlaces de interés
------------------

:doc:`installation`
    Manual sobre la instalación de la aplicación.

:doc:`guide`
    Manual de usuario para aprender el funcionamiento básico de la aplicación.

:doc:`api/nettrackercore`
   Documentación técnica sobre la aplicación en profundidad. Explicación de clases, objetos y herramientas utilizadas.