#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
#
# Jorge Obiols Software,
# Copyright (C) 2015-Today JEO <jorge.obiols@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# #############################################################################
# Directory structure
#   ~/postgresql
#   ~/odoo-[version]
#       /sources
#           /[repodir1]
#               /[repo1]
#       /[clientname1]
#           /config
#               openerp-server.conf
#           /data_dir
#
# TODO archivo xml que sobreescriba clients.
# TODO Revisar el tema de los subcomandos
##############################################################################

import argparse
import os
from datetime import datetime
import subprocess

from classes import Environment, clients__


def sc_(params):
    if args.verbose:
        print params
    return subprocess.call(params, shell=True)


def uninstall_client(e):
    clients = e.get_clients_from_params()
    if raw_input('Delete postgresql directory? (y/n) ') == 'y':
        if raw_input('Delete ALL databases for ALL clients SURE?? (y/n) ') == 'y':
            e.msginf('deleting all databases!')
            sc_(['sudo rm -r ' + e.getPsqlDir()])

    for clientName in clients:
        cli = e.get_client(clientName)
        e.msgrun('deleting client files for client ' + clientName)
        if sc_(['sudo rm -r ' + cli.get_home_dir() + clientName]):
            e.msgerr('fail uninstalling client ' + clientName)
    return True


def update_db(e):
    mods = e.get_modules_from_params()
    db = e.get_database_from_params()
    cli = e.get_client(e.get_clients_from_params('one'))

    msg = 'Performing update'
    if mods[0] == 'all':
        msg += ' of all modules'
    else:
        msg += ' of module(s) ' + ', '.join(mods)

    msg += ' on database "' + db + '"'

    if e.debug_mode():
        msg += ' forcing debug mode'
    e.msgrun(msg)

    params = 'sudo docker run --rm -it '
    params += '-v ' + cli.get_home_dir() + cli.get_name() + '/config:/etc/odoo '
    params += '-v ' + cli.get_home_dir() + cli.get_name() + '/data_dir:/var/lib/odoo '
    params += '-v ' + cli.get_home_dir() + 'sources:/mnt/extra-addons '
    params += '--link postgres:db '
    params += cli.get_image('odoo').get_image() + ' -- '
    params += ' --stop-after-init '
    params += ' --logfile=false '
    params += '-d ' + db + ' -u ' + ', '.join(mods) + ' '

    if e.debug_mode():
        params += '--debug'

    sc_(params)

    return True


def update_images_from_list(e, images):
    # avoid image duplicates
    tst_list = []
    unique_images = []
    for img in images:
        if img.getFormattedImage() not in tst_list:
            tst_list.append(img.getFormattedImage())
            unique_images.append(img)

    for img in unique_images:
        params = img.getPullImage()
        e.msginf('pulling image ' + img.getFormattedImage())
        if sc_(params):
            e.msgerr('Fail pulling image ' + img.get_name() + ' - Aborting.')
    return True


def update_repos_from_list(e, repos):
    # avoid repo duplicates
    tst_list = []
    unique_repos = []
    for repo in repos:
        if repo.get_formatted_repo() not in tst_list:
            tst_list.append(repo.get_formatted_repo())
            unique_repos.append(repo)

    for repo in unique_repos:
        # Check if repo exists
        if os.path.isdir(repo.getInstDir()):
            e.msginf('pull  ' + repo.get_formatted_repo())
            params = repo.getPullRepo()
        else:
            e.msginf('clone ' + repo.get_formatted_repo())
            params = repo.getCloneRepo()

        if sc_(params):
            e.msgerr('Fail installing environment, uninstall and try again.')

    return True


