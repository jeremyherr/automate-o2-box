import settings
from urllib2 import Request, urlopen, HTTPError, HTTPCookieProcessor, install_opener, build_opener
import hashlib
import re

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
		"""Retrieve the login page source"""
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

	def calculateHashes(self, jsVars):
		"""Calculate the MD5 checksums that the in-page JavaScript uses to send password over http"""
		HA1 = hashlib.md5(self.username + ":" + jsVars['realm'] + ":" + self.password).hexdigest()
		HA2 = hashlib.md5("GET" + ":" + jsVars['uri']).hexdigest()
		return hashlib.md5(HA1 + ":" + jsVars['nonce'] + ":" + "00000001" + ":" + "xyz" + ":" + jsVars['qop'] + ":" + HA2).hexdigest()

	def extractJavaScriptVars(self, html, wantedJsVars):
		"""Given page source, extract JavaScript variable values"""
		foundJsVars = {}
		regExpJsVar = re.compile(r"var\s+(\w+)\s*=\s*\"([^\"]+)\";")
		matches = re.findall(regExpJsVar, html)
		if matches:
			print "JavaScript vars found"
			for pair in matches:
				if pair[0] in wantedJsVars:
					print "%s: %s" % (pair[0], pair[1])
					foundJsVars[pair[0]] = pair[1]
		else:
			print "no JavaScript vars found"

		return foundJsVars

	def extractHtmlInputs(self, html, wantedHtmlVars):
		"""Given page source, extract HTML input fields"""
		foundHtmlVars = {}
		regExpHtmlInput = re.compile(r"\<input\s+type\s*=\s*\"hidden\"\s+name\s*=\s*\"([^\"]+)\"\s+value\s*=\s*\"([^\"]+)\"\s*\>")
		matches = re.findall(regExpHtmlInput, html)
		if matches:
			print "HTML input fields found"
			for pair in matches:
				if pair[0] in wantedHtmlVars:
					print "%s: %s" % (pair[0], pair[1])
					foundHtmlVars[pair[0]] = pair[1]
		else:
			print "no HTML input fields found"

		return foundHtmlVars

	def postLoginCredentials(self):
		pass

if __name__ == "__main__":
	rc = RouterControl()
	print rc.calculateHashes(rc.extractJavaScriptVars(rc.getLoginPage(), ['realm', 'nonce', 'qop', 'uri']))
	print rc.extractHtmlInputs(rc.getLoginPage(), ['rn'])