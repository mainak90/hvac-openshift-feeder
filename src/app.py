import argparse
import logging
import src.logger
import sys
import os
from src.mapping import Mapping

def main(args=None):
    src.logger.setLevel()
    parser = argparse.ArgumentParser(description='Listed arguments --action --pushconfig --namespace --path --out')
    parser.add_argument("-r", "--action", choices=['export'], help="layout the action to perform like import or export")
    parser.add_argument("-p", "--pushconfig", help="[OPTIONAL] layout the action to perform like import or export", action="store_true")
    parser.add_argument("-n", "--namespace", help="[OPTIONAL] The openshift and vault namespace to connect to, only use when the --pushconfig is set")
    #parser.add_argument("-a", "--all", help="use this to import/export all kv to and from from namespaces")
    parser.add_argument("--path", help="The directory path to the template files")
    parser.add_argument("-o", "--out", help="The secret outputpath")
    #parser.add_argument("-k", "--key", help="the key name to import/export the key pair from/to")
    #parser.add_argument("-a", "--all", help="use this to import/export all kv to and fro from namespaces")
    args = parser.parse_args()
    if args.action and args.path and args.out:
        action = args.action
        path = os.path.abspath(args.path)
        output = os.path.abspath(args.out)
        print('Path: ' + path + ' output: ' + output + ' action: ' + action)
    else:
        logging.info('All 3 params --action, --path and --out are mandatory to invoke this function')
        print('All 3 params --action, --path and --out are mandatory to invoke this function')
        sys.exit(1)
    if args.pushconfig and args.namespace and args.action == "export":
        namespace = args.namespace
        Mapping(templatepath=path, outputpath=output, namespace=namespace, pushconfig='True').mapSecrets()
    elif args.action == "export":
        logging.info('Pushconfig has not been requested, if --namspace is provided it will be ignored')
        print('Pushconfig has not been requested, if --namspace is provided it will be ignored')
        Mapping(templatepath=path, outputpath=output).mapSecrets()
    else:
        logging.info('Missing either of the mandatory params --action, --path and --out, please re-renter with proper params')
        print('Missing either of the mandatory params --action, --path and --out, please re-renter with proper params')
        sys.exit(1)if __name__ == '__main__':
    sys.exit(main())
