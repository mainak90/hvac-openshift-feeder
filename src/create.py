import yaml
from openshift.dynamic import DynamicClient
from src.apiclient import ApiClient
import sys
import logging



class Create(object):
    def __init__(self,resource_type,namespace,filepath):
        self.resource_type = resource_type
        self.namespace = namespace
        self.filepath = filepath

    def createResource(self):
        logging.info('Creating '+ self.resource_type + '  ' + self.filepath + ' into project ' + self.namespace)
        with open(self.filepath) as resource:
            resource_dict=yaml.load(resource)	 #config.load_kube_config()
            name=resource_dict['metadata']['name']
            data=resource_dict['data']
        k8s_client = ApiClient().apiclient()
        api_instance = k8s_client.CoreV1Api()
        sec  = k8s_client.V1Secret()
        try:
            sec.metadata = k8s_client.V1ObjectMeta(name=name)
            sec.type = "Opaque"
            sec.data = data
            resp = api_instance.create_namespaced_secret(namespace=self.namespace, body=sec)
            return resp
        except Exception as e:
            logging.error('Exception occured '+ str(e))
            sys.exc_clear()
