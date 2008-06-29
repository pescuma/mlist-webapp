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
import urllib



class File(db.Model):
	name = db.StringProperty(multiline=False)
	content = db.BlobProperty()
	author = db.UserProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	contentType = db.StringProperty(multiline=False)
	width = db.IntegerProperty()
	height = db.IntegerProperty()

	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)
	
	def id(self):
		return str(self.key())

	def isAuthor(self):
		return self.author and self.author == users.get_current_user()



class Background(db.Model):
	file = db.Reference(File)
	static = db.BooleanProperty()
	repeat = db.BooleanProperty()
	
	def getURL(self):
		return self.file.getURL()



class Page(db.Model):
	title = db.StringProperty(multiline=False)
	text = db.TextProperty()
	author = db.UserProperty()
	dateCreated = db.DateTimeProperty(auto_now_add=True)
	private = db.BooleanProperty()
	background = db.Reference(Background)
	
	def __comments(self):
		return list(self.comment_set.order('date'))
	comments = property(fget=__comments)
	
	def __attachments(self):
		return list(self.attachment_set.order('date'))
	attachments = property(fget=__attachments)

	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)
	
	def id(self):
		return str(self.key())
		
	def isAuthor(self):
		return self.author and self.author == users.get_current_user()
	
	def displayableType(self):
		if self.type == 'list':
			return t('Lista de compras')
		elif self.type == 'wiki':
			return t('Página wiki')
		elif self.type == 'counter':
			return t('Counter')
		elif self.type == 'todo':
			return t('Lista de coisas a fazer')
	
	def getURL(self):
		return '/' + self.type + '/' + self.id()


class Comment(db.Model):
	text = db.TextProperty()
	author = db.UserProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	page = db.Reference(Page)

	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)
	
	def id(self):
		return str(self.key())

	def isAuthor(self):
		return self.author and self.author == users.get_current_user()


class Attachment(File):
	page = db.Reference(Page)
	
	def getURL(self):
		return '/file/' + self.page.id() + '/' + self.name




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

	def handleBackground(self, form, page):
		if form.bkg_file:
			file = Attachment()
			file.name = form.bkg_file.file_name
			file.content = form.bkg_file.file_data
			file.contentType = form.bkg_file.content_type
			file.width = form.bkg_file.width
			file.height = form.bkg_file.height
			file.author = users.get_current_user()
			file.page = page
			file.put()
			
			bkg = Background()
			bkg.file = file
			bkg.static = form.bkg_static
			bkg.repeat = form.bkg_repeat
			bkg.put()
			
			page.background = bkg
			page.put()


class BaseViewPage(BasePage):
	TYPE = Page
	page = None
	
	def load(self, TYPE, id):
		page = TYPE.load(id)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		if not page:
			self.error(404)

		return page

	def get(self, *groups):
		BasePage.get(self)
		self.page = self.load(self.TYPE, groups[0])
		
		
	def post(self, *groups):
		BasePage.post(self)
		self.page = self.load(self.TYPE, groups[0])
		if not self.page:
			return
		
		text = self.form('addCommentText')
		if text:
			comment = Comment()
			comment.text = text
			comment.author = users.get_current_user()
			comment.page = self.page
			comment.put()
		
		id = self.form('removeCommentId')
		if id:
			comment = Comment.load(id)
			if comment:
				if not comment.isAuthor() and not self.page.isAuthor():
					self.err(t("Apenas o criador de um comentário pode apagá-lo"))
				else:
					comment.delete()
		
	def render(self, html, **keywords):
		keywords['page'] = self.page
		BasePage.render(self, html, **keywords)
		
	def handleBackground(self, form):
		if form.bkg_file:
			if self.page.background and self.page.background.file:
				file = self.page.background.file
			else:
				file = Attachment()
			file.name = form.bkg_file.file_name
			file.content = form.bkg_file.file_data
			file.contentType = form.bkg_file.content_type
			file.width = form.bkg_file.width
			file.height = form.bkg_file.height
			file.author = users.get_current_user()
			file.page = self.page
			file.put()
			
			if self.page.background:
				bkg = self.page.background
			else:
				bkg = Background()
			bkg.file = file
			bkg.static = form.bkg_static
			bkg.repeat = form.bkg_repeat
			bkg.put()
			
			if not self.page.background:
				self.page.background = bkg
				self.page.put()
		
		elif self.page.background:
			bkg = self.page.background
			bkg.static = form.bkg_static
			bkg.repeat = form.bkg_repeat
			bkg.put()



class AttachmentHandler(webapp.RequestHandler):
	URL = '/file/(.+)/(.+)'

	def load(self, id):
		page = Page.load(id)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		if not page:
			self.error(404)

		return page

	def get(self, *groups):
		self.page = self.load(groups[0])
		if not self.page:
			return
		
		filename = urllib.unquote(urllib.unquote(groups[1]))
		for file in self.page.attachments:
			if file.name == filename:
				self.response.headers['Content-Type'] = str(file.contentType)
				self.response.out.write(file.content)
				return
		
		self.error(404)
