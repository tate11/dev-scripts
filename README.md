# dev-scripts
###Scripts para administración de ambiente Odoo versiones 7, 8 y 9 (beta)
    
usage: odooenv.py [-h] [-i] [-U] [-R] [-S] [-r] [-s] [-p] [-l] [-v] [-n] [-k]
                  [-u] [-d DATABASE] [-t TIMESTAMP] [-m MODULE] [-c CLIENT]
                  [--backup] [--restore] [--debug] [--backup-list] [--cleanup]

Odoo environment setup v 2.0

optional arguments:
  -h, --help            show this help message and exit
  -i, --install-cli     Install clients, requires -c option. You can define
                        multiple clients like this: -c client1 -c client2 -c
                        client3
  -U, --uninstall-cli   Uninstall client and erase all files from environment
                        including database. The command ask for permission to
                        erase database. BE WARNED if say yes, all database
                        files will be erased. BE WARNED AGAIN, database is
                        common to all clients!!!! Required -c option
  -R, --run-env         Run database and aeroo images.
  -S, --stop-env        Stop database and aeroo images.
  -r, --run-cli         Run client odoo images, requieres -c options.
  -s, --stop-cli        Stop client images, requieres -c options.
  -p, --pull-all        Pull all images and repos.
  -l, --list            List all data in this server. Clients and images.
  -v, --verbose         Go verbose mode.
  -n, --no-ip-install   Install no-ip on this server.
  -k, --docker-install  Install docker on this server.
  -u, --update-database
                        Update database requires -d -c and -m options.
  -d DATABASE           Database to update.
  -t TIMESTAMP          Timestamp to restore database, see --backup-list for
                        available timestamps.
  -m MODULE             Module to update or all, you can specify multiple -m
                        options.
  -c CLIENT             Client name. You define can define multiple clients
                        like this: -c client1 -c client2 -c client3 and so
                        one.
  --backup              Lauch backup requieres -d and -c options.
  --restore             Lauch restore requieres -d, -c and -t options.
  --debug               This option has two efects: when doing an update
                        database, (option -u) it forces debug mode. When
                        running environment it opens port 5432 to access
                        postgres server databases.
  --backup-list         List available backups with timestamps to restore.
  --cleanup             Delete all files clients, sources, and databases in
                        this server. It ask about each thing.
