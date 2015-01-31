#!/bin/bash
################################################################################
# Script para hrrancar openerp sin el log
#-------------------------------------------------------------------------------
sudo -u odoo /opt/odoo/odoo-server/openerp-server --addons-path=/opt/odoo/odoo-server/addons,/opt/odoo/custom/addons,/opt/odoo/custom/addons/localizacion --db_user=odoo --db_password=melquiades 
exit
