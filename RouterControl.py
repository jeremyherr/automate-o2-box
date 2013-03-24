import settings
from urllib2 import Request, urlopen, HTTPError, HTTPCookieProcessor, install_opener, build_opener
import hashlib

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

	def calculateHashes(self, realm, nonce, qop, uri):
		"""Calculate the MD5 checksums that the in-page JavaScript uses to send password over http"""
		HA1 = hashlib.md5(self.username + ":" + realm + ":" + self.password).hexdigest()
		HA2 = hashlib.md5("GET" + ":" + uri).hexdigest()
		return hashlib.md5(HA1 + ":" + nonce + ":" + "00000001" + ":" + "xyz" + ":" + qop + ":" + HA2).hexdigest()

if __name__ == "__main__":
	rc = RouterControl()
	print rc.getLoginPage()
	print rc.calculateHashes("Technicolor Gateway", "1851954:341337:204731139790f1a60397421eea9eb90f", "auth", "/login.lp")
