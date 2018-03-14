import argparse

from . import config


class MergeDictAction(argparse.Action):
    """
    An argparse action that will merge the incoming dictionary into the
    destination.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        assert isinstance(values, dict), "Values must be dict"
        getattr(namespace, self.dest).update(values)


def add_config_arg(parser):
    parser.add_argument(
        '-c', '--config', help="Filename for YAML config",
        action=MergeDictAction, default=config.ConfigDict(),
        type=config.ConfigDict.from_yaml,
    )


def get_parser():
    parser = argparse.ArgumentParser()
    add_config_arg(parser)
    return parser
