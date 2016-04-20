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

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"
REPOS_DIR = '~/git-repos/'

repos = [
    {'usr': 'oca', 'repo': 'manufacture', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'web', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'odoomrp-wip', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'connector-magento', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'account-financial-reporting', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'server-tools', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'management-system', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'knowledge', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'rma', 'branch': '8.0'},
    {'usr': 'oca', 'repo': 'pos', 'branch': '8.0'},

    {'usr': 'aeroo', 'repo': 'aeroo_reports', 'branch': '8.0'},

    {'usr': 'tgalal', 'repo': 'yowsup', 'branch': 'master'},

    {'usr': 'waylan', 'repo': 'Python-Markdown', 'branch': 'master'},

    {'usr': 'ctmil', 'repo': 'payment_mercadopago', 'branch': 'master'},

    {'usr': 'csrocha', 'repo': 'fpoc-chrome', 'branch': 'master'},
    {'usr': 'csrocha', 'repo': 'odoo_fpoc', 'branch': 'master'},

    {'usr': 'ingadhoc', 'repo': 'docker-odoo', 'branch': 'master'},
    {'usr': 'ingadhoc', 'repo': 'docker-odoo-adhoc', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'odoo-argentina', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'odoo-addons', 'branch': '8.0'},
    # reemplazo de odoo-addons
    {'usr': 'ingadhoc', 'repo': 'adhoc-account-analytic', 'upstream': 'account-analytic',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-account-financial-tools',
     'upstream': 'account-financial-tools', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-account-invoicing',
     'upstream': 'account-invoicing', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-account-payment', 'upstream': 'account-payment',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-crm', 'upstream': 'crm', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-hr', 'upstream': 'hr', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-manufacture', 'upstream': 'manufacture',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-miscellaneous', 'upstream': 'miscellaneous',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-multi-company', 'upstream': 'multi-company',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-partner', 'upstream': 'partner', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-product', 'upstream': 'product', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-purchase', 'upstream': 'purchase',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-reporting-engine', 'upstream': 'reporting-engine',
     'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-sale', 'upstream': 'sale', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-stock', 'upstream': 'stock', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-survey', 'upstream': 'survey', 'branch': '8.0'},
    {'usr': 'ingadhoc', 'repo': 'adhoc-surveyor', 'upstream': 'surveyor',
     'branch': '8.0'},
]


class repository:
    def __init__(self, usr, repo, branch):
        self._usr = usr
        self._repo = repo
        self._branch = branch

    def usr(self):
        return self._usr

    def repo(self):
        return self._repo

    def branch(self):
        return self._branch

    def clone_str(self):
        return 'git clone -b ' + self._branch + \
               ' https://github.com/' + self._usr + '/' + self._repo


class unit:
    def __init__(self, dict):
        try:
            upstream_repo = dict['upstream']
        except:
            upstream_repo = dict['repo']

        self._upstream = repository(dict['usr'], upstream_repo, dict['branch'])
        self._origin = repository('jobiols', dict['repo'], dict['branch'])
        self._local = REPOS_DIR + dict['repo']

    def upstream(self):
        return self._upstream

    def origin(self):
        return self._origin

    def dir(self):
        return self._local

    def add_remote(self):
        return 'git -C ' + self._local + \
               ' remote add upstream https://github.com/' + \
               self._upstream.usr() + '/' + self._upstream.repo()

def sc_(params):
    return subprocess.call(params, shell=True)

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


def create_local_repo(rp):
    msgrun('Local repo does not exist!')

    msgrun('cloning origin')
    if sc_(rp.origin().clone_str() + ' ' + rp.dir()):
        msgerr('Fail!')
    # sc_('git -C ' + rp.dir() + ' remote -v ')

    msgrun('adding remote upstream')
    sc_(rp.add_remote())


#    sc_('git -C ' + rp.dir() + ' remote -v ')


def check_repo(dict):
    rp = unit(dict)
    msgrun(20 * '-' + ' ' +
           rp.upstream().usr() + ' ' +
           rp.upstream().repo() + ' ' +
           rp.upstream().branch())

    # chequear local repo y crearlo si no existe
    if sc_('git -C ' + rp.dir() + ' status') != 0:
        create_local_repo(rp)

    msgrun('fetch upstream')
    sc_('git -C ' + rp.dir() + ' fetch upstream')

    msgrun('checkout')
    sc_('git -C ' + rp.dir() + ' checkout ' + rp.upstream().branch())

    msgrun('merge')
    sc_('git -C ' + rp.dir() + ' merge upstream/' + rp.upstream().branch())

    msgrun('push')
    sc_('git -C ' + rp.dir() + ' push origin ' + rp.upstream().branch())

    msgdone('done')
    return


def update_all():
    for repo in repos:
        check_repo(repo)


def list():
    msgrun('Currently maintained repositories')
    for dict in repos:
        msginf('{:8} {:7} {}'.format(dict['usr'], dict['branch'], dict['repo']))


def update():
    if args.repo is None:
        msgerr('need -r')

    for dict in repos:
        if dict['repo'] == args.repo[0]:
            check_repo(dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update forks v 0.5')
    parser.add_argument('-U',
                        '--update-all',
                        action='store_true',
                        help="Update all forks without warning")

    parser.add_argument('-u',
                        '--update',
                        action='store_true',
                        help="Update specifics forks")

    parser.add_argument('-r',
                        '--repo',
                        action='append',
                        dest='repo',
                        help="Repo to update")

    parser.add_argument('-l',
                        '--list',
                        action='store_true',
                        help="List al currently maintained repos")

    args = parser.parse_args()

    if args.update_all:
        update_all()

    if args.list:
        list()

    if args.update:
        update()
