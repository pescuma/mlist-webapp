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


class ViewWiki(BasePage):
	URL = '/wiki/(.+)'

	def load(self, id):
		wiki = Wiki.load(id)
		if wiki and not wiki.isAuthor() and wiki.private:
			wiki = None
		return wiki
	
	def show(self, wiki):
		if wiki and wiki.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/wiki/edit/' + wiki.id()))
		
		self.title = wikisyntax.toHTML(wiki.title, True)
		self.render('wiki.view.html', wiki=wiki)
		
	def get(self, *groups):
		BasePage.get(self)
		
		wiki = self.load(groups[0])
		if not wiki:
			self.error(404)
			return
		
		self.show(wiki)


class EditWiki(ViewWiki):
	URL = '/wiki/edit/(.+)'
	
	def show(self, wiki):
		if not wiki.isAuthor():
			ViewWiki.show(self, wiki)
			return
		
		form = Form()
		form.title = wiki.title
		form.text = wiki.text
		form.private = wiki.private
		
		self.left_menus.insert(0, Menu(t('Cancel'), '/wiki/' + wiki.id()))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(wiki.title, False)
		self.render('wiki.edit.html', form=form, wiki=wiki)
	
	def post(self, *groups):
		ViewWiki.post(self)
		
		wiki = self.load(groups[0])
		if not wiki:
			self.error(404)
			return
		
		form = self.getForm(Field('title', max=500), Field('private', type='boolean'), Field('edit', type='boolean'))
		
		if not wiki.isAuthor() or not form.edit:
			self.show(wiki)
			return
		
		if len(form.title) <= 0:
			self.err(t('O título não pode estar em branco'))
			
		if len(self.errors) > 0:
			self.render('wiki.edit.html', form=form, wiki=wiki)
			return
			
		wiki.title = form.title
		wiki.text = form.text
		wiki.private = form.private
		wiki.put()
		
		self.redirect('/wiki/' + wiki.id())

