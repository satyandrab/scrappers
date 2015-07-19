'''
Created on 17-Jul-2015

@author: satyandra
'''

from lxml import html
import urllib2, csv

def extract_details(url):
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://www.fastweb.com/')
    parsed_source.make_links_absolute()
    
    title = "".join(parsed_source.xpath("//h1/text()"))
    #print title
    
    provided_by = "".join(parsed_source.xpath("//p[@class='provided_by']/text()")).strip()
    #print provided_by
    
    amount = "".join(parsed_source.xpath("//div[@class='award']/p[@class='info']/text()")).strip()
    #print amount
    
    deadline = "".join(parsed_source.xpath("//div[@class='deadline']/p[@class='info']/text()")).strip()
    #print deadline
    
    description = "".join(parsed_source.xpath("//div[@class='description']/text()")).strip()
    #print description
    
    data_list = [url, title, provided_by, amount, deadline, description]
    return data_list

def extract_scholerships_url(url):
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://www.fastweb.com/')
    parsed_source.make_links_absolute()
    
    div = parsed_source.xpath("//div[@id='scholarships']")
    for scholership_url in div:
        return scholership_url.xpath(".//a/@href")

def extract_scholership_list_url(url):
    url_list = []
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://www.fastweb.com/')
    parsed_source.make_links_absolute()
    
    all_urls = parsed_source.xpath("//li/a/@href")
    for urls in all_urls:
        if '//scholarships.' in urls:
            url_list.append(urls)
    return url_list

if __name__ == '__main__':
    data_writer = csv.writer(open("fastweb_scholarship.csv", "wb"))
    data_writer.writerow(['Scholarship URL', 'Scholarship Title', 'Provided By', 'Amount', 'Deadline', 'Description'])
    
    site_map_url = 'http://www.fastweb.com/content/sitemap'
    list_of_urls = extract_scholership_list_url(site_map_url)
    for list_url in list_of_urls:
        url_list = extract_scholerships_url(list_url)
        for details_url in url_list:
            datalist = extract_details(details_url)
            print "writing data for scholership url", details_url
            data_writer.writerow([unicode(s).encode("utf-8") for s in datalist])
            print '-'*78
