#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##############################################################################
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
# ##############################################################################

import argparse
import subprocess
import sys

# root = etree.Element('root')
# etree.SubElement(root,"c1")
# etree.SubElement(root,"c2")
# etree.SubElement(root,"c3")
# print(etree.tostring(root, pretty_print=True))

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"

# TODO sacar la info a un xml "http://lxml.de/tutorial.html"

data = {
    # Version 9.0 experimental
    '9.0': {
        'images': {
            'odoo': {'repo': 'adhoc', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
        },

        'clients': [
            {'client': 'jeo', 'port': '8069'},
        ],
        'repos': [
        ],
    },

    # version estable de jeo
    '8.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'aeroo': {'repo': 'jobiols', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''}
        },

        'clients': [
            {'client': 'str', 'port': '8070'},
            {'client': 'makeover', 'port': '8069'},
        ],
        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'aeroo_reports', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'web', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'management-system', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'knowledge', 'branch': '8.0'},
        ]
    },

    # ultima version de adhoc
    '8.0.1': {
        'images': {
            'odoo': {'repo': 'adhoc', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'aeroo': {'repo': 'adhoc', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
        },

        'clients': [
            {'client': 'jeo', 'port': '8070'},
            {'client': 'makeover', 'port': '8050'}
        ],

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

    # Version 7.0 de producción Makeover
    '7.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '7.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
        },

        'clients': [
            {'client': 'makeover', 'port': '8069'},
            {'client': 'pirulo', 'port': '8070'}
        ],
        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'}
        ],
    },

    # Version 7.0.1 experimental
    '7.0.1': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '7.0.1'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''}
        },

        'clients': [
            {'client': 'makeover', 'port': '8069'},
            {'client': 'pirulo', 'port': '8070'},
        ],

        'repos': [
            {'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'},
            {'repo': 'jobiols', 'dir': 'odoo-mailchimp-tools', 'branch': 'master'}
        ],
    },



    'ou-8.0': {
        'images': {
            'odoo': {'repo': 'jobiols', 'dir': 'docker-openupgrade', 'ver': '8.0'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
        },

        'clients': [
            {'client': 'makeover', 'port': '8069'},
            {'client': 'jeo', 'port': '8070'}
        ],

        'repos': [
            {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
            {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'jobiols', 'dir': 'str', 'branch': '8.0'}
        ]
    },

    '8.0.2': {
        'images': {
            'odoo': {'repo': 'adhoc', 'dir': 'odoo-adhoc', 'ver': '8.0'},
            'aeroo': {'repo': 'jobiols', 'dir': 'aeroo-docs', 'ver': 'latest'},
            'postgres': {'repo': 'postgres', 'dir': '', 'ver': '9.4'},
            'backup': {'repo': 'jobiols', 'dir': 'backup', 'ver': ''},
        },
        'clients': [
            {'client': 'str', 'port': '8069'},
            {'client': 'makeover', 'port': '8070'}
        ],

        'repos': [
            {'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0.x'},
            {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0.x'},
            {'repo': 'aeroo', 'dir': 'aeroo_reports', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'web', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'management-system', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'knowledge', 'branch': '8.0'},
            {'repo': 'oca', 'dir': 'margin-analysis', 'branch': '8.0'}
        ]
    }
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
    im = data[ver]
    im1 = im['images']
    im2 = []
    for name in im1:
        if name <> 'odoo':
            im2.append(im1[name])
    return im2


def getAllImages(ver):
    im = data[ver]
    im1 = im['images']
    return im1


def data2clients(ver):
    im = data[ver]
    cl = im['clients']
    return cl


def getReposList(ver):
    return data[ver]['repos']


def data2clients(ver):
    im = data[ver]
    re = im['clients']
    return re


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


def getClientPort(ver, clientName):
    port = ''
    for client in data[ver]['clients']:
        if client['client'] == clientName:
            port = client['port']
    if port == '':
        msgerr('There is no ' + clientName + ' client in this environment.')
    return port


def uninstallEnvironment(ver):
    msgrun('Uninstalling odoo environment ' + ver)
    subprocess.call(['sudo rm -r ' + HOME], shell=True)
    if raw_input('Delete postgresql directory? (y/n) ') == 'y':
        subprocess.call(['sudo rm -r ' + PSQL], shell=True)
    return True


def installEnvironment(ver):
    msgrun('Installing odoo environment ' + ver)

    # if not exist psql create it
    if subprocess.call(['ls ' + PSQL], shell=True):
        subprocess.call(['mkdir ' + PSQL], shell=True)

    # make sources dir
    subprocess.call(['mkdir -p ' + HOME + 'sources'], shell=True)

    # pull each repo in sources dir
    for repo in getReposList(ver):
        msginf('pulling repo ' + formatRepoFromDict(repo))
        if subprocess.call('git clone -b ' + repo['branch'] + ' --depth 1 http://github.com/' +
                                   formatRepoFromDict(repo) + ' ' + HOME + 'sources/' + repo['dir'],
                           shell=True):
            msgerr('Fail installing environment, uninstall and try again.')

    msgdone('Install Done ' + ver)
    return True


def update_database(ver):
    db = args.database[0]
    mods = args.module[0]
    cli = args.client[0]

    msgrun('Performing update database on ' + db + ' with module ' + ', '.join(mods))
    if ver[0:1] == '7':
        subprocess.call(
            'sudo docker run --rm -it \
            -p ' + getClientPort(ver, cli) + ':8069 \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            -v ' + HOME + 'sources:/mnt/extra-addons \
            --link db-odoo:db \
            --name ' + cli + '-update ' + \
            getImageFromName(ver, 'odoo') + ' -- '
                                            ' --db_user=odoo --db_password=odoo --db_host=db ' +
            ' --stop-after-init -d ' + db + ' -u ' + ', '.join(mods)
            , shell=True)
    else:
        subprocess.call(
            'sudo docker run --rm -it \
            -p ' + getClientPort(ver, cli) + ':8069 \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            -v ' + HOME + '/sources:/mnt/extra-addons \
            --link db-odoo:db \
            --name ' + cli + '-update ' + \
            getImageFromName(ver, 'odoo') + ' -- '
                                            ' --stop-after-init -d ' + db + ' -u ' + ', '.join(mods)
            , shell=True)

    return True


def installClient(ver):
    msgrun('Install clients')

    # Calculate addon_path
    path = '/mnt/extra-addons/'
    repos = getReposList(ver)
    addon_path = path + repos[0]['dir']
    for rep in repos[1:]:
        addon_path += ',' + path + rep['dir']

    for cli in args.client:
        msgrun('Installing Odoo image for client ' + cli)

        # Creating directory's for client
        subprocess.call('mkdir -p ' + HOME + cli + '/config', shell=True)
        subprocess.call('mkdir -p ' + HOME + cli + '/data_dir', shell=True)
        subprocess.call('chmod 777 -R ' + HOME + cli, shell=True)

        # creating config file for client
        if subprocess.call('sudo docker run --rm \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + 'sources:/mnt/extra-addons \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            --name ' + cli + '_tmp ' + getImageFromName(ver, 'odoo')
                                   + ' -- --stop-after-init -s \
            --addons-path=' + addon_path + ' --db-filter=' + cli + '_.*'
                , shell=True):
            msgerr('failing to write config file. Aborting')

    msgdone('Installing done')
    return True


def run_aeroo_image(ver):
    if subprocess.call('sudo docker run -d \
                    -p 127.0.0.1:8989:8989 \
                    --name="aeroo_docs" \
                    --restart=always ' + \
                    getImageFromName(ver, 'aeroo'), shell=True):
        msginfo('Fail running aeroo-image.')
    return True


def runEnvironment(ver):
    msgrun('Running environment images v' + ver)

    if ver[0:1] == '8':
        run_aeroo_image(ver)

    if subprocess.call('sudo docker run -d \
                    -e POSTGRES_USER=odoo \
                    -e POSTGRES_PASSWORD=odoo \
                    -v ' + PSQL + ':/var/lib/postgresql/data \
                    --restart=always \
                    --name db-odoo ' + \
                               getImageFromName(ver, 'postgres'), shell=True):
        msgerr('Fail running environment')
    else:
        msgdone("Environment up and running")
    return True


def run_developer(ver):
    msgrun('Running environment in developer mode.')

    if ver[0:1] == '8':
        run_aeroo_image(ver)

    if subprocess.call('sudo docker run -d \
                       -p 5432:5432 \
                       -e POSTGRES_USER=odoo \
                       -e POSTGRES_PASSWORD=odoo \
                       -v ' + PSQL + ':/var/lib/postgresql/data \
                    --restart=always \
                    --name db-odoo ' + \
                               getImageFromName(ver, 'postgres'), shell=True):
        msgerr('Fail running postgres image.')
    msgdone('Environment up and running.')
    return True


def run_client(ver):
    for cli in args.client:
        msgrun('Running image for client ' + cli)
        if ver[0:1] == '8':
            ok = subprocess.call(
                'sudo docker run -d \
                --link aeroo_docs:aeroo \
                -p ' + getClientPort(ver, cli) + ':8069 \
                -v ' + HOME + cli + '/config:/etc/odoo \
                -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
                -v ' + HOME + '/sources:/mnt/extra-addons \
                --link db-odoo:db \
                --restart=always \
                --name ' + cli + ' ' + \
                getImageFromName(ver, 'odoo') + ' -- --db-filter=' + cli + '_.*', shell=True)
        else:
            ok = subprocess.call(
                'sudo docker run -d \
                -p ' + getClientPort(ver, cli) + ':8069 \
                -v ' + HOME + cli + '/config:/etc/odoo \
                -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
                -v ' + HOME + 'sources:/mnt/extra-addons \
                --link db-odoo:db \
                --restart=always \
                --name ' + cli + ' ' + \
                getImageFromName(ver, 'odoo') + ' -- --db-filter=' + cli + '_.*' +
                ' --db_user=odoo --db_password=odoo --db_host=db'
                , shell=True)
        if not ok:
            msgdone('Client ' + cli + ' up and running')
        else:
            msgerr("Can't run client " + cli + ", by the way... did you run -R ?")

    return True


def stopClient(ver):
    msgrun('stopping clients ' + ', '.join(args.client))
    for cli in args.client:
        msginf('stop image for client ' + cli)
        subprocess.call('sudo docker stop ' + cli, shell=True)
        subprocess.call('sudo docker rm ' + cli, shell=True)

    msgdone('all clients stopped')

    return True


def stopEnvironment(ver):
    r1 = r2 = 0
    msgrun('Stopping environment ' + ver)
    for name in ['db-odoo', 'aeroo_docs']:
        msgrun('Stopping image ' + name)

        r1 += subprocess.call('sudo docker stop ' + name, shell=True)
        r2 += subprocess.call('sudo docker rm ' + name, shell=True)
    if r1 + r2 <> 0:
        msgerr('some images can not be stopped')

    msgdone('Environment stopped')
    return True


def pullAll(ver):
    msgrun('Pulling all images for ' + ver)

    for image_name in data[ver]['images']:
        image = getImageFromName(ver, image_name)
        msginf('Pulling ' + image)
        if subprocess.call('sudo docker pull ' + image, shell=True):
            msgerr('Fail pulling image ' + image + ' - Aborting.')

    msgdone('All images ok ' + ver)

    msgrun('Pulling all repos for ' + ver)
    for repo in data[ver]['repos']:
        msginf('pulling repo ' + formatRepoFromDict(repo))
        if subprocess.call('cd ' + HOME + 'sources/' + repo[
            'dir'] + '&&' + ' sudo git pull', shell=True):
            msgerr(
                'Fail pulling repos, uninstall and try again. By the way... did you run -I ?')

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

    msgrun('Clients ' + 18 * '-')
    for client in data2clients(ver):
        msgrun(client['port'] + ' ' + client['client'])

    msgdone('Repos ' + 20 * '-')
    return True


def noIpInstall(ver):
    msgrun('Installing no-ip client')
    subprocess.call('sudo apt-get install make', shell=True)
    subprocess.call('sudo apt-get -y install gcc', shell=True)
    subprocess.call(
        'wget -O /usr/local/src/noip.tar.gz http://www.noip.com/client/linux/noip-duc-linux.tar.gz',
        shell=True)
    subprocess.call('sudo tar -xf noip.tar.gz -C /usr/local/src/', shell=True)
    subprocess.call(
        'sudo wget -P /usr/local/src/ http://www.noip.com/client/linux/noip-duc-linux.tar.gz',
        shell=True)
    subprocess.call('sudo tar xf /usr/local/src/noip-duc-linux.tar.gz -C /usr/local/src/',
                    shell=True)
    subprocess.call('cd /usr/local/src/noip-2.1.9-1 && sudo make install', shell=True)
    msginf("Please answer some questions")
    subprocess.call('sudo rm /usr/local/src/noip-duc-linux.tar.gz', shell=True)
    subprocess.call('sudo cp /usr/local/src/noip-2.1.9-1/debian.noip2.sh  /etc/init.d/',
                    shell=True)
    subprocess.call('sudo chmod +x /etc/init.d/debian.noip2.sh', shell=True)
    subprocess.call('sudo update-rc.d debian.noip2.sh defaults', shell=True)
    subprocess.call('sudo /etc/init.d/debian.noip2.sh restart', shell=True)
    msgdone('no-ip service running')

    # To config defaults noip2 with capital C
    # sudo /usr/local/bin/noip2 -C
    return True


def dockerInstall(ver):
    msgrun('Installing docker')
    subprocess.call('wget -qO- https://get.docker.com/ | sh', shell=True)
    msgdone('Done.')
    return True


def backup(ver):
    msgrun('Backing up...')

    if subprocess.call('sudo docker run --rm \
        -v ' + HOME + cli + '/config:/etc/odoo \
        -v ' + HOME + 'sources:/mnt/extra-addons \
        -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
        --name ' + cli + '_tmp ' + getImageFromName(ver, 'backup')
                               + ' -- --stop-after-init -s \
        --addons-path=' + addon_path + ' --db-filter=' + cli + '_.*'
            , shell=True):
        msgerr('failing backup. Aborting')

    msgdone('Backup done')
    return True

# get choices from data structure
choices = []
for opt in data:
    choices.append(opt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Odoo environment setup v 1.2')
    parser.add_argument('version', choices=choices)
    parser.add_argument('-U', '--uninstall-env', action='store_true',
                        help='Uninstall and erase all files from environment including \
                        database (only current ver). The command ask for permission to \
                        erase database. BE WARNED if say yes, all database files will be erased.')
    parser.add_argument('-I', '--install-env', action='store_true',
                        help="Install all files and odoo repos needed. It will try to \
                        install postgres dir if doesn't exist")

    parser.add_argument('-i', '--install-cli', action='store_true',
                        help="Install clients, requires -c option. You can define multiple clients")

    parser.add_argument('-R', '--run-env', action='store_true',
                        help="Run database and aeroo images.")
    parser.add_argument('-D', '--run-dev', action='store_true',
                        help="Run database and aeroo images for developer mode (local db access).")
    parser.add_argument('-r', '--run-cli', action='store_true',
                        help="Run client odoo images, requieres -c options.")
    parser.add_argument('-S', '--stop-env', action='store_true',
                        help="Stop database and aeroo images.")
    parser.add_argument('-s', '--stop-cli', action='store_true',
                        help="Stop client images, requieres -c options.")
    parser.add_argument('-p', '--pull-all', action='store_true', help="Pull all images")
    parser.add_argument('-l', '--list', action='store_true',
                        help="List all data in this server. Clients and images.")
    parser.add_argument('-c', '--client', dest='client', action='append',
                        help="Client name. You can specify more than one as \
                        -c alexor -c danone -c tenaris ... etc.")
    parser.add_argument('-n', '--no-ip-install', action='store_true',
                        help="Install no-ip on this server")
    parser.add_argument('-k', '--docker-install', action='store_true',
                        help="Install docker on this server")

    parser.add_argument('-u', '--update-database', action='store_true',
                        help="Update database requires -d -c and -m options")
    parser.add_argument('-d', '--database', dest='database', action='store', nargs=1,
                        help="Database to update")
    parser.add_argument('-m', '--module', dest='module', action='append', nargs=1,
                        help="Module to update or all, you can specify multiple -m options")
    parser.add_argument('-b', '--backup', action='store_true',
                        help="Lauch backup")

    args = parser.parse_args()

    # Constant Definitins
    HOME = '~/odoo-' + args.version + '/'
    PSQL = '~/postgresql' + '/'

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
        run_client(args.version)
    if args.pull_all:
        pullAll(args.version)
    if args.list:
        listData(args.version)
    if args.no_ip_install:
        noIpInstall(args.version)
    if args.docker_install:
        dockerInstall(args.version)
    if args.update_database:
        update_database(args.version)
    if args.backup:
        backup(args.version)

    """
    # version estable
    if ODOOVER == '8.0':
        # images
        ODOO = {'repo': 'jobiols', 'dir': 'odoo-adhoc', 'ver': '8.0'}
        AEROO = {'repo': 'jobiols', 'dir': 'aeroo-docs', 'ver': 'latest'}
        POSTGRES = {'repo': 'postgres', 'dir': '', 'ver': '9.4'}
        BACKUP = {'repo': 'jobiols', 'dir': 'backup', 'ver': ''}
        IMAGES = [ODOO, AEROO, POSTGRES, BACKUP]

        # clients
        CLIENTS = [{'client': 'str', 'port': '8070'},
                   {'client': 'makeover', 'port': '8069'}]

        # repos
        REPOS = [{'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'odoo-argentina', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'aeroo_reports', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'web', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'management-system', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'knowledge', 'branch': '8.0'},
        ]

    elif ODOOVER == '7.0':
        # images
        ODOO = {'repo': 'jobiols',
                'dir': 'odoo-adhoc',
                'ver': '7.0'}
        POSTGRES = {'repo': 'postgres',
                    'dir': '',
                    'ver': '9.4'}
        BACKUP = {'repo': 'jobiols',
                  'dir': 'backup',
                  'ver': ''}
        IMAGES = [ODOO, POSTGRES, BACKUP]

        # clients
        CLIENTS = [{'client': 'makeover', 'port': '8069'},
                   {'client': 'pirulo', 'port': '8070'}]

        # repos
        REPOS = [{'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'}
        ]

    # Version de experimentación
    elif ODOOVER == '7.0.1':
        # images
        ODOO = {'repo': 'jobiols',
                'dir': 'odoo-adhoc',
                'ver': '7.0.1'}
        POSTGRES = {'repo': 'postgres',
                    'dir': '',
                    'ver': '9.4'}
        BACKUP = {'repo': 'jobiols',
                  'dir': 'backup',
                  'ver': ''}
        IMAGES = [ODOO, POSTGRES, BACKUP]

        # clients
        CLIENTS = [{'client': 'makeover', 'port': '8069'},
                   {'client': 'pirulo', 'port': '8070'}]

        # repos
        REPOS = [{'repo': 'jobiols', 'dir': 'odoo-addons', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'localizacion', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'server-tools', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'},
                 {'repo': 'jobiols', 'dir': 'odoo-mailchimp-tools', 'branch': 'master'}
        ]

    # utlima version estable de la Open Upgrade
    elif ODOOVER == 'ou-8.0':
        # images
        ODOO = {'repo': 'jobiols',
                'dir': 'docker-openupgrade',
                'ver': '8.0'}
        POSTGRES = {'repo': 'postgres',
                    'dir': '',
                    'ver': '9.4'}
        IMAGES = [ODOO, POSTGRES]

        # clients
        CLIENTS = [{'client': 'makeover', 'port': '8069'},
                   {'client': 'jeo', 'port': '8070'}]

        # repos
        REPOS = [{'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0'},
                 {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'str', 'branch': '8.0'}
        ]

    # ultima version de adhoc
    elif ODOOVER == '8.0.1':
        # images
        ODOO = {'repo': 'jobiols',
                'dir': 'odoo-adhoc',
                'ver': '8.0'}
        AEROO = {'repo': 'jobiols',
                 'dir': 'aeroo-docs',
                 'ver': 'latest'}
        POSTGRES = {'repo': 'postgres',
                    'dir': '',
                    'ver': '9.4'}
        BACKUP = {'repo': 'jobiols',
                  'dir': 'backup',
                  'ver': ''}
        IMAGES = [ODOO, AEROO, POSTGRES, BACKUP]

        # clients
        CLIENTS = [{'client': 'jeo', 'port': '8070'},
                   {'client': 'makeover', 'port': '8050'}]

        # repos
        REPOS = [{'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0.x'},
                 {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0.x'},
                 {'repo': 'aeroo', 'dir': 'aeroo_reports', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'web', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'management-system', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'knowledge', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'margin-analysis', 'branch': '8.0'},
                 {'repo': 'jobiols', 'dir': 'str', 'branch': '7.0'},
                 {'repo': 'oca', 'dir': 'account-financial-reporting', 'branch': '8.0'}
        ]

    # version experimental
    elif ODOOVER == '8.0.2':
        # images
        ODOO = {'repo': 'adhoc',
                'dir': 'odoo-adhoc',
                'ver': '8.0'}
        AEROO = {'repo': 'jobiols',
                 'dir': 'aeroo-docs',
                 'ver': 'latest'}
        POSTGRES = {'repo': 'postgres',
                    'dir': '',
                    'ver': '9.4'}
        BACKUP = {'repo': 'jobiols',
                  'dir': 'backup',
                  'ver': ''}
        IMAGES = [ODOO, AEROO, POSTGRES, BACKUP]

        # clients
        CLIENTS = [{'client': 'str', 'port': '8069'},
                   {'client': 'makeover', 'port': '8070'}]

        # repos jobiols
        REPOS = [{'repo': 'ingadhoc', 'dir': 'odoo-addons', 'branch': '8.0.x'},
                 {'repo': 'ingadhoc', 'dir': 'odoo-argentina', 'branch': '8.0.x'},
                 {'repo': 'aeroo', 'dir': 'aeroo_reports', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'server-tools', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'web', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'management-system', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'knowledge', 'branch': '8.0'},
                 {'repo': 'oca', 'dir': 'margin-analysis', 'branch': '8.0'}
        ]
    """

