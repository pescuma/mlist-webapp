#!/usr/bin/env python
# coding=utf-8

import cgi
import urllib


def isURLChar(c):
	return c in u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,/\\-_?=&%@#'

def isURL(word):
	if len(word) < 11:
		return False
	
	if not word.startswith(u'http://') and not word.startswith(u'https://'):
		return False
	
	for i in range(len(word)):
		if not isURLChar(word[i]):
			return False
	
	return True

def _removeOtherParams(text):
	pos = text.find('&')
	if pos >= 0:
		text = text[:pos]
	pos = text.find('?')
	if pos >= 0:
		text = text[:pos]
	pos = text.find('#')
	if pos >= 0:
		text = text[:pos]
	pos = text.find('/')
	if pos >= 0:
		text = text[:pos]
	return text

def _getParameter(url, param):
	pos = url.find('?')
	if pos < 0:
		return None
	url = url[pos+1:]
	pos = url.find(param + '=')
	if pos < 0:
		return None
	url = url[pos+len(param)+1:]
	return _removeOtherParams(url)
	
def _getTextAfter(word, textList):
	for base in textList:
		if word.startswith(base):
			return word[len(base):]
	return None

def _startsWith(word, textList):
	for base in textList:
		if word.startswith(base):
			return True
	return False

class ImageURLFormater:
	def handle(self, word):
		if not self.isImage(word):
			return None
		return u'<img src="' + word + u'" />'
	
	def isImage(self, word):
		return word.endswith('.png') or word.endswith('.jpg') or word.endswith('.jpeg') or word.endswith('.gif') \
		   	   or word.endswith('.bmp') or word.endswith('.ico') or word.endswith('.tif') 


class AnimotoURLFormater:
	_BASE_URLS = [ u'http://animoto.com/play/', u'http://www.animoto.com/play/' ]
	
	def handle(self, word):
		id = _getTextAfter(word, self._BASE_URLS)
		if not id:
			return None
		id = _removeOtherParams(id)
		return u'<span><embed id="video_player" width="432" height="263" flashvars="autostart=false&file=http://s3-p.animoto.com/Video/' + id + u'.flv&menu=true&volume=100&quality=high&repeat=false&usekeys=false&showicons=true&showstop=false&showdigits=false&enablejs=true&usecaptions=false&bufferlength=12&overstretch=false&remainonlastframe=true&javascriptid=video_player&backcolor=0x000000&frontcolor=0xBBBBBB&lightcolor=0xFFFFFF&screencolor=0x000000&width=432&height=263" allowscriptaccess="always" allowfullscreen="true" bgcolor="#000000" wmode="opaque" quality="high" name="video_player" src="http://animoto.com/swf/animotoplayer-3.15.swf" type="application/x-shockwave-flash"></embed></span>'


class CleVRURLFormater:
	_BASE_URLS = [ u'http://www.clevr.com/pano/', u'http://clevr.com/pano/' ]
	
	def handle(self, word):
		id = _getTextAfter(word, self._BASE_URLS)
		if not id:
			return None
		id = _removeOtherParams(id)
		return u'<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0" width="386" height="300"><param name="allowScriptAccess" value="never"><param name="movie" value="http://s3.clevr.com/CleVR?xmldomain=http://www.clevr.com/&amp;mov=' + id + u'"><embed src="http://s3.clevr.com/CleVR?xmldomain=http://www.clevr.com/&amp;mov=' + id + u'" width="386" height="300" name="CleVR" allowScriptAccess="never" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"></object>'


class YouTubeFormater:
	_BASE_URLS = [ u'http://youtube.com/watch?v=', u'http://www.youtube.com/watch?v=' ]
	
	def handle(self, word):
		id = _getTextAfter(word, self._BASE_URLS)
		if not id:
			return None
		id = _removeOtherParams(id)
		return u'<object width="425" height="355"><param name="movie" value="http://youtube.com/v/' + id + u'"></param><param name="wmode" value="transparent"></param><embed src="http://youtube.com/v/' + id + u'" type="application/x-shockwave-flash" wmode="transparent" width="425" height="355"></embed></object>'


