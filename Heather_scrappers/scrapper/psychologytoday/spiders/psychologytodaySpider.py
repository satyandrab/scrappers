from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from psychologytoday.items import myItem
from scrapy import log
import re
from scrapy.http.request import Request
from random import randint,sample
import os

class psychologytoday(CrawlSpider):
  name            = "psychologytoday"
  allowed_domains = ["psychologytoday.com"]
  start_urls      = ['http://therapists.psychologytoday.com/rms/prof_search.php']
  randomRun       = False

  profilesScraped = 0
  profilesMax     = 100
  maxOffset       = 500
  printHeader     = True

  csvfile         = open('profiles.csv', 'a')
  if os.stat('profiles.csv').st_size>0:
    printHeader   = False

  def to_csv(self, item):
    if self.csvfile:
      strWrite    = ''
      if self.printHeader:
        strWrite  ='id,name,gender,photo,photo_web,web_button,web_sendafriend,state,zipcode,btn_email,freeconsult,occupation,specialties,fields,clientFocus,programTreatment,fin_mincost,fin_maxcost,fin_slidescale,fin_payment,fin_insurance,qual_yrpractice,qual_school,qual_yrgrad,qual_licensenum,qual_licensestateCode,modified,yrmod\n'
        self.printHeader = False

      if not os.path.exists('profiles'):
        os.makedirs('profiles')
      with open(os.path.join('profiles', item["profileId"]+'.txt'), 'wb') as aboutFile:
        aboutFile.write('\n'.join(item["about"]).encode('utf8'))
        
      strWrite    += str(item["profileId"])+','+item ["name"].replace(',',' ')+','+str(item["gender"])+','
      if item ["photo"]:
        strWrite  += '1,'
      else:
        strWrite  += '0,'

      strWrite    += item ["profile"]+','

      if filter(lambda c: 'Website' in c,item["buttons"]):
        strWrite  += '1,'
      else:
        strWrite  += '0,'

      if filter(lambda c: 'Send to Friend' in c,item["buttons"]):
        strWrite  += '1,'
      else:
        strWrite  += '0,'
      
      strWrite    += item ["region"][0]+','+ item ["zipCode"][0]+','
      if item ["email"]:
        strWrite  += '1,'
      else:
        strWrite  += '0,'
      if item ["free"] and item ["free"] is not -1:
        strWrite  += '1,'
      else:
        strWrite  += '0,'
        
      #occupation,
      strWrite    +=';'.join(item ["occupation"]).replace(',',' ')+','
      #specialties,
      strWrite    +=';'.join(item ["specialties"]).replace(',',' ')+','
      #fields,
      strWrite    += ';'.join([x[0] + ';'.join(x[1]) for x in item ["fields"]]).replace(',',' ')+','
      #clientFocus,
      strWrite    += ';'.join([x[0] + ';'.join(x[1]) for x in item ["clientFocus"]]).replace(',',';')+','
      #programTreatment
      strWrite    += ';'.join([x[0]+':' +';'.join([y[0] +';'.join(y[1]) for y in x[1]]) for x in item ["programTreatment"]]).replace(',',' ')+','

      #fin_mincost,fin_maxcost,fin_slidescale,
      if u'Avg\xa0Cost\xa0(per\xa0session):' in item ["finance1"]:
        tmp       = [x.strip() for x in item ["finance1"][u'Avg\xa0Cost\xa0(per\xa0session):'].split('-')]
        strWrite  +=tmp[0]+','
        if len(tmp)>1:
          strWrite  +=tmp[1]+','
        else:
          strWrite  +=','
      else:
        strWrite  +=',,'
      if 'Sliding Scale:' in  item ["finance1"]:
        if 'Yes' in item ["finance1"]['Sliding Scale:']:
          strWrite  +='1,'
        else:
          strWrite  +='0,'
      else:
        strWrite    +=','

      #fin_payment,
      if 'Accepted Payment Methods:' in item ["finance2"]:
        strWrite  += ';'.join(item ["finance2"]['Accepted Payment Methods:']).replace(',',' ')+','
      else:
        strWrite  += ','
        
      #fin_insurance,
      strWrite    += ';'.join(item ["insurance"]).replace(',',' ')+','
      
      #qualification
      if 'Years in Practice:' in item ["qualification"]:
        strWrite  += item ["qualification"]['Years in Practice:'][0]+','
      else:
        strWrite  += ','
      if 'School:' in item ["qualification"]:
        strWrite  += item ["qualification"]['School:'][0].replace(',',' ')+','
      else:
        strWrite  += ','
      if 'Year Graduated:' in item ["qualification"]:
        strWrite  += item ["qualification"]['Year Graduated:'][0]+','
      else:
        strWrite  += ','
      if 'License No. and State:' in item ["qualification"]:
        strWrite  += item ["qualification"]['License No. and State:'][0]+','+item ["qualification"]['License No. and State:'][1]+','
      else:
        strWrite  += ',,'

      #modified
      strWrite    += item ["modified"]+','+ item ["modified"].split(' ')[2]+'\n'
      self.csvfile.write(strWrite.encode('utf8'))

  def parse(self,response):
    states                    = response.xpath("//div[@class='row listItems'][1]//@href").extract()
    if self.randomRun:
      while self.profilesScraped < self.profilesMax:
        stateRand                 = randint(0,len(states)-1)
        startOffset               = (randint(0,self.maxOffset/20)*20)+1
        gender                    = randint(1,2)
        url                       = "http://therapists.psychologytoday.com/rms/"+states[stateRand]+'?therapist_gender='+str(gender)+'&rec_next='+str(startOffset)
        request                   = Request(url,callback=self.parse_listing)
        request.meta['profiles']  = randint(1,5)
        request.meta['gender']    = gender
        yield request

    else:
      for state in states:
        url                       = "http://therapists.psychologytoday.com/rms/"+state+'?therapist_gender=1'
        request                   = Request(url,callback=self.parse_listing)
        request.meta['gender']    = 1
        yield request
        url                       = "http://therapists.psychologytoday.com/rms/"+state+'?therapist_gender=2'
        request                   = Request(url,callback=self.parse_listing)
        request.meta['gender']    = 2
        yield request
        

  def parse_listing(self,response):
    url                         = "http://therapists.psychologytoday.com/"
    gender                      = response.meta['gender']
    results                     = response.xpath('//div[@class="result-name"]//@href').extract()
    if self.randomRun:
      profiles                  = response.meta['profiles']
      results                   = sample(results,min(profiles,len(results)))
      
    if not response.xpath('//div[@class="NoMatchingFound"]').extract():
      for res in results:
        request                 = Request(url+res,callback=self.parse_item)
        request.meta['gender']  = gender
        if(self.profilesScraped<self.profilesMax):
          yield request

      if not self.randomRun:
        for x in response.xpath("//div[@class='endresults-right']//a[@title='More Therapists' and not(contains(@class,'here'))]//@href").extract():
          request                   = Request(url+x,callback=self.parse_listing)
          request.meta['gender']    = gender
          yield request
    
  def parse_item(self, response):
    if 'is no longer listed in' not in ' '.join(response.xpath("//div[@class='pageInner']//h1//text()").extract()):

      item = myItem()
      item ["profile"]      = response.url
      item ["gender"]       = response.meta['gender']
      item ["profileId"]    = response.url.split('profid=')[1].split('&')[0]
      item ["name"]         = response.xpath("//div[@class='section profile-name']/h1/text()").extract()[0]
      item ["photo"]        = response.xpath("//div[@class='section profile-photo']//@src").extract()
      item ["region"]       = response.xpath("//div[@class='address address-rank-1']//span[@itemprop='addressRegion']/text()").extract()
      item ["zipCode"]      = response.xpath("//div[@class='address address-rank-1']//span[@itemprop='postalcode']/text()").extract()
      item ["email"]        = response.xpath("//div[@class='profile-contact clearfix']//a[contains(@class,'btn-orange')]//text()").extract()
      item ["buttons"]      = filter(lambda c: len(c.strip())>0,response.xpath("//div[@class='profile-contact clearfix']//a[not(contains(@class,'btn-orange'))]//text()").extract())
      item ["about"]        = response.xpath("string(//div[@class='section profile-personalstatement'])").extract()

      item ["occupation"]   = filter(lambda y: len(y)>0 and y!=',',[x.strip() for x in response.xpath("//div[@class='profile-title']//text()").extract()])
      item ["free"]         = response.xpath("string(//div[@class='section profile-freeinitial'])").extract()[0].find(' free ')
      item ["specialties"]  = response.xpath("//div[@class='section profile-spec_zone_2']/div[@class='spec-list clearfix']//li[@class='highlight']/text()").extract()

      fields                = [x.split('</h3>')  for x in response.xpath("//div[@class='section profile-spec_zone_2']/div[@class='spec-list clearfix']").extract()[1:]]
      fields                = [[x[0].split('<h3>')[1],re.split('<li>|">',x[1])] for x in fields]
      item ["fields"]       = [[x[0],filter(lambda c: '<' not in c,[re.split('</li>|</',y)[0] for y in x[1][1:]])] for x in fields]

      clientFocus           = [re.split('</h3>|</strong>',x) for x in response.xpath("//div[@class='section profile-spec_zone_4']/div[@class='spec-list clearfix']").extract()]
      clientFocus           = [[re.split('<h3>|<strong>',x[0])[1],re.split('</div></div>|<li>',x[1])] for x in clientFocus]
      clientFocus           = [[x[0],[y.split('</li>')[0] for y in x[1]]] for x in clientFocus]  
      item ["clientFocus"]  = [[x[0],filter(lambda y:len(y)>0 and 'div' not in y,x[1])] for x in clientFocus]

      programTreatment      = [x.split('<h2>') for x in response.xpath("//div[@class='section profile-spec_zone_1']").extract()]
      if programTreatment:
        programTreatment      = [y.split('</h2>') for y in programTreatment[0][1:]]
        programTreatment      = [[x[0], x[1].split('<h3>')[1:]] for x in programTreatment]
        programTreatment      = [[x[0], [y.split('</h3>') for y in x[1]]] for x in programTreatment]
        item ["programTreatment"] = [[x[0],[[y[0],filter(lambda c: len(c)>0 and '<' not in c and '>' not in c,re.split('<li>|</li>|">|</',y[1]))] for y in x[1]]] for x in programTreatment]
      else:
        item ["programTreatment"]=''

      finance1              = [x.split('<li>')[1:] for x in response.xpath("//div[@class='section profile-finances']//div[@class='clearfix']").extract()]
      if finance1:
        finance1            = [re.split('<strong>|</strong>|</',x)[1:3] for x in finance1[0]]
        item ["finance1"]   = dict(finance1)

      finance2              = [re.split('<strong>|</strong>',x)[1:] for x in response.xpath("//div[@class='section profile-finances']//div[@class='profile-list-comma']").extract()]
      item ["finance2"]     = dict([[x[0], filter(lambda c: '>' not in c,re.split(',|<',x[1]))]for x in finance2])

      item ["insurance"]    = filter(lambda c: len(c)>0 and '<' not in c,re.split('<li>|</li>',(''.join(response.xpath("//div[@class='section profile-finances']//div[@class='spec-list clearfix']/h3/following-sibling::div").extract()))))

      qualification         = [[re.split('<strong>|</li>',y) for y in x.split('</strong>')] for x in response.xpath("//div[@class='section profile-qualifications']//li").extract()]
      tmp = {}
      for x in qualification:
        if len(x)>1:
          tmp[x[0][1]] = x[1][0].strip().split(u'\xa0')
      item ["qualification"] = tmp

      item ["modified"]     = response.xpath("//div[@class='last-modified']//text()").extract()[0].split(':')[1].strip()
      if(self.profilesScraped<self.profilesMax or not(self.randomRun)):
        self.to_csv(item)
        self.profilesScraped += 1
      return item