def install_client(e):
    # get clients to install from params
    clients = e.get_clients_from_params()
    if len(clients) > 1:
        plural = 's'
    else:
        plural = ''
    e.msgrun('Install client' + plural + ' ' + ', '.join(clients))

    for clientName in clients:
        cli = e.get_client(clientName)
        # Creating directory's for client
        sc_('mkdir -p ' + cli.get_home_dir() + cli.get_name() + '/config')
        sc_('mkdir -p ' + cli.get_home_dir() + cli.get_name() + '/data_dir')
        sc_('mkdir -p ' + cli.get_home_dir() + cli.get_name() + '/log')
        sc_('chmod 777 -R ' + cli.get_home_dir() + cli.get_name())
        sc_('mkdir -p ' + cli.get_home_dir() + 'sources')

        # if not exist postgresql create it
        if not os.path.isdir(e.getPsqlDir()):
            sc_('mkdir ' + e.getPsqlDir())

        # make sources dir
        # if not exist sources dir create it
        if not os.path.isdir(cli.get_home_dir() + 'sources'):
            sc_('mkdir -p ' + cli.get_home_dir() + 'sources')

        # clone or update repos as needed
        update_repos_from_list(e, cli.get_repos())

        # calculate addons path
        addons_path = cli.get_addons_path()

        # creating config file for client
        param = 'sudo docker run --rm '
        param += '-v ' + cli.get_home_dir() + cli.get_name() + '/config:/etc/odoo '
        param += '-v ' + cli.get_home_dir() + 'sources:/mnt/extra-addons '
        param += '-v ' + cli.get_home_dir() + cli.get_name() + '/data_dir:/var/lib/odoo '
        param += '-v ' + cli.get_home_dir() + cli.get_name() + '/log:/var/log/odoo '
        param += '--name ' + cli.get_name() + '_tmp '
        param += cli.get_image('odoo').get_image() + ' '
        param += '-- --stop-after-init -s '
        param += '--db-filter=' + cli.get_name() + '_.* '

        if addons_path != '':
            param += '--addons-path=' + addons_path + ' '

        param += '--logfile=/var/log/odoo/odoo.log '
        param += '--logrotate '

        e.msginf('creating config file')
        if sc_(param):
            e.msgerr('failing to write config file. Aborting')

    e.msgdone('Installing done')
    return True


def run_environment(e):
    e.msgrun('Running environment images')
    clientNames = e.get_clients_from_params()

    # TODO ver si lo modificamos para multiples clientes
    cli = e.get_client(clientNames[0])

    err = 0
    image = cli.get_image('postgres')
    params = 'sudo docker run -d '
    if e.debug_mode():
        params += '-p 5432:5432 '
    params += '-e POSTGRES_USER=odoo '
    params += '-e POSTGRES_PASSWORD=odoo '
    params += '-v ' + e.getPsqlDir() + ':/var/lib/postgresql/data '
    params += '--restart=always '
    params += '--name ' + image.get_name() + ' '
    params += image.get_image()
    err += sc_(params)

    image = cli.get_image('aeroo')
    params = 'sudo docker run -d '
    params += '-p 127.0.0.1:8989:8989 '
    params += '--name=' + image.get_name() + ' '
    params += '--restart=always '
    params += image.get_image()
    err += sc_(params)

    if err:
        e.msgerr('Fail running some images.')

    e.msgdone('images running')
    return True


def run_client(e):
    clients = e.get_clients_from_params()
    for clientName in clients:
        cli = e.get_client(clientName)
        txt = 'Running image for client ' + clientName
        if e.debug_mode():
            txt += ' with debug debug mode on port ' + cli.get_port()

        e.msgrun(txt)
        if e.debug_mode():
            params = 'sudo docker run --rm -it '
        else:
            params = 'sudo docker run -d '
        params += '--link aeroo:aeroo '
        params += '-p ' + cli.get_port() + ':8069 '
        params += '-v ' + cli.get_home_dir() + cli.get_name() + '/config:/etc/odoo '
        params += '-v ' + cli.get_home_dir() + cli.get_name() + '/data_dir:/var/lib/odoo '
        params += '-v ' + cli.get_home_dir() + 'sources:/mnt/extra-addons '
        params += '-v ' + cli.get_home_dir() + cli.get_name() + '/log:/var/log/odoo '
        params += '--link postgres:db '
        if not e.debug_mode():
            params += '--restart=always '
        params += '--name ' + cli.get_name() + ' '
        params += cli.get_image('odoo').get_image() + ' '
        if not e.no_dbfilter():
            params += '-- --db-filter=' + cli.get_name() + '_.* '
        if not e.debug_mode():
            params += '--logfile=/var/log/odoo/odoo.log '
            params += '--logrotate'
        else:
            params += '--logfile=False '
        if sc_(params):
            e.msgerr("Can't run client " + cli.get_name() +
                     ", by the way... did you run -R ?")
        e.msgdone('Client ' + clientName + ' up and running on port ' + cli.get_port())

    return True


