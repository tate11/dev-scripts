#!/usr/bin/env python
import argparse
import subprocess

################################
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
YELLOW_LIGHT = "\033[33m"
CLEAR = "\033[0;m"


def green(string):
    return GREEN + string + CLEAR


def yellow(string):
    return YELLOW + string + CLEAR


def red(string):
    return RED + string + CLEAR


def yellow_light(string):
    return YELLOW_LIGHT + string + CLEAR


fail_msg = red("FAIL")
success_msg = green("Success")
###################################

HOME = '~/odoo-80-test/'
PSQL = '~/postgresql-test/'
REPOS = ['odoo-addons', 'odoo-argentina', 'aeroo_reports', 'server-tools', 'web', 'management-system', 'knowledge',
         'str']
ODOO = 'jobiols/odoo-adhoc:8.0'


def msgrun(msg):
    print yellow(msg)


def msgdone(msg):
    print green(msg)


def msgerr(msg):
    print red(msg)


# ##############################
# uninstall environment
def uninstall_environment():
    msgrun('Uninstalling odoo environment')
    subprocess.call(['sudo rm -r ' + HOME], shell=True)
    subprocess.call(['sudo rm -r ' + PSQL], shell=True)
    return True


# ##############################
# install environment
def install_environment():
    msgrun('Installing odoo environment')

    # if not exist psql create it
    if subprocess.call(['ls ' + PSQL], shell=True):
        subprocess.call(['mkdir ' + PSQL], shell=True)

    # install sources
    subprocess.call(['mkdir -p ' + HOME + 'sources'], shell=True)

    # subprocess.call(['chmod 777 -R '+HOME+'/sources'], shell=True)
    for repo in REPOS:
        msgrun('pulling repo ' + repo)
        subprocess.call('git clone -b 8.0 --depth 1 http://github.com/jobiols/' + repo + ' ' + HOME + 'sources/' + repo,
                        shell=True)
    msgdone('Install Done')
    return True


# ##############################
# install client
def install_client():
    path = '/mnt/extra-addons/'
    addon_path = path + REPOS[0]
    for rep in REPOS[1:]:
        addon_path += ',' + path + rep

    for cli in args.client:
        msgrun('Installing odoo image for client ' + cli)
        # Creating directorys for client
        subprocess.call('mkdir -p ' + HOME + cli + '/config')
        subprocess.call('mkdir -p ' + HOME + cli + '/data_dir')
        # creating config file for client
        subprocess.call(
            'docker run --rm ' +
            '-v ' + HOME + cli + '/config:/etc/odoo ' +
            '-v ' + HOME + 'sources:/mnt/extra-addons ' +
            '-v ' + HOME + cli + '/data_dir:/var/lib/odoo ' +
            '--name ' + cli +
            ODOO + ' -- --stop-after-init -s ' +
            '--addons-path=' + addon_path, shell=True)

    msgdone('Installing done')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Odoo environment setup.')
    parser.add_argument('-U', '--uninstall-env', action='store_true',
                        help='uninstall and erase all files from environment including databases. \
                        WARNING all darabase files will be erased.')
    parser.add_argument('-I', '--install-env', action='store_true', help="install all files and odoo repos needed")
    parser.add_argument('-i', '--install-client', action='store_true',
                        help="install all clients, requiered at least one -c option")

    parser.add_argument('-R', '--run-env', action='store_true', help="run database and aeroo images")
    parser.add_argument('-r', '--run-client', dest='cli', help="run client odoo image")
    parser.add_argument('-S', '--stop-env', action='store_true', help="stop database and aeroo images")
    parser.add_argument('-s', '--stop-client', dest='cli', help="stop client image")
    parser.add_argument('-p', '--pull-all', action='store_true', help="pull all images")
    parser.add_argument('-n', '--no-ip-install', action='store_true', help="install no-ip on this server")
    parser.add_argument('-d', '--docker-install', action='store_true', help="install docker on this server")
    parser.add_argument('-l', '--list', action='store_true', help="list all data in this server. Clients and images.")
    #    parser.add_argument('-c', '--update-all', dest='cli', help="update all for client and database")
    parser.add_argument('-D', '--developer', action='store_true',
                        help="run database and aeroo images for developer mode (local db access)")

    parser.add_argument('-c', '--client', dest='client', action='append',
                        help="client name, you can specify more than one as -c alexor -c danone -c tenaris ... etc. Requiered -i option")

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 7.0')

    args = parser.parse_args()
    print args
    if args.uninstall_env:
        uninstall_environment()
    if args.install_env:
        install_environment()
    if args.install_client:
        install_client()
