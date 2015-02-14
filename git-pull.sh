#!/bin/bash
# odoo V8 Traer los datos de todos los repositorios
##############################################################################
echo -e "\n******************************************* pull dev-scripts"
cd /opt/odoo/dev-scripts
sudo git pull
#
echo -e "\n******************************************* pull odoo-server"
cd /opt/odoo/odoo-server
sudo git pull
