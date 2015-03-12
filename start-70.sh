#!/bin/bash
# Script to start docker instance
##############################################
sudo docker run \
  --name db -d \
  -e POSTGRES_PASSWORD=melquiades \
  -v /home/ubuntu/70/data:/var/lib/postgresql/data \
  jobiols/postgres

sudo docker run -d -p 8069:8069 --link db:db \
  --name odoo-70 \
  -v /home/ubuntu/70/log:/var/log/odoo \
  jobiols/odoo:70

sudo docker ps
