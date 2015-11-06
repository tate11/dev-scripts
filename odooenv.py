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

import argparse
import subprocess
import sys
import os

# TODO sacar el log fuera de la imagen.
# TODO archivo xml que sobreescriba clients.
# TODO evitar la duplicación de repos con el dict repos

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"

clients = [
    {'port': '8068', 'ver': '9.0', 'name': 'jeo'},
    {'port': '8069', 'ver': '8.0', 'name': 'makeover'},
    {'port': '8070', 'ver': '8.0', 'name': 'jeo'},
    {'port': '8071', 'ver': '8.0', 'name': 'demo'},
]

repos = {
    'origin': {
        'odoo-addons': {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '8.0'},
        'odoo-argentina': {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '8.0'},
    },
    'upstream': {
        'odoo-addons': {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
        'odoo-argentina': {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
    }
}

data = {
    # Version 9.0 experimental
    '9.0': {
        'images': {
            'odoo': {'repo': 'odoo', 'dir': '', 'ver': '9.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
        },

        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '9.0'},
        ],
    },

    # ultima version de adhoc
    '8.0.1': {
        'images': {
            'odoo': {'repo': 'adhoc', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'aeroo': {'repo': 'adhoc', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
        },

        'repos': [
            {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
            {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
            {'repo': 'aeroo', 'dir': 'aeroo_reports', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'web', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'management-system', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'knowledge', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'margin-analysis', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'},
            {'repo': 'oca', 'dir': 'account-financial-reporting', 'branch': '8.0'}
        ]
    },

    # version estable de jeo
    '8.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'aeroo': {'repo': 'jobiols', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''}
        },

        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'aeroo_reports', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'web', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'management-system', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'knowledge', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'rma', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'manufacture', 'branch': '8.0'},
        ]
    },

    # Version 7.0.1 experimental
    '7.0.1': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '7.0.1'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''}
        },

        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'odoo-mailchimp-tools', 'branch': 'master'}
        ],
    },

    # Version 7.0 de producción Makeover
    '7.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '7.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
        },

        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'}
        ],
    },

    'ou-8.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'docker-openupgrade', 'ver': '8.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
        },

        'repos': [
            {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
            {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '8.0'}
        ]
    },
}


def getImageFromName(ver, image):
    ret = ''
    image = data[ver]['images'][image]
    ret += image['repo']
    if image['dir'] != '':
        ret += '/'
        ret += image['dir']
    if image['ver'] != '':
        ret += ':' + image['ver']
    return ret


def getEnvironmentImages(ver):
    im1 = data[ver]['images']
    im2 = []
    for name in im1:
        if name <> 'odoo':
            im2.append(im1[name])
    return im2


def getAllImages(ver):
    return data[ver]['images']


def getClientPort(ver, clientName):
    port = ''
    for client in clients:
        if client['ver'] == ver and client['name'] == clientName:
            port = client['port']

    if port == '':
        msgerr('There is no ' + clientName + ' client in this environment.')
    return port


def getReposList(ver):
    return data[ver]['repos']


def formatRepoFromDict(dict):
    return dict['repo'] + '/' + dict['dir']


def green(string):
    return GREEN + string + CLEAR


def yellow(string):
    return YELLOW + string + CLEAR


def red(string):
    return RED + string + CLEAR


def yellow_light(string):
    return YELLOW_LIGHT + string + CLEAR


def msgrun(msg):
    print yellow(msg)


def msgdone(msg):
    print green(msg)


def msgerr(msg):
    print red(msg)
    sys.exit()


def msginf(msg):
    print yellow_light(msg)


def sc_(params):
    return subprocess.call(params, shell=True)


def uninstallEnvironment(ver):
    msgrun('Uninstalling odoo environment ' + ver)
    sc_(['sudo rm -r ' + HOME])
    if raw_input('Delete postgresql directory? (y/n) ') == 'y':
        sc_(['sudo rm -r ' + PSQL])
    return True


def installEnvironment(ver):
    msgrun('Installing odoo environment ' + ver)

    # if not exist postgresql create it
    if sc_(['ls ' + PSQL]):
        sc_(['mkdir ' + PSQL])

    # make sources dir
    sc_(['mkdir -p ' + HOME + 'sources'])

    # pull each repo in sources dir
    for repo in getReposList(ver):
        msginf('pulling repo ' + formatRepoFromDict(repo))

        params = 'git clone --depth 1 -b ' + \
                 repo['branch'] + ' http://github.com/' + formatRepoFromDict(repo) + \
                 ' ' + HOME + 'sources/' + repo['dir']

        if sc_(params):
            msgerr('Fail installing environment, uninstall and try again.')

    msgdone('Install Done ' + ver)
    return True


