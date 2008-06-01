#!/usr/bin/env python
# coding=utf-8

import unittest
from wikisyntax import * 

class WikiSyntaxTestCase(unittest.TestCase):
	def runTest(self):
		self.assertEquals(u'<p>a</p>', toHTML(u'a'))
		self.assertEquals(u'a', toHTML(u'a', True))
		self.assertEquals(u'<p>ab</p>', toHTML(u'ab'))
		self.assertEquals(u'ab', toHTML(u'ab', True))
		self.assertEquals(u'<p>ab cd</p>', toHTML(u'ab cd'))
		self.assertEquals(u'ab cd', toHTML(u'ab cd', True))
		self.assertEquals(u'<p>ab cd</p>', toHTML(u'ab  cd'))
		self.assertEquals(u'ab cd', toHTML(u'ab  cd', True))
		self.assertEquals(u'<p>ab cd</p>', toHTML(u'ab\rcd'))
		self.assertEquals(u'ab cd', toHTML(u'ab\rcd', True))
		self.assertEquals(u'<p>ab cd</p>', toHTML(u'ab\ncd'))
		self.assertEquals(u'ab cd', toHTML(u'ab\ncd', True))
		self.assertEquals(u'<p>ab cd</p>', toHTML(u'ab\tcd'))
		self.assertEquals(u'ab cd', toHTML(u'ab\tcd', True))
		self.assertEquals(u'<p>abc</p>', toHTML(u'abc'))
		self.assertEquals(u'abc', toHTML(u'abc', True))
		self.assertEquals(u'<p>a/b/c</p>', toHTML(u'a/b/c'))
		self.assertEquals(u'a/b/c', toHTML(u'a/b/c', True))
		self.assertEquals(u'<p>a*b*c</p>', toHTML(u'a*b*c'))
		self.assertEquals(u'a*b*c', toHTML(u'a*b*c', True))
		self.assertEquals(u'<p>a_b_c</p>', toHTML(u'a_b_c'))
		self.assertEquals(u'a_b_c', toHTML(u'a_b_c', True))
		self.assertEquals(u'<p>a^b^c</p>', toHTML(u'a^b^c'))
		self.assertEquals(u'a^b^c', toHTML(u'a^b^c', True))
		self.assertEquals(u'<p>a~b~c</p>', toHTML(u'a~b~c'))
		self.assertEquals(u'a~b~c', toHTML(u'a~b~c', True))
		self.assertEquals(u'<p>a,,b,,c</p>', toHTML(u'a,,b,,c'))
		self.assertEquals(u'a,,b,,c', toHTML(u'a,,b,,c', True))
		self.assertEquals(u'<p>a <i>b</i> c</p>', toHTML(u'a /b/ c'))
		self.assertEquals(u'a <i>b</i> c', toHTML(u'a /b/ c', True))
		self.assertEquals(u'<p>a <b>b</b> c</p>', toHTML(u'a *b* c'))
		self.assertEquals(u'a <b>b</b> c', toHTML(u'a *b* c', True))
		self.assertEquals(u'<p>a <u>b</u> c</p>', toHTML(u'a _b_ c'))
		self.assertEquals(u'a <u>b</u> c', toHTML(u'a _b_ c', True))
		self.assertEquals(u'<p>a <sup>b</sup> c</p>', toHTML(u'a ^b^ c'))
		self.assertEquals(u'a <sup>b</sup> c', toHTML(u'a ^b^ c', True))
		self.assertEquals(u'<p>a <del>b</del> c</p>', toHTML(u'a ~b~ c'))
		self.assertEquals(u'a <del>b</del> c', toHTML(u'a ~b~ c', True))
		self.assertEquals(u'<p>a <sub>b</sub> c</p>', toHTML(u'a ,,b,, c'))
		self.assertEquals(u'a <sub>b</sub> c', toHTML(u'a ,,b,, c', True))
		self.assertEquals(u'<p>a <i>b</i> c</p>', toHTML(u'a  /b/  c'))
		self.assertEquals(u'a <i>b</i> c', toHTML(u'a  /b/  c', True))
		self.assertEquals(u'<p>a <b>b</b> c</p>', toHTML(u'a  *b*  c'))
		self.assertEquals(u'a <b>b</b> c', toHTML(u'a  *b*  c', True))
		self.assertEquals(u'<p>a <u>b</u> c</p>', toHTML(u'a  _b_  c'))
		self.assertEquals(u'a <u>b</u> c', toHTML(u'a  _b_  c', True))
		self.assertEquals(u'<p>a <sup>b</sup> c</p>', toHTML(u'a  ^b^  c'))
		self.assertEquals(u'a <sup>b</sup> c', toHTML(u'a  ^b^  c', True))
		self.assertEquals(u'<p>a <del>b</del> c</p>', toHTML(u'a  ~b~  c'))
		self.assertEquals(u'a <del>b</del> c', toHTML(u'a  ~b~  c', True))
		self.assertEquals(u'<p>a <sub>b</sub> c</p>', toHTML(u'a  ,,b,,  c'))
		self.assertEquals(u'a <sub>b</sub> c', toHTML(u'a  ,,b,,  c', True))
		self.assertEquals(u'<p>a&gt;c</p>', toHTML(u'a>c'))
		self.assertEquals(u'a&gt;c', toHTML(u'a>c', True))
		self.assertEquals(u'<p>ahttp://a.com/a?b=Z&amp;x=%20c</p>', toHTML(u'ahttp://a.com/a?b=Z&x=%20c'))
		self.assertEquals(u'ahttp://a.com/a?b=Z&amp;x=%20c', toHTML(u'ahttp://a.com/a?b=Z&x=%20c', True))
		self.assertEquals(u'<p>a <a href="http://a.com/a?b=Z&x=%20">http://a.com/a?b=Z&amp;x=%20</a> c</p>', toHTML(u'a  http://a.com/a?b=Z&x=%20  c'))
		self.assertEquals(u'a <a href="http://a.com/a?b=Z&x=%20">http://a.com/a?b=Z&amp;x=%20</a> c', toHTML(u'a  http://a.com/a?b=Z&x=%20  c', True))
		self.assertEquals(u'<p>ahttp://a.com/a.gifc</p>', toHTML(u'ahttp://a.com/a.gifc'))
		self.assertEquals(u'ahttp://a.com/a.jpgc', toHTML(u'ahttp://a.com/a.jpgc', True))
		self.assertEquals(u'<p>a <img src="http://a.com/a.gif" /> c</p>', toHTML(u'a http://a.com/a.gif c'))
		self.assertEquals(u'a <img src="http://a.com/a.jpg" /> c', toHTML(u'a http://a.com/a.jpg c', True))
		self.assertEquals(u'<p>a b</p>', toHTML(u'a\nb'))
		self.assertEquals(u'a b', toHTML(u'a\nb', True))
		self.assertEquals(u'<p>a b</p>', toHTML(u'a\r\nb'))
		self.assertEquals(u'a b', toHTML(u'a\r\nb', True))
		self.assertEquals(u'<p>a</p><p>b</p>', toHTML(u'a\n\nb'))
		self.assertEquals(u'a b', toHTML(u'a\n\nb', True))
		self.assertEquals(u'<p>a</p><p>b</p>', toHTML(u'a\n \nb'))
		self.assertEquals(u'a b', toHTML(u'a\n \nb', True))
		self.assertEquals(u'<p>a</p><p>b</p>', toHTML(u'a \n \nb'))
		self.assertEquals(u'a b', toHTML(u'a \n \nb', True))
		self.assertEquals(u'<p>a</p><p>b</p>', toHTML(u'a\n \n b'))
		self.assertEquals(u'a b', toHTML(u'a\n \n b', True))
		self.assertEquals(u'<p>a c</p><p>b d</p>', toHTML(u'a c \n \n b d'))
		self.assertEquals(u'a c b d', toHTML(u'a c \n \n b d', True))
		self.assertEquals(u'<p>a[[]]c</p>', toHTML(u'a[[]]c'))
		self.assertEquals(u'a[[]]c', toHTML(u'a[[]]c', True))
		self.assertEquals(u'<p>a [[]] c</p>', toHTML(u'a [[]] c'))
		self.assertEquals(u'a [[]] c', toHTML(u'a [[]] c', True))
		self.assertEquals(u'<p>a [[asd]] c</p>', toHTML(u'a [[asd]] c'))
		self.assertEquals(u'a [[asd]] c', toHTML(u'a [[asd]] c', True))
		self.assertEquals(u'<p>a <a href="http://asd.com">http://asd.com</a> c</p>', toHTML(u'a [[http://asd.com]] c'))
		self.assertEquals(u'a <a href="http://asd.com">http://asd.com</a> c', toHTML(u'a [[http://asd.com]] c', True))
		self.assertEquals(u'<p>a <a href="http://asd.com">a b</a> c</p>', toHTML(u'a [[http://asd.com][a b]] c'))
		self.assertEquals(u'a <a href="http://asd.com">a b</a> c', toHTML(u'a [[http://asd.com][a b]] c', True))
		self.assertEquals(u'<p>a <a href="http://asd.com">a <i>d</i> b</a> c</p>', toHTML(u'a [[http://asd.com][a /d/ b]] c'))
		self.assertEquals(u'a <a href="http://asd.com">a <i>d</i> b</a> c', toHTML(u'a [[http://asd.com][a /d/ b]] c', True))
		self.assertEquals(u'<p>a a</p>', toHTML(u'a\na'))
		self.assertEquals(u'<p>a</p><p>a</p>', toHTML(u'a\n\na'))
		self.assertEquals(u'<p>a</p><p>a</p>', toHTML(u'a\n\n\na'))
		self.assertEquals(u'<p>a</p><br /><p>a</p>', toHTML(u'a\n\n\n\na'))
		self.assertEquals(u'<p>a</p><br /><p>a</p>', toHTML(u'a\n\n\n\n\na'))
		self.assertEquals(u'<p>a</p><br /><p>a</p>', toHTML(u'a\n\n\n\n\n\na'))
		self.assertEquals(u'<iframe align="center" src="http://www.flickr.com/slideShow/index.gne?user_id=12345678@N00&tags=foo" frameBorder="0" width="450" scrolling="no" height="300"></iframe>', toHTML(u'http://www.flickr.com/slideShow/index.gne?user_id=12345678@N00&tags=foo', True))
		self.assertEquals(u'<p><pre class="prettyprint">asf</pre></p>', toHTML(u'[code]asf[/code]'))
		self.assertEquals(u'<p>x<code class="prettyprint">asf</code>y</p>', toHTML(u'x[code]asf[/code]y'))
		self.assertEquals(u'<p><code class="prettyprint">asf</code><code class="prettyprint">xyz</code></p>', toHTML(u'[code]asf[/code][code]xyz[/code]'))
		self.assertEquals(u'<p><pre class="prettyprint">asf</pre></p><p><pre class="prettyprint">xyz</pre></p>', toHTML(u'[code]asf[/code]\n\n[code]xyz[/code]'))
		self.assertEquals(u'<p><pre name="code" class="c++">asf</pre></p>', toHTML(u'[c++]asf[/c++]'))



