'''
Created on 22-Jul-2015

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
    
    add_and_class_list = []
    address_and_classes = parsed_source.xpath("//p[@class='event_detail_entry']/text()")
    for add_and_class in address_and_classes:
        add_and_class = add_and_class.strip()
        if len(add_and_class) > 0:
            add_and_class_list.append(add_and_class)
    address = "".join(add_and_class_list[:2])
    #print address
    
    classes = "".join(re.findall(r'Classes:(.*?)<br>', html_source)).strip()
    #print classes
    
    camps = "".join(re.findall(r'Camps:(.*?)<br>', html_source)).strip()
    #print camps
    
    class_schedule_url = ''
    camp_schedule_url = ''
    try:
        pdf_urls = parsed_source.xpath("//p[@class='event_detail_entry']/a")
        for pdf_url in pdf_urls:
            if pdf_url.xpath(".//text()")[0] == 'CLASS SCHEDULE':
                class_schedule_url = "".join(pdf_url.xpath(".//@href"))
            elif pdf_url.xpath(".//text()")[0] == 'CAMP SCHEDULE':
                camp_schedule_url = "".join(pdf_url.xpath(".//@href"))
    except:
        class_schedule_url = ''
        camp_schedule_url = ''
    
    if len(class_schedule_url) > 0:
        class_schedule_url = class_schedule_url
    else:
        class_schedule_url = ''
        
    if len(camp_schedule_url) > 0:
        camp_schedule_url = camp_schedule_url
    else:
        camp_schedule_url = ''
    
    #print class_schedule_url
    #print camp_schedule_url
    
    hours = "".join(re.findall(r'<strong><small>HOURS:&nbsp;</small></strong>(.*?)<br>', html_source))
    #print hours
    
    registration = "".join(re.findall(r'<strong><small>REGISTRATION: </small></strong>(.*?)<br>', html_source))
    #print registration
    
    age_range = "".join(re.findall(r'<strong><small>AGE RANGE: </small></strong>(.*?)<br>', html_source))
    #print age_range
    
    cost = "".join(re.findall(r'<strong><small>COST:</small></strong>(.*?)<br>', html_source)).strip()
    #print cost
    
    phone = "".join(re.findall(r'<strong><small>CALL:.*?</small></strong>\s*<a href="tel:(.*?)">', html_source))
    #print phone
    
    website = "".join(re.findall(r'<span class="details_print_links"><a href="(.*?)" target="blank"><strong><small>WEBSITE</small></strong></a></span>', html_source)).strip()
    #print website
    
    mail_id = "".join(re.findall(r'<strong><small>EMAIL</small></strong></a><span class="print_only">\((.*?)\)</span>', html_source))
    #print mail_id
    
    description = "".join(parsed_source.xpath("//div[@id='more_details']/p/text()"))
    #print description
    
    love_rating = "".join(parsed_source.xpath("//p[@id='loved_val']/text()"))
    #print love_rating
    
    image_url = "".join(parsed_source.xpath("//img[@id='pick_photo']/@src"))
    #print image_url
    
    data_list = [url, title, address, classes, camps, class_schedule_url, camp_schedule_url, hours, registration, age_range, cost,
                 phone, website, mail_id, description, love_rating, image_url]
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
    detail_url = 'http://hulafrog.com/chandler-az/the-learning-place-preschool-queen-creek-372/'
    data_list = extract_details(detail_url)
    
    """
    csv_file_name = 'hulafrog_directory_classes.csv'
    
    data_writer = csv.writer(open(csv_file_name, 'wb'))
    data_writer.writerow(['URL', 'Title', 'Address', 'Classes', 'Camps', 'Class Schedule link', 'Camp Schedule Link', 'Hours', 'Registration', 'Age Range', 
                          'Cost', 'Phone', 'Website','Mail ID', 'Description', 'Love Rating', 'Image URL'])
    
    
    url = 'http://hulafrog.com/locations'
    location_link = extract_city_codes(url)
    for location_url in location_link:
        category_location_url = location_url+'/category-browse/?cat_id=5'
        show_all_link = extract_show_all_link(category_location_url)
        for category_link in show_all_link:
            details_urls = extract_details_url(category_link)
            for detail_url in details_urls:
                data_list = extract_details(detail_url)
                print "Writing data on CSV for URL", detail_url
                print data_list
                data_writer.writerow([unicode(s).encode("utf-8") for s in data_list])
                print '-'*78
    """