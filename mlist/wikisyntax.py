#!/usr/bin/env python
# coding=utf-8

import cgi

def isURLChar(c):
	return c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:./\\-_?=&%'

def isURL(word):
	if len(word) < 11:
		return False
	
	if not word.startswith(u'http://') and not word.startswith(u'https://'):
		return False
	
	for i in range(len(word)):
		if not isURLChar(word[i]):
			return False
	
	return True

def isImage(word):
	return word.endswith('.png') or word.endswith('.jpg') or word.endswith('.jpeg') or word.endswith('.gif') \
	   	   or word.endswith('.bmp') or word.endswith('.ico') or word.endswith('.tif') 

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


class LinkFormater:
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
		while parser.getChar(i) and isURLChar(parser.getChar(i)):
			url += parser.getChar(i)
			i += 1
		
		if not isURL(url):
			return None
		
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
		
		if text:
			text = toHTML(text, True)
		else:
			text = cgi.escape(url)
		
		parser.eat(i)
		return '<a href="' + url + '">' + text + '</a>'
	
	
class WikiParser:
	_i = 0
	_text = u''
	_word = u''
	_oneLineOnly = False
	_out = u''
	_lastWasEnter = False
	_needSpace = False
	_inParagraph = False
	_formaters = []
	
	def __init__(self, text, oneLineOnly = False):
		self._text = unicode(text)
		self._oneLineOnly = oneLineOnly
		self._formaters = [ Formater(u'/', u'<i>', u'</i>'), \
					  Formater(u'_', u'<u>', u'</u>'), \
					  Formater(u'*', u'<b>', u'</b>'), \
					  Formater(u'~', u'<del>', u'</del>'), \
					  Formater(u'^', u'<sup>', u'</sup>'), \
					  Formater(u',,', u'<sub>', u'</sub>'), \
					  Formater(u'!!', u'<span class="highlight">', u'</span>'), \
					  Formater(u'++', u'<span class="added">', u'</span>'), \
					  Formater(u'--', u'<span class="removed">', u'</span>'), \
					  LinkFormater() ]
	
	def getHTML(self):
		return self._out
	
	def getChars(self, diff = 1):
		if diff > 0:
			start = self._i
			end = self._i + diff
			if end > len(self._text):
				end = len(self._text)
		else:
			start = self._i + diff
			end = self._i
			if start < 0:
				start = 0
		
		return self._text[start:end]

	def getChar(self, diff = 0):
		pos = self._i + diff
		if pos < 0 or pos >= len(self._text):
			return None
		return self._text[pos]

	def eat(self, len = 1):
		self._i += len
	
	
	def startParagraph(self):
		if self._oneLineOnly:
		  return u''
		ret = u''
		if not self._inParagraph:
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
		ret = u''
		if isURL(word):
			after = u''
			if word[len(word)-1] in u'.?!:':
				after = word[len(word)-1]
				word = word[:len(word)-1]
			
			if isImage(word):
				ret += u'<img src="' + word + u'" />'
			else:
				ret += u'<a href="' + word + u'">' + cgi.escape(word) + u'</a>'
			ret += after
			
		else: 
			ret += cgi.escape(word)
		
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
		
	
	def parse(self):
		if self._oneLineOnly:
			self._inParagraph = True
		
		while self.getChar():
			c = self.getChar()
			
			if c == u'\r':
				if self.getChar(1) == u'\n':
					self.eat(1)
				c = u'\n'
			
			if c == u'\n':
				self.eat(1)
				self.appendWord(False)
				self._out += self.handleParagraph()
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


