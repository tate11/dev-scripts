#!/usr/bin/env bash

sudo docker rm -f odoo

#sudo docker run -d \
#    --name=aeroo \
#    --restart=always \
#    adhoc/aeroo-docs \

#sudo docker run -d \
#    -e POSTGRES_USER=odoo \
#    -e POSTGRES_PASSWORD=odoo \
#    -v /odoo/odoo-8.0/reves/postgresql:/var/lib/postgresql/data \
#    --name postgres \
#    postgres:9.6


## Configuracion para debug
sudo docker run -it --rm \
    --link aeroo:aeroo \
    -p 127.0.0.1:8069:8069 \
    -p 127.0.0.1:8072:8072 \
    -v /odoo/odoo-8.0/reves/config:/opt/odoo/etc \
    -v /odoo/odoo-8.0/reves/data_dir:/opt/odoo/data \
    -v /odoo/odoo-8.0/reves/log:/var/log/odoo \
    -v /odoo/odoo-8.0/reves/sources:/opt/odoo/custom-addons \
    --link postgres:db \
    --name odoo \
    jobiols/odoo-jeo:8.0 -- \
    --load=web,web_kanban,server_mode,database_tools \
    --logfile=/dev/stdout \
    --workers 2

    #--logfile=/var/log/odoo/odoo.log



#    -v /odoo/odoo-8.0/sources/dist-packages:/usr/lib/python2.7/dist-packages \
#    -v /odoo/odoo-8.0/sources/dist-local-packages:/usr/local/lib/python2.7/dist-packages \
#    --addons=/usr/lib/python2.7/dist-packages/openerp/addons \
#    --stop-after-init \
#    -s
#    -v /odoo/odoo-8.0/sources:/opt/odoo/custom-addons \
#    --logfile=/opt/odoo/etc \
#     -u cloudmanager \

# ejecutar odooenv.py
#sudo docker run -d
#    --link aeroo:aeroo
#    -p 8069:8069
#    -p 8072:8072
#    -v /odoo/odoo-8.0/reves/config:/opt/odoo/etc/
#    -v /odoo/odoo-8.0/reves/data_dir:/opt/odoo/data
#    -v /odoo/odoo-8.0/reves/log:/var/log/odoo
#    -v /odoo/odoo-8.0/sources:/opt/odoo/custom-addons
#    --link postgres:db
#    --restart=always
#    --name reves
#    jobiols/odoo-jeo:8.0 --
#    --db-filter=reves_.*
#    --logfile=/var/log/odoo/odoo.log
#    --workers 3
#    --max-cron-threads 1
#    --limit-request 8196
#    --limit-memory-soft 2147483648
#    --limit-memory-hard 2684354560
#    --limit-time-cpu 1600
#    --limit-time-real 3200
