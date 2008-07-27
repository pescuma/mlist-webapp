#!/usr/bin/env python
# coding=utf-8

from framework import *
from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from list import *
from recaptcha.client import captcha
from todo import *
from trans import *
from wiki import *
from page import *
import cgi
import datetime
import os
import wikisyntax
import wsgiref.handlers


attachments = dict()


class MyStuffPage(BasePage):
	URL = '/mystuff'
	
	def show(self):
		self.title = t('My stuff')
		
		pages = []
		if not users.get_current_user():
			self.err(t('Apenas usuários logados podem ver suas páginas'))
		else:
			for p in MList.gql('WHERE author = :1', users.get_current_user()):
				pages.append(p)
			for p in Wiki.gql('WHERE author = :1', users.get_current_user()):
				pages.append(p)
			for p in ToDo.gql('WHERE author = :1', users.get_current_user()):
				pages.append(p)
				
		pages.sort(key=lambda x: x.dateCreated, reverse=True)

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
		
	def get(self):
		BaseNewPage.get(self)
		self.title = t('Nova página')
		self.render('new.html')

		
class ViewPage(BasePage):
	URL = '/(.+)'
	
	def loadByURL(self, url):
		page = Page.loadByURL(url)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		return page
	
	def load(self, id):
		page = Page.load(id)
		
		if page and not page.isAuthor() and page.private:
			page = None
		
		return page

	def get(self, *groups):
		BasePage.get(self)
		
		name = groups[0]
		
		try:
			page = self.loadByURL('/' + name)
			if not page:
				if name.find('/') < 0:
						page = self.load(name)
		except:
			page = None
			
		if page:
			if page.type == 'list':
				view = ViewList()
				view.initialize(self.request, self.response)
				view.get(page.id())
				return
			if page.type == 'wiki':
				view = ViewWiki()
				view.initialize(self.request, self.response)
				view.get(page.id())
				return
			if page.type == 'todo':
				view = ViewToDo()
				view.initialize(self.request, self.response)
				view.get(page.id())
				return
		
		self.error(404)

		
class EditPage(BasePage):
	URL = '/edit/([^/]+)'
	
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


class MListAttachementLinkHandler: 
	def createLink(self, url, text, modifiers):
		if not attachments.has_key(url):
			return None
		
		attach = attachments[url]
		url = attach.getURL() 
		
		if text:
			text = toHTML(text, True)
		else:
			text = cgi.escape(attach.getName())
		
		cls = ''
		if modifiers & wikisyntax.LEFT_ALIGN:
			cls = ' class="left"'
		elif modifiers & wikisyntax.RIGHT_ALIGN:
			cls = ' class="right"'
		
		if self._isImage(attach):
			return u'<img src="' + url + u'" alt="' + text + '"' + cls + '/>'
		
		if self._isFlash(attach):
			return u'<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab" width="' + \
		 	   	   str(attach.width) + u'" height="' + str(attach.height) + u'"' + cls + u'><param name="movie" value="' + url + u'" /><param name="quality" value="high" /><param name="wmode" value="transparent" />' + \
		 	   	   u'<embed src="' + url + u'" quality="high" width="' + str(attach.width) + u'" height="' + str(attach.height) + u'" type="application/x-shockwave-flash" wmode="transparent" pluginspage="http://www.macromedia.com/go/getflashplayer">' + \
		 	   	   u'</embed></object>'

		return u'<a href="' + url + u'"' + cls + '>' + text + '</a>'

	def _isImage(self, attach):
		return attach.contentType.startswith('image/') 

	def _isFlash(self, attach):
		return attach.contentType == 'application/x-shockwave-flash' 


def _loadByURL(url):
	page = MList.gql('WHERE url = :1', url).get()
	if page:
		return page
	
	page = Wiki.gql('WHERE url = :1', url).get()
	if page:
		return page
	
	page = ToDo.gql('WHERE url = :1', url).get()
	if page:
		return page
	
	return None

def _existByURL(url):
	if MList.gql('WHERE url = :1 LIMIT 1', url).count() > 0:
		return True
	if Wiki.gql('WHERE url = :1 LIMIT 1', url).count() > 0:
		return True
	if ToDo.gql('WHERE url = :1 LIMIT 1', url).count() > 0:
		return True
	return False

def _countByURL(url):
	count = MList.gql('WHERE url = :1 LIMIT 2', url).count()
	if count > 1:
		return count
	count += Wiki.gql('WHERE url = :1 LIMIT 2', url).count()
	if count > 1:
		return count
	count += ToDo.gql('WHERE url = :1 LIMIT 2', url).count()
	return count

Page.loadByURL = staticmethod(_loadByURL) 
Page.existByURL = staticmethod(_existByURL) 
Page.countByURL = staticmethod(_countByURL) 
		

application = webapp.WSGIApplication([
  (MainPage.URL, MainPage),
  (AboutPage.URL, AboutPage),
  (MyStuffPage.URL, MyStuffPage),
  (AttachmentHandler.URL, AttachmentHandler),
  (NewPage.URL, NewPage),
  (NewList.URL, NewList),
  (EditList.URL, EditList),
  (ViewList.URL, ViewList),
  (NewWiki.URL, NewWiki),
  (EditWiki.URL, EditWiki),
  (ViewWiki.URL, ViewWiki),
  (NewToDo.URL, NewToDo),
  (EditToDo.URL, EditToDo),
  (ViewToDo.URL, ViewToDo),
  (EditPage.URL, EditPage),
  (ViewPage.URL, ViewPage),
], debug=DEBUG)

webapp.template.register_template_library('templatefilters')

wikisyntax.WikiParser.registerURLFormater(MListURLFormater())
wikisyntax.WikiParser.registerLinkHander(MListAttachementLinkHandler())

def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

