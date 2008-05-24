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


_DEBUG = True
_DEBUG_TRANSLATION = False



# Model #######################################################################



class MList(db.Model):
	title = db.StringProperty(multiline=False)
	description = db.TextProperty()
	author = db.UserProperty()
	dateCreated = db.DateTimeProperty(auto_now_add=True)
	private = db.BooleanProperty()
	
	def __items(self):
		return list(self.item_set.order('order'))
	
	items = property(fget=__items)
	
	
	def load(id):
		return db.get(db.Key(id))
	load = staticmethod(load)
	
	
	def id(self):
		return str(self.key())
	
	def getItemById(self, toFind):
		if toFind:
			for item in self.items:
				if item.id() == toFind:
					return item
		
	def isAuthor(self):
		return self.author and self.author == users.get_current_user()
	
	def delete(self):
		for item in self.items:
			item.delete()
		db.Model.delete(self)



class Item(db.Model):
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



class Menu:
	name = ''
	url = ''
	
	def __init__(self, name, url = ''):
		self.name = name
		self.url = url


class BasePage(webapp.RequestHandler):
	title = ''
	left_menus = []
	right_menus = []
	warnings = []
	errors = []
	infos = []
	
	def _initData(self):
		title = 'mlist'
		self.left_menus = [ Menu(t('New'), '/new') ]
		self.right_menus = []
		self.warnings = []
		self.errors = []
		self.infos = []
		
		if users.get_current_user():
			self.right_menus.append(Menu(users.get_current_user().email()))
		
		setLanguage(self._getAcceptedLanguages())
		

	def _getAcceptedLanguages(self):
		accept = os.environ['HTTP_ACCEPT_LANGUAGE']
		pos = accept.find(';')
		if pos >= 0:
			accept = accept[0:pos]
		langs = []
		for l in accept.split(','):
			l = l.strip(' \t\r\n')
			if l:
				langs.append(l)
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
	
	def render(self, html, **keywords):
		if users.get_current_user():
			self.left_menus.append(Menu(t('My lists'), '/mylists'))
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

class BaseListPage(BasePage):
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
			item = Item()
			item.text = text
			item.bought = 0
			item.mlist = mlist
			item.order = first
			item.put()
			
			first += 1
	

class MainPage(BasePage):
	def get(self):
		BasePage.get(self)
		
		self.title = 'mlist'
		self.render('index.html')		
	

class AboutPage(BasePage):
	def get(self):
		BasePage.get(self)
		
		self.title = 'mlist'
		self.render('about.html')		
	

class MyListsPage(BasePage):
	def show(self):
		self.title = t('My Lists') + ' :: mlist'
		
		if not users.get_current_user():
			self.err(t('Apenas usuários logados podem ver suas listas'))
			lists = []
		else:
			lists = MList.gql('WHERE author = :1 ORDER BY dateCreated DESC', users.get_current_user())
		
		mlists = []
		for mlist in lists:
			mlists.append(mlist)
		
		if len(mlists) <= 0:
			mlists = None
				
		self.render('mylists.html', mlists=mlists)		
		
	def get(self):
		BasePage.get(self)
		self.show()

	def post(self):
		BasePage.post(self)
		
		mlist = MList.load(self.form('delete'))
		if mlist:
			if mlist.isAuthor:
				mlist.delete()
			else:
				self.err(t('Apenas o criador de uma lista pode apagá-la'))
		
		self.show()
		

