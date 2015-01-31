#!/bin/bash
################################################################################
# Script para hacer update all
#-------------------------------------------------------------------------------
sudo -u odoo /opt/odoo/odoo-server/openerp-server -d mk --addons-path=/opt/odoo/odoo-server/addons,/opt/odoo/custom/addons,/opt/odoo/custom/addons/localizacion --update all --stop-after-init
exit
