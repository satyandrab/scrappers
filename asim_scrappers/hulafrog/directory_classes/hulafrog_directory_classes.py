'''
Created on 22-Jul-2015

@author: satyandra
'''

import mechanize, cookielib, random
from lxml import html
import urllib2, csv

def mechanize_br():
    version_list = ['5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0', '21.0', '22.0', '23.0',
                    '24.0', '25.0', '26.0', '27.0', '28.0', '29.0', '30.0', '31.0', '32.0', '33.0', '34.0', '35.0', '36.0', '37.0', '38.0',  '1.0',  '2.0', '3.0', '4.0']
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/'+(random.choice(version_list))+' (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    return br

def extract_details(url):
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
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