#!/bin/bash
# Script to start odoo docker instance
###############################################
sudo docker run -d --restart=always \
    --name db  \
    -e POSTGRES_PASSWORD=odoo
    -e POSTGRES_USER=odoo \
    -v /home/ubuntu/80/data:/var/lib/postgresql/data \
    postgres:9.3.6

sudo docker run -d -p 8989:8989 --restart=always \
    --name aeroo_docs  \
    rvalyi/aeroocker

sudo docker run -d --restart=always -p 80:8069
    --name odoo \
    --link db:db \
    --link aeroo_docs:aeroo_docs \
    jobiols/odoo:80
