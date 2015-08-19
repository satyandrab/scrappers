'''
Created on 28-Jul-2015

@author: Laxmi
'''
from lxml import html
import mechanize, cookielib, random, re, csv, sys
from urllib2 import Request, urlopen
import vobject
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

def extract_details(utexasEduPersonPubAffiliation, url):
    try:
        time.sleep(20)
        vcard_url = url+'&vcard'
        req = Request(vcard_url)
        response = urlopen(req)
        details_html = response.read()#.replace('\r', '').replace('\n', '')
        
        #print details_html
        #print '-'*78
        
        cn = "".join(re.findall(r'FN:(.*?)\n', details_html)).replace(',', '')
        #print cn
        
        gn = "".join(re.findall(r'\nN:(.*?)\n', details_html)).split(';')
        givenName = gn[0].replace(',', '')
        sn = gn[1].replace(',', '')
        #print givenName
        #print sn
        
        mail = "".join(re.findall(r'EMAIL;TYPE=INTERNET:(.*?)\n', details_html))
        #print mail
        
        telephoneNumber  = "".join(re.findall(r'TEL;VOICE;WORK:(.*?)\n', details_html))
        #print telephoneNumber
        
        utexasEduPersonOfficeLocation = "".join(re.findall(r'ADR;TYPE=WORK;ENCODING=QUOTED-PRINTABLE:;(.*?)\n', details_html)).replace('=0D=0A', ';').replace(',', '')
        #print utexasEduPersonOfficeLocation
        
        org = "".join(re.findall(r'ORG:(.*?)\n', details_html)).replace('=0D=0A', ';').replace(',', '')
        #print org
        
        return [utexasEduPersonPubAffiliation, cn, givenName, sn, mail, telephoneNumber, utexasEduPersonOfficeLocation, org]
        #print '-'*78
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        pass
        #raise
        #extract_details(utexasEduPersonPubAffiliation, url)

if __name__ == '__main__':
    #csv_file_name = file_name+'.csv'
    data_writer = csv.writer(open('utexas_directory.csv', 'wb'))
    data_writer.writerow(['utexasEduPersonPubAffiliation', 'cn', 'givenName', 'sn', 'mail', 'telephoneNumber', 'utexasEduPersonOfficeLocation', 'org'])
    
    urls_file = csv.reader(open('extracted_urls.csv', 'rb'))
    for p_url in urls_file:
        data_list = extract_details(p_url[1], p_url[0])
        print data_list
        if data_list:
            data_writer.writerow(data_list)
        print '*'*78
    """
    
    
    profile_url1 = 'http://www.utexas.edu/directory/advanced.php?aq%5BName%5D=adam&aq%5BCollege%2FDepartment%5D=&aq%5BTitle%5D=&aq%5BEmail%5D=&aq%5BHome+Phone%5D=&aq%5BOffice+Phone%5D=&scope=all&scope=all&i=38'
    profile_url = 'https://www.utexas.edu/directory/index.php?q=adam&scope=all&i=10'
    data_list = extract_details('faculty School of Architecture', profile_url)
    print data_list
    data_writer.writerow(data_list)
    """
    