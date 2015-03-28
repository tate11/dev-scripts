#!/bin/bash
# stop and remove all instances
###############################################
sudo docker stop odoo
sudo docker stop db
sudo docker rm odoo
sudo docker rm db
sudo docker stop aeroo_docs
sudo docker rm aeroo_docs
