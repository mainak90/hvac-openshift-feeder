import base64
import yaml
import sys
import logging
from src.actions import Actions
from src.create import Create


class Mapping(object):
    def __init__(self, templatepath=None, outputpath=None, namespace='default', ctx='kv/', mountpath='secret', key='Value', pushconfig='False'):
        self.templatepath = templatepath
        self.ctx = ctx
        self.outputpath = outputpath
        self.mountpath = mountpath
        self.key = key
        self.push = pushconfig
        self.namespace = namespace

    def mapSecrets(self):
            try:
                val = Actions(mount_point=self.ctx, secret_path=self.mountpath).fromVault()
                for key, value in val.iteritems():
                    b64val = base64.b64encode(value.encode("utf-8"))
                    val[key] = b64val
            except Exception as e:
                logging.error('Error encountered ' + str(e))
                sys.exc_clear()
            yamldata = yaml.safe_load(open(self.templatepath).read())
            secname = self.mountpath.split('/')[1]
            yamldata['metadata']['name'] = secname
            yamldata['data'] = val
            with open(self.outputpath + '/' + secname + '.yaml', 'w') as out:
                yaml.dump(yamldata, out)
                logging.info('Dumped yaml data into ' + self.outputpath + '/' + secname + '.yaml')
            if self.push == 'True':
                try:
                     Create('Secret', self.namespace, self.outputpath + '/' + secname + '.yaml').createResource()
                     logging.info('Secret ' + secname + '.yaml deployed in kubernetes')
                except Exception as e:
                     logging.error('Encountered error while creating secret in kubernetes ' + str(e))
                     sys.exc_clear()
                else:
                    logging.info('All vault secrets dumped into templates')

