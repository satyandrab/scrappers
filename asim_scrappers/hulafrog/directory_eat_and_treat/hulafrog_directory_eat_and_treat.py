'''
Created on 27-Jul-2015

@author: satyandra
'''

from lxml import html
import urllib2, csv, re

def extract_details(url):
    print url
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://hulafrog.com/')
    parsed_source.make_links_absolute()
    
    title = "".join(parsed_source.xpath("//div[@class='inner_col2_event_detail']/h1/text()"))
    #print title
    
    add_and_class_list = []
    address_and_classes = parsed_source.xpath("//p[@class='event_detail_entry']/text()")
    for add_and_class in address_and_classes:
        add_and_class = add_and_class.strip()
        if len(add_and_class) > 0:
            add_and_class_list.append(add_and_class)
    address = "".join(add_and_class_list[:2])
    if ',Classes:' in address:
        address = ''
    #print address
    
    classes = "".join(re.findall(r'Classes:(.*?)<br>', html_source)).strip()
    #print classes
    
    eats_and_treats = "".join(re.findall(r'Eats and Treats:(.*?)<br>', html_source)).strip()
    #print eats_and_treats
    
    places = "".join(re.findall(r'Places:(.*?)<br>', html_source)).strip()
    #print places
    
    birthdays = "".join(re.findall(r'Birthdays:(.*?)<br>', html_source)).strip()
    #print birthdays
    
    hours = "".join(re.findall(r'<strong><small>HOURS:&nbsp;</small></strong>(.*?)<br>', html_source)).replace("<br/>", ' || ')
    #print hours
    
    phone = "".join(re.findall(r'<strong><small>CALL:.*?</small></strong>\s*<a href="tel:(.*?)">', html_source))
    #print phone
    
    website = "".join(re.findall(r'<span class="details_print_links"><a href="(.*?)" target="blank"><strong><small>WEBSITE</small></strong></a></span>', html_source)).strip()
    #print website
    
    mail_id = "".join(re.findall(r'<a href="mailto:(.*?)\?SUBJECT=', html_source))
    #print mail_id
    
    facebook = "".join(re.findall(r'<span class="details_print_links"><a href="(https://www.facebook.com/.*?)" ', html_source))
    #print facebook
    
    description = "".join(parsed_source.xpath("//div[@id='more_details']/p/text()"))
    #print description
    
    love_rating = "".join(parsed_source.xpath("//p[@id='loved_val']/text()"))
    #print love_rating
    
    image_url = "".join(parsed_source.xpath("//img[@id='pick_photo']/@src"))
    #print image_url
    
    data_list = [url, title, address, classes, eats_and_treats, places, birthdays, hours, phone, website, mail_id, facebook, description, love_rating, image_url]
    return data_list

def extract_details_url(url):
    print url
    
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://hulafrog.com/')
    parsed_source.make_links_absolute()
    
    detail_urls = parsed_source.xpath("//h4/a/@href")
    return detail_urls
    
def extract_show_all_link(url):
    print url
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://hulafrog.com/')
    parsed_source.make_links_absolute()
    
    category_urls = parsed_source.xpath("//a[@class='cat_browse_link']/@href")
    return category_urls

def extract_city_codes(url):
    print url
    res = urllib2.urlopen(url)
    html_source = res.read()
    parsed_source = html.fromstring(html_source, 'http://hulafrog.com/')
    parsed_source.make_links_absolute()
    
    city_code_urls = parsed_source.xpath("//div[@class='panel-body']/ul/li/a/@href")
    return city_code_urls
    
if __name__ == '__main__':
    csv_file_name = 'hulafrog_directory_eats_and_treats.csv'
    
    data_writer = csv.writer(open(csv_file_name, 'wb'))
    data_writer.writerow(['URL', 'Title', 'Address', 'Classes', 'Eats and Treats', 'Places', 'Birthdays', 'Hours', 'Phone', 'Website','Mail ID', 'Facebook Link', 'Description', 'Love Rating', 'Image URL'])
    
    url = 'http://hulafrog.com/locations'
    location_link = extract_city_codes(url)
    for location_url in location_link:
        category_location_url = location_url+'/category-browse/?cat_id=7'
        show_all_link = extract_show_all_link(category_location_url)
        for category_link in show_all_link:
            details_urls = extract_details_url(category_link.replace(' ', '%20'))
            for detail_url in details_urls:
                data_list = extract_details(detail_url.replace(' ', '%20'))
                print "Writing data on CSV for URL", detail_url
                print data_list
                data_writer.writerow([unicode(s).encode("utf-8") for s in data_list])
                print '-'*78
