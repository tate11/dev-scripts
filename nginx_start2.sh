#!/usr/bin/env bash

#   --link reves:   --- enlaza con el contenedor de odoo
#   -v /odoo/nginx: --- mapea directorio del arch configuracion
#   -v /odoo/cert:  --- certificado del sitio

# Certificado autogenerado
# Esto crea dos archivos en /odoo/cert el .crt y el .key

# sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout \
# /odoo/cert/nginx.key -out /odoo/cert/nginx.crt
echo  "running docker nginx"

sd run -d \
    --name="nginx" \
    --restart="always" \
    --link reves:odoo \
    -v /odoo/nginx/conf:/etc/nginx/conf.d:ro \
    -v /odoo/nginx/cert:/etc/letsencrypt/live/certificadositio \
    -v /odoo/nginx/log:/var/log/nginx/ \
    -p 80:80 \
    -p 443:443 \
    nginx