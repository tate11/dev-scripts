Infraestructura de instalación Odoo
===================================
by jeoSoftware
Estructura de directorios de la instalación
-------------------------------------------
Esta es la estructura de directorios de una instalación de Odoo creada 
por odooenv.py, se diseñó así porque permite poner todo en un disco y 
dejar el SO en otro volumen. Se cambia el disco de máquina y sale andando.
Permite coexistir varias versiones de odoo y varios clientes en la misma 
máquina, compartiendo todos los servicios de postgres y aeroo.



      odoo
      ├─ postgresql
      ├──odoov-8.0
      │  ├──[clientname]
      │  │   ├──config
      │  │   │  └──openerp-server.conf
      │  │   ├──data_dir
      │  │   │  └──[filestore]
      │  │   └──log
      │  │      └──odoo.log
      │  └──sources
      └──odoov-9.0
         ├──[clientname]
         │   ├──config
         │   │  └──openerp-server.conf
         │   ├──data_dir
         │   │  └──[filestore]
         │   └──log
         │      └──odoo.log
         └──sources


Repositorio de utilidades
-------------------------
En este repo se encuentran todas las utilidades que se usan para el desarrollo, en este resumen se detallarán solo dos, sd y odooenv.py

https://github.com/jobiols/dev-scripts.git

Está clonado en ~/dev-scripts para actualizarlo hacer

$ cd ~/dev_scripts
$ ./install_scripts 

Esto baja el repositorio y copia dos scripts a /usr/bin

odooenv.py - para el mantenimiento de la infraestructura
sd               - short para sudo docker, y algunas cositas más.
Manifiesto de instalación
La definición de cómo se instala el sistema está en el archivo:

 ~/dev-scripts/classes/client_data.py 

buscamos ahí esmeralda y encontramos esto:

   {'name': 'esmeralda', 'port': '8069', 'odoover': '8.0',
     'repos': [
         {'usr': 'jobiols', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'adhoc-reporting-engine', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'adhoc-account-payment', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'adhoc-stock', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'web', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'adhoc-account-financial-tools', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'adhoc-account-invoicing', 'branch': '8.0'},
     ],
     'images': [
         {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
         {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo', 'ver': '8.0'},
         {'name': 'postgres', 'usr': 'postgres', 'ver': '9.4'},
         {'name': 'backup', 'usr': 'jobiols', 'img': 'backup'},
     ]
 },


En 'repos' están todos los repositorios
En 'images' estan todas las imágenes de docker 
Operaciones de mantenimiento
Ver todos los backups que hay
Esto muestra todos los backups que hay de todos los clientes en este caso ahy un solo cliente, si hubiese varios se puede agregar un -c CLIENTNAME
$ odooenv.py --backup-list
List of available backups for client esmeralda
esmeralda_prod 10/02/2017 03:00 GMT  [201702100300] 22M
esmeralda_prod 10/02/2017 15:00 GMT  [201702101500] 22M

Cada línea es un backup realizado, y cada backup se compone de dos archivos, un dump de la base de datos y un tar del filestore.
Para mover estos archivos a otro lugar hay que mover los dos y restarurarlos juntos. Los archivos están en /odoo/odoo-8.0/esmeralda/backup

Hacer un backup
Para hacer un backup manual, el script lanza una imagen docker con las herramientas de backup, se conecta a la instancia  odoo y mapea el directorio donde está la bd, el filestore y el postgress. Hace el backup, empaqueta el filestore y luego se destruye la imagen.

$ odooenv.py --backup -d esmeralda_prod -c esmeralda

Notar que en el host no está instalado posgres, ni las herramientas de backup.
Restaurar un backup
Para Restaurar un backup dado se listan los backups disponibles y se elige uno según su timestamp. 

esmeralda_prod 10/02/2017 03:00 GMT  [201702100300] 22M
esmeralda_prod 10/02/2017 15:00 GMT  [201702101500] 22M

Lo que se elige es el timestamp que está entre corchetes

luego se ejecuta el siguiente comando para restaurar la base de datos, 

$ odooenv.py --restore \			# restorear la bd
-d esmeralda_prod \		# nombre original de la bd
-c esmeralda \			# cliente
-t 201702072249 \			# timestamp a restorear
-w esmeralda_prod_restored	# nuevo nombre de la bd

Hay que pasarle el nombre original y un nuevo nombre, luego se usan las herramientas en linea para eliminar y renombrar con lo cual la filestore queda correctamente sincronizada con la base de datos.
Detener Odoo
Para detener la instancia de odoo
$ odooenv.py -s -c esmeralda

Iniciar Odoo
Para iniciar odoo, esto resiste el rebooteo.
$ odooenv.py -r -c esmeralda
Reiniciar Odoo
Detiene y arranca el servidor
$ odooenv.py -s -r -c esmeralda
Detener Postgress y Aeroo
Detiene los contenedores de postrgress y aeroo, el comando los ejecuta juntos pero son dos contenedores separados
$ odooenv.py -S -c esmeralda
Iniciar Postgress y Aeroo
$ odooenv.py -R -c esmeralda
Donde estan mis cosas
Repositorios
Archivo de configuración odoo
Archivo de log odoo
Filestore
Sobre las bases de datos
Cuidado con los nombres, dbfilter !

Cómo agregar / quitar un repositorio
Se supone que uno tiene muy claro lo que quiere hacer y porque quiere poner o sacar un repo.
Modificar el manifiesto que hay en ~/dev-scripts/classes/client_data.py y agregarle o quitarle el o los repos necesarios.
Actualizar los repos y reescribir el openerp-server.conf, para esto hacer:
$ odooenv.py -i -c esmeralda
Esto bajará los repos que falten, no tocará los que ya existan o sobren y actualizará el openerp-server.conf para que odoo vea los repos que queremos que vea. Los que están en el manifiesto.
Reiniciar odoo para que tome los cambios en el odooenv-server.conf
$ odooenv.py -s -r -c esmeralda
Ahora es necesario actualizar los modelos en la bd, esto como medida precautoria.
$ odooenv.py -u -m all -d esmeralda_prod -c esmeralda 
Esto significa:
	-u 			Update 
	-m all 			del módulo all (todos los módulos)
	-d esmeralda_prod  	la base de datos que actualizaremos
	-c esmeralda  		el cliente que actualizaremos

Cómo actualizar imágenes y repos
Como instalar desde cero
