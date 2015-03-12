#!/bin/bash
# Script to start docker instance
###############################################
sudo docker run \
  --name db -d --restart=always\
  -e POSTGRES_PASSWORD=melquiades \
  -v /home/ubuntu/80/data:/var/lib/postgresql/data \
  jobiols/postgres

sudo docker run -d --restart=always -p 8069:8069 --link db:db \
  --name odoo-80 \
  -v /home/ubuntu/80/log:/var/log/odoo \
  jobiols/odoo:80

sudo docker ps
