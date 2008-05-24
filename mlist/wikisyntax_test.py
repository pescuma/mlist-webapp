#!/usr/bin/env python
# coding=utf-8

import unittest
from wikisyntax import * 

class WikiSyntaxTestCase(unittest.TestCase):
    def runTest(self):
		assert toHTML(u'a') == '<p>a</p>'
		assert toHTML(u'a', True) == 'a'
		assert toHTML(u'ab') == '<p>ab</p>'
		assert toHTML(u'ab', True) == 'ab'
		assert toHTML(u'ab cd') == '<p>ab cd</p>'
		assert toHTML(u'ab cd', True) == 'ab cd'
		assert toHTML(u'ab  cd') == '<p>ab cd</p>'
		assert toHTML(u'ab  cd', True) == 'ab cd'
		assert toHTML(u'ab\rcd') == '<p>ab cd</p>'
		assert toHTML(u'ab\rcd', True) == 'ab cd'
		assert toHTML(u'ab\ncd') == '<p>ab cd</p>'
		assert toHTML(u'ab\ncd', True) == 'ab cd'
		assert toHTML(u'ab\tcd') == '<p>ab cd</p>'
		assert toHTML(u'ab\tcd', True) == 'ab cd'
		assert toHTML(u'abc') == '<p>abc</p>'
		assert toHTML(u'abc', True) == 'abc'
		assert toHTML(u'a/b/c') == '<p>a/b/c</p>'
		assert toHTML(u'a/b/c', True) == 'a/b/c'
		assert toHTML(u'a*b*c') == '<p>a*b*c</p>'
		assert toHTML(u'a*b*c', True) == 'a*b*c'
		assert toHTML(u'a_b_c') == '<p>a_b_c</p>'
		assert toHTML(u'a_b_c', True) == 'a_b_c'
		assert toHTML(u'a^b^c') == '<p>a^b^c</p>'
		assert toHTML(u'a^b^c', True) == 'a^b^c'
		assert toHTML(u'a~b~c') == '<p>a~b~c</p>'
		assert toHTML(u'a~b~c', True) == 'a~b~c'
		assert toHTML(u'a,,b,,c') == '<p>a,,b,,c</p>'
		assert toHTML(u'a,,b,,c', True) == 'a,,b,,c'
		assert toHTML(u'a /b/ c') == '<p>a <i>b</i> c</p>'
		assert toHTML(u'a /b/ c', True) == 'a <i>b</i> c'
		assert toHTML(u'a *b* c') == '<p>a <b>b</b> c</p>'
		assert toHTML(u'a *b* c', True) == 'a <b>b</b> c'
		assert toHTML(u'a _b_ c') == '<p>a <u>b</u> c</p>'
		assert toHTML(u'a _b_ c', True) == 'a <u>b</u> c'
		assert toHTML(u'a ^b^ c') == '<p>a <sup>b</sup> c</p>'
		assert toHTML(u'a ^b^ c', True) == 'a <sup>b</sup> c'
		assert toHTML(u'a ~b~ c') == '<p>a <del>b</del> c</p>'
		assert toHTML(u'a ~b~ c', True) == 'a <del>b</del> c'
		assert toHTML(u'a ,,b,, c') == '<p>a <sub>b</sub> c</p>'
		assert toHTML(u'a ,,b,, c', True) == 'a <sub>b</sub> c'
		assert toHTML(u'a  /b/  c') == '<p>a <i>b</i> c</p>'
		assert toHTML(u'a  /b/  c', True) == 'a <i>b</i> c'
		assert toHTML(u'a  *b*  c') == '<p>a <b>b</b> c</p>'
		assert toHTML(u'a  *b*  c', True) == 'a <b>b</b> c'
		assert toHTML(u'a  _b_  c') == '<p>a <u>b</u> c</p>'
		assert toHTML(u'a  _b_  c', True) == 'a <u>b</u> c'
		assert toHTML(u'a  ^b^  c') == '<p>a <sup>b</sup> c</p>'
		assert toHTML(u'a  ^b^  c', True) == 'a <sup>b</sup> c'
		assert toHTML(u'a  ~b~  c') == '<p>a <del>b</del> c</p>'
		assert toHTML(u'a  ~b~  c', True) == 'a <del>b</del> c'
		assert toHTML(u'a  ,,b,,  c') == '<p>a <sub>b</sub> c</p>'
		assert toHTML(u'a  ,,b,,  c', True) == 'a <sub>b</sub> c'
		assert toHTML(u'a>c') == '<p>a&gt;c</p>'
		assert toHTML(u'a>c', True) == 'a&gt;c'
		assert toHTML(u'ahttp://a.com/a?b=Z&x=%20c') == '<p>ahttp://a.com/a?b=Z&amp;x=%20c</p>'
		assert toHTML(u'ahttp://a.com/a?b=Z&x=%20c', True) == 'ahttp://a.com/a?b=Z&amp;x=%20c'
		assert toHTML(u'a  http://a.com/a?b=Z&x=%20  c') == '<p>a <a href="http://a.com/a?b=Z&x=%20">http://a.com/a?b=Z&amp;x=%20</a> c</p>'
		assert toHTML(u'a  http://a.com/a?b=Z&x=%20  c', True) == 'a <a href="http://a.com/a?b=Z&x=%20">http://a.com/a?b=Z&amp;x=%20</a> c'
		assert toHTML(u'ahttp://a.com/a.gifc') == '<p>ahttp://a.com/a.gifc</p>'
		assert toHTML(u'ahttp://a.com/a.jpgc', True) == 'ahttp://a.com/a.jpgc'
		assert toHTML(u'a http://a.com/a.gif c') == '<p>a <img src="http://a.com/a.gif" /> c</p>'
		assert toHTML(u'a http://a.com/a.jpg c', True) == 'a <img src="http://a.com/a.jpg" /> c'
		assert toHTML(u'a\nb') == '<p>a b</p>'
		assert toHTML(u'a\nb', True) == 'a b'
		assert toHTML(u'a\r\nb') == '<p>a b</p>'
		assert toHTML(u'a\r\nb', True) == 'a b'
		assert toHTML(u'a\n\nb') == '<p>a</p><p>b</p>'
		assert toHTML(u'a\n\nb', True) == 'a b'
		assert toHTML(u'a\n \nb') == '<p>a</p><p>b</p>'
		assert toHTML(u'a\n \nb', True) == 'a b'
		assert toHTML(u'a \n \nb') == '<p>a</p><p>b</p>'
		assert toHTML(u'a \n \nb', True) == 'a b'
		assert toHTML(u'a\n \n b') == '<p>a</p><p>b</p>'
		assert toHTML(u'a\n \n b', True) == 'a b'
		assert toHTML(u'a c \n \n b d') == '<p>a c</p><p>b d</p>'
		assert toHTML(u'a c \n \n b d', True) == 'a c b d'
		assert toHTML(u'a[[]]c') == '<p>a[[]]c</p>'
		assert toHTML(u'a[[]]c', True) == 'a[[]]c'
		assert toHTML(u'a [[]] c') == '<p>a [[]] c</p>'
		assert toHTML(u'a [[]] c', True) == 'a [[]] c'
		assert toHTML(u'a [[asd]] c') == '<p>a [[asd]] c</p>'
		assert toHTML(u'a [[asd]] c', True) == 'a [[asd]] c'
		assert toHTML(u'a [[http://asd.com]] c') == '<p>a <a href="http://asd.com">http://asd.com</a> c</p>'
		assert toHTML(u'a [[http://asd.com]] c', True) == 'a <a href="http://asd.com">http://asd.com</a> c'
		assert toHTML(u'a [[http://asd.com][a b]] c') == '<p>a <a href="http://asd.com">a b</a> c</p>'
		assert toHTML(u'a [[http://asd.com][a b]] c', True) == 'a <a href="http://asd.com">a b</a> c'
		assert toHTML(u'a [[http://asd.com][a /d/ b]] c') == '<p>a <a href="http://asd.com">a <i>d</i> b</a> c</p>'
		assert toHTML(u'a [[http://asd.com][a /d/ b]] c', True) == 'a <a href="http://asd.com">a <i>d</i> b</a> c'