def updateDatabase(ver):
    db = args.database[0]
    mods = args.module
    cli = args.client[0]

    msg = 'Performing update'
    if mods[0] == 'all':
        msg += ' of all modules'
    else:
        msg += ' of module(s) ' + ', '.join(mods)

    msg += ' on database "' + db + '"'

    if args.debug:
        msg += ' forcing debug mode'
    msgrun(msg)

    params = 'sudo docker run --rm -it \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            -v ' + HOME + 'sources:/mnt/extra-addons \
            --link db-odoo:db ' + \
             getImageFromName(ver, 'odoo') + ' -- ' + \
             ' --stop-after-init \
             -d ' + db + ' -u ' + ', '.join(mods)

    if ver[0:1] == '7':
        params += ' --db_user=odoo --db_password=odoo --db_host=db '

    if args.debug:
        params += ' --debug'

    sc_(params)

    return True


def installClient(ver):
    msgrun('Install clients')

    # Calculate addon_path
    path = '/mnt/extra-addons/'
    repos = getReposList(ver)

    lis = []
    for dir in repos:
        lis.append(path + dir['dir'])
    addon_path = ','.join(lis)

    for cli in args.client:
        msgrun('Installing Odoo image for client ' + cli)

        # Creating directory's for client
        sc_('mkdir -p ' + HOME + cli + '/config')
        sc_('mkdir -p ' + HOME + cli + '/data_dir')
        sc_('chmod 777 -R ' + HOME + cli)

        # creating config file for client
        param = 'sudo docker run --rm \
                -v ' + HOME + cli + '/config:/etc/odoo \
                -v ' + HOME + 'sources:/mnt/extra-addons \
                -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
                --name ' + cli + '_tmp ' + getImageFromName(ver, 'odoo') \
                + ' -- --stop-after-init -s ' \
                  ' --db-filter=' + cli + '_.* '

        if addon_path <> '':
            param += '--addons-path=' + addon_path

        if sc_(param):
            msgerr('failing to write config file. Aborting')

    msgdone('Installing done')
    return True


def run_aeroo_image(ver):
    params = 'sudo docker run -d \
        -p 127.0.0.1:8989:8989   \
        --name="aeroo_docs"   \
        --restart=always ' \
             + getImageFromName(ver, 'aeroo')

    if sc_(params):
        msginfo('Fail running aeroo-image.')

    return True


def runEnvironment(ver):
    msgrun('Running environment images v' + ver)

    if ver[0:1] == '8':
        run_aeroo_image(ver)

    params = 'sudo docker run -d \
                    -e POSTGRES_USER=odoo \
                    -e POSTGRES_PASSWORD=odoo \
                    -v ' + PSQL + ':/var/lib/postgresql/data \
                    --restart=always \
                    --name db-odoo ' + \
             getImageFromName(ver, 'postgres')

    if sc_(params):
        msgerr('Fail running environment')
    else:
        msgdone("Environment up and running")
    return True


def runClient(ver):
    for cli in args.client:
        msgrun('Running image for client ' + cli)
        params = 'sudo docker run -d \
                 --link aeroo_docs:aeroo  \
                 -p ' + getClientPort(ver, cli) + ':8069  \
                 -v ' + HOME + cli + '/config:/etc/odoo  \
                 -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
                 -v ' + HOME + '/sources:/mnt/extra-addons  \
                 --link db-odoo:db  \
                 --restart=always  \
                 --name ' + cli + ' ' + \
                 getImageFromName(ver, 'odoo') + ' -- --db-filter=' + cli + '_.*',

        if ver[0:1] == '7':
            params += ' --db_user=odoo --db_password=odoo --db_host=db'

        if not sc_(params):
            msgdone(
                'Client ' + cli + ' up and running on port ' + getClientPort(ver, cli))
        else:
            msgerr("Can't run client " + cli + ", by the way... did you run -R ?")

    return True


