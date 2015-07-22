'''
Created on 22-Jul-2015

@author: satyandra
'''

from lxml import html
import urllib2, csv

def extract_details(url):
    print url
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://hulafrog.com/')
    parsed_source.make_links_absolute()
    
    title = "".join(parsed_source.xpath("//h1[@class='no_mb']/text()"))
    print title
    
    add_and_class_list = []
    address_and_classes = parsed_source.xpath("//p[@class='event_detail_entry']/text()")
    for add_and_class in address_and_classes:
        add_and_class = add_and_class.strip()
        if len(add_and_class) > 0:
            add_and_class_list.append(add_and_class)
    address = "".join(add_and_class_list[:2])
    print address
    
    classes = add_and_class_list[-2].replace('Classes:', '').strip()
    print classes
    
    camps = add_and_class_list[-1].replace('Camps:', '').strip()
    print camps
    
    class_schedule_url = "".join(parsed_source.xpath("//p[@class='event_detail_entry']/a/@href"))
    print class_schedule_url
    
if __name__ == '__main__':
    url = 'http://hulafrog.com/chandler-az/snedigar-recreation-center-chandler-75/'
    extract_details(url)