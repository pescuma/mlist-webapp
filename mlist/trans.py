#!/usr/bin/env python
# coding=utf-8

import os

_PT_BR = {
	'New' : 'Nova',
	'Edit' : 'Editar', 
	'My lists' : 'Minhas listas',
	'About' : 'Sobre',
	'Log in' : 'Logar',
	'Log out' : 'Deslogar',
	'Bugs?' : 'Bugs?',
	'Para criar uma lista, escolha Nova na barra no topo da página.' : 'Para criar uma lista, escolha Nova na barra no topo da página.',
	'Não é necessário estar logado para criar uma nova lista, mas se isto ocorrer a lista não poderá ser editada.' : 'Não é necessário estar logado para criar uma nova lista, mas se isto ocorrer a lista não poderá ser editada.',
	'Criado por' : 'Criado por',
	'Muito obrigado a' : 'Muito obrigado a',
	'pelo ótimo conjunto de icones chamado Silk Icons, que são utilizados pelo site' : 'pelo ótimo conjunto de icones chamado Silk Icons, que são utilizados pelo site',
	'pelo CSS provido, que foi a base para o layout deste site' : 'pelo CSS provido, que foi a base para o layout deste site',
	'que hospeda o site e provê o framework que faz ele funcionar' : 'que hospeda o site e provê o framework que faz ele funcionar',
	'pelo' : 'pelo',
	'código Python' : 'código Python',
	'para usar o reCaptcha e pela explicação de como usar' : 'para usar o reCaptcha e pela explicação de como usar',
	'templates customizados do django' : 'templates customizados do django',
	'com o Google Apps Engine' : 'com o Google Apps Engine',
	'Change log' : 'Change log',
	'My Lists, captchas para usuários não logados, Wiki syntax' : 'My Lists, captchas para usuários não logados, Wiki syntax',
	'versão inicial do site' : 'versão inicial do site',   
	'Nova lista' : 'Nova lista',
	'Cancel' : 'Cancelar',
	'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja',
	'logar-se' : 'logar-se', 
	'O Nome da lista não pode estar em branco' : 'O Nome da Lista não pode estar em branco',
	'A lista de itens não pode estar em branco' : 'A lista de itens não pode estar em branco',
	'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)' : 'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)',
	'Nome da lista' : 'Nome da lista',
	'Descrição da lista' : 'Descrição da lista',
	'Itens da lista (um por linha)' : 'Itens da lista (um por linha)',
	'Outras opções' : 'Outras opções',
	'Editando' : 'Editando',  
}

_EN = {
	'New' : 'New',
	'Edit' : 'Edit', 
	'My lists' : 'My lists',
	'About' : 'About',
	'Log in' : 'Log in',
	'Log out' : 'Log out',
	'Bugs?' : 'Bugs?',  
	'Para criar uma lista, escolha Nova na barra no topo da página.' : 'To create a list, select New at the menu in top of page.',
	'Não é necessário estar logado para criar uma nova lista, mas se isto ocorrer a lista não poderá ser editada.' : 'You don\'t need to be logged in to create a new list, but if this happens the new list can\'t be edited.',  
	'Criado por' : 'Created by',
	'Muito obrigado a' : 'Thanks to',
	'pelo ótimo conjunto de icones chamado Silk Icons, que são utilizados pelo site' : 'for the great Silk Icons, used by this site',
	'pelo CSS provido, que foi a base para o layout deste site' : 'for the CSS which was used as basis for this site',
	'que hospeda o site e provê o framework que faz ele funcionar' : 'who hosts this side and provides the framework that makes it work',
	'pelo' : 'for the',
	'código Python' : 'Python code',
	'para usar o reCaptcha e pela explicação de como usar' : 'to use the reCaptcha and for the tutorial on how to use',
	'templates customizados do django' : 'django custom templates',
	'com o Google Apps Engine' : 'with Google Apps Engine',
	'Change log' : 'Change log',
	'My Lists, captchas para usuários não logados, Wiki syntax' : 'My Lists, captchas to not logged users, Wiki syntax',
	'versão inicial do site' : 'initial version', 
	'Nova lista' : 'New list',
	'Cancel' : 'Cancel',
	'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'You are not logged in. You won\'t be able to edit the lists you create. Are you sure that you don\'t want to',
	'logar-se' : 'log in', 
	'O Nome da Lista não pode estar em branco' : 'List Name can\'t be empty',
	'A lista de itens não pode estar em branco' : 'Items can\'t be empty',
	'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)' : 'The captcha at the end of page must be filled (Logged users don\'t need to do that)',
	'Nome da lista' : 'List name',
	'Descrição da lista' : 'List description',
	'Itens da lista (um por linha)' : 'List items (one per line)',
	'Outras opções' : 'Other options',
	'Editando' : 'Editing',  
}


_LANGUAGES = { 
	'pt_br' : _PT_BR, 
	'en' : _EN 
}


_lang = _LANGUAGES.keys()[0]

trans_notfound = []


def _getMatchingLanguage(langs):
	for l in langs:
		if _LANGUAGES.has_key(l):
			return l
	
	for l in langs:
		pos = l.find('_')
		if pos < 0:
			continue
		l = l[0:pos]
		if _LANGUAGES.has_key(l):
			return l
	
	return _LANGUAGES.keys()[0]

	
def setLanguage(langs):
	_lang = _getMatchingLanguage(langs).lower()
	

def t(text):
	l = _LANGUAGES[_lang]
	if l.has_key(text):
		return _LANGUAGES[_lang][text]

	trans_notfound.append("'" + text + "' : '" + text + "', ") 
	
	return text
