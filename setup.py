#!/usr/bin/env python
import os
import sysfrom setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()packages = ['actions', 'apiclient', 'hvclient', 'logger', 'mapping', 'verbs']

package_dir = {
    'actions': 'src/',
    'apiclient': 'src/',
    'hvclient': 'src/',
    'logger': 'src/',
    'mapping': 'src/',
    'verbs': 'src/'
}

requires = [
    'openshift==0.9.0',
    'hvac==0.9.6',
    'ruamel.yaml==0.15.97'
]

setup(
    name='hvac-openshift-feeder',
    version='1.0.0',
    description='Feed to and from Vault onto openshift',
    author='mdhar',
    author_email='',
    url='https://github.com/mainak90/hvac-openshift-feeder',
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=requires,
    license='Apache GPL',
    entry_points='''
        [console_scripts]
        feeder=src.app:main
    '''
)
