import base64
from jinja2 import Template
import re
import os
import sys
import logging
import ruamel.yaml
from src.actions import Actions
from src.create import Create


class Mapping(object):
    def __init__(self, templatepath=None, outputpath=None, namespace='swift-alliancecloud-pilot', mountpath='secret', key='Value', pushconfig='False'):
        self.templatepath = templatepath
        self.outputpath = outputpath
        self.mountpath = mountpath
        self.key = key
        self.push = pushconfig
        self.namespace = namespace

    def mapSecrets(self):
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.preserve_quotes = True
        for filename in os.listdir(self.templatepath):
            logging.info('Found template file at ' + self.templatepath + '/' + filename)
            s = open(self.templatepath + '/' +  filename).read()
            rgx = re.compile('{{(?P<name>[^{}]+)}}')
            templ = Template(s)
            variable_names = {match.group('name') for match in rgx.finditer(s)}
            new = s
            arr = []
            for var in variable_names:
                arr.append(var.strip())
            for element in arr:
                try:
                    val = Actions(key=self.key, mount_point=self.mountpath, secret_path=element).fromVault()
                    encodedBytes = base64.b64encode(val.encode("utf-8"))
                except Exception as e:
                    logging.error('Error encountered ' + str(e))
                    sys.exc_clear()
                new = new.replace('{{ ' + element + ' }}', str(encodedBytes))
                new = new
            logging.info('Yaml file ' + filename + ' is mapped')
            data = yaml.load(new)
            with open(self.outputpath + '/' + filename, 'w') as out:
                yaml.dump(data, out)
                logging.info('Dumped yaml data into ' + self.outputpath + '/' + filename)
            if self.push == 'True':
                try:
                    Create('Secret', self.namespace, self.outputpath + '/' + filename).createResource()
                    logging.info('Secret ' + filename + ' deployed in kubernetes')
                except Exception as e:
                    logging.error('Encountered error while creating secret in kubernetes ' + str(e))
                    sys.exc_clear()
            else:
                logging.info('All vault secrets dumped into templates')

