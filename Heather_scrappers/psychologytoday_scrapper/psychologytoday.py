'''
Created on 23-Jul-2015

@author: laxmi
'''
from lxml import html
from urlparse import urlparse, parse_qs
import mechanize, cookielib, random, re, csv
import time, sys
time_value = random.uniform(1.5, 2.5)
#time_value = 0

state_url_file = open('data/state.txt', 'ab')
profid_file = open('data/profid.txt', 'ab')
temp_list = []

def mechanize_br():
    version_list = ['5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0', '21.0', '22.0', '23.0',
                    '24.0', '25.0', '26.0', '27.0', '28.0', '29.0', '30.0', '31.0', '32.0', '33.0', '34.0', '35.0', '36.0', '37.0', '38.0',  '1.0',  '2.0', '3.0', '4.0']
    #print "Browser version ", (random.choice(version_list))
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
    print details_url
    try:
        time.sleep(time_value)
        
        br_instance = mechanize_br()
        html_response = br_instance.open(details_url)
        html_source = html_response.read()
        parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
        parsed_source.make_links_absolute()
        
        #extracting profile id
        profile_id = "".join(parsed_source.xpath("//div[@class='profile']/@data-profid"))
        if profile_id:
            profile_id = profile_id
        else:
            try:
                profile_id = details_url.split('=')[1].replace('&sid','')
            except:
                profile_id = None
        #print profile_id
        with open('data/profid.txt', 'rb') as profid_file_r:
            mylist = profid_file_r.read().splitlines()
        
        if profile_id in mylist or profile_id in temp_list:
            print "Passing profile"
            return None
        else:
            
            #extracting profile name
            profile_name = "".join(parsed_source.xpath("//h1[@itemprop='name']/text()")).replace(',', '').strip()
            #print profile_name
            
            #extracting female parameter
            parsed_url = urlparse(details_url)
            try:
                gender = "".join(parse_qs(parsed_url.query)['therapist_gender'])
                if gender == '2':
                    female = 1
                elif gender == '1':
                    female = 0
                else:
                    female = 'N/A'
            except:
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
            
            #personal statement
            personal_statements = parsed_source.xpath("//div[@class='statementPara']/text()")
            #print personal_statements
            
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
            
            #extract perweburl 
            perweburl = "".join(parsed_source.xpath("//li[contains(text(), 'Homepage:')]/a/text()")).replace(',', '').strip()
            #print perweburl
            
            #extract state 
            state = "".join(parsed_source.xpath("//span[@itemprop='addressRegion']/text()")[0]).replace(',', '').strip()
            #print state
            
            #extract zipcode
            try:
                zipcode = "".join(parsed_source.xpath("//span[@itemprop='postalcode']/text()")[0]).replace(',', '').strip()
            except:
                zipcode = ''
            #print zipcode
            
            #extract phone
            try:
                phone = "".join(parsed_source.xpath("//div[@itemprop='address']/span[@itemprop='telephone']/text()")[0]).strip().replace(',', '')
            except:
                phone = ''
            #print phone
            
            #check if free consultation available
            freeconsult = "".join(parsed_source.xpath("//div[@class='section profile-freeinitial']//text()")).strip()
            if ' free ' in freeconsult:
                freeconsultation = 1
            else:
                freeconsultation = 0
            #print freeconsultation
            
            #extract occupation
            occupation = []
            occupation_t = parsed_source.xpath("//div[@class='profile-title']/h2//text()")
            for occu in occupation_t:
                occu_t = occu.replace(',', '').strip()
                if occu_t != '':
                    occupation.append(occu_t)
            
            #extract specialties
            specialties = parsed_source.xpath("//li[@class='highlight']/text()")
            specialties = [s.replace(',', '').strip() for s in specialties]
            #print specialties
            
            #extract issues
            issues = parsed_source.xpath("//h3[contains(text(), 'Issues:')]")
            if len(issues) == 2:
                issues1 = issues[0].xpath(".//following-sibling::div/ul/li//text()")
                issues2 = issues[1].xpath(".//following-sibling::div/ul/li//text()")
                issues2 = [s.strip() for s in issues2 if len(s) > 1]
                #print issues2
                #print '+'*78
            else:
                try:
                    issues1 = issues[0].xpath(".//following-sibling::div/ul/li//text()")
                    issues2 = []
                except:
                    issues1 = []
                    issues2 = []
            issues1 = [s.replace(',', '').strip() for s in issues1]
            issues2 = [s.replace(',', '').strip() for s in issues2]
            
            #extract mental health
            mental_health = parsed_source.xpath("//h3[contains(text(), 'Mental Health:')]/following-sibling::div/ul/li/text()")
            mental_health = [s.replace(',', '').strip() for s in mental_health]
            #print mental_health
            
            #extract client focusage group
            cf_age = parsed_source.xpath("//h3[contains(text(), 'Age:')]/following-sibling::div/ul/li/text()")
            cf_age = [s.replace(',', '').strip() for s in cf_age]
            #print cf_age
            
            #extract client focusage group
            cf_relig = "".join(re.findall(r'<strong>Religious Orientation:</strong>(.*?)</div>', html_source)).strip().split(',')
            cf_relig = [x.replace(',', '').strip() for x in cf_relig]
            #print cf_relig
            
            #extract client focusage cf_ethnic
            cf_ethnic = "".join(re.findall(r'<strong>Ethnicity:</strong>(.*?)</div>', html_source)).strip().split(',')
            cf_ethnic = [x.replace(',', '').strip() for x in cf_ethnic]
            #print cf_ethnic
            
            #extract client focusage cf_ethnic
            cf_language = "".join(re.findall(r'<strong>Alternative Languages:</strong>(.*?)</div>', html_source)).strip().split(',')
            cf_language = [x.replace(',', '').strip() for x in cf_language]
            #print cf_language
            
            #extract client focusage cf_sexual
            cf_sexual = parsed_source.xpath("//h3[contains(text(), 'Sexuality:')]/following-sibling::div/ul/li/text()")
            cf_sexual = [x.replace(',', '').strip() for x in cf_sexual]
            #print cf_sexual
            
            #extract client focusage cf_categ
            cf_categ = parsed_source.xpath("//h3[contains(text(), 'Categories:')]/following-sibling::div/ul/li/text()")
            cf_categ = [x.replace(',', '').strip() for x in cf_categ]
            #print cf_categ
            
            #extract treatment Orientation
            treatment_orientation = parsed_source.xpath("//h3[contains(text(), 'Treatment Orientation:')]/following-sibling::div/ul/li//text()")
            treatment_orientation_list = []
            for treat in treatment_orientation:
                if treat.strip():
                    treatment_orientation_list.append(treat.strip())
            treatment_orientation_list = [s.replace(',', '').strip() for s in treatment_orientation_list]
            #print treatment_list
            
            #extract treatment Modality
            treatment_modality = parsed_source.xpath("//h3[contains(text(), 'Modality:')]/following-sibling::div/ul/li//text()")
            treatment_modality_list = []
            for treat_m in treatment_modality:
                if treat_m.strip():
                    treatment_modality_list.append(treat_m.strip())
            treatment_modality_list = [s.replace(',', '').strip() for s in treatment_modality_list]
            #print treatment_modality_list
            
            #Extract minimum and maximum cost
            cost = "".join(re.findall(r'<strong>Avg&nbsp;Cost&nbsp;\(per&nbsp;session\):</strong>\s*(.*?)\s*</li>', html_source))
            if len(cost) > 0:
                if '-' in cost:
                    splitted_cost = cost.split(' - ')
                    min_cost = splitted_cost[0].replace('$', '').strip()
                    max_cost = splitted_cost[1].replace('$', '').strip()
                    avgcost = ""
                else: 
                    min_cost = ''
                    max_cost = ''
                    avgcost = cost.replace('$', '')
            else:
                min_cost = ''
                max_cost = ''
                avgcost = ''
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
            payment_methods = [x.replace(',', '').strip() for x in payment_methods]
            #print payment_methods
            
            #extract Insurance
            insurance = parsed_source.xpath("//h3[contains(text(), 'Accepted Insurance Plans:')]/following-sibling::div/ul/li/text()")
            insurance = [x.replace(',', '').strip() for x in insurance]
            #print insurance
            
            #extract practice years
            practice_year = "".join(re.findall(r'<strong>Years in Practice:</strong>(.*?)\s*</li>', html_source)).replace(',', '').strip().replace('&lt;', '<').replace('&gt;', '>')
            #print practice_year
            
            #extract qualification school
            qual_school = "".join(re.findall(r'<strong>School:</strong>(.*?)\s*</li>', html_source)).replace(',', '').strip()
            #print qual_school
        
            #extract qualification school year
            qual_yrgrad = "".join(re.findall(r'<strong>Year Graduated:</strong>(.*?)\s*</li>', html_source)).replace(',', '').strip()
            #print qual_yrgrad
            
            #extract licence number
            qual_licensenum_state = "".join(re.findall(r'<li><strong>License No. and State:</strong>(.*?)</li>', html_source.replace('\n', '').replace('\r', ''))).replace(',', '').strip()
            #print qual_licensenum_state
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
            datemod = "".join(parsed_source.xpath("//div[@class='last-modified']/text()")).replace('Last Modified:', '').replace(',', '').strip()
            #print datemod
            
            gropus = parsed_source.xpath("//div[@class='group-small']/h2/a/text()")
            gropus = [x.replace(',', '').strip() for x in gropus]
            #print gropus
            
            #extract connection information
            connections = re.findall(r'<div class="connection-photo">.*?<div class="connection-type">.*?</div>', html_source.replace('\r', '').replace('\n', ''))
            connection_list = []
            for connect in connections:
                try:
                    name = "".join(re.findall(r'<span itemprop="name"><a.*?>(.*?)</a>', connect)).strip().replace(',', '')
                    name_t = html.fromstring(name).text
                    url = "".join(re.findall(r'<span itemprop="name"><a href="(.*?)">', connect)).strip()
                    thrpst_type = "".join(re.findall(r'<div class="connection-thrpst-type">(.*?)</div>', connect)).strip().replace(',', '')
                    connection_type = "".join(re.findall(r'<div class="connection-type">(.*?)</div>', connect)).strip().replace(',', '')
                    conn_list = [name_t, url, thrpst_type, connection_type]
                    connection_list.append(" ^!^ ".join(conn_list))
                except:
                    pass
    #        print connection_list
        
            verified_t = parsed_source.xpath("//div[@class='profile-verified']")
            if verified_t:
                verified = 1
            else:
                verified = 0
            
            data_dict = {'profile_id':profile_id, 'profile_name':profile_name, 'female':female, 'photo':photo, 'profile_url':profile_url, "btn_perweb":btn_website,
                         "btn_sendfriend":btn_sendfriend, "btn_emailme":btn_emailme, "btn_emailus":btn_emailus, "btn_videocall":button_videocall, "perweburl":perweburl,
                         "state":state, "zipcode":zipcode, "phone":phone, "freeconsultation":freeconsultation, "occupation":occupation, "specialties":specialties, "issues1":issues1,
                         "issues2":issues2, "cf_age":cf_age, "cf_relig":cf_relig, "cf_ethnic":cf_ethnic, "cf_language":cf_language, "cf_sexual":cf_sexual, "cf_categ":cf_categ,
                         "treatment_orientation_list":treatment_orientation_list, "treatment_modality_list":treatment_modality_list,"min_cost":min_cost,
                         "max_cost":max_cost, "avgcost":avgcost, "fin_slidescale":fin_slidescale, "payment_methods": payment_methods, "mental_health":mental_health,
                         "insurance":insurance, "practice_year":practice_year, "qual_school":qual_school, "qual_yrgrad":qual_yrgrad, "licence_number":licence_number,
                         "licence_state":licence_state, "datemod":datemod, "gropus":gropus, "connection_list":connection_list, "personal_statements":personal_statements,
                         "verified":verified}
            
            profid_file.write(profile_id)
            profid_file.write('\r\n')
            temp_list.append(profile_id)
    
            return data_dict
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        try:
        #raise
            extract_details(details_url)
        except RuntimeError:
            return None

