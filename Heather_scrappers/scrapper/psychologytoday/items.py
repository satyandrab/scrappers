# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class myItem(scrapy.Item):
    name                    = scrapy.Field()
    gender                  = scrapy.Field()
    photo                   = scrapy.Field()
    region                  = scrapy.Field()
    zipCode                 = scrapy.Field()
    email                   = scrapy.Field()
    occupation              = scrapy.Field()
    free                    = scrapy.Field()
    specialties             = scrapy.Field()
    fields                  = scrapy.Field()
    clientFocus             = scrapy.Field()
    programTreatment        = scrapy.Field()
    finance1                = scrapy.Field()
    finance2                = scrapy.Field()
    insurance               = scrapy.Field()
    qualification           = scrapy.Field()
    modified                = scrapy.Field()
    profile                 = scrapy.Field()
    buttons                 = scrapy.Field()
    profileId               = scrapy.Field()
    about                   = scrapy.Field()
