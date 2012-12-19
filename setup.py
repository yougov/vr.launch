#!/usr/bin/env python
# Generated by jaraco.develop (https://bitbucket.org/jaraco/jaraco.develop)
import setuptools

setup_params = dict(
	name='yg.launch',
	use_hg_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	url="https://bitbucket.org/jaraco/yg.launch",
	packages=setuptools.find_packages(),
	namespace_packages=['yg'],
	zip_safe=False,
	install_requires=[
		'pyyaml',
	],
	setup_requires=[
		'hgtools',
	],
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
