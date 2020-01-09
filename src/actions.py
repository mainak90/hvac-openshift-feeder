from src.hvclient import HvClient
import os
import sys
from src.apiclient import ApiClient
import logging
import ruamel.yaml
import yaml
import json

class Actions(object):
    def __init__(self, key=None, configpath=None, mount_point='', secret_path='', secret=None):
        self.key = key
        self.configpath = configpath
        self.secret = secret
        self.mount_point = mount_point
        self.secret_path = secret_path

    def fromVault(self):
        client = HvClient(configpath=self.configpath).newClient()
        read_secret_latest_version = client.secrets.kv.v2.read_secret_version(
            path=str(self.secret_path),
            mount_point=str(self.mount_point)
        )
        version = read_secret_latest_version['data']['metadata']['version']
        read_secret_result = client.secrets.kv.v2.read_secret_version(
            path=str(self.secret_path),
            mount_point=str(self.mount_point),
            version=version
        )
        return read_secret_result['data']['data'][self.key]    def listFromVault(self):
        client = HvClient(configpath=self.configpath).newClient()
        read_secret_result = client.secrets.kv.v2.list_secrets(
            mount_point=str(self.mount_point),
            path=str(self.secret_path),
        )
        return read_secret_result['data']['keys']

    def toVault(self):
        client = HvClient(configpath=self.configpath).newClient()
        try:
            client.secrets.kv.v2.create_or_update_secret(
                path=self.secret_path,
                secret=self.secret,
                mount_point=self.mount_point
            )
            logging.info('The kv ' + self.secret + ' has been added into path ' + self.mount_point + '/' + self.secret_path)
        except Exception as e:
            logging.error('Exception encountered while pushing into vault : ' + str(e))