def run_developer(ver):
    msgrun('Running environment in developer mode.')

    if ver[0:1] == '8':
        run_aeroo_image(ver)

    params = 'sudo docker run -d \
              -p 5432:5432 \
              -e POSTGRES_USER=odoo \
              -e POSTGRES_PASSWORD=odoo \
              -v ' + PSQL + ':/var/lib/postgresql/data \
              --restart=always \
              --name db-odoo ' + \
             getImageFromName(ver, 'postgres')

    if sc_(params):
        msgerr('Fail running postgres image.')
    msgdone('Environment up and running.')
    return True


def stopClient(ver):
    msgrun('stopping clients ' + ', '.join(args.client))
    for cli in args.client:
        msginf('stop image for client ' + cli)
        sc_('sudo docker stop ' + cli)
        sc_('sudo docker rm ' + cli)

    msgdone('all clients stopped')

    return True


def stopEnvironment(ver):
    r1 = r2 = 0
    msgrun('Stopping environment ' + ver)
    for name in ['db-odoo', 'aeroo_docs']:
        msgrun('Stopping image ' + name)

        r1 += sc_('sudo docker stop ' + name)
        r2 += sc_('sudo docker rm ' + name)

    if r1 + r2 <> 0:
        msgerr('some images can not be stopped')

    msgdone('Environment stopped')
    return True


def pullAll(ver):
    msgrun('Pulling all images for ' + ver)

    for image_name in data[ver]['images']:
        image = getImageFromName(ver, image_name)
        msginf('Pulling ' + image)
        if sc_('sudo docker pull ' + image):
            msgerr('Fail pulling image ' + image + ' - Aborting.')

    msgdone('All images ok ' + ver)

    msgrun('Pulling all repos for ' + ver)
    for repo in getReposList(ver):
        msginf('pulling repo ' + formatRepoFromDict(repo))
        params = 'cd ' + HOME + 'sources/' + repo['dir'] + '&&' + ' sudo git pull'
        if sc_(params):
            msgerr('Fail pulling repos, uninstall and try again. \
            By the way... did you run -I ?')

    msgdone('All repos ok ' + ver)

    return True


def listData(ver):
    msgrun('Data for this environment - Odoo ' + ver)
    msgrun('Images ' + 19 * '-')
    for image in data[ver]['images']:
        msgdone(getImageFromName(ver, image))

    msgrun('Repos ' + 20 * '-')
    for rep in getReposList(ver):
        msgdone(formatRepoFromDict(rep) + '  b ' + rep['branch'])

    msgrun('Repos ' + 30 * '-')
    for remote in repos:
        msgrun(remote)
        for repo_name in repos[remote]:
            print formatRepoFromDict(repos[remote][repo_name]), 'b ', \
                repos[remote][repo_name]['branch']

    msgrun('Clients ' + 18 * '-')
    for client in clients:
        if client['ver'] == ver:
            msgrun(client['port'] + ' ' + client['name'])

    return True


def noIpInstall(ver):
    msgrun('Installing no-ip client')
    sc_('sudo apt-get install make')
    sc_('sudo apt-get -y install gcc')
    sc_('wget -O /usr/local/src/noip.tar.gz \
    http://www.noip.com/client/linux/noip-duc-linux.tar.gz')
    sc_('sudo tar -xf noip.tar.gz -C /usr/local/src/')
    sc_('sudo wget -P /usr/local/src/ \
    http://www.noip.com/client/linux/noip-duc-linux.tar.gz')
    sc_('sudo tar xf /usr/local/src/noip-duc-linux.tar.gz -C /usr/local/src/')
    sc_('cd /usr/local/src/noip-2.1.9-1 && sudo make install')
    msginf("Please answer some questions")
    sc_('sudo rm /usr/local/src/noip-duc-linux.tar.gz')
    sc_('sudo cp /usr/local/src/noip-2.1.9-1/debian.noip2.sh  /etc/init.d/')
    sc_('sudo chmod +x /etc/init.d/debian.noip2.sh')
    sc_('sudo update-rc.d debian.noip2.sh defaults')
    sc_('sudo /etc/init.d/debian.noip2.sh restart')
    msgdone('no-ip service running')

    # To config defaults noip2 with capital C
    # sudo /usr/local/bin/noip2 -C
    return True


def dockerInstall(ver):
    msgrun('Installing docker')
    sc_('wget -qO- https://get.docker.com/ | sh')
    msgdone('Done.')
    return True


