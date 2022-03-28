# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

# get version from __version__ variable in sentry/__init__.py
from sentry import __version__ as version

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
	name='sentry',
	version=version,
	description='Logs errors to Sentry',
	author='Parsimony LLC',
	author_email='valmik@parsimony.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
