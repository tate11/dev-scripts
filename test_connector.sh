sudo docker run --rm -it \
    -v /odoo/odoo-9.0/test/config:/opt/odoo/etc/ \
    -v /odoo/odoo-9.0/test/data_dir:/opt/odoo/data \
    -v /odoo/odoo-9.0/test/log:/var/log/odoo \
    -v /odoo/odoo-9.0/sources:/opt/odoo/custom-addons \
    --link postgres:db \
    jobiols/odoo-jeo:9.0.debug -- \
    --addons-path=/opt/odoo/custom-addons/connector-odoo2odoo,/opt/odoo/custom-addons/connector,/opt/odoo/extra-addons/ingadhoc-odoo-support,/opt/odoo/extra-addons/ingadhoc-aeroo_reports,/opt/odoo/extra-addons/ingadhoc-odoo-argentina \
    --no-xmlrpc \
    --stop-after-init \
    --logfile=false \
    -d bulonfer_test \
    --log-level=test \
    --test-file=/opt/odoo/custom-addons/connector-odoo2odoo/odoo2odoo/tests/test_01.py


#sudo docker run --rm 
#    -v /odoo/odoo-9.0/bulonfer/config:/opt/odoo/etc/ \
#    -v /odoo/odoo-9.0/bulonfer/data_dir:/opt/odoo/data \
#    -v /odoo/odoo-9.0/bulonfer/log:/var/log/odoo \
#    --link postgres:db \
#    --name bulonfer_tmp \
#    jobiols/odoo-jeo:9.0 \
#    -- \
#    --stop-after-init -s \

#sudo docker run --rm 
#    -v /odoo/odoo-9.0/bulonfer/config:/opt/odoo/etc/ 
#    --name bulonfer_tmp 
#    --entrypoint=/patch_config.py 
#    jobiols/odoo-jeo:9.0.debug /opt/odoo/custom-addons/cl-bulonfer,/opt/odoo/custom-addons/odoo-addons,/opt/odoo/custom-addons/connector

# sudo docker run -d --link aeroo:aeroo -p 8069:8069 -p 8072:8072 \
#   -v /odoo/odoo-9.0/bulonfer/config:/opt/odoo/etc/ 
#   -v /odoo/odoo-9.0/bulonfer/data_dir:/opt/odoo/data 
#   -v /odoo/odoo-9.0/sources:/opt/odoo/custom-addons 
#   -v /odoo/odoo-9.0/bulonfer/log:/var/log/odoo 
#--link postgres:db --restart=always -e SERVER_MODE= --name bulonfer jobiols/odoo-jeo:9.0 -- --db-filter=bulonfer_.* --logfile=/var/log/odoo/odoo.log --workers 0 --max-cron-threads 1 --limit-request 8196 --limit-memory-soft 2147483648 --limit-memory-hard 2684354560 --limit-time-cpu 1600 --limit-time-real 3200