class NewList(BaseListPage):
	def createMenus(self):
		self.title = t('Nova lista') + ' :: mlist'
		
		self.left_menus = [ Menu(t('Cancel'), '/') ]
		
		if not users.get_current_user():
			self.warn(cgi.escape(t('Você não está logado. As listas criadas não poderão ' + \
						'ser editadas. Você tem certeza que não deseja')) + ' <a href="' + \
						users.create_login_url(self.request.uri) + '">' + cgi.escape(t('logar-se')) + '</a>?') 
		
	def get(self):
		BasePage.get(self)
		
		self.createMenus()
		
		if not users.get_current_user():
			captchaHTML = captcha.displayhtml('6LcG6QEAAAAAAEVUud_yg47BURDnRyqgx6F_TP4P', False)
		else:
			captchaHTML = None
			
		self.render('new.html', captcha=captchaHTML)
		
	def post(self):
		BasePage.post(self)
		
		self.createMenus()
		
		mlist = MList()
		mlist.title = self.form('title')[:500]
		mlist.description = self.form('description')
		
		if self.form('private'):
			mlist.private = True
		else: 
			mlist.private = False
		
		in_items = self.getItemNames(self.form('items'))
		
		if len(mlist.title) <= 0:
			self.err(t('O Nome da lista não pode estar em branco'))
		if len(in_items) <= 0:
			self.err(t('A lista de itens não pode estar em branco'))
		
		captchaError = None
		if not users.get_current_user():
			response = captcha.submit(self.form('recaptcha_challenge_field'), self.form('recaptcha_response_field'), \
									'6LcG6QEAAAAAALXl-GCqPWdTYKgvhZGIYtC3vLLW', os.environ['REMOTE_ADDR'])
			if not response.is_valid:
				self.err(t('O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)'))
				captchaError = response.error_code 
		
		if len(self.errors) > 0:
			if not users.get_current_user():
				captchaHTML = captcha.displayhtml('6LcG6QEAAAAAAEVUud_yg47BURDnRyqgx6F_TP4P', False, captchaError)
			else:
				captchaHTML = None
			
			items = ''
			for item in in_items:
				items = items + item + '\n'
			
			self.render('new.html', f_title=mlist.title, f_description=mlist.description, f_items=items, captcha=captchaHTML, f_private=mlist.private)
			return
		
		mlist.author = users.get_current_user()
		mlist.put()
		
		self.addItems(mlist, in_items)
		
		self.redirect('/' + mlist.id())


class ViewList(BaseListPage):

	def getId(self):
		return self.request.path[1:]

	def load(self):
		mlist = MList.load(self.getId())
		
		if mlist and not mlist.isAuthor() and mlist.private:
			mlist = None
		
		return mlist
	
	def show(self, mlist):
#		if not users.get_current_user():
#			self.warn(cgi.escape('Você não está logado. Se você alterar um item, você não ' + \
#						'poderá desfazer isso depois. Você tem certeza que não deseja ') + '<a href="' + \
#						users.create_login_url(self.request.uri) + '">logar-se</a>?')
		
		if mlist and mlist.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/edit/' + mlist.id()))
		
		self.title = wikisyntax.toHTML(mlist.title, True) + ' :: mlist'
		self.render('view.html', mlist=mlist)
		
	def get(self):
		BasePage.get(self)
		
		mlist = self.load()
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
	
	def post(self):
		BasePage.post(self)
		
		mlist = self.load()
		if not mlist:
			self.error(404)
			return
		
		self.handlePublicChanges(mlist)
		
		self.show(mlist)


class EditList(ViewList):
	
	def getId(self):
		return self.request.path[6:]

	def show(self, mlist):
		if not mlist.isAuthor():
			ViewList.show(self, mlist)
			return
		
		self.left_menus.insert(0, Menu(t('Cancel'), '/' + mlist.id()))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(mlist.title, False) + ' :: mlist'
		self.render('edit.html', mlist=mlist)
	
	def post(self):
		BasePage.post(self)
		
		mlist = self.load()
		if not mlist:
			self.error(404)
			return
		
		self.handlePublicChanges(mlist)
		
		if not mlist.isAuthor() or self.form('edit') != '1':
			self.show(mlist)
			return
		
		title = self.form('title')[:500]
		if len(title) <= 0:
			self.err(t('O título não pode estar em branco'))
		else:
			mlist.title = self.form('title')
		
		mlist.description = self.form('description')
		
		if self.form('private'):
			mlist.private = True
		else: 
			mlist.private = False
		
		mlist.put()
		
		self.addItems(mlist, self.getItemNames(self.form('items')))
		
		self.redirect('/' + mlist.id())
		

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/about', AboutPage),
  ('/mylists', MyListsPage),
  ('/new', NewList),
  ('/edit/.+', EditList),
  ('/.+', ViewList),
], debug=_DEBUG)

webapp.template.register_template_library('templatefilters')


def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

