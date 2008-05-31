#!/usr/bin/env python
# coding=utf-8

from framework import *
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from recaptcha.client import captcha
from trans import *
import cgi
import datetime
import os
import wikisyntax
import wsgiref.handlers



class Page(db.Model):
	title = db.StringProperty(multiline=False)
	text = db.TextProperty()
	author = db.UserProperty()
	dateCreated = db.DateTimeProperty(auto_now_add=True)
	private = db.BooleanProperty()
	
	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)
	
	def id(self):
		return str(self.key())
		
	def isAuthor(self):
		return self.author and self.author == users.get_current_user()
	
	def displayableType(self):
		if self.type == 'list':
			return t('List')
		elif self.type == 'wiki':
			return t('Wiki Page')
		elif self.type == 'counter':
			return t('Counter')






class BaseNewPage(BasePage):
	def createMenus(self):
		self.left_menus = [ Menu(t('Cancel'), '/') ]
		
		if not users.get_current_user():
			self.warn(cgi.escape(t('Você não está logado. As páginas criadas não poderão ' + \
						'ser editadas. Você tem certeza que não deseja')) + ' <a href="' + \
						users.create_login_url(self.request.uri) + '">' + cgi.escape(t('logar-se')) + '</a>?')
	
	def getCaptchaHTML(self, captchaError = None): 
		if not users.get_current_user():
			return captcha.displayhtml('6LcG6QEAAAAAAEVUud_yg47BURDnRyqgx6F_TP4P', False, captchaError)
		else:
			return None
	
	def getCaptchaError(self):
		captchaError = None
		if not users.get_current_user():
			response = captcha.submit(self.form('recaptcha_challenge_field'), self.form('recaptcha_response_field'), \
									'6LcG6QEAAAAAALXl-GCqPWdTYKgvhZGIYtC3vLLW', os.environ['REMOTE_ADDR'])
			if not response.is_valid:
				self.err(t('O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)'))
				captchaError = response.error_code 
		return captchaError
		
	def get(self):
		BasePage.get(self)
		self.createMenus()
		
	def post(self):
		BasePage.post(self)
		self.createMenus()
