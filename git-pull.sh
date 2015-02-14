#!/bin/bash
# odoo V8  Trae todas las modificaciones desde los repositorios
##################################################################################
#
echo -e "\n******************************************* pull curso"
cd /opt/odoo/custom/addons/curso
sudo git pull
#
echo -e "\n******************************************* pull dev-scripts"
cd /opt/odoo/dev-scripts
sudo git pull
#
echo -e "\n******************************************* pull odoo-server"
cd /opt/odoo/odoo-server
sudo git pull
#
echo -e "\n******************************************* pull localizacion (ver nota)"
cd /opt/odoo/custom/addons/localizacion
sudo bzr pull
#
echo -e "\n******************************************* pull odoerp_no_phoning_home"
cd /opt/odoo/custom/addons/oerp_no_phoning_home
sudo git pull
