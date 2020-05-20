#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://iffm.me'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

DISQUS_SITENAME = 'iferminmblog'
GOOGLE_ANALYTICS = "UA-96148260-1"