def extract_details_url(url):
    try:
        time.sleep(time_value)
        br_instance = mechanize_br()
        html_response = br_instance.open(url)
        html_source = html_response.read()
        parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
        parsed_source.make_links_absolute()
        
        nomatchflag = parsed_source.xpath("//div[@class='NoMatchingFound']")
        if nomatchflag:
            return 'nomatchflag'
        else:
            details_urls = parsed_source.xpath("//a[@class='result-name']/@href")
            print details_urls
            return details_urls
    except:
        extract_details_url(url)

def check_last_page(pagination_url):
    try:
        time.sleep(time_value)
        br_instance = mechanize_br()
        html_response = br_instance.open(pagination_url)
        html_source = html_response.read()
        parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
        parsed_source.make_links_absolute()
        
        profile_div = parsed_source.xpath("//div[@class='results-unmatched']")
        if len(profile_div) == 1:
            return True
        else:
            return False
    except:
        check_last_page(pagination_url)

def write_personal_statements_table(data_dict, personal_statements_data_writer):
    try:
        if data_dict.has_key('personal_statements'):
                personal_statements_data_writer.write('||')
                personal_statements_data_writer.write('\n')
                personal_statements_data_writer.write('profid='+data_dict['profile_id'])
                personal_statements_data_writer.write('\n')
                for para in data_dict['personal_statements']:
                    personal_statements_data_writer.write(unicode(para).encode('utf8'))
                    personal_statements_data_writer.write('\n')
                personal_statements_data_writer.write('\n')
    except:
        pass

