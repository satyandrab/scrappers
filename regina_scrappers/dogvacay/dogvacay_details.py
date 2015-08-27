'''
Created on 13-Aug-2015

@author: satyandra
'''

import re, csv, mechanize, cookielib
import random
from lxml import html
import datetime, time


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

def extract_details(url):
    try:
        time.sleep(0)
        br_instance = mechanize_br()
        html_response = br_instance.open(url)
        html_source = html_response.read()
        result = html_source.replace('\n', '').replace('\r', '')
        parsed_source = html.fromstring(result, 'https://dogvacay.com/')
        parsed_source.make_links_absolute()
        
        unique_url = url
        #print unique_url
        
        title = "".join(parsed_source.xpath("//h1/text()")).strip()
        #print title
        
        review_count = "".join(parsed_source.xpath("//span[@itemprop='reviewCount']/text()")).strip()
        #print review_count
        
        zip_code = "".join(parsed_source.xpath("//span[@itemprop='postalCode']/text()")).strip()
        #print zip_code
        
        list_price = "".join(parsed_source.xpath("//span[contains(text(), 'Dog Boarding Rate')]/following-sibling::span/b/text()")).strip()
        #print list_price
        
        date_list = [unique_url, title, review_count, zip_code, list_price]
        return date_list
    except:
        return None

if __name__ == '__main__':
    
    date = datetime.date.today().strftime("%B %d, %Y")
    data_writer = csv.writer(open('dogvacay '+date+'.csv', 'wb'))
    #data_writer.writerow(['URL', 'Title', '# of Guest Reviews', 'Zip Code', 'List Price'])
    
    data_reader = open('dogvacay August 20, 2015.csv - dogvacay August 20, 2015.csv', 'rb')
    for data_url in data_reader:
        if '""' in data_url:
            list1 = data_url.split('""')[0]
            list2 = data_url.split('""')[1].replace(',', '')
            list3 = data_url.split('""')[2]
            list = list1+list2+list3
            data_list_t = [x.strip() for x in list.replace('"', '').split(',')]
        else:
            data_list_t = [x.strip() for x in data_url.split(',')]
        print data_list_t
        data_writer.writerow(data_list_t)
        print '+'*78
    
    """
    
    url_file_w = open('url.txt', 'ab')
    
    date = datetime.date.today().strftime("%B %d, %Y")
    data_writer = csv.writer(open('dogvacay '+date+'.csv', 'ab'))
    #data_writer.writerow(['URL', 'Title', '# of Guest Reviews', 'Zip Code', 'List Price'])
    
    data_reader = csv.reader((open('dogvacay url August 17, 2015.csv', 'rb')))
    for data_url in data_reader:
        detail_url = data_url[0]
        print detail_url
        open_file = open('url.txt', 'rb')
        url_list = open_file.readlines()
        if detail_url+'\n' in url_list:
            print "Passing url"
            pass
        else:
            data = extract_details(detail_url)
            if data is not None:
                print "Writing data for url", detail_url
                print data
                data_writer.writerow([unicode(s).encode("utf-8") for s in data])
                url_file_w.write(str(detail_url))
                url_file_w.write('\n')
        print '+'*78
    """
    
