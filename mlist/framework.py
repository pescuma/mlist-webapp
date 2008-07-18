#!/usr/bin/env python
# coding=utf-8

from getimageinfo import *
from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from recaptcha.client import captcha
from trans import *
import cgi
import datetime
import os
import wikisyntax
import wsgiref.handlers


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
	desc = ''
	type = 'text'
	max = None
	required = False
	cls = None
	
	def __init__(self, name, **keywords):
		self.name = name
		for kw in keywords.keys():
			setattr(self, kw, keywords[kw])

class Form:
	pass

class FormFile:
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
		if not os.environ.has_key('HTTP_ACCEPT_LANGUAGE'):
			return []
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
		val = self.request.POST.get(fieldName, None)
		if not val is None and hasattr(val, 'filename') and val.filename:
			file = FormFile()
			file.file_name = val.filename
			file.file_data = val.file.read()
			if len(file.file_data) > 10 * 1024 * 1024:
				self.err('Os arquivos devem possuir no máximo 10MB')
				return None
			file.content_type, file.width, file.height = getImageInfo(file.file_data)
			return file
		else:
			return self.request.get(fieldName).strip(' \t\r\n')
		
	def formField(self, fieldName, fieldType):
		val = self.form(fieldName)
		
		if hasattr(val, 'file_name') and fieldType != 'file':
			val = ''
			
		if fieldType == 'file':
			if hasattr(val, 'file_name'):
				return val
			else:
				return None
		elif fieldType == 'boolean':
			if val:
				return bool(val)
			else:
				return False
		elif fieldType == 'text' or fieldType == '':
			if val:
				return val
			else:
				return ''
		elif getattr(fieldType, 'load') and callable(getattr(fieldType, 'load')):
			if val:
				return fieldType.load(val)
			else:
				return None
		
		return val
	
	def getForm(self, *props, **keywords):
		fields = dict()
		for prop in props:
			fields[prop.name] = prop
			
		form = Form()
		for field in props:
			val = self.formField(field.name, field.type)
			if field.max:
				val = val[:field.max]
			setattr(form, field.name, val)
		
		if not keywords.has_key('strict') or not keywords['strict']:
			for name in self.request.POST:
				val = self.request.POST.get(name)
				if hasattr(form, name):
					continue
				setattr(form, name, self.form(name))
		
		# Validate
		for field in props:
			if field.required and not getattr(form, field.name):
				self.err(t('%s não pode estar em branco') % field.desc)
		
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
			self.response.out.write(cgi.escape(str(txt)));


	

class MainPage(BasePage):
	URL = '/'
	TEMPLATE = 'index.html' 
	
	def get(self):
		BasePage.get(self)
		
		out = ''
		if DEBUG:
			for k, v in os.environ.iteritems():
				out += k + ' : ' + v + '<br>'
		
		self.render(self.TEMPLATE, env = out)		


class AboutPage(BasePage):
	URL = '/about'
	TEMPLATE = 'about.html'
	
	def get(self):
		BasePage.get(self)
		
		self.title = t('About')
		self.render(self.TEMPLATE)		
	


