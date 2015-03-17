#!/bin/bash
# Script to start odoo docker instance
###############################################
sudo docker run \
  --name db -d --restart=always \
  -e POSTGRES_PASSWORD=odoo -e POSTGRES_USER=odoo \
  -v /home/ubuntu/80/data:/var/lib/postgresql/data \
   postgres:9.3.6

sudo docker run -d --restart=always -p 80:8069 --link db:db \
  --name odoo \
  jobiols/odoo:80
#  -v /home/ubuntu/80-80/log:/var/log/odoo \
#  jobiols/odoo:80

