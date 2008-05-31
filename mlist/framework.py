#!/usr/bin/env python
# coding=utf-8

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import cgi
import datetime
import os
import wsgiref.handlers
from recaptcha.client import captcha
import wikisyntax
from trans import *


DEBUG = (os.environ['SERVER_NAME'] == 'localhost')
_DEBUG_TRANSLATION = True and DEBUG  


def getServerURL():
	url = 'http://' + os.environ['SERVER_NAME']
	if os.environ['SERVER_PORT'] != 80:
		url += ':' + os.environ['SERVER_PORT']
	return url



class Menu:
	name = ''
	url = ''
	
	def __init__(self, name, url = ''):
		self.name = name
		self.url = url


class Field:
	type = 'text'
	max = None
	
	def __init__(self, name, **keywords):
		self.name = name
		for kw in keywords.keys():
			setattr(self, kw, keywords[kw])

class Form:
	pass

class BasePage(webapp.RequestHandler):
	URL = None
	TEMPLATE = None
	
	title = ''
	left_menus = []
	right_menus = []
	warnings = []
	errors = []
	infos = []
	
	def _initData(self):
		setLanguage(self._getAcceptedLanguages())
		
		title = None
		self.left_menus = [ Menu(t('New'), '/new') ]
		self.right_menus = []
		self.warnings = []
		self.errors = []
		self.infos = []
		
		if users.get_current_user():
			self.right_menus.append(Menu(users.get_current_user().email()))

	def _getAcceptedLanguages(self):
		accept = os.environ['HTTP_ACCEPT_LANGUAGE']
		next = accept
		langs = []
		for l in accept.split(','):
			pos = l.find(';')
			if pos >= 0:
				l = l[:pos]
			l = l.strip(' \t\r\n')
			if l:
				langs.append(l.replace('-', '_').strip())
		return langs
	
	def get(self):
		self._initData()
		
	def post(self):
		self._initData()
		
	def err(self, error):
		self.errors.append(error)
		
	def warn(self, warn):
		self.warnings.append(warn)
		
	def info(self, info):
		self.infos.append(info)
		
	def form(self, fieldName):
		return self.request.get(fieldName).strip(' \t\r\n')
	
	def getForm(self, *props):
		fields = dict()
		for prop in props:
			fields[prop.name] = prop
			
		form = Form()
		for name in self.request.POST:
			val = self.request.POST.get(name)
			if hasattr(val, 'filename'):
				file = object()
				file.name = val.filename
				file.data = val.file.read()
				file.isFile = True
				setattr(form, name, file)
			else:
				val = val.strip(' \t\r\n')
				
				if fields.has_key(name):
					field = fields[name]
					if field.max:
						val = val[:field.max]
					if field.type == 'boolean':
						val = bool(val)
			
				setattr(form, name, val)
		
		for field in props:
			if hasattr(form, field.name):
				continue
			if field.type == 'boolean':
				val = False
			else:
				val = ''
				 
			setattr(form, field.name, val)
		
		return form
	
	def render(self, html, **keywords):
		if self.title:
			self.title = self.title + ' :: mlist'
		else:
			self.title = 'mlist'
		
		if users.get_current_user():
			self.left_menus.append(Menu(t('My stuff'), '/mystuff'))
			self.right_menus.append(Menu(t('Log out'), users.create_logout_url(self.request.uri)))
		else:
			self.right_menus.append(Menu(t('Log in'), users.create_login_url(self.request.uri)))
		self.right_menus.append(Menu(t('About'), '/about'))
		self.right_menus.append(Menu(t('Bugs?'), 'http://code.google.com/p/mlist-webapp/issues/list'))
			
		template_values = {
		  'title' : self.title,
		  'left_menus' : self.left_menus,
		  'right_menus' : self.right_menus,
		  'warnings' : self.warnings,
		  'errors' : self.errors,
		  'infos' : self.infos,
		  'user' : users.get_current_user()
		  }
		
		keys = keywords.keys()
		for kw in keys:
			template_values[kw] = keywords[kw]
			
		if _DEBUG_TRANSLATION:
			template.render(html, template_values)
			template_values['trans_notfound'] = trans_notfound
		
		self.response.out.write(template.render(html, template_values))
		
	def debug(self, txt):
		if not DEBUG:
			return
		
		if txt == None:
			self.response.out.write('<br />None');
			return
			
		self.response.out.write('<br />' + cgi.escape(str(txt.__class__)) + ' : ');
		if txt.__class__ == list:
			for l in txt:
				self.response.out.write('<br /> - ' + cgi.escape(l));
		else:
			self.response.out.write(cgi.escape(txt));


	

class MainPage(BasePage):
	URL = '/'
	TEMPLATE = 'index.html' 
	
	def get(self):
		BasePage.get(self)
		
		out = ''
		if DEBUG:
			for k,v in os.environ.iteritems():
				out += k + ' : ' + v + '<br>'
		
		self.render(self.TEMPLATE, env = out)		


class AboutPage(BasePage):
	URL = '/about'
	TEMPLATE = 'about.html'
	
	def get(self):
		BasePage.get(self)
		
		self.title = t('About')
		self.render(self.TEMPLATE)		
	