def stop_client(e):
    clients = e.get_clients_from_params()
    e.msgrun('stopping clients ' + ', '.join(clients))

    for clientName in clients:
        e.msginf('stopping image for client ' + clientName)
        if sc_('sudo docker stop ' + clientName):
            e.msgerr('cannot stop client ' + clientName)

        if sc_('sudo docker rm ' + clientName):
            e.msgerr('cannot remove client ' + clientName)

    e.msgdone('all clients stopped')

    return True


def stopEnvironment(e):
    images_to_stop = ['postgres', 'aeroo']
    e.msgrun('Stopping images ' + ', '.join(images_to_stop))
    err = 0
    for name in images_to_stop:
        e.msgrun('Stopping image ' + name)
        err += sc_('sudo docker stop ' + name)
        err += sc_('sudo docker rm ' + name)

    if err:
        e.msgerr("errors stopping images")

    e.msgdone('Images stopped')
    return True


def pull_all(e):
    e.msgrun('--- Pulling all images')

    images = []
    for cli in e.getClients():
        if cli.get_name() in e.get_clients_from_params():
            images.extend(cli.get_images())
    update_images_from_list(e, images)

    e.msgdone('All images ok ')
    e.msgrun('--- Pulling all repos')

    repos = []
    for cli in e.getClients():
        if cli.get_name() in e.get_clients_from_params():
            repos.extend(cli.get_repos())
    update_repos_from_list(e, repos)

    e.msgdone('All repos ok ')

    return True


def list_data(e):
    # if no -c option get all clients else get -c clients
    if args.client is None:
        clients = e.getClients()
    else:
        clients = []
        for clientName in e.get_clients_from_params():
            clients.append(e.get_client(clientName))

    for cli in clients:
        e.msginf('client -- ' + cli.get_name(0) + ' -- on port ' + cli.get_port())

        e.msgrun(3 * '-' +
                 ' Images ' +
                 72 * '-')
        for image in cli.get_images():
            e.msgrun('   ' +
                     image.getFormattedImage())
        e.msgrun(' ')
        e.msgrun(3 * '-' + 'branch' +
                 4 * '-' + 'repository' +
                 25 * '-' + 'instalation dir' +
                 20 * '-')
        for repo in cli.get_repos():
            e.msgrun('   ' +
                     repo.get_formatted_repo() +
                     ' ' + repo.getInstDir())
        e.msgrun(' ')

    return True


def no_ip_install(e):
    e.msgrun('Installing no-ip client')
    sc_('sudo apt-get install make')
    sc_('sudo apt-get -y install gcc')
    sc_('wget -O /usr/local/src/noip.tar.gz \
    http://www.noip.com/client/linux/noip-duc-linux.tar.gz')
    sc_('sudo tar -xf noip.tar.gz -C /usr/local/src/')
    sc_('sudo wget -P /usr/local/src/ \
    http://www.noip.com/client/linux/noip-duc-linux.tar.gz')
    sc_('sudo tar xf /usr/local/src/noip-duc-linux.tar.gz -C /usr/local/src/')
    sc_('cd /usr/local/src/noip-2.1.9-1 && sudo make install')
    e.msginf("Please answer some questions")
    sc_('sudo rm /usr/local/src/noip-duc-linux.tar.gz')
    sc_('sudo cp /usr/local/src/noip-2.1.9-1/debian.noip2.sh  /etc/init.d/')
    sc_('sudo chmod +x /etc/init.d/debian.noip2.sh')
    sc_('sudo update-rc.d debian.noip2.sh defaults')
    sc_('sudo /etc/init.d/debian.noip2.sh restart')
    e.msgdone('no-ip service running')

    # To config defaults noip2 with capital C
    # sudo /usr/local/bin/noip2 -C
    return True


