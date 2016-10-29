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
from datetime import datetime
import json

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"
REPOS_DIR = '~/git-repos/'

# levantar datos de archivo de configuracion
with open('update-forks-data.json') as f:
    json = json.load(f)
repos = json['repos']

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
        return 'git clone -b {} https://github.com/{}/{}'.format(
            self._branch, self._usr, self._repo)


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
        return 'git -C {} remote add upstream https://github.com/{}/{}'.format(
            self._local, self._upstream.usr(), self._upstream.repo())


def sc_(params):
    if args.verbose:
        print '>', params
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

    msgrun('adding remote upstream')
    sc_(rp.add_remote())


def update_repo(dict):
    rp = unit(dict)
    msgrun('{} {} {} {}'.format(
        20 * '-', rp.upstream().usr(), rp.upstream().repo(), rp.upstream().branch()))

    def _shortver():
        return datetime.now().strftime('%Y%m%d%H%M')

    def _longver():
        return datetime.now().strftime(':%B %d, %Y')

    # chequear local repo y crearlo si no existe
    if sc_('git -C {} status'.format(rp.dir())):
        create_local_repo(rp)

    # traer el repo de upstream el repo original
    msgrun('fetch upstream')
    if sc_('git -C {} fetch upstream'.format(rp.dir())):
        msgerr('fetch fail')

    # lo extraigo
    msgrun('checkout')
    if sc_('git -C {} checkout {}'.format(
            rp.dir(), rp.upstream().branch())):
        msgerr('checkout fail')

    # lo mergeo con el mio
    msgrun('merge')
    if sc_('git -C {} merge upstream/{}'.format(
            rp.dir(), rp.upstream().branch())):
        msgerr('merge fail')

    # le pongo el tag a la nueva versión creada
    msgrun('tagging repo')
    if sc_('git -C {} tag -a v{} -m "update fork on {}"'.format(
            rp.dir(), _shortver(), _longver())):
        msgerr('tagging fail')

    # subo la version nueva a mi repo
    msgrun('push')
    if sc_('git -C {} push origin {}'.format(
            rp.dir(), rp.upstream().branch())):
        msgerr('push fail')

    # subo el tag
    msgrun('push --tags')
    if sc_('git -C {} push origin --tags {}'.format(
            rp.dir(), rp.upstream().branch())):
        msgerr('push fail')

    msgdone('done')
    return


def update_all():
    for repo in repos:
        update_repo(repo)


def list():
    msgrun('Currently maintained repositories')
    for dict in repos:
        msginf('{:8} {:7} {}'.format(dict['usr'], dict['branch'], dict['repo']))


def update():
    if args.repo is None:
        msgerr('need -r')

    for dict in repos:
        if dict['repo'] == args.repo[0]:
            update_repo(dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Update forks v 1.0 ---
    This script manages a set of repositories, each one having three locations: The original one,
    the fork of the original in my github and a clone of this fork in my workstation.
    The program's goal is to update the fork in github to the latest version of the original repo.
    To do that it makes a fetch to the original repo downloading the last version to the workstation,
    does a merge and then makes a push to the fork.

    """)
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

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Show commands")

    args = parser.parse_args()

    if args.update_all:
        update_all()

    if args.list:
        list()

    if args.update:
        update()
