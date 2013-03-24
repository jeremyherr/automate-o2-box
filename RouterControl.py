import settings
from urllib2 import Request, urlopen, HTTPError, HTTPCookieProcessor, install_opener, build_opener

class RouterControl:
	"""Class for logging into O2 Wireless router and changing settings"""

	def __init__(self, **kwargs):
		"""Any optional parameters passed will overwrite parameters set in settings.py"""
		for s in ['loginUrl', 'username', 'password']:
			if s in kwargs:
				setattr(self, s, kwargs[s])
			else:
				setattr(self, s, getattr(settings, s))

	def getLoginPage(self):

		request = Request(self.loginUrl)

		opener = build_opener(HTTPCookieProcessor())
		install_opener(opener)

		try:
			response = urlopen(request)
			html = response.read()
			print "info: %s"    % response.info()
			print "getcode: %s" % response.getcode()
			print "geturl: %s"  % response.geturl()
			return html
		except HTTPError, e:
			error_message = str(e.code) + e.msg

if __name__ == "__main__":
	rc = RouterControl()
	print rc.getLoginPage()
