'''
Created on 23-Jul-2015

@author: satyandra
'''
from lxml import html
import mechanize, cookielib, random, re, csv

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

def extract_details(details_url):
    br_instance = mechanize_br()
    html_response = br_instance.open(details_url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
    parsed_source.make_links_absolute()
    
    #extracting profile id
    profile_id = "".join(parsed_source.xpath("//div[@class='profile']/@data-profid"))
    #print profile_id
    
    #extracting profile name
    profile_name = "".join(parsed_source.xpath("//h1[@itemprop='name']/text()"))
    #print profile_name
    
    #extracting female parameter
    if "Mrs." in profile_name or 'Ms.' in profile_name:
        female = 1
    elif 'Mr.' in profile_name:
        female = 0
    else:
        female = 'N/A'
    #print female
    
    #Checking photo
    image_url = "".join(parsed_source.xpath("//div[@class='section profile-photo']/a/img[@itemprop='image']/@src"))
    if len(image_url) == 0:
        photo = 0
    else:
        photo = 1
    #print photo
    
    #Profile URL
    profile_url = "https://therapists.psychologytoday.com/rms/prof_detail.php?profid="+str(profile_id)
    #print profile_url
    
    #Check website button
    button_website = parsed_source.xpath("//a[contains(text(),'Website')]")
    if button_website:
        btn_website = 1
    else:
        btn_website = 0
    #print btn_website
    
    #Check sendfriend button
    button_sendfriend = parsed_source.xpath("//a[contains(text(),'Send to Friend')]")
    if button_sendfriend:
        btn_sendfriend = 1
    else:
        btn_sendfriend = 0
    #print btn_sendfriend
    
    #Check emailme button
    button_emailme = parsed_source.xpath("//a[contains(text(),'Email Me')]")
    if button_emailme:
        btn_emailme = 1
    else:
        btn_emailme = 0
    #print btn_emailme
    
    #Check emailus button
    button_emailus = parsed_source.xpath("//a[contains(text(),'Email Us')]")
    if button_emailus:
        btn_emailus = 1
    else:
        btn_emailus = 0
    #print btn_emailus
    
    
    #Check videocall button
    button_videocall = parsed_source.xpath("//a[contains(text(),'Video Call')]")
    if button_videocall:
        button_videocall = 1
    else:
        button_videocall = 0
    #print button_videocall
    
    #extract state 
    state = "".join(parsed_source.xpath("//span[@itemprop='addressRegion']/text()"))
    #print state
    
    #extract zipcode
    zipcode = "".join(parsed_source.xpath("//span[@itemprop='postalcode']/text()"))
    #print zipcode
    
    #extract phone
    phone = "".join(parsed_source.xpath("//div[@itemprop='address']/span[@itemprop='telephone']/text()")).strip()
    #print phone
    
    #check if free consultation available
    freeconsult = "".join(parsed_source.xpath("//div[@class='section profile-freeinitial']//text()")).strip()
    if ' free ' in freeconsult:
        freeconsultation = 1
    else:
        freeconsultation = 0
    #print freeconsultation
    
    #thera_center_group???
    #TODO
    
    #extract occupation
    occupation = parsed_source.xpath("//div[@class='profile-title']/h2/span/text()")
    #print occupation
    
    #extract specialties
    specialties = parsed_source.xpath("//li[@class='highlight']/text()")
    #print specialties
    
    #extract issues
    issues = parsed_source.xpath("//h3[contains(text(), 'Issues:')]/following-sibling::div/ul/li/text()")
    #print issues
    
    #extract age group
    age = parsed_source.xpath("//h3[contains(text(), 'Age:')]/following-sibling::div/ul/li/text()")
    #print age
    
    #extract treatment
    treatment = parsed_source.xpath("//h3[contains(text(), 'Treatment Orientation:')]/following-sibling::div/ul/li//text()")
    treatment_list = []
    for treat in treatment:
        if treat.strip():
            treatment_list.append(treat.strip())
    #print treatment_list
    
    #Extract minimum and maximum cost
    cost = "".join(re.findall(r'<strong>Avg&nbsp;Cost&nbsp;\(per&nbsp;session\):</strong>\s*(.*?)\s*</li>', html_source))
    if len(cost) > 0:
        if '-' in cost:
            splitted_cost = cost.split(' - ')
            min_cost = splitted_cost[0].strip()
            max_cost = splitted_cost[1].strip()
        else: 
            min_cost = cost
            max_cost = ''
    else:
        min_cost = ''
        max_cost = ''
    #print min_cost
    #print max_cost
    
    #extract slide scale
    slidescale = "".join(re.findall(r'<strong>Sliding Scale:</strong>(.*?)</li>', html_source)).strip().lower()
    if slidescale == 'yes':
        fin_slidescale = 1
    elif slidescale == 'no':
        fin_slidescale = 0
    else:
        fin_slidescale = ''
    #print fin_slidescale
    
    #extract payment methods
    payment_methods = "".join(re.findall(r'<strong>Accepted Payment Methods:</strong>(.*?)</div>', html_source)).strip().split(',')
    payment_methods = [x.strip() for x in payment_methods]
    #print payment_methods
    
    #extract Insurance
    insurance = parsed_source.xpath("//h3[contains(text(), 'Accepted Insurance Plans:')]/following-sibling::div/ul/li/text()")
    #print insurance
    
    #extract practice years
    practice_year = "".join(re.findall(r'<strong>Years in Practice:</strong>(.*?)\s*</li>', html_source)).strip()
    #print practice_year
    
    #extract qualification school
    qual_school = "".join(re.findall(r'<strong>School:</strong>(.*?)\s*</li>', html_source)).strip()
    #print qual_school

    #extract qualification school year
    qual_yrgrad = "".join(re.findall(r'<strong>Year Graduated:</strong>(.*?)\s*</li>', html_source)).strip()
    #print qual_yrgrad
    
    #extract licence number
    qual_licensenum_state = "".join(re.findall(r'<strong>License No. and State:</strong>(.*?)\s*</li>', html_source)).strip()
    if '&nbsp;' in qual_licensenum_state:
        lic_state =  qual_licensenum_state.split('&nbsp;')
        licence_number = lic_state[0]
        licence_state = lic_state[1]
    else:
        licence_number = qual_licensenum_state
        licence_state = ''
    #print licence_number
    #print licence_state
    
    #extract last modified
    datemod = "".join(parsed_source.xpath("//div[@class='last-modified']/text()")).replace('Last Modified:', '').strip()
    #print datemod
    
    #extract connection information
    connections = parsed_source.xpath("//div[@class='connection-info']")
    connection_list = []
    for connect in connections:
        name = "".join(connect.xpath(".//span[@itemprop='name']/a/text()")).strip()
        url = "".join(connect.xpath(".//span[@itemprop='name']/a/@href")).strip()
        thrpst_type = "".join(connect.xpath(".//div[@class='connection-thrpst-type']/text()")).strip()
        connection_type = "".join(connect.xpath(".//div[@class='connection-type']/text()")).strip()
        conn_list = [name, url, thrpst_type, connection_type]
        connection_list.append(conn_list)
    #print connection_list
    
    data_list = [profile_id, profile_name, female, photo, profile_url, btn_website, btn_sendfriend, btn_emailme, btn_emailus, button_videocall,
                 state, zipcode, phone, freeconsultation, occupation, specialties, issues, age, treatment_list, min_cost, max_cost, fin_slidescale,
                 payment_methods, insurance, practice_year, qual_school, qual_yrgrad, licence_number, licence_state, datemod, connection_list]
    return data_list

def extract_details_url(url):
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
    parsed_source.make_links_absolute()
    
    details_urls = parsed_source.xpath("//a[@class='result-name']/@href")
    print details_urls
    return details_urls
    
if __name__ == '__main__':
    csv_main_file_name = 'data/main_table.csv'
    main_data_writer = csv.writer(open(csv_main_file_name, 'wb'))
    main_data_writer.writerow(['profid', 'name', 'female', 'photo', 'url', 'btn_website', 'btn_sendfriend', 'btn_emailme',
                          'btn_emailus', 'btn_videocall','state', 'zipcode', 'phone', 'freeconsult', 'fin_mincost', 'fin_maxcost',
                          'fin_slidescale', 'qual_yrpractice', 'qual_school', 'qual_yrgrad', 'qual_licensenum', 'qual_licensestatecode', 'datemod'])
    
    csv_occupation_file_name = 'data/occupation_table.csv'
    occupation_data_writer = csv.writer(open(csv_occupation_file_name, 'wb'))
    occupation_data_writer.writerow(['profid', 'occupation'])
    
    csv_specialties_file_name = 'data/specialties_table.csv'
    specialties_data_writer = csv.writer(open(csv_specialties_file_name, 'wb'))
    specialties_data_writer.writerow(['profid', 'specialties'])
    
    csv_issues_file_name = 'data/issues_table.csv'
    issues_data_writer = csv.writer(open(csv_issues_file_name, 'wb'))
    issues_data_writer.writerow(['profid', 'issues'])
    
    csv_clientfocus_file_name = 'data/clientfocus_table.csv'
    clientfocus_data_writer = csv.writer(open(csv_clientfocus_file_name, 'wb'))
    clientfocus_data_writer.writerow(['profid', 'clientfocus'])
    
    csv_treatment_file_name = 'data/treatment_table.csv'
    treatment_data_writer = csv.writer(open(csv_treatment_file_name, 'wb'))
    treatment_data_writer.writerow(['profid', 'programtreatment'])
    
    csv_payment_file_name = 'data/payment_table.csv'
    payment_data_writer = csv.writer(open(csv_payment_file_name, 'wb'))
    payment_data_writer.writerow(['profid', 'fin_payment'])
    
    csv_insurance_file_name = 'data/insurance_table.csv'
    insurance_data_writer = csv.writer(open(csv_insurance_file_name, 'wb'))
    insurance_data_writer.writerow(['profid', 'fin_insurance'])
    
    csv_connections_file_name = 'data/connections_table.csv'
    connection_data_writer = csv.writer(open(csv_connections_file_name, 'wb'))
    connection_data_writer.writerow(['profid', 'connectionname', 'connectionurl', 'therapiststype', 'connectiontype'])
    
    
    
    pagination_url = 'https://therapists.psychologytoday.com/rms/state/Oklahoma.html'
    details_url_list = extract_details_url(pagination_url)
    for details_url in details_url_list:
        print "Writing data for url", details_url
        data_list = extract_details(details_url)
        print data_list
        main_data_list = []
        main_data_list.extend(data_list[:14])
        main_data_list.extend(data_list[19:22])
        main_data_list.extend(data_list[24:30])
        main_data_writer.writerow(main_data_list)
        
        for occu in data_list[14]:
            occupation_data_writer.writerow([data_list[0], occu])
        
        for spec in data_list[15]:
            specialties_data_writer.writerow([data_list[0], spec])
        
        for issue in data_list[16]:
            issues_data_writer.writerow([data_list[0], issue])
        
        for clientfocus in data_list[17]:
            clientfocus_data_writer.writerow([data_list[0], clientfocus])
            
        for treatment in data_list[18]:
            treatment_data_writer.writerow([data_list[0], treatment])
        
        for payment in data_list[22]:
            payment_data_writer.writerow([data_list[0], payment])
        
        for insurance in data_list[23]:
            insurance_data_writer.writerow([data_list[0], insurance])
        
        for insurance in data_list[-1]:
            insurance.insert(0, data_list[0])
            connection_data_writer.writerow(insurance)
        print '*'*78