class VimeoURLFormater:
	_BASE_URLS = [ u'http://www.vimeo.com/', u'http://vimeo.com/' ]
	
	def handle(self, word):
		id = _getTextAfter(word, self._BASE_URLS)
		if not id:
			return None
		id = _removeOtherParams(id)
		return u'<object width="400" height="300"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="never" /><param name="movie" value="http://www.vimeo.com/moogaloop.swf?clip_id=' + id + u'&amp;server=www.vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://www.vimeo.com/moogaloop.swf?clip_id=' + id + u'&amp;server=www.vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="never" width="400" height="300"></embed></object>'


class FlickrFormater:
	_BASE_URLS = [ u'http://www.flickr.com/slideShow/', u'http://flickr.com/slideShow/' ]
	
	def handle(self, word):
		if not _startsWith(word, self._BASE_URLS):
			return None
		
		return u'<iframe align="center" src="' + word + u'" frameBorder="0" width="450" scrolling="no" height="300"></iframe>' 


class FlickrFormaterPictoBrowser:
	_BASE_URLS = [ u'http://www.flickr.com/photos/', u'http://flickr.com/photos/' ]
	
	def handle(self, word):
		data = _getTextAfter(word, self._BASE_URLS)
		if not data:
			return None
		
		username = _removeOtherParams(data)
		params = '' # TODO '&userId='
		data = data[len(username):]
		
		if data.startswith('/sets/'):
			data = data[len('/sets/'):]
			id = _removeOtherParams(data)
			if not id:
				return None
			params = u'&source=sets&ids=' + id
			
#		elif data.startswith('/tags/'):
#			data = data[len('/tags/'):]
#			id = _removeOtherParams(data)
#			if not id:
#				return None
#			params = u'&source=keyword&ids=' + id + u'&names=' + id
		
		else:
			return None
			
		return u'<object width="400" height="300" align="middle"><param name="FlashVars" VALUE="userName=' + username + params + u'&titles=on&displayNotes=on&thumbAutoHide=on&imageSize=medium&vAlign=center&displayZoom=on&vertOffset=0&initialScale=off&bgAlpha=80"></param><param name="PictoBrowser" value="http://www.db798.com/pictobrowser.swf"></param><param name="scale" value="noscale"></param><param name="bgcolor" value="#dddddd"></param><embed src="http://www.db798.com/pictobrowser.swf" FlashVars="userName=' + username + params + u'&titles=on&displayNotes=on&thumbAutoHide=on&imageSize=medium&vAlign=center&displayZoom=on&vertOffset=0&initialScale=off&bgAlpha=80" loop="false" scale="noscale" bgcolor="#dddddd" width="400" height="300" name="PictoBrowser" align="middle"></embed></object>' 


class PicasaURLFormater:
	_BASE_URLS = [ u'http://picasaweb.google.com/', u'http://www.picasaweb.google.com/' ]
	
	def handle(self, word):
		word = _getTextAfter(word, self._BASE_URLS)
		if not word:
			return None
		
		p = word.find('/')
		if p < 0:
			return None
		
		user = _removeOtherParams(word[:p]) 
		word = word[p+1:]
		p = word.find('?authkey=')
		if p < 0:
			return None
		
		album = _removeOtherParams(word[:p]) 
		authkey = _removeOtherParams(word[p + len('?authkey='):])
		
		return u'<span><embed type="application/x-shockwave-flash" src="http://picasaweb.google.com/s/c/bin/slideshow.swf" width="400" height="267" flashvars="host=picasaweb.google.com&RGB=0x000000&feed=http%3A%2F%2Fpicasaweb.google.com%2Fdata%2Ffeed%2Fapi%2Fuser%2F' + user + u'%2Falbum%2F' + album + '%3Fkind%3Dphoto%26alt%3Drss%26authkey%3D' + authkey + '" pluginspage="http://www.macromedia.com/go/getflashplayer"></embed></span>'



