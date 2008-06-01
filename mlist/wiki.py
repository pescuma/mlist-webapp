#!/usr/bin/env python
# coding=utf-8

from framework import *
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from page import *
from recaptcha.client import captcha
from trans import *
import cgi
import datetime
import os
import wikisyntax
import wsgiref.handlers



# Model #######################################################################



class Wiki(Page):
	type = 'wiki'




# View ########################################################################




class NewWiki(BaseNewPage):
	URL = '/wiki/new'
	TEMPLATE = 'wiki.new.html'
	title = t('Nova página wiki')
		
	def get(self):
		BaseNewPage.get(self)
		self.render(self.TEMPLATE, captcha=self.getCaptchaHTML())
		
	def post(self):
		BaseNewPage.post(self)
		
		form = self.getForm(Field('title', max=500), Field('private', type='boolean'))
		
		if len(form.title) <= 0:
			self.err(t('O Nome da página não pode estar em branco'))
		
		captchaError = self.getCaptchaError()
		
		if len(self.errors) > 0:
			self.render(self.TEMPLATE, form=form, captcha=self.getCaptchaHTML(captchaError))
			return
		
		wiki = Wiki()
		wiki.title = form.title
		wiki.text = form.text
		wiki.private = form.private
		wiki.author = users.get_current_user()
		wiki.put()
		
		self.redirect('/wiki/' + wiki.id())


class ViewWiki(BaseViewPage):
	URL = '/wiki/(.+)'
	TYPE = Wiki
	
	def show(self):
		if self.page.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/wiki/edit/' + self.page.id()))
		
		self.title = wikisyntax.toHTML(self.page.title, True)
		self.render('wiki.view.html')
		
	def get(self, *groups):
		BaseViewPage.get(self, *groups)
		if not self.page:
			return
		
		self.show()
		
	def post(self, *groups):
		BaseViewPage.post(self, *groups)
		if not self.page:
			return
		
		self.show()


class EditWiki(ViewWiki):
	URL = '/wiki/edit/(.+)'
	
	def renderForm(self, form):
		self.left_menus.insert(0, Menu(t('Cancel'), '/wiki/' + self.page.id()))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(self.page.title, False)
		self.render('wiki.edit.html', form=form)
	
	def show(self):
		if not self.page.isAuthor():
			ViewWiki.show(self)
			return
		
		form = Form()
		form.title = self.page.title
		form.text = self.page.text
		form.private = self.page.private
		
		self.renderForm(form)
		
	def post(self, *groups):
		BaseViewPage.post(self, *groups)
		if not self.page:
			return
		if not self.page.isAuthor():
			self.show()
			return
		
		form = self.getForm(Field('title', desc='O título', max=500, required=True), \
						    Field('private', type='boolean'))
		if len(self.errors) > 0:
			self.renderForm(form)
			return
			
		self.page.title = form.title
		self.page.text = form.text
		self.page.private = form.private
		self.page.put()
		
		self.redirect('/wiki/' + self.page.id())

