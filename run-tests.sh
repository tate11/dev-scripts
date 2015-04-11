#!/bin/bash
###############################################
# Script para correr los tests yaml
# odoo v7
#-------------------------------------------------------------------------------
sudo -u odoo /opt/odoo/odoo-server/openerp-server -d test --addons-path=/opt/odoo/odoo-server/addons,/opt/odoo/custom/addons,/opt/odoo/custom/addons/localizacion --log-level=test -i curso --test-enable --stop-after-init
exit
