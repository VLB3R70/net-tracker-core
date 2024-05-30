# net-tracker-core

[![Coverage Status](https://coveralls.io/repos/github/VLB3R70/net-tracker-core/badge.svg)](https://coveralls.io/github/VLB3R70/net-tracker-core)

**Net-Tracker** es una aplicación diseñada para ayudar a los administradores de sistemas a monitorizar redes utilizando 
diversas herramientas existentes. La herramienta principal empleada para esta monitorización es [Nmap](https://nmap.org/). 
Con **Nmap**, se realizan escaneos sobre una red basados en los parámetros que el usuario proporciona, los cuales deben 
ser compatibles con **Nmap**.

Posteriormente, la información obtenida se procesa y almacena en una base de datos [MongoDB](https://www.mongodb.com/), 
permitiendo al usuario consultarla cuando sea necesario.

Todo esto, junto a una **API REST** desarrollada con [Flask](https://flask.palletsprojects.com/en/3.0.x/), hace posible 
que la aplicación sea accesible desde un terminal móvil. Para más detalles sobre el proyecto, visita su página en GitHub: 
[Net-Tracker-App](https://github.com/VLB3R70/net-tracker-app).
