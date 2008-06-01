#!/usr/bin/env python
# coding=utf-8

from django import template
from google.appengine.ext import webapp
from trans import *
import cgi
import wikisyntax


def nick(value):
	if not value:
		return cgi.escape(t('Anonimo'))
	
	nick = value.nickname()
	pos = nick.rfind('@')
	if pos >= 0:
	  nick = nick[:pos] + '@...'
	return cgi.escape(nick)

def wiki(value):
	return wikisyntax.toHTML(value, False)

def wikiSL(value):
	return wikisyntax.toHTML(value, True)

class TransNode(template.Node):
	def __init__(self, text):
		self.text = text
	def render(self, context):
		return cgi.escape(t(self.text))

def trans(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		tag_name, format_string = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
	
	if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
		raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
	
	return TransNode(format_string[1:-1])

register = webapp.template.create_template_register()
register.filter(nick)
register.filter(wiki)
register.filter(wikiSL)
register.tag('trans', trans)
