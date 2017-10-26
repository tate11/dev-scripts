#!/usr/bin/env bash

sudo docker run -d \
    --link aeroo:aeroo \
    -v /odoo/odoo-8.0/reves/config:/etc/odoo \
    -v /odoo/odoo-8.0/reves/data_dir:/var/lib/odoo \
    -v /odoo/odoo-8.0/sources:/mnt/extra-addons \
    -v /odoo/odoo-8.0/reves/log:/var/log/odoo \
    --link postgres:db \
    --restart=always \
    --name reves \
    jobiols/odoo-jeo:8.0 -- --db-filter=reves_.* --logfile=/var/log/odoo/odoo.log
