'''
Created on Aug 19, 2015

@author: satyandrababu
'''

from lxml import html
import mechanize, cookielib, random, re
import time
time_value = 0
import json

comp_file = open('data/compid.txt', 'ab')
temp_list = []


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

def extract_country_codes(url):
    time.sleep(time_value)
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'http://www.ttnet.net/')
    parsed_source.make_links_absolute()
    
    country_codes = []
    country_code_urls = parsed_source.xpath("//div[@class='nation_result_list']//ul/li/a")
    for country_code in country_code_urls:
        country_codes_t = "".join(country_code.xpath('.//@data-nationcode'))
        pages = (int("".join(country_code.xpath('.//span/text()')).replace(')', '').replace('(', ''))/12)+1
        country_codes.append([country_codes_t, pages])
    return country_codes

def extract_details_url(url):
    time.sleep(time_value)
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()#.decode("utf-8")#.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(html_source, 'http://www.ttnet.net/')
    #parsed_source.make_links_absolute()
    
    list = []
    details_urls = parsed_source.xpath("//a[@class='company_detail_btn']")
    for detail_url in details_urls:
        comp_id = "".join(detail_url.xpath('.//@data-value'))
        comp_url = "".join(detail_url.xpath('.//@href'))
        list.append([comp_id, comp_url])
    print list
    return list

