import os
import re
import copy
import platform
import warnings

import six

import yaml
import yamlenv
import jaraco.collections


class ConfigDict(jaraco.collections.ItemsAsAttributes, dict):
    """
    A simple config dictionary implementation with YAML helpers
    """
    @classmethod
    def from_yaml(cls, filename):
        with open(filename) as f:
            return cls.from_yaml_stream(f)

    @classmethod
    def from_yaml_stream(cls, stream):
        """
        >>> os.environ['PORT_TEST'] = '5000'
        >>> ConfigDict.from_yaml_stream('port_test: ${PORT_TEST}')
        {'port_test': '5000'}
        """
        return cls(yamlenv.load(stream))

    @classmethod
    def from_velociraptor(cls, fallback=None):
        """
        Load the config from file indicated by APP_SETTINGS_YAML or the
        fallback filepath (if it is a file). Return None if no file is found.
        """
        filename = os.environ.get('APP_SETTINGS_YAML', fallback) or ''
        return cls.from_yaml(filename) if os.path.isfile(filename) else None

    def to_yaml(self, filename):
        with open(filename, 'w') as f:
            yaml.dump(self, f)

    def apply_environment_overrides(self):
        """
        Allow the environment to override keys in self if the vars match
        keys already present.

        Consider if PORT_TEST is defined thusly in the environment:
        >>> os.environ['PORT_TEST'] = '5000'

        >>> d = ConfigDict(port_test='8010')
        >>> d.apply_environment_overrides()
        >>> d['port_test']
        5000

        Environment overrides should decode yaml.
        >>> os.environ['PORT_TEST'] = '"5000"'
        >>> d = ConfigDict(port_test=8010)
        >>> d.apply_environment_overrides()
        >>> d['port_test']
        '5000'
        """
        warnings.warn(
            'apply_environment_overrides is deprecated '
            'in favour of yamlenv environment interpolation',
            DeprecationWarning)
        environ = self._case_insensitive_environ()

        matching_keys = [key for key in self if key in environ]
        for key in matching_keys:
            self[key] = yaml.safe_load(environ[key])

    @staticmethod
    def _case_insensitive_environ():
        if platform.system() == 'Windows':
            return os.environ
        return jaraco.collections.FoldedCaseKeyedDict(os.environ)


def obscure(src, sensitive_keys=['password']):
    """
    Return a deep copy of src (MutableMapping) with sensitive keys obscured.

    >>> nested = dict(password='top secret')
    >>> d = dict(a=1, b=2, password='very secret', nested=nested)
    >>> obscure(d)['a']
    1
    >>> obscure(d)['password']
    '********'
    >>> obscure(d)['nested']['password']
    '********'

    >>> type(obscure(ConfigDict(d)))
    <class 'vr.launch.config.ConfigDict'>
    """
    result = copy.copy(src)

    for key, value in six.iteritems(result):
        if isinstance(value, dict):
            result[key] = obscure(value, sensitive_keys)
        elif key in sensitive_keys:
            result[key] = '********'
    return result


def env_substitute(config, key):
    """
    For the key in config, substutite $env:name or
    ${env:name with spaces and stuff} with values from the environment
    (os.environ[name]).

    config should be a ConfigDict or other MutableMapping.
    """

    def env_repl(match):
        var_spec = match.group('var')
        var_spec = var_spec.lstrip('{').rstrip('}')
        _, _, var = var_spec.partition(':')
        return os.environ[var]

    value = config.get(key, None)
    if not isinstance(value, six.string_types):
        return
    # allow the name to be specified as
    #  $env:name or ${env:name with spaces and stuff}
    pattern = re.compile(r'\$(?P<var>({env:[\w ()-]+})|(env:\w+))')
    after_sub = pattern.sub(env_repl, value)
    # Run the value through yaml.safe_load so the resulting value
    #  can be an integer or other YAML value.
    config[key] = yaml.safe_load(after_sub)