def backup(ver):
    dbname = args.database[0]
    client = args.client[0]
    msgrun('Backing up database client ' + client + ' with db ' + dbname)

    params = 'sudo docker run --rm -i \
                --link db-odoo:db \
                --volumes-from ' + client + '  \
                -v ' + HOME + client + '/' + 'backup/' + ':/backup  \
                --env DBNAME=' + dbname + ' \
                jobiols/backup backup'

    if sc_(params):
        msgerr('failing backup. Aborting')

    msgdone('Backup done')
    return True


def backup_list(ver):
    client = args.client[0]
    dir = HOME + client + '/' + 'backup/'
    msgrun('List of available backups')

    for root, dirs, files in os.walk(dir):
        for file in files:
            print file

if __name__ == '__main__':
    choices = []
    for opt in data:
        choices.append(opt)

    parser = argparse.ArgumentParser(description='Odoo environment setup v 1.3')
    parser.add_argument('version', choices=choices)

    parser.add_argument('-U', '--uninstall-env',
                        action='store_true',
                        help='Uninstall and erase all files from environment including \
                        database (only current ver). The command ask for permission to \
                        erase database. BE WARNED if say yes, all database files will be erased.')

    parser.add_argument('-I', '--install-env',
                        action='store_true',
                        help="Install all files and odoo repos needed. It will try to \
                        install postgres dir if doesn't exist")

    parser.add_argument('-i', '--install-cli',
                        action='store_true',
                        help="Install clients, requires -c option. You can define \
                        multiple clients like this: -c client1 -c client2 -c client3")

    parser.add_argument('-R', '--run-env',
                        action='store_true',
                        help="Run database and aeroo images.")

    parser.add_argument('-D', '--run-dev',
                        action='store_true',
                        help="Run database and aeroo images for developer mode (local db access).")

    parser.add_argument('-r', '--run-cli',
                        action='store_true',
                        help="Run client odoo images, requieres -c options.")

    parser.add_argument('-S', '--stop-env',
                        action='store_true',
                        help="Stop database and aeroo images.")

    parser.add_argument('-s', '--stop-cli',
                        action='store_true',
                        help="Stop client images, requieres -c options.")

    parser.add_argument('-p', '--pull-all',
                        action='store_true',
                        help="Pull all images")

    parser.add_argument('-l', '--list',
                        action='store_true',
                        help="List all data in this server. Clients and images.")

    parser.add_argument('-c',
                        action='append',
                        dest='client',
                        help="Client name. You define multiple clients like this \
                        multiple clients like this: -c client1 -c client2 -c client3")

    parser.add_argument('-n', '--no-ip-install',
                        action='store_true',
                        help="Install no-ip on this server")

    parser.add_argument('-k', '--docker-install',
                        action='store_true',
                        help="Install docker on this server")

    parser.add_argument('-u', '--update-database',
                        action='store_true',
                        help="Update database requires -d -c and -m options")

    parser.add_argument('-d', '--database',
                        action='store',
                        nargs=1,
                        dest='database',
                        help="Database to update")

    parser.add_argument('-m', '--module',
                        action='append',
                        dest='module',
                        help="Module to update or all, you can specify multiple -m options")

    parser.add_argument('--backup',
                        action='store_true',
                        help="Lauch backup")

    parser.add_argument('--debug',
                        action='store_true',
                        help="force debug mode on update database")

    parser.add_argument('--backup-list',
                        action='store_true',
                        help="List available backups")

    args = parser.parse_args()

    # Constant Definitins
    HOME = os.path.expanduser('~/odoo-' + args.version + '/')
    PSQL = os.path.expanduser('~/postgresql' + '/')

    # Check for valid client
    if args.client != None:
        for cli in args.client:
            getClientPort(args.version, cli)

    if args.uninstall_env:
        uninstallEnvironment(args.version)
    if args.install_env:
        installEnvironment(args.version)
    if args.install_cli:
        installClient(args.version)
    if args.stop_env:
        stopEnvironment(args.version)
    if args.run_env:
        runEnvironment(args.version)
    if args.run_dev:
        run_developer(args.version)
    if args.stop_cli:
        stopClient(args.version)
    if args.run_cli:
        runClient(args.version)
    if args.pull_all:
        pullAll(args.version)
    if args.list:
        listData(args.version)
    if args.no_ip_install:
        noIpInstall(args.version)
    if args.docker_install:
        dockerInstall(args.version)
    if args.update_database:
        updateDatabase(args.version)
    if args.backup:
        backup(args.version)
    if args.backup_list:
        backup_list(args.version)
