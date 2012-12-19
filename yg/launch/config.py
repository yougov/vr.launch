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
