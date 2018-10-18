.. image:: https://img.shields.io/pypi/v/vr.launch.svg
   :target: https://pypi.org/project/vr.launch

.. image:: https://img.shields.io/pypi/pyversions/vr.launch.svg

.. image:: https://img.shields.io/travis/yougov/vr.launch/master.svg
   :target: https://travis-ci.org/yougov/vr.launch

.. .. image:: https://img.shields.io/appveyor/ci/yougov/vr.launch/master.svg
..    :target: https://ci.appveyor.com/project/yougov/vr.launch/branch/master

.. .. image:: https://readthedocs.org/projects/vrlaunch/badge/?version=latest
..    :target: https://vrlaunch.readthedocs.io/en/latest/?badge=latest

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
