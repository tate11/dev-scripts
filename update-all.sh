#!/bin/bash
################################################################################
# Script para hacer update all
#-------------------------------------------------------------------------------
sudo -u openerp /opt/openerp/v7/server/openerp-server -d mk --addons-path=/opt/openerp/v7/addons,/opt/openerp/v7/web/addons,/opt/openerp/v7/localizacion,/opt/openerp/v7/custom/addons --update all
exit
