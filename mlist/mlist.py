#!/usr/bin/env python
# coding=utf-8

from framework import *
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from list import *
from recaptcha.client import captcha
from trans import *
from wiki import *
import cgi
import datetime
import os
import wikisyntax
import wsgiref.handlers


class MyStuffPage(BasePage):
	URL = '/mystuff'
	
	def show(self):
		self.title = t('My stuff')
		
		pages = []
		if not users.get_current_user():
			self.err(t('Apenas usuários logados podem ver suas páginas'))
		else:
			for p in MList.gql('WHERE author = :1 ORDER BY dateCreated DESC', users.get_current_user()):
				pages.append(p)
			for p in Wiki.gql('WHERE author = :1 ORDER BY dateCreated DESC', users.get_current_user()):
				pages.append(p)

		if len(pages) <= 0:
			pages = None
				
		self.render('mystuff.html', pages=pages)		
		
	def get(self):
		BasePage.get(self)
		
		self.show()

	def post(self):
		BasePage.post(self)
		
		page = Page.load(self.form('delete'))
		if page:
			if page.isAuthor:
				page.delete()
			else:
				self.err(t('Apenas o criador de uma página pode apagá-la'))
		
		self.show()

		
class NewPage(BaseNewPage):
	URL = '/new'
	title = t('Nova página')
		
	def get(self):
		BaseNewPage.get(self)
		self.render('new.html')

		
class ViewPage(BasePage):
	URL = '/(.+)'
	
	def load(self, id):
		page = Page.load(id)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		return page

	def get(self, *groups):
		BasePage.get(self)
		
		page = self.load(groups[0])
		if not page:
			self.error(404)
			return
		
		self.redirect('/' + page.type + '/' + page.id())

		
class EditPage(BasePage):
	URL = '/edit/(.+)'
	
	def load(self, id):
		page = Page.load(id)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		return page

	def get(self, *groups):
		BasePage.get(self)
		
		page = self.load(groups[0])
		if not page:
			self.error(404)
			return
		
		self.redirect('/' + page.type + '/edit/' + page.id())



class MListURLFormater:
	_BASE_URL = getServerURL() + '/'
	
	def handle(self, word):
		if not word.startswith(self._BASE_URL):
			return None
		
		id = word[len(self._BASE_URL):]
		if len(id) < 25 or id.find(u'/') >= 0:
			return None
		
		page = Page.load(id)
		if not page:
			return None
		
		title = wikisyntax.toHTML(page.title, True)
		if page.private and not page.isAuthor():
			return title 
		else:
			return u'<a href="' + word + '">' + title + u'</a>'
		

application = webapp.WSGIApplication([
  (MainPage.URL, MainPage),
  (AboutPage.URL, AboutPage),
  (MyStuffPage.URL, MyStuffPage),
  (NewPage.URL, NewPage),
  (NewList.URL, NewList),
  (EditList.URL, EditList),
  (ViewList.URL, ViewList),
  (NewWiki.URL, NewWiki),
  (EditWiki.URL, EditWiki),
  (ViewWiki.URL, ViewWiki),
  (EditPage.URL, EditPage),
  (ViewPage.URL, ViewPage),
], debug=DEBUG)

webapp.template.register_template_library('templatefilters')

wikisyntax.WikiParser.registerURLFormater(MListURLFormater())

def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