def extract_details(url):
    print url
    details = {}
    time.sleep(time_value)
        
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read().replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(html_source, 'http://www.ttnet.net/')
    parsed_source.make_links_absolute()
    
    details['url'] = url
    
    comp_name = "".join(re.findall(r'<th>\s*Company Name\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source))
    details['Company Name'] = comp_name
    print comp_name
    
    address = "".join(re.findall(r'<th>\s*Address\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source))
    print address
    details['Address'] = address
    
    telephones = "".join(re.findall(r'<th>\s*Tel\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source))
    print telephones
    details['Phone'] = telephones
    
    fax = "".join(re.findall(r'<th>\s*Fax\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source))
    print fax
    details['Fax'] = fax
    
    product_category = ", ".join(parsed_source.xpath("//div[@id='treeleft_1']/ul/li/a/text()"))
    print product_category
    details['Product Category'] = product_category
    
    country = "".join(re.findall(r'<th>\s*Country of Origin\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source))
    print country
    details['Country'] = country
    
    #president = "".join(re.findall(r'<th scope="row"><span>President</span></th>\s*<td>\s*(.*?)\s*</td>', html_source))
    #print president
    details['President'] = ''
    
    #established_year = "".join(re.findall(r'<th scope="row"><span>Year established</span></th>\s*<td>\s*(.*?)\s*</td>', html_source))
    #print established_year
    details['Year established'] = ''
    
    #employee = "".join(re.findall(r'<th scope="row"><span>No. of Total Employees</span></th>\s*<td>\s*(.*?)\s*</td>', html_source))
    #print employee
    details['No. of Total Employees'] = ''
    
    #main_market = "".join(re.findall(r'<th scope="row"><span>Main Markets</span></th>\s*<td>(.*?)</td>', html_source)).strip().replace('\t', '')
    #print main_market
    details['Main Markets'] = ''
    
    #main_products = "".join(re.findall(r'<th scope="row" class="lst"><span>Main Product</span></th>\s*<td class="lst">(.*?)</td>', html_source)).strip().replace('\t', '').replace('<br>', ', ')
    #print main_products
    details['Main Product'] = product_category
    
    try:
        get_url_about_us = "".join(parsed_source.xpath("//a[contains(text(), 'About Us')]/@href")[0])
        print get_url_about_us
        raw_desc_text = get_description(get_url_about_us)
    except:
        raw_desc_text = ''
        
    details['Company introduction'] = raw_desc_text
    
    website_url = ", ".join(re.findall(r'<a.*?href="(.*?)"', ("".join(re.findall(r'<th>\s*Website\s*</th>\s*<td>\s*(.*?)\s*</td>', html_source)))))
    print website_url
    if website_url is not None:
        details['Website'] = website_url
    else:
        details['Website'] = ''
    return details

def get_description(url):
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read().replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(html_source, 'http://www.ttnet.net/')
    parsed_source.make_links_absolute()
    
    desc = "".join(parsed_source.xpath("//div[@class='description']//text()")).strip()
    return desc
    
def get_home_url(url):
    try:
        br_instance = mechanize_br()
        html_response = br_instance.open(url)
        html_source = html_response.read().replace('\n', '').replace('\r', '')
        parsed_source = html.fromstring(html_source, 'http://www.ttnet.net/')
        parsed_source.make_links_absolute()
        
        comp_name = "".join(re.findall(r'<li class="lst"><em>Homepage</em>\s*<span>\s*<a href="(.*?)" target="_blank">', html_source))
        return comp_name
    except:
        return None
    
    
if __name__ == '__main__':
    url = 'http://www.ttnet.net/ttnet/gotohtm/0/1303033303835383.htm'
    data = extract_details(url)
    print data
    
    """
    json_sample_file = open('data.json', 'ab')
    
    country_page_file = open('country_page_file.txt', 'ab')
    
    country_c_pages = [['KR', 4620], ['CN', 1707], ['US', 277], ['IN', 271], ['VN', 127], ['ID', 90], ['MY', 85], ['PK', 84], ['HK', 67], ['TH', 63], ['IR', 58], ['GB', 55], ['TW', 54], ['JP', 50], ['SG', 49], ['AU', 46], ['AE', 44], ['CA', 43], ['PH', 41], ['TR', 37], ['BD', 36], ['RU', 33], ['SA', 31], ['EG', 30], ['CM', 30], ['DE', 25], ['NG', 23], ['ZA', 21], ['UA', 20], ['BR', 20], ['ES', 16], ['IT', 14], ['CL', 13], ['MX', 13], ['NZ', 13], ['LK', 13], ['GH', 12], ['FR', 12], ['PE', 11], ['MN', 10], ['IL', 10], ['PL', 10], ['CO', 10], ['NL', 10], ['GR', 9], ['JO', 8], ['KW', 8], ['RO', 7], ['AR', 7], ['SY', 6], ['KE', 6], ['NP', 6], ['KH', 6], ['MM', 6], ['HU', 6], ['SE', 6], ['IQ', 5], ['QA', 5], ['BE', 5], ['CH', 5], ['BG', 5], ['UZ', 5], ['EC', 5], ['BJ', 5], ['LB', 5], ['BH', 5], ['KP', 5], ['KZ', 4], ['UG', 4], ['MO', 4], ['OM', 4], ['YE', 4], ['ET', 4], ['MA', 4], ['TZ', 4], ['PT', 4], ['CZ', 4], ['AT', 4], ['DZ', 4], ['IE', 3], ['DK', 3], ['DO', 3], ['VE', 3], ['CY', 3], ['BO', 3], ['ZW', 3], ['GE', 3], ['LY', 3], ['TN', 3], ['CI', 3], ['LT', 3], ['ML', 3], ['NO', 3], ['TG', 3], ['FI', 3], ['MU', 3], ['SD', 3], ['AF', 3], ['AZ', 3], ['SN', 3], ['BN', 2], ['HR', 2], ['TD', 2], ['CR', 2], ['LA', 2], ['AO', 2], ['EE', 2], ['AM', 2], ['MV', 2], ['PY', 2], ['SI', 2], ['TT', 2], ['FJ', 2], ['GT', 2], ['LV', 2], ['GN', 2], ['KG', 2], ['SK', 2], ['BY', 2], ['JM', 2], ['BF', 2], ['CS', 2], ['LR', 2], ['MT', 2], ['PA', 2], ['SV', 2], ['UY', 2], ['ZM', 2], ['AL', 1], ['FX', 1], ['PR', 1], ['HN', 1], ['BW', 1], ['SL', 1], ['BT', 1], ['NA', 1], ['AN', 1], ['CF', 1], ['CG', 1], ['LU', 1], ['CD', 1], ['MD', 1], ['MG', 1], ['MZ', 1], ['NC', 1], ['NI', 1], ['PG', 1], ['PS', 1], ['SO', 1], ['YD', 1], ['AS', 1], ['BS', 1], ['IS', 1], ['TJ', 1], ['VI', 1], ['BA', 1], ['BZ', 1], ['HT', 1], ['LC', 1], ['MW', 1], ['RE', 1], ['RW', 1], ['YM', 1], ['YU', 1], ['AQ', 1], ['AW', 1], ['BB', 1], ['CX', 1], ['DJ', 1], ['GQ', 1], ['MK', 1], ['MR', 1], ['PF', 1], ['TP', 1], ['VU', 1], ['BM', 1], ['DM', 1], ['EH', 1], ['ER', 1], ['GA', 1], ['GY', 1], ['MI', 1], ['PC', 1], ['PO', 1], ['SB', 1], ['SR', 1], ['SZ', 1], ['TM', 1], ['UM', 1], ['AD', 1], ['AG', 1], ['AI', 1], ['BI', 1], ['CT', 1], ['FK', 1], ['FM', 1], ['FO', 1], ['GM', 1], ['HM', 1], ['IO', 1], ['KM', 1], ['KY', 1], ['LI', 1], ['LS', 1], ['MC', 1], ['MH', 1], ['NT', 1], ['PZ', 1], ['SC', 1], ['SM', 1], ['ST', 1], ['SU', 1], ['VA', 1], ['WS', 1], ['ZR', 1]]
    for country_pages in country_c_pages:
        country_code = country_pages[0]
        pages = country_pages[1]
        for page in range(1, pages+1):
            pagination_url = 'http://www.tradekorea.com/total_search/total_search.do?action=searchAjax&pagenum='+str(page)+'&action=returnUrl&totsearch_option=COMPANIES&totsearch_nationcode='+str(country_code)+'&totsearch_view_type=01&totsearch_sortby=01&totsearch_categorypath=&totsearch_categorynopath=&totsearch_rowsize=&totsearch_selected_catename=&totsearch_categorypath_y=&totsearch_categoryno=&totsearch_categoryname=&totsearch_nationcode_y=&totsearch_keyword=&totsearch_search_no=&totsearch_cert_typecode=&totsearch_cert_keyword=&totsearch_cert_nationname=&totsearch_cert_nationcode=&totsearch_or_and=OR'
            print pagination_url
            open_file = open('country_page_file.txt', 'rb')
            lines_list = open_file.readlines()
            if pagination_url+'\n' in lines_list:
                print 'passing page'
                pass
            else:
                details_url = extract_details_url(pagination_url)
                for detail_url in details_url:
                    url = detail_url[1]
                    comp_id = detail_url[0]
                    with open('data/compid.txt', 'rb') as compid_file_r:
                        mylist = compid_file_r.read().splitlines()
                    if comp_id in temp_list or comp_id in mylist:
                        print "passing company"
                        pass
                    else:
                        company_url = 'http://www.tradekorea.com/mytradekorea/myInterest.do?action=detailInterestCompanyAjax&businessno='+str(comp_id)
                        data_dict = extract_details(company_url)
                        json_sample_file.write(json.dumps(data_dict))
                        json_sample_file.write('\r\n')
                        comp_file.write(comp_id)
                        comp_file.write('\r\n')
                        temp_list.append(comp_id)
                        print '*'*78
                country_page_file.write(str(pagination_url))
                country_page_file.write('\n')
            open_file.close()
            print '-'*78
    """
    
