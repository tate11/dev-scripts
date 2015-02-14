#!/bin/bash
# odoo V8 Traer los datos de todos los repositorios
##############################################################################
#
#
echo -e "\n******************************************* pull dev-scripts"
cd /opt/odoo/dev-scripts
git status
sudo git pull
#
echo -e "\n******************************************* pull odoo-server"
cd /opt/odoo/odoo-server
git status
sudo git pull
