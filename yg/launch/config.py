import os
import re

import six

import yaml
import jaraco.util.dictlib

class ConfigDict(jaraco.util.dictlib.ItemsAsAttributes, dict):
	"""
	A simple config dictionary implementation with YAML helpers
	"""
	@classmethod
	def from_yaml(cls, filename):
		with open(filename) as f:
			return cls.from_yaml_stream(f)

	@classmethod
	def from_yaml_stream(cls, stream):
		return cls(yaml.load(stream))

	def to_yaml(self, filename):
		with open(filename, 'w') as f:
			yaml.dump(self, f)

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
	if not isinstance(value, six.string_types): return
	# allow the name to be specified as
	#  $env:name or ${env:name with spaces and stuff}
	pattern = re.compile(r'\$(?P<var>({env:[\w ()-]+})|(env:\w+))')
	after_sub = pattern.sub(env_repl, value)
	# Run the value through yaml.safe_load so the resulting value
	#  can be an integer or other YAML value.
	config[key] = yaml.safe_load(after_sub)
