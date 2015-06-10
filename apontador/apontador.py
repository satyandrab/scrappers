#!/usr/bin/python


from urllib2 import Request, urlopen, URLError
import re, math, csv, mechanize, cookielib


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
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def extract_information(url, number_of_pages, data_writer):
    for page in range(1,number_of_pages+1):
        pagination_url = url+'&page='+str(page)
        print pagination_url
        
        html_response = br.open(pagination_url)
        html_source = html_response.read()
        pagination_html = html_source.replace('\n', '').replace('\r', '')
    
        #req = Request(pagination_url)
        #response = urlopen(req)
        #pagination_html = response.read().replace('\r', '').replace('\n', '')
        
        get_details_page_url = re.findall(r'<h3 class="poi name">.*?<a href="(.*?)"', pagination_html)
        for details_url in get_details_page_url:
            extract_details(details_url, data_writer)
        
def extract_details(details_url, file_name):
    print details_url
    
    html_response = br.open(details_url)
    html_source = html_response.read()
    details_html = html_source.replace('\n', '').replace('\r', '')
    
    #req = Request(details_url)
    #response = urlopen(req)
    #details_html = response.read().replace('\r', '').replace('\n', '')
    
    try:
        phone_number = re.sub('&.*?;', '', re.findall(r'<strong itemprop="telephone".*?data-content="\((.*?)"', details_html)[0].replace(')',''))
    except:
        phone_number = ''
    #print phone_number
    
    try:
        title = re.sub('&.*?;', '', re.findall(r'<h1 class="title" itemprop="name".*?>(.*?)</h1>', details_html)[0].strip().replace('&amp;', '&'))
    except:
        title = ''
    #print title
    
    try:
        street_address = re.sub('&.*?;', '', re.sub('\s+', ' ', re.sub('<.*?>','', re.findall(r'<span itemprop="streetAddress">.*?<br>',
                                                                          details_html)[0]).replace('  ','')).strip().replace(',','-').replace('&amp;', '&'))
    except:
        street_address = ''
    #print street_address
    
    try:
        address_locality = re.sub('&.*?;', '', re.findall(r'<meta property="business:contact_data:locality" content="(.*?)" />',
                                                          details_html)[0].strip().replace('&amp;', '&'))
    except:
        address_locality = ''
    #print address_locality
    
    try:
        address_region = re.sub('&.*?;', '', re.findall(r'<meta property="business:contact_data:region" content="(.*?)" />',
                                                        details_html)[0].strip().replace('&amp;', '&'))
    except:
        address_region = ''
    #print address_region
    
    try:
        address_country = re.sub('&.*?;', '', re.findall(r'<meta property="business:contact_data:country_name" content="(.*?)" />',
                                                         details_html)[0].strip().replace('&amp;', '&'))
    except:
        address_country
    #print address_country
    
    try:
        postal_code = re.sub('&.*?;', '', re.findall(r'itemprop="postalCode">(.*?)</a>', details_html)[0].strip().replace('&amp;', '&'))
    except:
        postal_code = ''
    #print postal_code
    
    print "writing data into csv file for url.."+details_url
    print [details_url, title, phone_number, street_address, address_locality, address_region, address_country, postal_code]
    data_writer.writerow([details_url, title, phone_number, street_address, address_locality, address_region, address_country, postal_code])
    print '*'*78

def validate_url(url, data_writer):
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        html = response.read()
        try:
            items_count = re.findall(r'<span class="js-found-number">(.*?)</span>',html)[0].replace('.', '')
            number_of_pages = int(math.floor(int(items_count)/15)+1)
            print items_count +" result found on " +str(number_of_pages) +" pages"
            extract_information(url, number_of_pages, data_writer)
        except:
            raise
            print "Not able to get pages....."
        
if __name__ == "__main__":
    
    #http://www.apontador.com.br/local/search.html?q=S%C3%A3o+Jos%C3%A9+do+Rio+Preto&loc_z=S%C3%A3o+Paulo&loc=S%C3%A3o+Paulo%2C+SP&loc_y=S%C3%A3o+Paulo%2C+SP
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    #f = open('imported_data/'+csv_file_name, "wb")
    #data_writer = csv.writer(f)

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['URL', 'Title', 'Phone', 'Street Address', 'Locality', 'Region', 'Country', 'Postal Code'])
    url = raw_input('Enter search URL to extract information......\n')
    validate_url(url, data_writer)
