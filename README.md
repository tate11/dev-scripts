# dev-scripts
    scripts para administración de ambiente Odoo versiones 7 , 8 y 9 (beta)
    
    usage: odooenv.py [-h] [-U] [-I] [-i] [-R] [-D] [-r] [-S] [-s] [-p] [-l]
                      [-c CLIENT] [-n] [-k] [-u] [-d DATABASE] [-m MODULE]
                      [--backup] [--debug] [--backup-list]
                      {8.0,7.0.1,8.0.1,7.0,ou-8.0,9.0}
    
    Odoo environment setup v 1.3
    
    positional arguments:
      {8.0,7.0.1,8.0.1,7.0,ou-8.0,9.0}
    
    optional arguments:
      -h, --help            show this help message and exit
      -U, --uninstall-env   Uninstall and erase all files from environment
                            including database (only current ver). The command ask
                            for permission to erase database. BE WARNED if say
                            yes, all database files will be erased.
      -I, --install-env     Install all files and odoo repos needed. It will try
                            to install postgres dir if doesn't exist
      -i, --install-cli     Install clients, requires -c option. You can define
                            multiple clients like this: -c client1 -c client2 -c
                            client3
      -R, --run-env         Run database and aeroo images.
      -D, --run-dev         Run database and aeroo images for developer mode
                            (local db access).
      -r, --run-cli         Run client odoo images, requieres -c options.
      -S, --stop-env        Stop database and aeroo images.
      -s, --stop-cli        Stop client images, requieres -c options.
      -p, --pull-all        Pull all images
      -l, --list            List all data in this server. Clients and images.
      -c CLIENT             Client name. You define multiple clients like this
                            multiple clients like this: -c client1 -c client2 -c
                            client3
      -n, --no-ip-install   Install no-ip on this server
      -k, --docker-install  Install docker on this server
      -u, --update-database
                            Update database requires -d -c and -m options
      -d DATABASE, --database DATABASE
                            Database to update
      -m MODULE, --module MODULE
                            Module to update or all, you can specify multiple -m
                            options
      --backup              Lauch backup requieres -d y -c
      --debug               force debug mode on update database
      --backup-list         List available backups