def docker_install(e):
    e.msgrun('Installing docker')
    sc_('wget -qO- https://get.docker.com/ | sh')
    e.msgdone('Done.')
    return True


def backup(e):
    dbname = e.get_database_from_params()
    clientName = e.get_clients_from_params('one')
    e.msgrun('Backing up database ' + dbname + ' of client ' + clientName)

    client = e.get_client(clientName)
    img = client.get_image('backup')

    params = 'sudo docker run --rm -i '
    params += '--link postgres:db '
    params += '--volumes-from ' + clientName + ' '
    params += '-v ' + client.get_backup_dir() + ':/backup '
    params += '--env DBNAME=' + dbname + ' '
    params += img.get_image() + ' backup'

    if sc_(params):
        e.msgerr('failing backup. Aborting')

    e.msgdone('Backup done')
    return True


def restore(e):
    dbname = e.get_database_from_params()
    clientName = e.get_clients_from_params('one')
    timestamp = e.get_timestamp_from_params()

    e.msgrun('Restoriing database ' + dbname + ' of client ' + clientName)

    client = e.get_client(clientName)
    img = client.get_image('backup')

    params = 'sudo docker run --rm -i '
    params += '--link postgres:db '
    params += '--volumes-from ' + clientName + ' '
    params += '-v ' + client.get_backup_dir() + ':/backup '
    params += '--env NEW_DBNAME=' + dbname + '-new '
    params += '--env DBNAME=' + dbname + ' '
    params += '--env DATE=' + timestamp + ' '
    params += img.get_image() + ' restore'

    if sc_(params):
        e.msgerr('failing backup. Aborting')

    e.msgdone('Backup done')
    return True


def decode_backup(root, filename):
    # bkp format: jeo_datos_201511022236

    # size of bkp
    path = os.path.join(root, filename + '.dump')
    try:
        size = os.stat(path).st_size
    except:
        size = 0

    # plus size of tar
    path = os.path.join(root, filename + '.tar')
    try:
        size += os.stat(path).st_size
    except:
        size += 0

    size = size / 1000

    # strip db name
    a = len(filename) - 13
    dbname = filename[0:a]

    # strip date
    date = filename[-12:]
    dt = datetime.strptime(date, '%Y%m%d%H%M')

    # format date
    fdt = datetime.strftime(dt, '%d/%m/%Y %H:%M')
    n = 15 - len(dbname)

    return dbname + n * ' ' + fdt + '  [' + date + '] ' + str(size) + 'k'


def backup_list(e):
    # if no -c option get all clients else get -c clients
    if args.client is None:
        clients = []
        for cli in e.getClients():
            clients.append(cli.get_name())
    else:
        clients = e.get_clients_from_params()

    for clientName in clients:
        cli = e.get_client(clientName)
        dir = cli.get_backup_dir()

        filenames = []
        # walk the backup dir
        for root, dirs, files in os.walk(dir):
            for file in files:
                # get the .dump files and decode it to human redable format
                filename, file_extension = os.path.splitext(file)
                if file_extension == '.dump':
                    filenames.append(filename)

        if len(filenames):
            filenames.sort()
            e.msgrun('List of available backups for client ' + clientName)
            for fn in filenames:
                e.msginf(decode_backup(root, fn))


