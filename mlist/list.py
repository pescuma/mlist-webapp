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



class MList(Page):
	type = 'list'
	textAfter = db.TextProperty()
	
	def __items(self):
		return list(self.mlistitem_set.order('order'))
	items = property(fget=__items)
	
	def getItemById(self, toFind):
		if toFind:
			for item in self.items:
				if item.id() == toFind:
					return item
	
	def delete(self):
		for item in self.items:
			item.delete()
		db.Model.delete(self)



class MListItem(db.Model):
	text = db.StringProperty(multiline=False)
	bought = db.IntegerProperty(default=0)
	boughtBy = db.UserProperty()
	boughtDate = db.DateTimeProperty(auto_now_add=False)
	mlist = db.Reference(MList)
	order = db.IntegerProperty()
	
	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)

	def id(self):
		return str(self.key())




# View ########################################################################



class BaseListPage:
	
	def getItemNames(self, text):
		items = []
		for item in text.split('\n'):
			item = item.lstrip(' \t\r\n-#').rstrip(' \t\r\n')[:500]
			if item:
				items.append(item)
		return items

	def addItems(self, mlist, in_items):
		first = 0
		for item in mlist.items:
			if item.order >= first:
				first = item.order + 1
				
		for text in in_items:
			item = MListItem()
			item.text = text
			item.bought = 0
			item.mlist = mlist
			item.order = first
			item.put()
			
			first += 1

	

class NewList(BaseListPage, BaseNewPage):
	URL = '/list/new'
	TEMPLATE = 'list.new.html'
		
	def get(self):
		BaseNewPage.get(self)
		self.title = t('Nova lista de compras')
		self.render(self.TEMPLATE, captcha=self.getCaptchaHTML())
		
	def post(self):
		BaseNewPage.post(self)
		self.title = t('Nova lista de compras')
		
		form = self.getForm(Field('title', desc=t('O título'), max=500, required=True), Field('private', type='boolean'), \
						    Field('bkg_file', type='file'), Field('bkg_static', type='boolean'), Field('bkg_repeat', type='boolean'))
		
		in_items = self.getItemNames(form.items)
		
		if len(in_items) <= 0:
			self.err(t('A lista de itens não pode estar em branco'))
		if form.bkg_file and form.bkg_file.content_type not in ('image/gif', 'image/png', 'image/jpeg'):
			self.err(t('A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG'))
		
		captchaError = self.getCaptchaError()
		
		if len(self.errors) > 0:
			self.render(self.TEMPLATE, form=form, captcha=self.getCaptchaHTML(captchaError))
			return
		
		mlist = MList()
		mlist.title = form.title
		mlist.text = form.text
		mlist.textAfter = form.text_after
		mlist.private = form.private
		mlist.author = users.get_current_user()
		mlist.put()
		
		self.addItems(mlist, in_items)
		
		self.handleBackground(form, mlist)
		self.handleAttachments(form, mlist)
		
		self.redirect(mlist.getURL())


class ViewList(BaseListPage, BaseViewPage):
	URL = '/list/(.+)'
	TYPE = MList
	
	def show(self):
#		if not users.get_current_user():
#			self.warn(cgi.escape('Você não está logado. Se você alterar um item, você não ' + \
#						'poderá desfazer isso depois. Você tem certeza que não deseja ') + '<a href="' + \
#						users.create_login_url(self.request.uri) + '">logar-se</a>?')
		
		if self.page and self.page.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/list/edit/' + self.page.id()))
		
		self.title = wikisyntax.toHTML(self.page.title, True)
		self.render('list.view.html')
		
	def get(self, *groups):
		BaseViewPage.get(self, *groups)
		if not self.page:
			return
		
		self.show()

	def canUnbuy(self, mlist, item):
		if item.bought == 0:
		  return False
		 
		if mlist.isAuthor():
			return True
		
		if item.boughtBy and item.boughtBy == users.get_current_user():
			return True
		
		return False

	def canDelete(self, mlist, item):
		if mlist.isAuthor():
			return True
		
		return False
	
	def handlePublicChanges(self, mlist):
		form = self.getForm(Field('bought', type=MListItem), \
						    Field('unbought', type=MListItem), \
						    Field('delete', type=MListItem), \
						    strict = True)
		
		if form.bought:
			item = form.bought
			if item.bought != 0:
				self.err(t("Este item já foi comprado por outra pessoa"))
			else:
				item.bought = 1
				item.boughtBy = users.get_current_user()
				item.boughtDate = datetime.datetime.now()
				item.put()
		
		if form.unbought:
			item = form.unbought
			if item.bought == 0:
				self.err(t("Você não pode desmarcar este ítem, pois ele não foi comprado ainda"))
			elif not self.canUnbuy(mlist, item):
				self.err(t("Você não pode desmarcar este ítem, pois ele foi comprado por outra pessoa"))
			else:
				item.bought = 0
				item.boughtBy = None
				item.boughtDate = None
				item.put()
		
		if form.delete:
			item = form.delete
			if not self.canDelete(mlist, item):
				self.err(t("Apenas o criador da lista pode apagar itens"))
			else:
				item.delete()
	
	
	def post(self, *groups):
		BaseViewPage.post(self, *groups)
		if not self.page:
			return
		
		self.handlePublicChanges(self.page)
		self.show()


class EditList(ViewList):
	URL = '/list/edit/(.+)'
	
	def renderForm(self, form):
		self.left_menus.insert(0, Menu(t('Cancel'), '/list/' + self.page.id()))
		self.left_menus.insert(0, Menu(t('Salvar'), 'javascript: document.mainForm.submit();'))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(self.page.title, False)
		self.render('list.edit.html', form=form)
	
	def show(self):
		if not self.page.isAuthor():
			ViewList.show(self)
			return
		
		form = Form()
		form.title = self.page.title
		form.text = self.page.text
		form.text_after = self.page.textAfter
		form.private = self.page.private
				
		if not form.text_after:
			form.text_after = ''
		 
		if self.page.background:
			form.bkg = self.page.background
			form.bkg_static = self.page.background.static
			form.bkg_repeat = self.page.background.repeat

		self.renderForm(form)
		
	
	def post(self, *groups):
		done = BaseViewPage.post(self, *groups)
		if not self.page:
			return
		if not self.page.isAuthor():
			self.show()
			return
		
		self.handlePublicChanges(self.page)
		
		if not self.formField('edit', 'boolean'):
			self.show()
			return
		
		form = self.getForm(Field('title', desc=t('O título'), max=500, required=True), Field('private', type='boolean'), \
						  	Field('edit', type='boolean'), \
						    Field('bkg_file', type='file'), Field('bkg_static', type='boolean'), Field('bkg_repeat', type='boolean'))
		
		if done:
			form.bkg = self.page.background
			self.renderForm(form)
			return
		
		if form.bkg_file and form.bkg_file.content_type not in ('image/gif', 'image/png', 'image/jpeg'):
			self.err(t('A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG'))

		if len(self.errors) > 0:
			form.bkg = self.page.background
			self.renderForm(form)
			return
			
		self.page.title = form.title
		self.page.text = form.text
		self.page.textAfter = form.text_after
		self.page.private = form.private
		self.page.put()
		
		self.addItems(self.page, self.getItemNames(form.items))
	
		self.handleBackground(form)
		self.handleAttachments(form)
		
		self.redirect(self.page.getURL())