class Formater:
	text = u''
	htmlStart = u''
	htmlEnd = u''
	inside = False
	
	def __init__(self, text, htmlStart, htmlEnd):
		self.text = text
		self.htmlStart = htmlStart
		self.htmlEnd = htmlEnd
	
	def start(self):
		out = u''
		if not self.inside:
			out += self.htmlStart
		self.inside = True
		return out

	def finish(self):
		out = u''
		if self.inside:
			out += self.htmlEnd
		self.inside = False
		return out
	
	def handle(self, parser):
		if parser.getChars(len(self.text)) == self.text:
			if parser.getChars(len(self.text) * 2)[len(self.text):] == self.text:
				return None 
			if parser.getChars(-len(self.text)) == self.text:
				return None
			 
			b = parser.getChar(-1)
			a = parser.getChar(len(self.text))
			if self.inside:
				if b and b not in u' \r\n\t' and (not a or a in u' \r\n\t.()[]{}-_?!@#\\/%&*^~+=|\'",<>:;'):
					parser.eat(len(self.text))
					return self.finish()
			else: 
				if a and a not in u' \r\n\t' and (not b or b in u' \r\n\t.()[]{}-_?!@#\\/%&*^~+=|\'",<>:;'):
					parser.eat(len(self.text))
					return self.start()
		return None


class MapLink:
	def handle(self, url, text = None):
		if not url.startswith(u'http://maps.google.'):
			return None
		
		ll = _getParameter(url, u'll')
		if not ll:
			return None
		 
		z = _getParameter(url, u'z')
		if z:
			ll += ',' + z
		
		if text:
			return u'<div name="gmap" class="gmap" style="width: 500px; height: 300px">GPS:' + cgi.escape(ll) + u'<br/>Text:' + toHTML(text, True) + u'</div>'
		else:
			return u'<div name="gmap" class="gmap" style="width: 500px; height: 300px">GPS:' + cgi.escape(ll) + u'</div>'
	
	def createLink(self, url, text):
		if url.startswith(u'map:'):
			if text:
				return u'<div name="gmap" class="gmap" style="width: 500px; height: 300px">' + cgi.escape(url[4:]) + u'<br/>Text:' + toHTML(text, True) + u'</div>'
			else:
				return u'<div name="gmap" class="gmap" style="width: 500px; height: 300px">' + cgi.escape(url[4:]) + u'</div>'
		
		return None
#		return self.handle(url, text)


class SimpleLink:
	def createLink(self, url, text):
		if not isURL(url):
			return None
		
		if text:
			text = toHTML(text, True)
		else:
			text = cgi.escape(url)
		
		return u'<a href="' + url + u'">' + text + u'</a>'


class LinkFormater:
	_handlers = [ MapLink(), SimpleLink() ]
	
	def start(self):
		return u''

	def finish(self):
		return u''
	
	def handle(self, parser):
		if parser.getChars(2) != '[[':
			return None
		if parser.getChars(-1) not in ' \t\r\n.?!\'":()':
			return None

		i = 2
		url = u''
		while parser.getChar(i) and parser.getChar(i) not in '\r\n[]':
			url += parser.getChar(i)
			i += 1
		
		if parser.getChar(i) != ']':
			return None
		i += 1
		
		text = u''
		if parser.getChar(i) == '[':
			i += 1
			while parser.getChar(i) and parser.getChar(i) not in '\r\n[]':
				text += parser.getChar(i)
				i += 1
			
			if parser.getChar(i) != ']':
				return None
			i += 1
				
		if parser.getChar(i) != ']':
			return None
		i += 1
		
		output = None
		for handler in self._handlers:
			output = handler.createLink(url, text)
			if output:
				break
		
		if not output:
			return None
		
		parser.eat(i)
		return output


