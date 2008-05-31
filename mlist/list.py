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
	
	def id(self):
		return str(self.key())
	
	def boughtDisplayableNick(self):
		if not self.boughtBy:
			return t('Anonimo')
		
		nick = self.boughtBy.nickname()
		pos = nick.rfind('@')
		if pos >= 0:
		  nick = nick[:pos] + '@...'
		return nick




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
	title = t('Nova lista')
		
	def get(self):
		BaseNewPage.get(self)
		self.render(self.TEMPLATE, captcha=self.getCaptchaHTML())
		
	def post(self):
		BaseNewPage.post(self)
		
		form = self.getForm(Field('title', max=500), Field('private', type='boolean'))
		
		in_items = self.getItemNames(form.items)
		
		if len(form.title) <= 0:
			self.err(t('O Nome da lista não pode estar em branco'))
		if len(in_items) <= 0:
			self.err(t('A lista de itens não pode estar em branco'))
		
		captchaError = self.getCaptchaError()
		
		if len(self.errors) > 0:
			self.render(self.TEMPLATE, form=form, captcha=self.getCaptchaHTML(captchaError))
			return
		
		mlist = MList()
		mlist.title = form.title
		mlist.text = form.text
		mlist.private = form.private
		mlist.author = users.get_current_user()
		mlist.put()
		
		self.addItems(mlist, in_items)
		
		self.redirect('/list/' + mlist.id())


class ViewList(BaseListPage, BasePage):
	URL = '/list/(.+)'

	def load(self, id):
		mlist = MList.load(id)
		
		if mlist and not mlist.isAuthor() and mlist.private:
			mlist = None
		
		return mlist
	
	def show(self, mlist):
#		if not users.get_current_user():
#			self.warn(cgi.escape('Você não está logado. Se você alterar um item, você não ' + \
#						'poderá desfazer isso depois. Você tem certeza que não deseja ') + '<a href="' + \
#						users.create_login_url(self.request.uri) + '">logar-se</a>?')
		
		if mlist and mlist.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/list/edit/' + mlist.id()))
		
		self.title = wikisyntax.toHTML(mlist.title, True)
		self.render('list.view.html', mlist=mlist)
		
	def get(self, *groups):
		BasePage.get(self)
		
		mlist = self.load(groups[0])
		if not mlist:
			self.error(404)
			return
		
		self.show(mlist)

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
		item = mlist.getItemById(self.form('bought'))
		if item:
			item.bought = 1
			item.boughtBy = users.get_current_user()
			item.boughtDate = datetime.datetime.now()
			item.put()
		
		item = mlist.getItemById(self.form('unbought'))
		if item and item.bought != 0:
			if not self.canUnbuy(mlist, item):
				self.err(t("Você não pode desmarcar este ítem, pois ele foi comprado por outra pessoa"))
			else:
				item.bought = 0
				item.boughtBy = None
				item.boughtDate = None
				item.put()
		
		item = mlist.getItemById(self.form('delete'))
		if item:
			if not self.canDelete(mlist, item):
				self.err(t("Apenas o criador da lista pode apagar itens"))
			else:
				item.delete()
	
	def post(self, *groups):
		BasePage.post(self)
		
		mlist = self.load(groups[0])
		if not mlist:
			self.error(404)
			return
		
		self.handlePublicChanges(mlist)
		
		self.show(mlist)


class EditList(ViewList):
	URL = '/list/edit/(.+)'
	
	def show(self, mlist):
		if not mlist.isAuthor():
			ViewList.show(self, mlist)
			return
		
		form = Form()
		form.title = mlist.title
		form.text = mlist.text
		form.private = mlist.private
		
		self.left_menus.insert(0, Menu(t('Cancel'), '/list/' + mlist.id()))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(mlist.title, False)
		self.render('list.edit.html', form=form, mlist=mlist)
	
	def post(self, *groups):
		BasePage.post(self)
		
		mlist = self.load(groups[0])
		if not mlist:
			self.error(404)
			return
		
		self.handlePublicChanges(mlist)
		
		form = self.getForm(Field('title', max=500), Field('private', type='boolean'), Field('edit', type='boolean'))
		
		if not mlist.isAuthor() or not form.edit:
			self.show(mlist)
			return
		
		if len(form.title) <= 0:
			self.err(t('O título não pode estar em branco'))
			
		if len(self.errors) > 0:
			self.render('list.edit.html', form=form, mlist=mlist)
			return
			
		mlist.title = form.title
		mlist.text = form.text
		mlist.private = form.private
		mlist.put()
		
		self.addItems(mlist, self.getItemNames(form.items))
		
		self.redirect('/list/' + mlist.id())