def write_main_table(data_dict, mywriter):
    wide_form_data_list = []
    try:
        wide_form_data_list.append(data_dict['profile_id'])
        wide_form_data_list.append(data_dict['profile_url'])
        wide_form_data_list.append(data_dict['profile_name'])
        wide_form_data_list.append(data_dict['female'])
        wide_form_data_list.append(data_dict['photo'])
        wide_form_data_list.append(data_dict['btn_sendfriend'])
        wide_form_data_list.append(data_dict['btn_emailme'])
        wide_form_data_list.append(data_dict['btn_emailus'])
        wide_form_data_list.append(data_dict['btn_videocall'])
        wide_form_data_list.append(data_dict['btn_perweb'])
        wide_form_data_list.append(data_dict['perweburl'])
        wide_form_data_list.append(data_dict['phone'])
        wide_form_data_list.append(data_dict['state'])
        wide_form_data_list.append(data_dict['zipcode'])
        wide_form_data_list.append(data_dict['freeconsultation'])
        wide_form_data_list.append(" || ".join(data_dict['occupation']))
        wide_form_data_list.append(" || ".join(data_dict['specialties']))
        wide_form_data_list.append(" || ".join(data_dict['issues1']))
        wide_form_data_list.append(" || ".join(data_dict['mental_health']))
        wide_form_data_list.append(" || ".join(data_dict['issues2']))
        wide_form_data_list.append(" || ".join(data_dict['cf_relig']))
        wide_form_data_list.append(" || ".join(data_dict['cf_ethnic']))
        wide_form_data_list.append(" || ".join(data_dict['cf_language']))
        wide_form_data_list.append(" || ".join(data_dict['cf_age']))
        wide_form_data_list.append(" || ".join(data_dict['cf_sexual']))
        wide_form_data_list.append(" || ".join(data_dict['cf_categ']))
        wide_form_data_list.append(" || ".join(data_dict['treatment_orientation_list']))
        wide_form_data_list.append(" || ".join(data_dict['treatment_modality_list']))
        wide_form_data_list.append(data_dict['min_cost'])
        wide_form_data_list.append(data_dict['max_cost'])
        wide_form_data_list.append(data_dict['avgcost'])
        wide_form_data_list.append(data_dict['fin_slidescale'])
        wide_form_data_list.append(" || ".join(data_dict['payment_methods']))
        wide_form_data_list.append(" || ".join(data_dict['insurance']))
        wide_form_data_list.append(data_dict['practice_year'])
        wide_form_data_list.append(data_dict['qual_school'])
        wide_form_data_list.append(data_dict['qual_yrgrad'])
        wide_form_data_list.append(data_dict['licence_number'])
        wide_form_data_list.append(data_dict['licence_state'])
        wide_form_data_list.append(data_dict['datemod'])
        wide_form_data_list.append(" || ".join(data_dict['gropus']))
        wide_form_data_list.append(" || ".join(data_dict['connection_list']))
        wide_form_data_list.append(data_dict['verified'])
        
        print wide_form_data_list
        print '*'*78
        mywriter.writerow([unicode(s).encode("utf-8") for s in wide_form_data_list])
    except:
        pass

