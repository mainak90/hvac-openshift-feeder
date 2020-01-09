import yaml
from openshift.dynamic import DynamicClient
from src.apiclient import ApiClient
import sys
import logging
import time
import kubernetes.client
from pprint import pprint
from kubernetes import client, config


class Create(object):

     def __init__(self,resource_type,namespace,filepath,url=None):
        self.resource_type = resource_type
        self.namespace = namespace
        self.filepath = filepath
        self.url = url

    def createResource(self):
        logging.info('Creating '+ self.resource_type + '  ' + self.filepath + ' into project ' + self.namespace)
        with open(self.filepath) as resource:
            resource_dict=yaml.load(resource)        #config.load_kube_config()
        #v1 = client.CoreV1Api()
        #response = v1.create_namespaced_secret(namespace=self.namespace, body=resource_dict)
        k8s_client = ApiClient().apiclient()
        dyn_client = DynamicClient(k8s_client)
        v1_resources=dyn_client.resources.get(api_version='v1', kind=self.resource_type)
        try:
            resp = v1_resources.create(body=resource_dict, namespace=self.namespace)
            return resp
        except Exception as e:
            logging.error('Exception occured '+ str(e))
            sys.exc_clear()
