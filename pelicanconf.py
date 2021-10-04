#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Israel Fermin Montilla'
SITENAME = u'/dev/isra/blog/*'
DATE_FORMAT = '%a %d %b, %Y'
SITEURL = '//127.0.0.1:8000'

PATH = 'content'

TIMEZONE = 'Asia/Dubai'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ATOM = 'feeds/main.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
TAG_FEED_ATOM = 'feeds/{slug}.tag.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    ('Atom', f'{SITEURL}/feeds/all.atom.xml'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'http://twitter.com/iferminm'),
    ('LinkedIn', 'http://www.linkedin.com/profile/view?id=66587805&trk=tab_pro'),
    ('GitHub', 'https://github.com/iferminm'),
    ('Email', 'mailto:ferminster@gmail.com'),
    ('Newsletter', 'http://newsletter.iffm.me')
)

DEFAULT_PAGINATION = 10
USE_FOLDER_AS_CATEGORY = True

# Theme setup
THEME = os.path.join(os.path.dirname(__file__), 'mymedius/')
DEFAULT_CAT = 'Blog'
MEDIUS_AUTHORS = {
    'Israel Fermín Montilla': {
        'image': 'https://dl.dropboxusercontent.com/s/1bvnowsfke4rs2k/isra.jpg',
        'description':  {
            ''' Full time husband and dad who loves technology and programming. Senior Software Engineer @ Careem'''
        }
    }
}
MEDIUS_CATEGORIES = {
    'Blog': {}
}

LONG_DESCRIPTION = "I'm an experienced software engineer and tech lead. I've designed system architectures and also managed implementations at dubizzle (OLX) and at my own startup previously. I'm currently a Senior Software Engineer at Careem (Uber), one of the top tech companies in the Middle East." 
LONG_DESCRIPTIONS = {
    'Israel Fermín Montilla': {
        'image': 'https://dl.dropboxusercontent.com/s/1bvnowsfke4rs2k/isra.jpg',
        'description':  {
            '''
            I'm an experienced software engineer and tech lead. I've designed system architectures and also managed implementations at dubizzle (OLX) and at my own startup previously. I'm currently a Senior Software Engineer at Careem (Uber), one of the top tech companies in the Middle East. I have limited slots for consultancy.
            '''
        }
    }
}
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
