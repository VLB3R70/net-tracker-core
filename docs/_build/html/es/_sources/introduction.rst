Introducción
============

**Net-Tracker** es una aplicación diseñada para ayudar a los administradores de sistemas a monitorizar redes utilizando
diversas herramientas existentes. La herramienta principal empleada para esta monitorización es `Nmap <https://nmap.org/>`_.
Con **Nmap**, se realizan escaneos sobre una red basados en los parámetros que el usuario proporciona, los cuales deben
ser compatibles con **Nmap**.

Posteriormente, la información obtenida se procesa y almacena en una base de datos `MongoDB <https://www.mongodb.com>`_,
permitiendo al usuario consultarla cuando sea necesario.

Todo esto, junto a una **API REST** desarrollada con `Flask <https://flask.palletsprojects.com/en/3.0.x/>`_, hace posible
que la aplicación sea accesible desde un terminal móvil. Para más detalles sobre el proyecto, visita su página en GitHub:
`Net-Tracker-App <https://github.com/VLB3R70/net-tracker-app>`_.

Requisitos
----------

- Python 3.7 o superior (Se recomienda la última versión)
- MongoDB 7.0 o superior
- Docker 26 o superior
- Nmap 7.80 o superior

La aplicación funciona tanto en Linux como en Windows. Para Windows, se recomienda el uso de la nueva terminal `Windows Terminal <https://github.com/microsoft/terminal/releases>`_.

.. warning::
    Aunque se han realizado pruebas en entornos Windows y la aplicación ha funcionado correctamente, se pueden experimentar
    fallos en la conexión con la base de datos o al desplegar la API REST.

Contribuciones
--------------

Debido a que la aplicación está en desarrollo y aún no es estable ni contiene todas las funcionalidades planeadas, todas
las contribuciones y ayuda serán bienvenidas. El código fuente está disponible en `GitHub <https://github.com/VLB3R70/net-tracker-core>`_.

Enlaces de interés
------------------

:doc:`installation`
    Manual sobre la instalación de la aplicación.

:doc:`api/nettrackercore`
    Documentación técnica en profundidad sobre la aplicación. Explicación de clases, objetos y herramientas utilizadas.
