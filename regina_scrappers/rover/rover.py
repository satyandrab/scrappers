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

def extract_details(url, zip_code):
    time.sleep(2)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    unique_url = url
    print unique_url
    
    title = "".join(parsed_source.xpath("//span[@itemprop='name']/text()")).strip()
    print title
    
    review_count = "".join(parsed_source.xpath("//meta[@itemprop='ratingCount']/@content")).strip()
    print review_count
    
    print zip_code
    
    list_price = "".join(parsed_source.xpath("//span[@itemprop='priceRange']/text()")[0]).strip()+' per night'
    print list_price
    
    date_list = [unique_url, title, review_count, zip_code, list_price]
    return date_list

def extract_pagination(url):
    print url
    time.sleep(2)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    items = "".join(parsed_source.xpath("//span[@class='button-meta']/strong/text()")[0]).strip()
    pages = (int(items)/15)+1
    return pages

def extract_details_url(url):
    time.sleep(2)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    url_list = []
    items_urls = parsed_source.xpath("//div[@class='sitter-card-body media-body']")
    for items_url in items_urls:
        detail_url = "".join(items_url.xpath(".//a[@class='sitter-link js-profile-link']/@href"))
        zipcode =  "".join(items_url.xpath(".//span[@class='heading-number']/text()"))
        url_list.append([detail_url, zipcode])
    return url_list
    
if __name__ == '__main__':
    #det_url = 'https://www.rover.com/members/jean-d-a-loving-home-for-paws-on-weekends/?centerlat=39.952340&service=home&maxlng=-75.1184713965&minlng=-75.2091086035&centerlng=-75.163790&apt=False&maxprice=100&zoomlevel=12&minlat=39.9070213965&maxlat=39.9976586035&hs=False&promoted=False&per_page=20&minprice=10&type=homes&refer=search'
    #extract_details(det_url, '19130')
    
    #url = 'https://www.rover.com/philadelphia--pa--dog-boarding/?person_summary=true&no_children_6_12=false&petsitusa=false&apartments=false&maxlng=&spaces_required=1&maxprice=100&apt=false&houses=false&zoomlevel=12&minlat=&radius=&doggy_day_care=false&per_page=20&senior_dog_care=false&volunteer_donor=false&injected_medication=false&has_fenced_yard=false&dog_walking=false&person_does_not_have_dogs=false&search_score_debug=false&special_needs=false&females_in_heat=false&unspayed_females=false&location=Philadelphia%2C+PA&non_smoking=false&service_type=overnight-boarding&minprice=10&has_no_children=false&start_date=&todate=&end_date=&oral_medication=false&knows_first_aid=false&more_than_one_client=false&centerlng=-75.163790&minlng=&dogs_allowed_on_furniture=false&no_children_0_5=false&user=&maxlat=&dog_preferences=&no_cats=false&medium_dogs=false&dogs_allowed_on_bed=false&min_rating=&uncrated_dogs=false&cat_care=false&no_caged_pets=false&puppy=false&non_neutered_males=false&has_house=false&person=&bathing_grooming=false&large_dogs=false&fromdate=&giant_dogs=false&hs=false&centerlat=39.952340&promoted=false&small_dogs=false&page=1&apse=false'
    #extract_details_url(url)
    
    date = datetime.date.today().strftime("%B %d, %Y")
    data_writer = csv.writer(open('rover '+date+'.csv', 'wb'))
    data_writer.writerow(['URL', 'Title', '# of Guest Reviews', 'Zip Code', 'List Price'])
    
    category_url = 'https://www.rover.com/philadelphia--pa--dog-boarding/?person_summary=true&no_children_6_12=false&petsitusa=false&apartments=false&maxlng=&spaces_required=1&maxprice=100&apt=false&houses=false&zoomlevel=12&minlat=&radius=&doggy_day_care=false&per_page=20&senior_dog_care=false&volunteer_donor=false&injected_medication=false&has_fenced_yard=false&dog_walking=false&person_does_not_have_dogs=false&search_score_debug=false&special_needs=false&females_in_heat=false&unspayed_females=false&location=Philadelphia%2C+PA&non_smoking=false&service_type=overnight-boarding&minprice=10&has_no_children=false&start_date=&todate=&end_date=&oral_medication=false&knows_first_aid=false&more_than_one_client=false&centerlng=-75.163790&minlng=&dogs_allowed_on_furniture=false&no_children_0_5=false&user=&maxlat=&dog_preferences=&no_cats=false&medium_dogs=false&dogs_allowed_on_bed=false&min_rating=&uncrated_dogs=false&cat_care=false&no_caged_pets=false&puppy=false&non_neutered_males=false&has_house=false&person=&bathing_grooming=false&large_dogs=false&fromdate=&giant_dogs=false&hs=false&centerlat=39.952340&promoted=false&small_dogs=false&apse=false'
    for page in range(1, 21):
        page_url = category_url+'&page='+str(page)
        detail_urls = extract_details_url(page_url)
        for detail_url in detail_urls:
            detail_url_t = detail_url[0]
            zipcode = detail_url[1]
            data = extract_details(detail_url_t, zipcode)
            print "Writing data for url", detail_url
            print data
            data_writer.writerow([unicode(s).encode("utf-8") for s in data])
            print '*'*78
