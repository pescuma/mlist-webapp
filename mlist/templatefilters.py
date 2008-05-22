from google.appengine.ext import webapp
import wikisyntax


def wiki(value):
	return wikisyntax.toHTML(value, False)

def wikiSL(value):
	return wikisyntax.toHTML(value, True)


register = webapp.template.create_template_register()
register.filter(wiki)
register.filter(wikiSL)

