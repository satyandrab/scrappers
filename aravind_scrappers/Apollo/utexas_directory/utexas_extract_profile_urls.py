'''
Created on 29-Jul-2015

@author: Laxmi
'''
from lxml import html
import mechanize, cookielib, random, re, csv, sys
import time

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

def extract_profile_url(url, url_file_writer):
    time.sleep(30)
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read().replace('\n', '').replace('\r', '')
    #parsed_source = html.fromstring(html_source, 'https://www.utexas.edu/')
    #parsed_source.make_links_absolute()

    profile_urls = re.findall(r'<a href="(index.php\?q=.*?)">.*?<p class="dir_info">(.*?)</p></li>', html_source)
    for profile_url in profile_urls:
        p_url = 'https://www.utexas.edu/directory/'+profile_url[0].replace('&amp;', '&')
        p_affliation = profile_url[1].strip()
        print "writing in urls file for ", p_url
        url_file_writer.writerow([p_url, p_affliation])

if __name__ == '__main__':
    url_file_writer = csv.writer(open('extracted_urls_1.csv', 'wb'))
    
    last_names = open('last_names.txt', 'rb').readlines()
    for last_name in last_names:
        l_name = last_name.lower().strip()
        search_url = 'https://www.utexas.edu/directory/index.php?q='+str(l_name)+'&scope=all&submit=Search'
        extract_profile_url(search_url, url_file_writer)
        print '*'*78