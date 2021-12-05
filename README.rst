.. image:: https://img.shields.io/pypi/v/skeleton.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/skeleton.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/skeleton

.. image:: https://github.com/jaraco/skeleton/workflows/tests/badge.svg
   :target: https://github.com/jaraco/skeleton/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2021-informational
   :target: https://blog.jaraco.com/skeleton

Deploying against Velociraptor? Need to load the config? It's easy::

    parser = argparse.ArgumentParser()
    yg.launch.cmdline.add_config_arg(parser)
    # add your own custom args too
    args = parser.parse_args()
    startup_app(args.config)

This module loads the config from YAML into a nice ItemsAsAttributes
dictionary, so you can get the config values as items or as attributes::

    args.config.foo == args.config['foo']

Config is loaded using `yamlenv <https://pypi.org/project/yamlenv/>`,
so any YAML can reference environment variables and other YAML files
to be interpolated.

Enjoy!
