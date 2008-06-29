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



class ToDo(Page):
	type = 'todo'
	
	def __items(self):
		return list(self.todoitem_set.order('order'))
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



class ToDoItem(db.Model):
	text = db.StringProperty(multiline=False)
	done = db.BooleanProperty()
	doneBy = db.UserProperty()
	doneDate = db.DateTimeProperty(auto_now_add=False)
	todo = db.Reference(ToDo)
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

	def addItems(self, todo, in_items):
		first = 0
		for item in todo.items:
			if item.order >= first:
				first = item.order + 1
				
		for text in in_items:
			item = ToDoItem()
			item.text = text
			item.done = False
			item.todo = todo
			item.order = first
			item.put()
			
			first += 1

	

class NewToDo(BaseListPage, BaseNewPage):
	URL = '/todo/new'
	TEMPLATE = 'todo.new.html'
		
	def get(self):
		BaseNewPage.get(self)
		self.title = t('Nova lista de coisas a fazer')
		self.render(self.TEMPLATE, captcha=self.getCaptchaHTML())
		
	def post(self):
		BaseNewPage.post(self)
		self.title = t('Nova lista de coisas a fazer')
		
		form = self.getForm(Field('title', max=500), Field('private', type='boolean'), \
						    Field('bkg_file', type='file'), Field('bkg_static', type='boolean'), Field('bkg_repeat', type='boolean'))
		
		in_items = self.getItemNames(form.items)
		
		if len(form.title) <= 0:
			self.err(t('O Nome da lista não pode estar em branco'))
		if len(in_items) <= 0:
			self.err(t('A lista de tarefas não pode estar em branco'))
		if form.bkg_file and form.bkg_file.content_type not in ('image/gif', 'image/png', 'image/jpeg'):
			self.err(t('A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG'))
		
		captchaError = self.getCaptchaError()
		
		if len(self.errors) > 0:
			self.render(self.TEMPLATE, form=form, captcha=self.getCaptchaHTML(captchaError))
			return
		
		todo = ToDo()
		todo.title = form.title
		todo.text = form.text
		todo.private = form.private
		todo.author = users.get_current_user()
		todo.put()
		
		self.addItems(todo, in_items)
		
		self.handleBackground(form, todo)
		
		self.redirect(todo.getURL())


class ViewToDo(BaseListPage, BaseViewPage):
	URL = '/todo/(.+)'
	TYPE = ToDo
	
	def show(self):
#		if not users.get_current_user():
#			self.warn(cgi.escape('Você não está logado. Se você alterar um item, você não ' + \
#						'poderá desfazer isso depois. Você tem certeza que não deseja ') + '<a href="' + \
#						users.create_login_url(self.request.uri) + '">logar-se</a>?')
		
		if self.page and self.page.isAuthor():
			self.left_menus.insert(0, Menu(t('Edit'), '/todo/edit/' + self.page.id()))
		
		self.title = wikisyntax.toHTML(self.page.title, True)
		self.render('todo.view.html')
		
	def get(self, *groups):
		BaseViewPage.get(self, *groups)
		if not self.page:
			return
		
		self.show()

	def canUndo(self, todo, item):
		if not item.done:
		  return False
		 
		if todo.isAuthor():
			return True
		
		if item.doneBy and item.doneBy == users.get_current_user():
			return True
		
		return False

	def canDelete(self, todo, item):
		if todo.isAuthor():
			return True
		
		return False
	
	def handlePublicChanges(self, todo):
		form = self.getForm(Field('done', type=ToDoItem), \
						    Field('undo', type=ToDoItem), \
						    Field('delete', type=ToDoItem),
						    strict = True)
		
		if form.done:
			item = form.done
			if item.done:
				self.err(t("Esta tarefa já foi realizada por outra pessoa"))
			else:
				item.done = True
				item.doneBy = users.get_current_user()
				item.doneDate = datetime.datetime.now()
				item.put()
		
		if form.undo:
			item = form.undo
			if not item.done:
				self.err(t("Você não pode desfazer esta tarefa, pois ela não foi feita ainda"))
			elif not self.canUndo(todo, item):
				self.err(t("Você não pode desfazer esta tarefa, pois ela foi feita por outra pessoa"))
			else:
				item.done = False
				item.doneBy = None
				item.doneDate = None
				item.put()
		
		if form.delete:
			item = form.delete
			if not self.canDelete(todo, item):
				self.err(t("Apenas o criador da lista pode apagar tarefas"))
			else:
				item.delete()
	
	
	def post(self, *groups):
		BaseViewPage.post(self, *groups)
		if not self.page:
			return
		
		self.handlePublicChanges(self.page)
		self.show()


class EditToDo(ViewToDo):
	URL = '/todo/edit/(.+)'
	
	def renderForm(self, form):
		self.left_menus.insert(0, Menu(t('Cancel'), '/todo/' + self.page.id()))
		self.title = t('Editando') + ' ' + wikisyntax.toHTML(self.page.title, False)
		self.render('todo.edit.html', form=form)
	
	def show(self):
		if not self.page.isAuthor():
			ViewList.show(self)
			return
		
		form = Form()
		form.title = self.page.title
		form.text = self.page.text
		form.private = self.page.private
				
		if self.page.background:
			form.bkg = self.page.background
			form.bkg_static = self.page.background.static
			form.bkg_repeat = self.page.background.repeat

		self.renderForm(form)
		
	
	def post(self, *groups):
		BaseViewPage.post(self, *groups)
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
						    Field('bkg_file', type='file'), Field('bkg_static', type='boolean'), Field('bkg_repeat', type='boolean'), \
						    Field('delete_bkg', type='boolean'))
		
		if form.delete_bkg:
			if self.page.background:
				if self.page.background.file:
					self.page.background.file.delete()
				self.page.background.delete()
				self.page.background = None
				self.page.put()
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
		self.page.private = form.private
		self.page.put()
		
		self.addItems(self.page, self.getItemNames(form.items))
	
		self.handleBackground(form)
		
		self.redirect(self.page.getURL())

