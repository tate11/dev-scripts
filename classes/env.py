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
import os
import sys

clients__ = [
    #######################################################################
    {'name': 'makeover', 'port': '8068', 'odoover': '8.0',
     'repos': [
         {'usr': 'jobiols', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'str', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'knowledge', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
     ],
     'images': [
         {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
         {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '8.0'},
         {'name': 'postgres', 'usr': 'postgres', 'ver': '9.4'},
         {'name': 'backup', 'usr': 'jobiols', 'img': 'backup'},
     ]
     },

    #######################################################################
    {'name': 'jeo', 'port': '8069', 'odoover': '8.0',
     'repos': [
         {'usr': 'ingadhoc', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'str', 'branch': '8.0'},
     ],
     'images': [
         {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
         {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '8.0'},
         {'name': 'postgres', 'usr': 'postgres', 'ver': '9.4'},
         {'name': 'backup', 'usr': 'jobiols', 'img': 'backup'},
     ]
     },

    #######################################################################
    {'name': 'nixel', 'port': '8090', 'odoover': '8.0',
     'repos': [
         {'usr': 'jobiols', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
     ],
     'images': [
         {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
         {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '8.0'},
         {'name': 'postgres', 'usr': 'postgres', 'ver': '9.4'},
         {'name': 'backup', 'usr': 'jobiols', 'img': 'backup'},
     ]
     },
    #######################################################################
    {'name': 'tst', 'port': '8090', 'odoover': '8.0',
     'repos': [
         {'usr': 'jobiols', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'str', 'branch': '8.0'},
         {'usr': 'jobiols', 'instdir': 'ml', 'repo': 'meli_oerp', 'branch': 'master'},
         {'usr': 'jobiols', 'instdir': 'ml', 'repo': 'payment_mercadopago',
          'branch': 'master'},

     ],
     'images': [
         {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
         {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '8.0'},
         {'name': 'postgres', 'usr': 'postgres', 'ver': '9.4'},
         {'name': 'backup', 'usr': 'jobiols', 'img': 'backup'},
     ]
     },
]

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"


class Environment:
    def __init__(self, args, dic):
        self._clients = []
        for cli in dic:
            self._clients.append(Client(self, cli))

        self._home_template = os.path.expanduser('~/odoo-')
        self._psql = os.path.expanduser('~/postgresql/')
        self._args = args

    def debug_mode(self):
        return self._args.debug

    def get_modules_from_params(self):
        if self._args.module is None:
            self.msgerr('need -m option')
        return self._args.module

    def get_database_from_params(self):
        if self._args.database is None:
            self.msgerr('need -d option')
        if len(self._args.database) > 1:
            self.msgerr('only one database expected')
        return self._args.database[0]

    def get_timestamp_from_params(self):
        if self._args.timestamp is None:
            self.msgerr('need -t option')
        if len(self._args.database) > 1:
            self.msgerr('only one timestamp expected')
        return self._args.timestamp[0]

    def get_clients_from_params(self, cant='multi'):
        if self._args.client is None:
            self.msgerr('need -c option')

        for cli in self._args.client:
            if self.get_client(cli) is None:
                self.msgerr('there is no ' + cli + ' client in this environment')

        if cant == 'multi':
            return self._args.client
        else:
            if len(self._args.client) > 1:
                self.msgerr('only one client expected')
            return self._args.client[0]

    def get_args(self):
        return self._args

    def get_client(self, clientName):
        cli = None
        for client in self._clients:
            if client.get_name() == clientName:
                cli = client
        return cli

    def getClients(self):
        return self._clients

    def getClientArgs(self):
        return ', '.join(self._args.client)

    def getTemplateDir(self):
        return self._home_template

    def getPsqlDir(self):
        return self._psql

    def green(self, string):
        return GREEN + string + CLEAR

    def yellow(self, string):
        return YELLOW + string + CLEAR

    def red(self, string):
        return RED + string + CLEAR

    def yellow_light(self, string):
        return YELLOW_LIGHT + string + CLEAR

    def msgrun(self, msg):
        print self.yellow(msg)

    def msgdone(self, msg):
        print self.green(msg)

    def msgerr(self, msg):
        print self.red(msg)
        sys.exit()

    def msginf(self, msg):
        print self.yellow_light(msg)


class Client:
    def __init__(self, env, dic):
        self._env = env
        self._name = dic['name']
        self._port = dic['port']
        self._ver = dic['odoover']

        self._repos = []
        for rep in dic['repos']:
            self._repos.append(Repo(self, rep))

        self._images = []
        for img in dic['images']:
            self._images.append(Image(self, img))

    def get_ver(self):
        return self._ver

    def get_backup_dir(self):
        return self.get_home_dir() + self._name + '/backup/'

    def get_repos(self):
        return self._repos

    def get_images(self):
        return self._images

    def get_image(self, ImageName):
        ret = None
        for img in self._images:
            if img.get_name() == ImageName:
                ret = img
        if ret is None:
            raise Exception('no image ' + ImageName + ' found')
        return ret

    def get_name(self, pad=0):
        return self._name.ljust(pad)

    def get_port(self):
        return self._port

    def get_home_dir(self):
        return self._env.getTemplateDir() + self._ver + '/'

    def get_addons_path(self):
        # path to addons inside image
        path = '/mnt/extra-addons/'
        paths = []
        for repo in self.get_repos():
            paths.append(path + repo.getPathDir())
        return ','.join(paths)


class Repo:
    def __init__(self, cli, dict):
        self._dict = dict
        self._cli = cli

    def _getRepo(self):
        return self._dict['usr'] + '/' + self._dict['repo']

    def get_formatted_repo(self):
        ret = 'b ' + self._dict['branch'].ljust(7) + ' ' + self._getRepo().ljust(30)
        return ret

    def getPathDir(self):
        try:
            ret = self._dict['instdir'] + '/' + self._dict['repo']
        except:
            ret = self._dict['repo']
        return ret

    def getInstDir(self):
        try:
            ret = self._dict['instdir'] + '/' + self._dict['repo']
        except:
            ret = self._dict['repo']
        return self._cli.get_home_dir() + 'sources/' + ret

    def getPullRepo(self):
        return 'git -C ' + self.getInstDir() + ' pull'

    def getCloneRepo(self):
        return 'git clone --depth 1 -b ' + \
               self._dict['branch'] + \
               ' http://github.com/' + \
               self._getRepo() + ' ' + \
               self.getInstDir()


class Image:
    def __init__(self, cli, dict):
        self._cli = cli
        self._dict = dict

    def getVer(self):
        try:
            ver = self._dict['ver']
        except:
            ver = 'latest'
        return ver

    def getFormattedImage(self):
        ret = self._dict['usr']
        try:
            ret += '/' + self._dict['img']
        except:
            a = 1

        try:
            ret += ':' + self._dict['ver']
        except:
            a = 1

        return ret

    def get_image(self):
        try:
            usr = self._dict['usr']
        except:
            usr = ''

        try:
            image = self._dict['img']
        except:
            image = ''

        try:
            ver = self._dict['ver']
        except:
            ver = ''

        ret = usr
        if image != '':
            ret += '/' + image
        if ver != '':
            ret += ':' + ver

        return ret

    def get_name(self):
        return self._dict['name']

    def getPullImage(self):
        return 'sudo docker pull ' + self.get_image()