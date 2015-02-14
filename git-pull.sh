#!/bin/bash
<<<<<<< HEAD
# odoo V8 Traer los datos de todos los repositorios
##############################################################################
=======
# odoo V8  Trae todas las modificaciones desde los repositorios
##################################################################################
#
echo -e "\n******************************************* pull curso"
cd /opt/odoo/custom/addons/curso
sudo git pull
#
>>>>>>> 876100cfeeb20bd67f25ac70a638d81c7e3e1d2a
echo -e "\n******************************************* pull dev-scripts"
cd /opt/odoo/dev-scripts
sudo git pull
#
echo -e "\n******************************************* pull odoo-server"
cd /opt/odoo/odoo-server
sudo git pull
<<<<<<< HEAD
=======
#
echo -e "\n******************************************* pull localizacion (ver nota)"
cd /opt/odoo/custom/addons/localizacion
sudo bzr pull
#
echo -e "\n******************************************* pull odoerp_no_phoning_home"
cd /opt/odoo/custom/addons/oerp_no_phoning_home
sudo git pull
>>>>>>> 876100cfeeb20bd67f25ac70a638d81c7e3e1d2a
