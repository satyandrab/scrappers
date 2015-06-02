#!/usr/bin/python


from urllib2 import Request, urlopen, URLError
import re, math, csv

def extract_information(url, number_of_pages, data_writer):
    for page in range(1,number_of_pages+1):
        pagination_url = url+'&page='+str(page)
        print pagination_url
        req = Request(pagination_url)
        response = urlopen(req)
        pagination_html = response.read().replace('\r', '').replace('\n', '')
        
        get_details_page_url = re.findall(r'<h3 class="poi name">.*?<a href="(.*?)"', pagination_html)
        for details_url in get_details_page_url:
            extract_details(details_url, data_writer)
        
def extract_details(details_url, file_name):
    print details_url
    req = Request(details_url)
    response = urlopen(req)
    details_html = response.read().replace('\r', '').replace('\n', '')
    
    try:
        phone_number = re.findall(r'<strong itemprop="telephone".*?data-content="\((.*?)"', details_html)[0].replace(')','')
    except:
        phone_number = ''
#    print phone_number
    
    try:
        title_address = re.findall(r'<title>(.*?)</title>', details_html)[0].split('-')
        title = title_address[0].strip()
        address = title_address[-1].strip()
    except:
        title = ''
        address = ''
    
    try:
        postal_code = re.findall(r'itemprop="postalCode">(.*?)</a>', details_html)[0].strip()
    except:
        postal_code = ''
    print "writing data into csv file for url.."+details_url
    print [details_url, title, phone_number, address, postal_code]
    data_writer.writerow([details_url, title, phone_number, address, postal_code])
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
            print "Not able to get pages....."
        
if __name__ == "__main__":
    #http://www.apontador.com.br/local/search.html?q=S%C3%A3o+Jos%C3%A9+do+Rio+Preto&loc_z=S%C3%A3o+Paulo&loc=S%C3%A3o+Paulo%2C+SP&loc_y=S%C3%A3o+Paulo%2C+SP
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    #f = open('imported_data/'+csv_file_name, "wb")
    #data_writer = csv.writer(f, delimiter='\t')

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'), delimiter='\t')
    data_writer.writerow(['URL','Title', 'Phone', 'address', 'Postal Code'])
    url = raw_input('Enter search URL to extract information......\n')
    validate_url(url, data_writer)
    