#!/usr/bin/env python
import argparse
import subprocess

ODOOVER = '8.0'
HOME = '~/odoo-test-' + ODOOVER + '/'
PSQL = '~/postgresql-test/'

ODOO = 'jobiols/odoo-adhoc:' + ODOOVER
AEROO = "jobiols/aeroo-docs"
POSTGRES = "postgres:9.4"
BACKUP = "jobiols/backup"

IMAGES = [ODOO, AEROO, POSTGRES, BACKUP]
CLIENTS = [{'client': 'str', 'port': '8069'},
           {'client': 'makeover', 'port': '8070'}]

REPOS = ['odoo-addons', 'odoo-argentina', 'aeroo_reports', 'server-tools', 'web', 'management-system', 'knowledge',
         'str']


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



def msgrun(msg):
    print green(msg)


def msgdone(msg):
    print green(msg)


def msgerr(msg):
    print red(msg)


def msginf(msg):
    print yellow(msg)


def client_port(client):
    port = ''
    for cli in CLIENTS:
        if cli['client'] == client:
            port = cli['port']
    return port


def uninstall_environment():
    msgrun('Uninstalling odoo environment')
    subprocess.call(['sudo rm -r ' + HOME], shell=True)
    if raw_input('Delete postgresql directory? (y/n) ') == 'y':
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
        msginf('pulling repo ' + repo)
        if subprocess.call('git clone -b ' + ODOOVER +
                                   ' --depth 1 http://github.com/jobiols/' + repo + ' ' + HOME + 'sources/' + repo,
                           shell=True):
            msgerr('Fail installing environment, uninstall and try again.')
            return True

    msgdone('Install Done')
    return True


def install_client():
    msgrun('Install clients')
    # Calculate addon_path
    path = '/mnt/extra-addons/'
    addon_path = path + REPOS[0]
    for rep in REPOS[1:]:
        addon_path += ',' + path + rep

    for cli in args.client:
        msgrun('Installing Odoo image for client ' + cli)
        # Creating directory's for client
        subprocess.call('mkdir -p ' + HOME + cli + '/config', shell='True')
        subprocess.call('mkdir -p ' + HOME + cli + '/data_dir', shell='True')
        subprocess.call(['chmod 777 -R ' + HOME + cli], shell=True)

        # creating config file for client
        subprocess.call(
            'sudo docker run --rm \
            -v ' + HOME + cli + '/config:/etc/odoo \
            -v ' + HOME + 'sources:/mnt/extra-addons \
            -v ' + HOME + cli + '/data_dir:/var/lib/odoo \
            --name ' + cli + ' ' + \
            ODOO + ' -- --stop-after-init -s \
            --addons-path=' + addon_path, shell=True)
    msgdone('Installing done')
    return True


def run_aeroo_image():
    msgrun("Running aeroo and postgres images")
    subprocess.call(
        'sudo docker run -d \
	    -p 127.0.0.1:8989:8989 \
	    --name="aeroo_docs" \
    	--restart=always ' + \
        AEROO, shell=True)
    return True


def run_environment():
    run_aeroo_image()

    subprocess.call(
        'sudo docker run -d \
	    -e POSTGRES_USER=odoo \
	    -e POSTGRES_PASSWORD=odoo \
	    -v ~/postgresql:/var/lib/postgresql/data \
	    --restart=always \
	    --name db-odoo ' + \
        POSTGRES, shell=True)
    msgdone("Images up and running")

    return True


def run_developer():
    msgrun('Running developer mode')
    run_aeroo_image()

    subprocess.call(
        'sudo docker run -d \
	    -e POSTGRES_USER=odoo \
        -p 5432:5432 \
	    -e POSTGRES_PASSWORD=odoo \
	    -v ~/postgresql:/var/lib/postgresql/data \
	    --restart=always \
	    --name db-odoo ' + \
        POSTGRES, shell=True)

    return True


def run_client():
    for cli in args.client:
        msgrun('starting ' + cli)
        subprocess.call(
            'sudo docker run -d \
            --link aeroo_docs:aeroo \
            -p ' + client_port(cli) + ':8069 \
            -v ~/odoo80/' + cli + '/config:/etc/odoo \
            -v ~/odoo80/' + cli + '/data_dir:/var/lib/odoo \
            -v ~/odoo80/sources:/mnt/extra-addons \
            --link db-odoo:db \
            --restart=always \
            --name ' + cli + ' ' + \
            ODOO + ' -- --db-filter= ' + cli, shell=True)

    return True


def stop_client():
    msgrun('stopping clients ' + ', '.join(args.client))
    for cli in args.client:
        msgrun('stop image for client ' + cli)
        subprocess.call('sudo docker stop ' + cli, shell=True)
        subprocess.call('sudo docker rm ' + cli, shell=True)

    msgdone('all client stopped')

    return True


def stop_environment():
    msgrun('Stopping environment')

    for name in ['db-odoo', 'aeroo_docs']:
        msgrun
        'Stoping image ' + name
        subprocess.call('sudo docker stop ' + name, shell=True)
        subprocess.call('sudo docker rm ' + name, shell=True)

    return True


def pull_all_images():
    msgrun('Pulling all images for ' + ODOOVER)

    for image in IMAGES:
        msgrun('Pulling ' + image)
        subprocess.call('sudo docker pull ' + image, shell=True)

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
    msgrun('Installing no-ip client')
    subprocess.call('apt-get install make', shell=True)
    subprocess.call('apt-get -y install gcc', shell=True)

    """
        cd /usr/local/src/
        wget http://www.noip.com/client/linux/noip-duc-linux.tar.gz
        tar xf noip-duc-linux.tar.gz
        cd noip-2.1.9-1/
        make install
        msginfo "Please answer some questions"
        #Please enter login/email: jobiols
        #Please enter password: veconceR
        #contestar preguntas sobre defaults y grupos.
        rm /usr/local/src/noip-duc-linux.tar.gz
        #Poner el script en init.d
        cp /usr/local/src/noip-2.1.9-1/debian.noip2.sh  /etc/init.d/
        #Make script executable
        chmod +x /etc/init.d/debian.noip2.sh
        #hacer que se ejecute al booteo
        update-rc.d debian.noip2.sh defaults
        #arrancar y parar el demonio
        msgrun "Starting no-ip daemon"
        /etc/init.d/debian.noip2.sh restart
        msgdone "no-ip service running"
    """
    return True


def docker_install():
    msgrun('Installing docker')
    subprocess.call('wget -qO- https://get.docker.com/ | sh', shell=True)
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

    if args.uninstall_env:
        uninstall_environment()
    if args.install_env:
        install_environment()
    if args.install_cli:
        install_client()
    if args.run_env:
        run_environment()
    if args.run_dev:
        run_developer()
    if args.run_cli:
        run_client()
    if args.stop_env:
        stop_environment()
    if args.stop_cli:
        stop_client()
    if args.pull_all:
        pull_all_images()
    if args.list:
        list_data()
    if args.no_ip_install:
        no_ip_install()
    if args.docker_install:
        docker_install()
