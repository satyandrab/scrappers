#!/usr/bin/python


from urllib2 import Request, urlopen, URLError
import re, math, csv, mechanize, cookielib
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

def extract_details(details_url, file_name):
    try:
        print details_url
        br_instance = mechanize_br()
        html_response = br_instance.open(details_url)
        html_source = html_response.read()
        details_html = html_source.replace('\n', '').replace('\r', '')
        
        try:
            title = "".join(re.findall(r'<span itemprop="name">(.*?)</span>', details_html))
        except:
            title = ''
        print title
        
        try:
            phone = "".join(re.findall(r'Tel: (.*?) <', details_html))
            if len(phone) == 0:
                phone = " !! ".join(re.findall(r'Cel: (.*?) <', details_html))
        except:
            phone = ''
        print phone
        
        try:
            street_address = "".join(re.findall(r'<span itemprop="streetAddress">(.*?)</span>', details_html))
        except:
            street_address = ''
        print street_address
        
        try:
            address_locality = "".join(re.findall(r'<span itemprop="addressLocality">(.*?)</span>', details_html))
        except:
            address_locality = ''
        print address_locality
        
        try:
            address_region = "".join(re.findall(r'<span itemprop="addressRegion">(.*?)</span>', details_html))
        except:
            address_region = ''
        print address_region
        
        try:
            postal_code = "".join(re.findall(r'<span itemprop="postalCode">(.*?)</span>', details_html))
        except:
            postal_code = ''
        print postal_code
        
        print "writing data into csv file for url.."+details_url
        print [details_url, title, phone, street_address, address_locality, address_region, postal_code]
        data_writer.writerow([details_url, title, phone, street_address, address_locality, address_region, postal_code])
        print '*'*78
    except Exception, e:
        if str(e) == 'HTTP Error 403: Forbidden':
            extract_details(details_url, file_name)
            
def get_pagination(search_url):
    number_of_pages = 0
    try:
        print search_url
        br_instance = mechanize_br()
        html_response = br_instance.open(search_url)
        html_source = html_response.read()
        details_html = html_source.replace('\n', '').replace('\r', '')
        
        number_of_results = "".join(re.findall(r'padBottom_10">(.*?) Empresas', details_html))
        print number_of_results
        number_of_pages = (int(number_of_results)/10)+1
#        print number_of_pages
        return number_of_pages
    except Exception, e:
        if str(e) == 'HTTP Error 403: Forbidden':
            pages = get_pagination(search_url)
            return pages
    except:
        raise
    
def get_landing_pages(url, data_writer):
    try:
        print url
        br_instance = mechanize_br()
        html_response = br_instance.open(url)
        html_source = html_response.read()
        details_html = html_source.replace('\n', '').replace('\r', '')
        
        #
        details_results = re.findall(r'<a href="http://www.123achei.com.br/classificados/conta.php.*?url=(http://www.123achei.com.br/.*?)"', details_html)
        for det_url in details_results:
            extract_details(det_url, data_writer)
    except Exception, e:
        if str(e) == 'HTTP Error 403: Forbidden':
            get_landing_pages(url, data_writer)
            
def get_details_pages(pages, data_writer):
    for i in range(pages):
        url = 'http://www.123achei.com.br/classificados/resultado.php?tipo=&ncidade=&rele=&pagina='+str(i)+'&idatividade=7527&atividade=Restaurantes&codLocal=11562&sreg=801&zona='
        get_landing_pages(url, data_writer)
        
    
if __name__ == "__main__":
    """
    url1 = 'http://www.123achei.com.br/servicos/bares-e-restaurantes/restaurantes/sao-jose-do-rio-preto/emporio-multi-sabores.html'
    url = 'http://www.123achei.com.br/servicos/bares-e-restaurantes/restaurantes/sao-jose-do-rio-preto/di-carlos-restaurante2.html'
    extract_details(url1, 'abc')
    """
    #url = 'http://www.123achei.com.br/classificados/resultado.php?suf=SP&sreg=801x11562&idatividade=7527'
    #pages = get_pagination(url)
    #print pages
    #pages = 2
    #get_details_pages(pages)
    
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'ab'))
    data_writer.writerow(['URL', 'Title', 'Phone', 'Street Address', 'Locality', 'Region', 'Postal Code'])
    category_file = open('categories.txt', 'rb')
    for category in category_file.readlines():
        url = 'http://www.123achei.com.br/classificados/resultado.php?suf=SP&sreg=801x11562&idatividade='+str(category.strip())
        pages = get_pagination(url)
        get_details_pages(pages, data_writer)
    