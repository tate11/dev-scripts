#!/usr/bin/env python
import argparse
import subprocess

# ###############################
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

###################################

ODOOVER = '8.0'
HOME = '~/odoo-test-' + ODOOVER + '/'
PSQL = '~/postgresql-test/'
REPOS = ['odoo-addons', 'odoo-argentina', 'aeroo_reports', 'server-tools', 'web', 'management-system', 'knowledge',
         'str']
ODOO = 'jobiols/odoo-adhoc:' + ODOOVER
CLIENTS = [{'client': 'str', 'port': '8069'}]


def msgrun(msg):
    print green(msg)


def msgdone(msg):
    print green(msg)


def msgerr(msg):
    print red(msg)


def uninstall_environment():
    msgrun('Uninstalling odoo environment')
    subprocess.call(['sudo rm -r ' + HOME], shell=True)
    subprocess.call(['sudo rm -r ' + PSQL], shell=True)
    return True


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
        subprocess.call(
            'git clone -b ' + ODOOVER + ' --depth 1 http://github.com/jobiols/' + repo + ' ' + HOME + 'sources/' + repo,
            shell=True)
    msgdone('Install Done')
    return True


def install_client():
    # Calculate addon_path
    path = '/mnt/extra-addons/'
    addon_path = path + REPOS[0]
    for rep in REPOS[1:]:
        addon_path += ',' + path + rep

    for cli in args.client:
        msgrun('Installing Odoo image for client ' + cli)
        # Creating directory's for client
        subprocess.call('mkdir -p ' + HOME + cli + '/config')
        subprocess.call('mkdir -p ' + HOME + cli + '/data_dir')

        # creating config file for client
        subprocess.call(
            'docker run --rm \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + 'sources:/mnt/extra-addons \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            --name ' + cli +
            ODOO + ' -- --stop-after-init -s \
            --addons-path=' + addon_path, shell=True)

    msgdone('Installing done')
    return True


def run_environment():
    msgrun("Running AEROO image")
    subprocess.call(
        'docker run -d \
	    -p 127.0.0.1:8989:8989 \
	    --name="aeroo_docs" \
    	--restart=always \
	    ${AEROO} ')
    msgdone("AEROO up and running")

    msgrun ("Running POSTGRES")
    subprocess.call(
        'docker run -d \
	    -e POSTGRES_USER=odoo \
	    -e POSTGRES_PASSWORD=odoo \
	    -v ~/postgresql:/var/lib/postgresql/data \
	    --restart=always \
	    --name db-odoo \
	    ${POSTGRES} ')
 	msgdone ("POSTGRES up and running")

    return True


def run_developer():
    return True


def run_client():
    return True


def stop_environment():
    return True


def stop_client():
    return True


def pull_all_images():
    return True


def list_data():
    msgrun('Data for this environment')
    msgrun('Repos ' + 20 * '-')
    for rep in REPOS:
        msgrun('jobiols/' + rep)
    msgrun('Clients ' + 18 * '-')
    for cli in CLIENTS:
        msgrun(cli['port'] + ' ' + cli['client'])
    return True


def no_ip_install():
    return True


def docker_install():
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Odoo environment setup.')
    parser.add_argument('-U', '--uninstall-env', action='store_true',
                        help='Uninstall and erase all files from environment including databases. \
                        WARNING all database files will be erased.')
    parser.add_argument('-I', '--install-env', action='store_true', help="Install all files and odoo repos needed")
    parser.add_argument('-i', '--install-cli', action='store_true',
                        help="Install all clients, required at least one -c option")

    parser.add_argument('-R', '--run-env', action='store_true', help="Run database and aeroo images.")
    parser.add_argument('-D', '--run-dev', action='store_true',
                        help="Run database and aeroo images for developer mode (local db access).")

    parser.add_argument('-r', '--run-cli', action='store_true', help="Run client odoo images, requieres -c option.")
    parser.add_argument('-S', '--stop-env', action='store_true', help="Stop database and aeroo images.")
    parser.add_argument('-s', '--stop-cli', action='store_true', help="Stop client images, requieres -c option.")
    parser.add_argument('-p', '--pull-all', action='store_true', help="Pull all images")
    parser.add_argument('-l', '--list', action='store_true', help="List all data in this server. Clients and images.")
    parser.add_argument('-c', '--client', dest='client', action='append',
                        help="Client name. You can specify more than one as \
                        -c alexor -c danone -c tenaris ... etc. Requiered -i option")
    parser.add_argument('-n', '--no-ip-install', action='store_true', help="Install no-ip on this server")
    parser.add_argument('-d', '--docker-install', action='store_true', help="Install docker on this server")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 7.0')

    args = parser.parse_args()

    if args.uninstall_env:        uninstall_environment()
    if args.install_env:         install_environment()
    if args.install_cli:        install_client()
    if args.run_env:        run_environment()
    if args.run_dev: run_developer()
    if args.run_cli: run_client()
    if args.stop_env: stop_environment()
    if args.stop_cli: stop_client()
    if args.pull_all: pull_all_images()
    if args.list: list_data()
    if args.no_ip_install: no_ip_install()
    if args.docker_install: docker_install()

