'''
Created on Jul 11, 2015

@author: satyandrababu
'''
import re, csv, mechanize, cookielib
import random


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
    details_html = html_source.replace('\n', '').replace('\r', '')
    
    title = "".join(re.findall(r'<h2>(.*?)</h2>', details_html)).strip()
    #print title
    
    categories = "".join(re.findall(r'<h5>Categories</h5><ul><li>(.*?)</li></ul>', details_html)).strip()
    #print categories
    
    address = "".join(re.findall(r'<th>Address</th>.*?<td>(.*?)<br />\s*</td>', details_html)).strip().split('<br />')
    add = [x.strip() for x in address]
    address_t = ", ".join(add)
    if len(address_t) > 0:
        address_p = address_t
    else:
        address = "".join(re.findall(r'<div id="address">(.*?)<br />\s*<br />', details_html)).strip().split('<br />')
        add = [x.strip() for x in address]
        address_k = ", ".join(add)
        address_p = address_k
        
    #print address_t
    
    phone = "".join(re.findall(r'<tr>\s*<th>Phone</th><td>(.*?)</td>\s*</tr>', details_html)).strip()
    if len(phone) > 0 :
        phone = phone
    else:
        phone_t = "".join(re.findall(r'<div id="address">.*?<br />\s*<br />(.*?)</div>', details_html)).strip()
        phone = phone_t
    #print phone
    
    website = "".join(re.findall(r'<th>Website URL</th><td>\s*<a href="(.*?)"', details_html)).strip()
    #print website
    
    description = re.sub(r'<.*?>', '', "".join(re.findall(r'<div id="description">(.*?)</div>', details_html)).strip())
    #print description
    
    image = 'http://www.toronto4kids.com'+"".join(re.findall(r'<div class="gallery-thumb">.*?<img src="(.*?)".*?>', details_html))
    if image == 'http://www.toronto4kids.com':
        image = ''
    #print image
    
    data_list = [url, title, categories, address_p, phone, website, description, image]
    print data_list
    data_writer.writerow(data_list)

def extract_details_link(url):
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    details_html = html_source.replace('\n', '').replace('\r', '')
    
    details_urls = re.findall(r'<h5>\s*<span class="counter">.*?</span>\s*<a href="(http://www.toronto4kids.com/Directories/.*?)"', details_html)
    return details_urls
    
if __name__ == '__main__':
    

    
    alpha_list = ['0', '1', '2', '3', '4', '5', '6','7', '8', '9',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                  'V', 'W', 'X', 'Y', 'Z']
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['URL', 'Title', 'Categories', 'Address', 'Phone', 'Website', 'Description', 'Image URL'])
    
    category_list_all = ['http://www.toronto4kids.com/Directories/Babies-Toddlers/',
                     'http://www.toronto4kids.com/Directories/Birthdays-Parties/',
                     'http://www.toronto4kids.com/Directories/Camps/',
                     'http://www.toronto4kids.com/Directories/Childcare/',
                     'http://www.toronto4kids.com/Directories/Classes-Programs/',
                     'http://www.toronto4kids.com/Directories/Education/',
                     'http://www.toronto4kids.com/Directories/Family-Attractions/',
                     'http://www.toronto4kids.com/Directories/Restaurants/',
                     'http://www.toronto4kids.com/Directories/Services/',
                     'http://www.toronto4kids.com/Directories/Shopping/',
                     'http://www.toronto4kids.com/Directories/Support-Groups/']
    
    #category_list = ['http://www.toronto4kids.com/Directories/Babies-Toddlers/']
    for category in category_list_all:
        for alpha in alpha_list:
            alphabetical_list_url = str(category)+'index.php/alpha/'+str(alpha)+'/'
            details_urls = extract_details_link(alphabetical_list_url)
            if len(details_urls) > 0:
                for det_url in details_urls:
                    extract_details(det_url, data_writer)
                    print '-'*78
            