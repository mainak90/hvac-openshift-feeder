from src.apiclient import ApiClient
from openshift.dynamic import DynamicClient
from src.actions import Actions
import sys
import logging
import yaml

class Sync(object):
    def __init__(self, namespace):
        self.namespace = namespace
    def syncToVault(self):
        k8s_client = ApiClient().apiclient()
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind='Secret')
        try:
            resource_list = v1_resources.get(namespace=self.namespace)
            logging.info('Retrieved list of secrets from project ' + self.namespace)
        except Exception as e:
            logging.error('Error encountered ' + str(e))
            sys.exit(1)
        secdict = []
        for resource in resource_list.items:
            secdict.append(resource.metadata.name)
        logging.info('Secret list is ' + str(secdict))
        for secret in secdict:
            try:
                fullyaml = v1_resources.get(name=secret, namespace=self.namespace)
                yamlresponse = yaml.safe_load(str(fullyaml))
                yamldata = yamlresponse['ResourceInstance[Secret]']['data']
                for key, value in yamldata.iteritems():
                    try:
                        Actions(secret_path=self.namespace + '/' + secret, mount_point='secret', secret={ key: value }).toVault()
                        logging.info('Secret ' + secret + ' key ' + key + ' added to hashicorp vault')
                    except Exception as e:
                        logging.error('Error pushing secret key ' + key + ' from secret ' + secret + ' to hashicorp vault. See ERROR: ' + str(e))
            except Exception as e:
                logging.error('Encountered error while getting Secret ' + secret + ' Error: ' + str(e))
            logging.info('All secrets in namespace ' + self.namespace + ' pushed to Vault')