class CodePretiffyTag:
	def canHandle(self, tagname):
		return tagname == 'code'

	def handle(self, parser, tag, text):
		if not parser.isInParagraph() and parser.isAtEndOfParagraph():
			return u'<pre class="prettyprint">' + cgi.escape(text) + u'</pre>'
		else:
			return u'<code class="prettyprint">' + cgi.escape(text) + u'</code>'
	


class SyntaxHightlighterTag:
	_langs = [ 'cpp', 'c', 'c++', 'c#', 'c-sharp', 'csharp', 'css', \
			   'delphi', 'pascal', 'java', 'js', 'jscript', 'javascript', \
			   'php', 'py', 'python', 'rb', 'ruby', 'rails', 'ror', 'sql', \
			   'vb', 'vb.net', 'xml', 'html', 'xhtml', 'xslt', 'bash', 'sh' ]
	
	def canHandle(self, tagname):
		for l in self._langs:
			if tagname == l:
				return True
		return False

	def handle(self, parser, tag, text):
		return u'<pre name="code" class="' + tag + '">' + cgi.escape(text) + u'</pre>'


class TagFormater:
	_tags = [ SyntaxHightlighterTag(), CodePretiffyTag() ]
	
	def start(self):
		return u''

	def finish(self):
		return u''

	def handle(self, parser):
		if parser.getChar() != '[':
			return None
		
		i = parser.find(']', 1)
		if not i:
			return None
			
		tagname = parser.getCharSlice(1, i-1)
		tag = self._getTag(tagname)
		if not tag:
			return None
		
		parser.eat(i + 1)

		endTag = '[/' + tagname + ']'
		i = parser.find(endTag)
		if not i:
			i = parser.getLenToParse()
		
		text = parser.getChars(i)
		parser.eat(i + len(endTag))
		
		return tag.handle(parser, tagname, text)
		
	def _getTag(self, name):
		for tag in self._tags:
			if tag.canHandle(name):
				return tag
		return None
		
	
