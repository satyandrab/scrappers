# -*- coding: utf-8 -*-

# Scrapy settings for psychologytoday project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'psychologytoday'

SPIDER_MODULES = ['psychologytoday.spiders']
NEWSPIDER_MODULE = 'psychologytoday.spiders'


LOG_STDOUT = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent

LOG_FILE = 'debug_log.txt'

#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
USER_AGENT = 'Opera/9.80 (X11; Linux x86_64) Presto/2.12.388 Version/12.16'

DOWNLOAD_DELAY = 2
