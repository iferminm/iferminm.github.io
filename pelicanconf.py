#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Israel Fermin Montilla'
SITENAME = u'/dev/isra/blog/*'
DATE_FORMAT = '%a %d %b, %Y'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Dubai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'http://twitter.com/iferminm'),
    ('LinkedIn', 'http://www.linkedin.com/profile/view?id=66587805&trk=tab_pro'),
    ('GitHub', 'https://github.com/iferminm'),
    ('Email', 'mailto:iferminmontilla@gmail.com'),
)

DEFAULT_PAGINATION = 10

# Theme setup
THEME = os.path.join(os.path.dirname(__file__), 'mymedius/')
DEFAULT_CAT = 'Blog'
MEDIUS_AUTHORS = {
    'Israel Fermín Montilla': {
        'image': 'https://dl.dropboxusercontent.com/s/1bvnowsfke4rs2k/isra.jpg',
        'description':  {
            ''' Full time husband and dad who loves technology and programming. Software Engineer @ Careem / Online Mentor @ codeinstitute.net'''
        }
    }
}
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