def cleanup(e):
    if raw_input('Delete ALL databases for ALL clients SURE?? (y/n) ') == 'y':
        e.msginf('deleting all databases!')
        sc_(['sudo rm -r ' + e.getPsqlDir()])

    if raw_input('Delete clients and sources SURE?? (y/n) ') == 'y':
        e.msginf('deleting all client and sources!')
        sc_(['sudo rm -r ' + e._home_template + '*'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Odoo environment setup v 2.0')
    parser.add_argument('-i', '--install-cli',
                        action='store_true',
                        help="Install clients, requires -c option. You can define \
                        multiple clients like this: -c client1 -c client2 -c client3")

    parser.add_argument('-U', '--uninstall-cli',
                        action='store_true',
                        help='Uninstall client and erase all files from environment \
                        including \
                        database. The command ask for permission to erase database. \
                        BE WARNED if say yes, all database files will be erased. \
                        BE WARNED AGAIN, database is common to all clients!!!!  \
                        Required -c option')

    parser.add_argument('-R', '--run-env',
                        action='store_true',
                        help="Run database and aeroo images.")

    parser.add_argument('-S', '--stop-env',
                        action='store_true',
                        help="Stop database and aeroo images.")

    parser.add_argument('-r', '--run-cli',
                        action='store_true',
                        help="Run client odoo images, requieres -c options.")

    parser.add_argument('-s', '--stop-cli',
                        action='store_true',
                        help="Stop client images, requieres -c options.")

    parser.add_argument('-p', '--pull-all',
                        action='store_true',
                        help="Pull all images and repos.")

    parser.add_argument('-l', '--list',
                        action='store_true',
                        help="List all data in this server. Clients and images.")

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="Go verbose mode.")

    parser.add_argument('-n', '--no-ip-install',
                        action='store_true',
                        help="Install no-ip on this server.")

    parser.add_argument('-k', '--docker-install',
                        action='store_true',
                        help="Install docker on this server.")

    parser.add_argument('-u', '--update-db',
                        action='store_true',
                        help="Update database requires -d -c and -m options.")

    parser.add_argument('-d',
                        action='store',
                        nargs=1,
                        dest='database',
                        help="Database to update.")

    parser.add_argument('-t',
                        action='store',
                        nargs=1,
                        dest='timestamp',
                        help="Timestamp to restore database, see --backup-list \
                        for available timestamps.")

    parser.add_argument('-m',
                        action='append',
                        dest='module',
                        help="Module to update or all, you can specify multiple -m \
                        options.")

    parser.add_argument('-c',
                        action='append',
                        dest='client',
                        help="Client name. You define can define multiple clients \
                        like this: -c client1 -c client2 -c client3 and so one.")

    parser.add_argument('--backup',
                        action='store_true',
                        help="Lauch backup requieres -d and -c options.")

    parser.add_argument('--restore',
                        action='store_true',
                        help="Lauch restore requieres -d, -c and -t options.")

    parser.add_argument('--debug',
                        action='store_true',
                        help='This option has two efects: \
                             when doing an update database, (option -u) it forces \
                             debug mode. When running environment it opens port 5432 \
                             to access postgres server databases.')

    parser.add_argument('--backup-list',
                        action='store_true',
                        help="List available backups with timestamps to restore.")

    parser.add_argument('--cleanup',
                        action='store_true',
                        help='Delete all files clients, sources, and databases \
                         in this server. It ask about each thing.')

    parser.add_argument('--no-dbfilter',
                        action='store_true',
                        help='Eliminates dbfilter: The client can see any database. \
                        Without this, only sees databases starting with clientname_')

    args = parser.parse_args()
    enviro = Environment(args, clients__)

    if args.install_cli:
        install_client(enviro)
    if args.uninstall_cli:
        uninstall_client(enviro)
    if args.stop_env:
        stopEnvironment(enviro)
    if args.run_env:
        run_environment(enviro)
    if args.stop_cli:
        stop_client(enviro)
    if args.run_cli:
        run_client(enviro)
    if args.pull_all:
        pull_all(enviro)
    if args.list:
        list_data(enviro)
    if args.no_ip_install:
        no_ip_install(enviro)
    if args.docker_install:
        docker_install(enviro)
    if args.update_db:
        update_db(enviro)
    if args.backup:
        backup(enviro)
    if args.restore:
        restore(enviro)
    if args.backup_list:
        backup_list(enviro)
    if args.cleanup:
        cleanup(enviro)
