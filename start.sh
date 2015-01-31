#!/bin/bash
################################################################################
# Script para hrrancar openerp sin el log
#-------------------------------------------------------------------------------
sudo -u openerp /opt/openerp/v7/server/openerp-server --addons-path=/opt/openerp/v7/addons,/opt/openerp/v7/web/addons,/opt/openerp/v7/localizacion
exit
