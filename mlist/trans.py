#!/usr/bin/env python
# coding=utf-8

import os


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
	'Nova lista de compras' : 'New list',
	'Cancel' : 'Cancel',
	'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'You are not logged in. You won\'t be able to edit the lists you create. Are you sure that you don\'t want to',
	'Nova página' : 'New Page',
	'Você não está logado. As páginas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'You are not logged in. You won\'t be able to edit the pages you create. Are you sure that you don\'t want to',
	'logar-se' : 'log in', 
	'O Nome da Lista não pode estar em branco' : 'List Name can\'t be empty',
	'A lista de itens não pode estar em branco' : 'Items can\'t be empty',
	'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)' : 'The captcha at the end of page must be filled (Logged users don\'t need to do that)',
	'Nome da lista' : 'List name',
	'Descrição da lista' : 'List description',
	'Itens da lista (um por linha)' : 'List items (one per line)',
	'Outras opções' : 'Other options',
	'Editando' : 'Editing',  
	'Cria uma nova página com uma lista de itens que podem ser marcados como comprados' : 'Creates a new page with a list of items that can be bought',
	'Nova página wiki' : 'New wiki page',
	'Cria uma nova página em formato Wiki' : 'Creates a new page in wiki format',
	'Novo contador' : 'New counter',
	'Cria uma nova página com uma lista que armazena um dado numérico coletado ao passar do tempo' : 'Creates a new that stores numeric data collected over time',
	'My stuff' : 'My stuff', 
	'Lista privada' : 'Private list',
	'(apenas o criador pode vê-la)' : '(only the owner can see it)',
	'O Nome da lista não pode estar em branco' : 'List name can\'t be empty',
	'Salvar' : 'Save',
	'Nome da página' : 'Page name',
	'%s não pode estar em branco' : '%s can\'t be empty',   
	'Você não pode desmarcar este ítem, pois ele não foi comprado ainda' : 'You can\'t unmark this item, because it was not bought yet',
	'Adicionar comentário:' : 'Add comment:',
	'Adicionar' : 'Add',
	'Comentário por' : 'Comment by',
	'em' : 'in',   
	'O título não pode estar em branco' : 'Title can\'t be empty', 
	'Página privada' : 'Private page',
	'Imagem de fundo' : 'Background',
	'Estática' : 'Static',
	'(a imagem não se meche com a página)' : '(the image don\'t move with the page)',
	'Repetida' : 'Repeat',
	'Mudar para' : 'Change to',  
	'A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG' : 'The background image have to be a GIF, PNG or JPEG',
	'Nova lista de coisas a fazer' : 'New to-do list',
	'Cria uma nova página com uma lista de tarefas a serem realizadas' : 'Creates a new page with a list of tasks to be fullfiled',
	'Tarefas (uma por linha)' : 'To-do items (one per line)', 
	'Adicionar tarefas (uma por linha)' : 'Add to-do items (one per line)', 
	'Você não pode desfazer esta tarefa, pois ela não foi feita ainda' : 'You can\'t undo this task, because it was not marked as done yet',
	'O título' : 'Title', 
	'Lista de coisas a fazer' : 'To-do list',
	'Lista de compras' : 'List',
	'Página wiki' : 'Wiki page',
	'Lista de coisas a fazer, background nas páginas' : 'To-do lists, page backgrounds',
	'Outros tipos de página (wiki), mostra links para sites como mídia (Animoto, Picasa, etc), comentários' : 'Other pages (wiki), handle media links (Animoto, Picasa, etc), comments',
	'Correção do modo de armazenamento, listas privadas, começo da tradução do site' : 'Fix for storage, private lists, start of site translation',
	'criada em' : 'created at', 
	'Anonimo' : 'Anonimous', 
	'Privacidade' : 'Privacy',
	'Link permanente' : 'Permalink',
	'Usar um link permanente' : 'Use a permalink', 
}



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
	'Nova lista de compras' : 'Nova lista de compras',
	'Cancel' : 'Cancelar',
	'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'Você não está logado. As listas criadas não poderão ser editadas. Você tem certeza que não deseja',
	'Nova página' : 'Nova página',
	'Você não está logado. As páginas criadas não poderão ser editadas. Você tem certeza que não deseja' : 'Você não está logado. As páginas criadas não poderão ser editadas. Você tem certeza que não deseja',
	'logar-se' : 'logar-se', 
	'O Nome da lista não pode estar em branco' : 'O Nome da Lista não pode estar em branco',
	'A lista de itens não pode estar em branco' : 'A lista de itens não pode estar em branco',
	'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)' : 'O captcha ao final da página deve ser preenchido (Usuários logados não precisam fazer isso)',
	'Nome da lista' : 'Nome da lista',
	'Descrição da lista' : 'Descrição da lista',
	'Itens da lista (um por linha)' : 'Itens da lista (um por linha)',
	'Outras opções' : 'Outras opções',
	'Editando' : 'Editando',  
	'Cria uma nova página com uma lista de itens que podem ser marcados como comprados' : 'Cria uma nova página com uma lista de itens que podem ser marcados como comprados',
	'Nova página wiki' : 'Nova página wiki',
	'Cria uma nova página em formato Wiki' : 'Cria uma nova página em formato Wiki',
	'Novo contador' : 'Novo contador',
	'Cria uma nova página com uma lista que armazena um dado numérico coletado ao passar do tempo' : 'Cria uma nova página com uma lista que armazena um dado numérico coletado ao passar do tempo',
	'My stuff' : 'Minhas coisas',
	'Lista privada' : 'Lista privada',
	'(apenas o criador pode vê-la)' : '(apenas o criador pode vê-la)',  
	'O Nome da lista não pode estar em branco' : 'O Nome da lista não pode estar em branco',
	'Salvar' : 'Salvar',
	'Nome da página' : 'Nome da página',
	'%s não pode estar em branco' : '%s não pode estar em branco', 
	'Você não pode desmarcar este ítem, pois ele não foi comprado ainda' : 'Você não pode desmarcar este ítem, pois ele não foi comprado ainda',
	'Adicionar comentário:' : 'Adicionar comentário:',
	'Adicionar' : 'Adicionar',
	'Comentário por' : 'Comentário por',
	'em' : 'em',   
	'O título não pode estar em branco' : 'O título não pode estar em branco', 
	'Página privada' : 'Página privada',
	'Imagem de fundo' : 'Imagem de fundo',
	'Estática' : 'Estática',
	'(a imagem não se meche com a página)' : '(a imagem não se meche com a página)',
	'Repetida' : 'Repetida', 
	'Mudar para' : 'Mudar para',
	'A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG' : 'A Imagem de Fundo deve ser um arqivo do tipo GIF, PNG ou JPEG', 
	'Nova lista de coisas a fazer' : 'Nova lista de coisas a fazer',
	'Cria uma nova página com uma lista de tarefas a serem realizadas' : 'Cria uma nova página com uma lista de tarefas a serem realizadas',
	'Tarefas (uma por linha)' : 'Tarefas (uma por linha)', 
	'Adicionar tarefas (uma por linha)' : 'Adicionar tarefas na lista (uma por linha)', 
	'Você não pode desfazer esta tarefa, pois ela não foi feita ainda' : 'Você não pode desfazer esta tarefa, pois ela não foi feita ainda',
	'O título' : 'O título', 
	'Lista de coisas a fazer' : 'Lista de coisas a fazer',
	'Lista de compras' : 'Lista de compras',
	'Página wiki' : 'Página wiki',
	'Lista de coisas a fazer, background nas páginas' : 'Lista de coisas a fazer, background nas páginas',
	'Outros tipos de página (wiki), mostra links para sites como mídia (Animoto, Picasa, etc), comentários' : 'Outros tipos de página (wiki), mostra links para sites como mídia (Animoto, Picasa, etc), comentários',
	'Correção do modo de armazenamento, listas privadas, começo da tradução do site' : 'Correção do modo de armazenamento, listas privadas, começo da tradução do site',
	'criada em' : 'criada em',
	'Anonimo' : 'Anonimo',
	'Privacidade' : 'Privacidade',
	'Link permanente' : 'Link permanente',
	'Usar um link permanente' : 'Usar um link permanente', 
}



_LANGUAGES = { 
	'pt_br' : _PT_BR, 
	'pt' : _PT_BR, 
	'en' : _EN 
}


_lang = 'pt_br'

trans_notfound = []


def _getMatchingLanguage(langs):
	for l in langs:
		if _LANGUAGES.has_key(l):
			return l
	
	for l in langs:
		pos = l.find('_')
		if pos < 0:
			continue
		l = l[:pos]
		if _LANGUAGES.has_key(l):
			return l
	
	return 'pt_br'

	
def setLanguage(langs):
	global _lang
	_lang = _getMatchingLanguage(langs).lower()
	return _lang
	

def t(text):
	l = _LANGUAGES[_lang]
	if l.has_key(text):
		return l[text]

	trans_notfound.append("'" + text + "' : '" + text + "', ") 
	
	return text

