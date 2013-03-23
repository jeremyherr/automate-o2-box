import settings

class RouterControl:
	"""Class for logging into O2 Wireless router and changing settings"""

	def __init__(self, **kwargs):
		"""Any optional parameters passed will overwrite parameters set in settings.py"""
		for s in ['loginUrl', 'username', 'password']:
			if s in kwargs:
				setattr(self, s, kwargs[s])
			else:
				setattr(self, s, getattr(settings, s))

if __name__ == "__main__":
	rc = RouterControl()

