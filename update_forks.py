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

data = [
    {'ver': '8.0', 'dir': '~/git-repos/odoo'},
    {'ver': '8.0', 'dir': '~/git-repos/odoomrp-wip'},
    {'ver': 'master', 'dir': '~/git-repos/Python-Markdown'},
    {'ver': '8.0', 'dir': '~/git-repos/account-financial-reporting'},
    {'ver': '8.0', 'dir': '~/git-repos/odoo-web'},
    {'ver': '8.0', 'dir': '~/git-repos/odoo-argentina'},
    {'ver': '8.0', 'dir': '~/git-repos/odoo-addons'},
    {'ver': '8.0', 'dir': '~/git-repos/aeroo_reports'},
    {'ver': '8.0', 'dir': '~/git-repos/server-tools'},
    {'ver': '8.0', 'dir': '~/git-repos/web'},
    {'ver': '8.0', 'dir': '~/git-repos/management-system'},
    {'ver': '8.0', 'dir': '~/git-repos/knowledge'},
    {'ver': '8.0', 'dir': '~/git-repos/rma'},
]


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


def updateRepo(repo):
    msgrun(30 * '-' + ' ' + repo['dir'])
    sc_('git -C ' + repo['dir'] + ' status')
    msgrun("fetch upstream")
    sc_('git -C ' + repo['dir'] + ' fetch upstream')
    msgrun("checkout")
    sc_('git -C ' + repo['dir'] + ' checkout ' + repo['ver'])
    msgrun("merge")
    sc_('git -C ' + repo['dir'] + ' merge upstream/' + repo['ver'])
    msgrun("push")
    sc_('git -C ' + repo['dir'] + ' push origin ' + repo['ver'])
    msgdone('done')
    return


def updateAll():
    for repo in data:
        updateRepo(repo)
    return


if __name__ == '__main__':
    choices = ['8.0']
    parser = argparse.ArgumentParser(description='Update forks v 0.2')
    parser.add_argument('version', choices=choices)

    parser.add_argument('-U',
                        '--update-all',
                        action='store_true',
                        help="Update all forks without warning")
    parser.add_argument('-u',
                        '--update',
                        action='append',
                        dest='repo',
                        help="Update specific forks (not implemented yet)")
    parser.add_argument('-c',
                        '--check',
                        action='store_true',
                        help="Check upstream repos (not implemented yet)")

    args = parser.parse_args()
    print args

    if args.update_all:
        updateAll()
