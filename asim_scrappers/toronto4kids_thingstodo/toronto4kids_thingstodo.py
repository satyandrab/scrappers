#!/usr/bin/python
'''
Created on Jul 11, 2015

@author: satyandrababu
'''

import re, csv, mechanize, cookielib
import random
from lxml import html


def mechanize_br():
    version_list = ['5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0', '21.0', '22.0', '23.0',
                    '24.0', '25.0', '26.0', '27.0', '28.0', '29.0', '30.0', '31.0', '32.0', '33.0', '34.0', '35.0', '36.0', '37.0', '38.0',  '1.0',  '2.0', '3.0', '4.0']
    # print "Browser version ", (random.choice(version_list))
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(False)
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
    br.addheaders = [('User-agent', 'Mozilla/'+(random.choice(version_list))+' (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'), ('Accept', '*/*')]
    
    return br

def extract_details(url, data_writer):
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'http://www.toronto4kids.com/')
    parsed_source.make_links_absolute()
    
    category = "".join(parsed_source.xpath("//h1/text()")).strip()
    #print category
    
    data_part = parsed_source.xpath("//tr[@class='article-item']")
    for details_part in data_part:
        details_url = "".join(details_part.xpath(".//td[@class='article-image']/a/@href"))
        #print details_url
        
        title = "".join(details_part.xpath(".//h4/a/text()")).encode("utf-8").strip()
        #print title
        
        thumb_image_url = "".join(details_part.xpath(".//td[@class='article-image']/a/img/@src")).split('?')[0]
        #print thumb_image_url
    
        issue = "".join(details_part.xpath(".//td[@class='issue']/a/text()")).encode("utf-8").strip()
        #print issue
        
        summary = "".join(details_part.xpath(".//p/text()")).encode("utf-8").strip()
        #summary = unicode(summary, "utf-8")
        #print summary
        
        data_list = [url, title, details_url, category, thumb_image_url, issue, summary]
        print data_list
        data_writer.writerow(data_list)
        print '-'*78

def extract_pagination_link(url):
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'http://www.toronto4kids.com/')
    parsed_source.make_links_absolute()
    
    pagination = parsed_source.xpath("//div[@id='pager']/a/text()")[-2]
    return pagination
    
if __name__ == '__main__':
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['Category URL', 'Title', 'Details URL', 'Category', 'Image URl', 'Description'])
    
    category_list_all = ['http://www.toronto4kids.com/Article-Archive/index.php?tagID=422',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=421',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=426',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=367',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=281',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=353',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=430',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=423',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=424',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=368',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=425',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=283',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=280',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=285',
                         'http://www.toronto4kids.com/Article-Archive/index.php?tagID=284']
    
    for category in category_list_all:
        number_of_pages = extract_pagination_link(category)
        for page in range(1, int(number_of_pages)+1):
            splitted_url = category.split('tagID=')
            tag_id = splitted_url[-1]
            remaining_url = splitted_url[0]
            si = (int(page)-1)*10
            pagination_url = remaining_url+'cp='+str(page)+'&si='+str(si)+'&tagID='+tag_id
            extract_details(pagination_url, data_writer)
            print '*'*78
