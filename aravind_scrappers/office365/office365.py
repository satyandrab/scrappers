import mechanize
import cookielib
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

def get_access(url, username, passwd):
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://outlook.office365.com')
    parsed_source.make_links_absolute()
    
    br_instance.select_form(nr = 0)
    br_instance.form['login'] = username
    br_instance.form['passwd'] = passwd
    br_instance.submit()
    
    contact_url = 'https://outlook.office365.com/owa/?realm=smu.edu#path=/people'
    br_instance = mechanize_br()
    html_response_c = br_instance.open(contact_url)
    html_source_c = html_response_c.read()
    result_c = html_source_c.replace('\n', '').replace('\r', '')
    #parsed_source = html.fromstring(result, 'https://outlook.office365.com')
    #parsed_source.make_links_absolute()
    
    f = open('html.html', 'wb')
    f.write(result_c)
    

if __name__ == "__main__":
    username = 'avenkatarama@smu.edu'
    passwd = 'Buy1Teach1$'
    url = 'https://login.microsoftonline.com/'
    get_access(url, username, passwd)