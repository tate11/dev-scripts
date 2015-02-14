#!/bin/bash
################################################################################
# Script para hacer update al modulo curso
# odoo v8
#-------------------------------------------------------------------------------
sudo -u odoo /opt/odoo/odoo-server/openerp-server -d mk --addons-path=/opt/odoo/odoo-server/addons,/opt/odoo/custom/addons,/opt/odoo/custom/addons/localizacion --update curso --stop-after-init
exit