class WikiParser:
	_i = 0
	_text = u''
	_len = 0
	_word = u''
	_oneLineOnly = False
	_out = u''
	_lastWasEnter = False
	_lastNumEnters = 0
	_needSpace = False
	_inParagraph = False
	_formaters = [ LinkFormater(), \
				   TagFormater(), \
				   Formater(u'/', u'<i>', u'</i>'), \
				   Formater(u'_', u'<u>', u'</u>'), \
				   Formater(u'*', u'<b>', u'</b>'), \
				   Formater(u'~', u'<del>', u'</del>'), \
				   Formater(u'^', u'<sup>', u'</sup>'), \
				   Formater(u',,', u'<sub>', u'</sub>'), \
				   Formater(u'!!', u'<span class="highlight">', u'</span>'), \
				   Formater(u'++', u'<span class="added">', u'</span>'), \
				   Formater(u'--', u'<span class="removed">', u'</span>') ]
	_urlFormaters = [ ImageURLFormater(), AnimotoURLFormater(), PicasaURLFormater(), \
					  CleVRURLFormater(), YouTubeFormater(), FlickrFormater(), FlickrFormaterPictoBrowser(), \
					  VimeoURLFormater(), MapLink() ]
	
	
	def registerURLFormater(urlFormater):
		WikiParser._urlFormaters.append(urlFormater)
	registerURLFormater = staticmethod(registerURLFormater)
	
	def __init__(self, text, oneLineOnly = False):
		self._text = unicode(text)
		self._len = len(self._text)
		self._oneLineOnly = oneLineOnly
	
	def getHTML(self):
		return self._out
	
	def getChars(self, diff = 1):
		if diff > 0:
			start = self._i
			end = self._i + diff
		else:
			start = self._i + diff
			end = self._i
			if start < 0:
				start = 0
		
		return self._text[start:end]
	
	def getCharSlice(self, start, diff = 1):
		start = self._i + start
		end = start + diff
		if start < 0:
			start = 0
		if end < 0:
			end = 0
		
		return self._text[start:end]

	def getChar(self, diff = 0):
		pos = self._i + diff
		if pos < 0 or pos >= self._len:
			return None
		return self._text[pos]
	
	def isInParagraph(self):
		return self._inParagraph

	def eat(self, len = 1):
		self._i += len
	
	def find(self, text, start = 0):
		textLen = len(text)
		pos = self._i + start
		while pos < self._len and self._text[pos:pos+textLen] != text:
			pos += 1
		if pos >= self._len:
			return None
		return pos - self._i
	
	def getLenToParse(self):
		return self._len - self._i
	
	
	def startParagraph(self):
		if self._oneLineOnly:
		  return u''
		ret = u''
		if not self._inParagraph:
			if self._lastNumEnters >= 4:
				ret += u'<br />'
			ret += u'<p>'
		self._inParagraph = True
		return ret

	def finishParagraph(self):
		if self._oneLineOnly:
		  return u''
		ret = u''
		if self._inParagraph:
			for f in self._formaters:
				ret += f.finish()
			ret += u'</p>'
		self._inParagraph = False
		return ret
		
	def handleParagraph(self):
		if self._oneLineOnly:
		  return u''
		ret = u''
		if self._lastWasEnter:
			ret += self.finishParagraph()
		return ret
		
	def formatWord(self, word):
		ret = None
		
		if isURL(word):
			after = u''
			if word[len(word)-1] in u'.?!:':
				after = word[len(word)-1]
				word = word[:len(word)-1]
			
			for urlFormater in self._urlFormaters:
				ret = urlFormater.handle(word)
				if ret:
					break
			
			if not ret:  
				ret = u'<a href="' + word + u'">' + cgi.escape(word) + u'</a>'
			
			ret += after
			
		else: 
			ret = cgi.escape(word)
		
		return ret
				
	
	def appendWord(self, always):
		if not always and not self._word:
			return
		
		p = self.startParagraph()
		if p:
			self._out += p
		elif self._needSpace:
			self._out += u' '
		self._out += self.formatWord(self._word)
		
		self._word = u''
		self._needSpace = False
	
	def isAtEndOfParagraph(self):
		i = 0
		count = 0
		while self.getChar(i) and count < 2:
			c = self.getChar(i)
			
			if c == u'\r':
				if self.getChar(i + 1) == u'\n':
					i += 1
				c = u'\n'
			
			if c == u'\n':
				count += 1
			
			if c not in u' \t\n':
				break
		
		return count >= 2 or not self.getChar(i)
			
	
	def parse(self):
		if self._oneLineOnly:
			self._inParagraph = True
		
		while self._i < self._len:
			c = self._text[self._i]
			
			if c == u'\r':
				if self.getChar(1) == u'\n':
					self.eat(1)
				c = u'\n'
			
			if c == u'\n':
				self.eat(1)
				self.appendWord(False)
				self._out += self.handleParagraph()
				if self._lastWasEnter:
					self._lastNumEnters += 1
				else:
					self._lastNumEnters = 1
				self._lastWasEnter = True
				self._needSpace = True
				continue

			form = None
			for f in self._formaters:
				form = f.handle(self)
				if form:
					break
			
			char = None
			if not form:
				if c not in u' \t':
					char = c
				self.eat(1)
			
			if form:
				self.appendWord(True)
				self._out += form
			
			elif not char:
				self.appendWord(False)
				self._needSpace = True
				
			else:
				self._word += char
			
			if form or char:
				self._lastWasEnter = False
		
		self.appendWord(False)
		
		for f in self._formaters:
			self._out += f.finish()
		
		self._out += self.finishParagraph()
			
		

def toHTML(text, oneLineOnly = False):
	parser = WikiParser(text, oneLineOnly)
	parser.parse()
	return parser.getHTML()


