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
from datetime import datetime

# TODO sacar el log fuera de la imagen.
# TODO archivo xml que sobreescriba clients.

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"

clients_ = [
    {'port': '8068', 'ver': '9.0', 'name': 'jeo'},
    {'port': '8069', 'ver': '8.0', 'name': 'makeover'},
    {'port': '8070', 'ver': '8.0', 'name': 'jeo'},
    {'port': '8071', 'ver': '8.0', 'name': 'demo'},
]

# TODO evitar la duplicación de repos con el dict repos
repos_ = {
    'origin': {
        'odoo-addons': {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '8.0'},
        'odoo-argentina': {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '8.0'},
    },
    'upstream': {
        'odoo-addons': {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
        'odoo-argentina': {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
    }
}

data_ = {
    # Version 9.0 experimental
    '9.0': {
        'images': {
            'odoo': {'repo': 'odoo', 'dir': '', 'ver': '9.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'aeroo': {'repo': 'jobiols', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
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


class environment:
    """Contiene la definicion del ambiente"""

    def __init__(self, args):
        self.HOME = os.path.expanduser('~/odoo-' + args.version + '/')
        self.PSQL = os.path.expanduser('~/postgresql' + '/')
        self._clients = clients_
        self._repos = repos_
        self._data = data_[args.version]
        self.ver = args.version
        self.args = args

        # Check for valid client
        if args.client != None:
            for cli in args.client:
                self.getClientPort(cli)

    def getClientPort(self, clientName):
        port = ''
        for client in self._clients:
            if client['ver'] == self.ver and client['name'] == clientName:
                port = client['port']

        if port == '':
            msgerr('There is no ' + clientName + ' client in this environment.')
        return port

    def checkClient(self):
        if self.args.client == None:
            msgerr('need -c option')

    def checkModules(self):
        if self.args.module == None:
            msgerr('need -m option')

    def checkDatabase(self):
        if self.args.database == None:
            msgerr('need -d option')

    def GetClientsFromParams(self):
        self.checkClient()
        return args.client

    def GetModulesFromParams(self):
        self.checkModules()
        return args.module

    def GetDatabaseFromParams(self):
        self.checkDatabase()
        return self.args.database[0]

    def GetClients(self):
        ret = []
        for cli in self._clients:
            if cli['ver'] == self.ver:
                ret.append(cli)
        return ret

    def GetClientFromParams(self):
        self.checkClient()
        if len(self.args.client) > 1:
            msgerr('only one client expected')
        return self.args.client[0]

    def DebugMode(self):
        return self.args.debug

    def GetData(self):
        return self._data

    def getReposList(self):
        return self._data['repos']

    def formatRepoFromDict(self, dict):
        return dict['repo'] + '/' + dict['dir']

    def formatImageFromName(self, imageName):
        ret = ''
        imageDict = self._data['images'][imageName]
        ret += imageDict['repo']
        if imageDict['dir'] != '':
            ret += '/'
            ret += imageDict['dir']
        if imageDict['ver'] != '':
            ret += ':' + imageDict['ver']
        return ret

    def backupdir(self):
        return '/backup/' + self.ver + '/' + self.GetClientFromParams()


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


# TODO eliminar también el backup dir pidiendo permiso antes
def uninstallEnvironment(e):
    msgrun('Uninstalling odoo environment ' + e.ver)
    sc_(['sudo rm -r ' + e.HOME])
    if raw_input('Delete postgresql directory? (y/n) ') == 'y':
        sc_(['sudo rm -r ' + e.PSQL])
    return True


def installEnvironment(e):
    msgrun('Installing odoo environment ' + e.ver)

    # if not exist postgresql create it
    if sc_(['ls ' + e.PSQL]):
        sc_(['mkdir ' + e.PSQL])

    # make sources dir
    sc_(['mkdir -p ' + e.HOME + 'sources'])

    # pull each repo in sources dir
    for repo in e.getReposList():
        msginf('pulling repo ' + e.formatRepoFromDict(repo))

        params = 'git clone --depth 1 -b ' + \
                 repo['branch'] + ' http://github.com/' + e.formatRepoFromDict(repo) + \
                 ' ' + e.HOME + 'sources/' + repo['dir']

        if sc_(params):
            msgerr('Fail installing environment, uninstall and try again.')

    msgdone('Install Done ' + e.ver)
    return True


def updateDatabase(e):
    mods = e.GetModulesFromParams()
    db = e.GetDatabaseFromParams()
    cli = e.GetClientFromParams()

    msg = 'Performing update'
    if mods[0] == 'all':
        msg += ' of all modules'
    else:
        msg += ' of module(s) ' + ', '.join(mods)

    msg += ' on database "' + db + '"'

    if e.DebugMode():
        msg += ' forcing debug mode'
    msgrun(msg)

    params = 'sudo docker run --rm -it \
            -v ' + e.HOME + cli + '/config:/etc/odoo \
            -v ' + e.HOME + cli + '/data_dir:/var/lib/odoo \
            -v ' + e.HOME + 'sources:/mnt/extra-addons \
            --link db-odoo:db ' + \
             e.formatImageFromName('odoo') + ' -- ' + \
             ' --stop-after-init \
             -d ' + db + ' -u ' + ', '.join(mods)

    if e.ver[0:1] == '7':
        params += ' --db_user=odoo --db_password=odoo --db_host=db '

    if e.DebugMode():
        params += ' --debug'

    sc_(params)

    return True


def installClient(e):
    msgrun('Install clients')

    # Calculate addon_path
    path = '/mnt/extra-addons/'
    repos = e.getReposList()

    lis = []
    for dir in repos:
        lis.append(path + dir['dir'])
    addon_path = ','.join(lis)

    for cli in e.GetClientsFromParams():
        msgrun('Installing Odoo image for client ' + cli)

        # Creating directory's for client
        sc_('mkdir -p ' + e.HOME + cli + '/config')
        sc_('mkdir -p ' + e.HOME + cli + '/data_dir')
        sc_('chmod 777 -R ' + e.HOME + cli)

        # creating config file for client
        param = 'sudo docker run --rm \
                -v ' + e.HOME + cli + '/config:/etc/odoo \
                -v ' + e.HOME + 'sources:/mnt/extra-addons \
                -v ' + e.HOME + cli + '/data_dir:/var/lib/odoo \
                --name ' + cli + '_tmp ' + e.formatImageFromName('odoo') \
                + ' -- --stop-after-init -s ' \
                  ' --db-filter=' + cli + '_.* '

        if addon_path <> '':
            param += '--addons-path=' + addon_path

        if sc_(param):
            msgerr('failing to write config file. Aborting')

    msgdone('Installing done')
    return True


def run_aeroo_image(e):
    params = 'sudo docker run -d \
        -p 127.0.0.1:8989:8989   \
        --name="aeroo_docs"   \
        --restart=always ' \
             + e.formatImageFromName('aeroo')

    if sc_(params):
        msginfo('Fail running aeroo-image.')

    return True


def runEnvironment(e):
    msgrun('Running environment images v' + e.ver)

    if e.ver[0:1] <> '7':
        run_aeroo_image(e)

    params = 'sudo docker run -d \
                    -e POSTGRES_USER=odoo \
                    -e POSTGRES_PASSWORD=odoo \
                    -v ' + e.PSQL + ':/var/lib/postgresql/data \
                    --restart=always \
                    --name db-odoo ' + \
             e.formatImageFromName('postgres')

    if sc_(params):
        msgerr('Fail running environment')
    else:
        msgdone("Environment up and running")
    return True


def runClient(e):
    for cli in e.GetClientsFromParams():
        msgrun('Running image for client ' + cli)
        params = 'sudo docker run -d \
                 --link aeroo_docs:aeroo  \
                 -p ' + e.getClientPort(cli) + ':8069  \
                 -v ' + e.HOME + cli + '/config:/etc/odoo  \
                 -v ' + e.HOME + cli + '/data_dir:/var/lib/odoo \
                 -v ' + e.HOME + '/sources:/mnt/extra-addons  \
                 --link db-odoo:db  \
                 --restart=always  \
                 --name ' + cli + ' ' + \
                 e.formatImageFromName('odoo') + ' -- --db-filter=' + cli + '_.*',

        if e.ver[0:1] == '7':
            params += ' --db_user=odoo --db_password=odoo --db_host=db'

        if not sc_(params):
            msgdone(
                'Client ' + cli + ' up and running on port ' + e.getClientPort(cli))
        else:
            msgerr("Can't run client " + cli + ", by the way... did you run -R ?")

    return True


def runDeveloper(e):
    msgrun('Running environment in developer mode.')

    if e.ver[0:1] <> '7':
        run_aeroo_image(e)

    params = 'sudo docker run -d \
              -p 5432:5432 \
              -e POSTGRES_USER=odoo \
              -e POSTGRES_PASSWORD=odoo \
              -v ' + e.PSQL + ':/var/lib/postgresql/data \
              --restart=always \
              --name db-odoo ' + \
             e.formatImageFromName('postgres')

    if sc_(params):
        msgerr('Fail running postgres image.')
    msgdone('Environment up and running.')
    return True


def stopClient(e):
    msgrun('stopping clients ' + ', '.join(e.GetClientsFromParams()))
    for cli in e.GetClientsFromParams():
        msginf('stop image for client ' + cli)
        sc_('sudo docker stop ' + cli)
        sc_('sudo docker rm ' + cli)

    msgdone('all clients stopped')

    return True


def stopEnvironment(e):
    r1 = r2 = 0
    msgrun('Stopping environment ' + e.ver)
    for name in ['db-odoo', 'aeroo_docs']:
        msgrun('Stopping image ' + name)

        r1 += sc_('sudo docker stop ' + name)
        r2 += sc_('sudo docker rm ' + name)

    if r1 + r2 <> 0:
        msgerr('some images can not be stopped')

    msgdone('Environment stopped')
    return True


def pullAll(e):
    msgrun('Pulling all images for ' + e.ver)

    for image_name in e.GetData()['images']:
        image = e.formatImageFromName(image_name)
        msginf('Pulling ' + image)
        if sc_('sudo docker pull ' + image):
            msgerr('Fail pulling image ' + image + ' - Aborting.')

    msgdone('All images ok ' + e.ver)

    msgrun('Pulling all repos for ' + e.ver)
    for repo in e.getReposList():
        msginf('pulling repo ' + e.formatRepoFromDict(repo))
        params = 'cd ' + e.HOME + 'sources/' + repo['dir'] + '&&' + ' sudo git pull'
        if sc_(params):
            msgerr('Fail pulling repos, uninstall and try again. \
            By the way... did you run -I ?')

    msgdone('All repos ok ' + e.ver)

    return True


def listData(e):
    msgrun('Data for this environment - Odoo ' + e.ver)
    msgrun('Images ' + 19 * '-')

    for image in e.GetData()['images']:
        msgdone(e.formatImageFromName(image))

    msgrun('Repos ' + 20 * '-')
    for rep in e.getReposList():
        msgdone(e.formatRepoFromDict(rep) + '  b ' + rep['branch'])

    msgrun('Repos ' + 30 * '-')
    for remote in e.getReposList():
        msgrun('b ' + remote['branch'] + ' ' + e.formatRepoFromDict(remote))

    msgrun('Clients ' + 18 * '-')
    for client in e.GetClients():
        msgrun(client['port'] + ' ' + client['name'])

    return True


def noIpInstall(e):
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


def dockerInstall(e):
    msgrun('Installing docker')
    sc_('wget -qO- https://get.docker.com/ | sh')
    msgdone('Done.')
    return True


def backup(e):
    dbname = e.GetDatabaseFromParams()
    client = e.GetClientFromParams()
    msgrun('Backing up database client ' + client + ' with db ' + dbname)

    params = 'sudo docker run --rm -i \
                --link db-odoo:db \
                --volumes-from ' + client + '  \
                -v ' + e.backupdir() + ':/backup  \
                --env DBNAME=' + dbname + ' \
                jobiols/backup backup'

    if sc_(params):
        msgerr('failing backup. Aborting')

    msgdone('Backup done')
    return True


def decodeBackup(filename):
    # bkp format: jeo_datos_201511022236

    # strip db name
    a = len(filename) - 13
    dbname = filename[0:a]

    # strip date
    date = filename[-12:]
    dt = datetime.strptime(date, '%Y%m%d%H%M')

    # format date
    fdt = datetime.strftime(dt, '%d/%m/%Y %H:%M')
    n = 15 - len(dbname)

    return dbname + n * ' ' + fdt + '  [' + date + ']'


def backup_list(e):
    dir = e.backupdir()
    msgrun('List of available backups for client ' + e.GetClientFromParams())

    fns = []
    # walk the backup dir
    for root, dirs, files in os.walk(dir):
        for file in files:
            # get the .dump files and decode it to human redable format
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.dump':
                fns.append(filename)

    fns.sort()
    for fn in fns:
        print decodeBackup(fn)


if __name__ == '__main__':
    choices = []
    for opt in data_:
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
                        help="Lauch backup requieres -d y -c")

    parser.add_argument('--debug',
                        action='store_true',
                        help="force debug mode on update database")

    parser.add_argument('--backup-list',
                        action='store_true',
                        help="List available backups")

    args = parser.parse_args()

    env = environment(args)

    if args.uninstall_env:
        uninstallEnvironment(env)
    if args.install_env:
        installEnvironment(env)
    if args.install_cli:
        installClient(env)
    if args.stop_env:
        stopEnvironment(env)
    if args.run_env:
        runEnvironment(env)
    if args.run_dev:
        runDeveloper(env)
    if args.stop_cli:
        stopClient(env)
    if args.run_cli:
        runClient(env)
    if args.pull_all:
        pullAll(env)
    if args.list:
        listData(env)
    if args.no_ip_install:
        noIpInstall(env)
    if args.docker_install:
        dockerInstall(env)
    if args.update_database:
        updateDatabase(env)
    if args.backup:
        backup(env)
    if args.backup_list:
        backup_list(env)
