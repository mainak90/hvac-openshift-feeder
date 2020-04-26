import argparse
import logging
import sys
import os
import json
import src.logger
from src.sync import Sync
from src.mapping import Mapping


def main(args=None):
	src.logger.setLevel()
	parser = argparse.ArgumentParser(description='Listed arguments --action --pushconfig --namespace --path --out')
	parser.add_argument("-r", "--action", choices=['export', 'import'], help="layout the action to perform like import or export")
	parser.add_argument("-p", "--pushconfig", help="[OPTIONAL] layout the action to perform like import or export", action="store_true")
	parser.add_argument("-n", "--namespace", help="[OPTIONAL] The openshift and vault namespace to connect to, only use when the --pushconfig is set")
	parser.add_argument("--path", help="The directory path to the template files")
	parser.add_argument("-o", "--out", help="The secret outputpath")
	parser.add_argument("-p", "--secretpath", help="the secret name to export the key pair from vault into openshift")
	args = parser.parse_args()
	if args.action and args.out:
		action = args.action
		output = os.path.abspath(args.out)
		print(' output: ' + output + ' action: ' + action)
	else:
		logging.info('Unless action equals import, all 3 params --action, --path and --out are mandatory to invoke this function')
		print('Unless action is import, all 3 params --action, --path and --out are mandatory to invoke this function')
		sys.exit(1)
	path = args.path if args.path is not None else os.path.abspath('template/secret.yaml')
	ctx = os.environ['FEEDER_SECRETENGINE_CTX'] if 'FEEDER_SECRETENGINE_CTX' in os.environ else json.load(open(os.path.expanduser("~") + '/hvac.json', 'r'))['ctx']
	if args.pushconfig and args.namespace and args.action == "export":
		secretpath = args.secretpath
		namespace = args.namespace
		Mapping(ctx=ctx, mountpath=secretpath, templatepath=path, outputpath=output, namespace=namespace, pushconfig='True').mapSecrets()
	elif args.action == "export":
		secretpath=args.secretpath
		logging.info('Pushconfig has not been requested, if --namspace is provided it will be ignored')
		print('Pushconfig has not been requested, if --namspace is provided it will be ignored')
		Mapping(ctx=ctx, mountpath=secretpath, templatepath=path, outputpath=output).mapSecrets()
	elif args.action == "import":
		Sync(args.namespace).syncToVault()
	else:
		logging.info('Missing either of the mandatory params --action, --path and --out, please re-renter with proper params')
		print('Missing either of the mandatory params --action, --path and --out, please re-renter with proper params')
		sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())
