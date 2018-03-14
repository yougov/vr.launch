.. image:: https://gitlab.yougov.net/support/yg.launch/badges/master/pipeline.svg
   :target: https://gitlab.yougov.net/support/yg.launch/commits/master

Deploying against Velociraptor? Need to load the config? It's easy::

    parser = argparse.ArgumentParser()
    yg.launch.cmdline.add_config_arg(parser)
    # add your own custom args too
    args = parser.parse_args()
    startup_app(args.config)

This module loads the config from YAML into a nice ItemsAsAttributes
dictionary, so you can get the config values as items or as attributes::

    args.config.foo == args.config['foo']

Enjoy!
