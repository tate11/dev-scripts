__author__ = 'jorge'
# jeo Software,

clients__ = [
    {'name': 'jeo', 'port': 8069,
     'repos': [
         {'usr': 'ingadhoc', 'repo': 'odoo-argentina', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'aeroo_reports', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'server-tools', 'branch': '8.0'},
         {'usr': 'jobiols', 'repo': 'str', 'branch': '8.0'},
         {'usr': 'jobiols', 'instdir': 'ml', 'repo': 'meli_oerp', 'branch': 'master'},
         {'usr': 'jobiols', 'instdir': 'ml', 'repo': 'payment_mercadopago', 'branch': 'master'},
     ],
     'images': [
         {'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '7.0'},
         {'usr': 'postgres', 'ver': '9.4'},
         {'usr': 'jobiols', 'img': 'backup'},
     ]
    }
]


class Environment:
    def __init__(self, dict):
        self._clients = []
        for cli in dict:
            self._clients.append(cli)

    def getClient(self,clientName):
        for cli in self._clients:
            if cli.getName() == clientName:
                return cli
            else:
                raise Exception('No client')


class Client:
    def __init__(self,dict):
        self._name = dict['name']

        self._repos = []
        for rep in dict['repos']:
            self._repos.append(Repo(rep))

        self._images = []
        for img in dict['images']:
            self._images.append(Image(img))

    def getRepos(self):
        return self._repos

    def getImages(self):
        return self._images

    def getName(self):
        return self._name

#         {'usr': 'jobiols', 'repo': 'str', 'branch': '8.0'},
#         {'usr': 'jobiols', 'instdir': 'ml', 'repo': 'meli_oerp', 'branch': 'master'},

class Repo:
    def __init__(self,dict):
        self._dict = dict

    def getRepo(self):
        return self._dict['usr']+'/'+self._dict['repo']

    def getFormattedRepo(self):
        ret = 'b ' + self._dict['branch'] + ' ' + self.getRepo()
        return ret

    def getInstDir(self):
        try:
            ret = self._dict['instdir']
        except:
            ret = self._dict['repo']
        return ret

class Image:
    def __init__(self,dict):
        self._dict = dict

#  {'usr': 'jobiols', 'img': 'odoo-adhoc', 'ver': '7.0'},

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


cli = Client(clients__[0])
for re in cli.getRepos():
    print 'repo', re.getFormattedRepo(), re.getInstDir()

for im in cli.getImages():
    print 'imag', im.getFormattedImage()

