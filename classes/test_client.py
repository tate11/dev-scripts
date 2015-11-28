from unittest import TestCase
from env import Client
from env import Environment

__author__ = 'jorge'

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
     }
]


class TestClient(TestCase):
    def get_cli(self):
        args = None
        env = Environment(args, clients__)
        cli = env.get_client('makeover')
        return cli

    def test_get_ver(self):
        cli = self.get_cli()
        self.assertEqual(cli.get_ver(), '8.0')

    def test_get_backup_dir(self):
        cli = self.get_cli()
        self.assertEqual(cli.get_backup_dir(), '/home/jorge/odoo-8.0/makeover/backup/')

    def test_get_repos(self):
        cli = self.get_cli()
        self.assertEqual(cli.get_repos(), '')

    def test_get_images(self):
        self.fail()

    def test_get_image(self):
        self.fail()

    def test_get_name(self):
        self.fail()

    def test_get_port(self):
        self.fail()

    def test_get_home_dir(self):
        self.fail()

    def test_get_addons_path(self):
        self.fail()