def extract_states_urls(url):
    time.sleep(time_value)
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
    parsed_source.make_links_absolute()
    
    states_urls = parsed_source.xpath("//div[@class='span3']/ul/li/a/@href")
    return states_urls

def extract_more_city_codes(url):
    time.sleep(time_value)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
    parsed_source.make_links_absolute()
    
    city_code = parsed_source.xpath("//a[contains(@href, '/rms/state/')]/text()")
    return city_code

def get_state_code_more_city(url):
    time.sleep(time_value)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    parsed_source = html.fromstring(html_source, 'https://therapists.psychologytoday.com/')
    parsed_source.make_links_absolute()
    
    state_code = "".join(re.findall(r'Therapists in .*? \((.*?)\)', "".join(parsed_source.xpath("//div[@id='results-right']/h1/text()")).strip()))
    if len(state_code) == 0:
        city_codes = extract_more_city_codes(url)
        city_codes = [x.replace(' ', '+') for x in city_codes]
        return city_codes
    else:
        return [state_code]
    
if __name__ == '__main__':
    
    csv_main_file_name = 'data/main_table.txt'
    fileObject = open(csv_main_file_name,'ab')
    csv.register_dialect('MyDialect', delimiter='\t',doublequote=False,quotechar='',lineterminator='\n',escapechar=' ',quoting=csv.QUOTE_NONE)
    mywriter = csv.writer(fileObject,'MyDialect')
    
    mywriter.writerow(['profid', 'profurl', 'name', 'female', 'photo', 'btn_sendfriend', 'btn_emailme', 'btn_emailus', 'btn_videocall', 'btn_perweb', 'perweburl',
                               'phone', 'state', 'zipcode', 'freeconsult', 'occupation', 'specialties', 'issues1', 'menthealth', 'issues2', 'cf_relig', 'cf_ethnic', 'cf_language',
                               'cf_age', 'sexuality', 'cf_categ', 'trt_orient', 'trt_modal', 'fin_mincost', 'fin_maxcost', 'fin_avgcost', 'fin_slidescale', 'fin_paymethod',
                               'fin_insur', 'qual_yrpractice', 'qual_school', 'qual_yrgrad', 'qual_licensenum', 'qual_licensestate', 'datemod', 'groups', 'connections', 'verified'])
    txt_personal_statements_file_name = 'data/personalStatements.txt'
    personal_statements_data_writer = open(txt_personal_statements_file_name, 'ab')
    
    
    gender_list = ['1', '2']
    start_url = 'https://therapists.psychologytoday.com/rms/prof_search.php'
    states_urls = extract_states_urls(start_url)
    for state_url in states_urls:
        state_codes = get_state_code_more_city(state_url)
        for state_code in state_codes:
            print state_code
            open_state_file = open('data/state.txt', 'rb')
            state_url_file_r = open_state_file.readlines()
            if state_code+'\n' in state_url_file_r:
                print "passing city"
                pass
            else:
                print "writing for state"
                if len(state_code) > 0:
                    for gender in gender_list:
                        for num in range(1, 1000, 20):
                            if len(state_codes) == 1:
                                ga_female_th_url = 'https://therapists.psychologytoday.com/rms/prof_results.php?&state='+state_code+'&s=R&therapist_gender='+str(gender)+'&rec_next='+str(num)
                            else:
                                ga_female_th_url = 'https://therapists.psychologytoday.com/rms/prof_results.php?&city='+state_code+'&s=R&therapist_gender='+str(gender)+'&rec_next='+str(num)
                                
                            print ga_female_th_url
                            print '+'*78
                            open_state_file = open('data/state.txt', 'rb')
                            state_url_file_r = open_state_file.readlines()
                            if ga_female_th_url+'\n' in state_url_file_r:
                                print "passing city"
                                pass
                            else:
                                check_flag = check_last_page(ga_female_th_url)
                                if check_flag:
                                    profile_urls = extract_details_url(ga_female_th_url)
                                    if profile_urls == 'nomatchflag':
                                        break
                                        print "Area widen"
                                    else:
                                        if profile_urls is not None:
                                            if len(profile_urls) < 19:
                                                for pr_url in profile_urls:
                                                    profile_id = pr_url.split('=')[1].replace('&sid','')
                                                    with open('data/profid.txt', 'rb') as profid_file_r:
                                                        mylist = profid_file_r.read().splitlines()
                                                    #print mylist
                                                    if profile_id in mylist or profile_id in temp_list:
                                                        print "Passing profile"
                                                        pass
                                                    else:
                                                        data_dict = extract_details(pr_url)
                                                        if data_dict is not None:
                                                            write_main_table(data_dict, mywriter)
                                                            write_personal_statements_table(data_dict, personal_statements_data_writer)
                                                    profid_file.write(profile_id)
                                                    profid_file.write('\r\n')
                                                    temp_list.append(profile_id)
                                                break
                                    break
                                else:
                                    profile_urls = extract_details_url(ga_female_th_url)
                                    if profile_urls == 'nomatchflag':
                                        break
                                    else:
                                        if profile_urls is not None:
                                            print profile_urls
                                            print '+'*78
                                            for pr_url in profile_urls:
                                                profile_id = pr_url.split('=')[1].replace('&sid','')
                                                with open('data/profid.txt', 'rb') as profid_file_r:
                                                    mylist = profid_file_r.read().splitlines()
                                                #print mylist
                                                if profile_id in mylist or profile_id in temp_list:
                                                    print "Passing profile"
                                                    pass
                                                else:
                                                    data_dict = extract_details(pr_url)
                                                    if data_dict is not None:
                                                        write_main_table(data_dict, mywriter)
                                                        write_personal_statements_table(data_dict, personal_statements_data_writer)
                                                profid_file.write(profile_id)
                                                profid_file.write('\r\n')
                                                temp_list.append(profile_id)
                                state_url_file.write(ga_female_th_url)
                                state_url_file.write('\n')
                    state_url_file.write(state_code)
                    state_url_file.write('\n')
                    open_state_file.close()
                else:
                    city_urls = extract_states_urls(state_url)
                    pass
                print '*'*78
