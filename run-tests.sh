#!/bin/bash
################################################################################
# Script para correr los tests yaml esto es un cambio
#-------------------------------------------------------------------------------
sudo -u openerp /opt/openerp/v7/server/openerp-server --addons-path=/opt/openerp/v7/addons,/opt/openerp/v7/web/addons,/opt/openerp/v7/localizacion,/opt/openerp/v7/custom/addons --log-level=test -u email_template --test-enable -d test --stop-after-init
exit
