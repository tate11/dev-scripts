# dev-scripts
###Odoo docker based  infrastructure management 
 
    
    usage: odooenv.py [-h] [-i] [-U] [-R] [-S] [-r] [-s] [-p] [-l] [-v] [-q] [-n]
                      [-k] [-u] [-d DATABASE] [--home HOME_DIR] [-w NEW_DATABASE]
                      [-m MODULE] [-c CLIENT] [--debug] [--cleanup]
                      [--no-dbfilter] [--test] [-H] [--backup] [--backup-list]
                      [--restore] [-t TIMESTAMP]
    
    Odoo environment setup v 2.1
    
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
      -q, --quiet           Supress all standard output.
      -n, --no-ip-install   Install no-ip on this server.
      -k, --docker-install  Install docker on this server.
      -u, --update-db       Update database requires -d -c and -m options.
      -d DATABASE           Database name.
      --home HOME_DIR       Your home dir expanded, if your user is john you must
                            write --home /home/john. It is only needed when
                            running from a diferent user, i.e. if you run
                            odooenv.py from cron to schedule a backup the home
                            defaults to /root instead of /home/your_username
      -w NEW_DATABASE       New database name.
      -m MODULE             Module to update or all, you can specify multiple -m
                            options.
      -c CLIENT             Client name. You can define multiple clients like
                            this: -c client1 -c client2 -c client3 and so one.
      --debug               This option has two efects: when doing an update
                            database, (option -u) it forces debug mode. When
                            running environment it opens port 5432 to access
                            postgres server databases.
      --cleanup             Delete all files clients, sources, and databases in
                            this server. It ask about each thing.
      --no-dbfilter         Eliminates dbfilter: The client can see any database.
                            Without this, only sees databases starting with
                            clientname_
      --test                Run tests, requieres -d and -m options
      -H, --server-help     List server help requieres -c option
      --backup              Lauch backup requieres -d and -c options.
      --backup-list         List available backups with timestamps to restore.
      --restore             Lauch restore requieres -c, -d, -w and -t options.
      -t TIMESTAMP          Timestamp to restore database, see --backup-list for
                            available timestamps.
