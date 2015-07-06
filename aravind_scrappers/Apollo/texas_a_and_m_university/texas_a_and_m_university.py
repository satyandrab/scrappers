#!/usr/bin/python

'''
Created on Jun 9, 2015

@author: satyandrababu
'''

import csv, re
from urllib2 import Request, urlopen

def extract_details(details_url):
    req = Request(details_url)
    response = urlopen(req)
    details_html = response.read().replace('\r', '').replace('\n', '')
    
    name = "".join(re.findall(r'<th>Name:</th>.*?<td>(.*?)</td>', details_html))
    if ',' in name:
        name = name.split(',')
        first_name = name[1].strip()
        last_name = name[0].strip()
    else:
        name = name.split()
        first_name = name[0].strip()
        last_name = name[0].strip()
    
    print first_name
    print last_name
    
    title = "".join(re.findall(r'<th>Title:</th>.*?<td>(.*?)</td>', details_html))
    print title
    
    work_department = "".join(re.findall(r'<th>Work Department:</th>.*?<td>(.*?)</td>', details_html)).replace('&amp;', '&')
    if len(work_department) > 0:
        work_department = work_department
    else:
        work_department = 'Student'
    print work_department
    
    major = "".join(re.findall(r'<th>Major:</th>.*?<td>(.*?)</td>', details_html))
    print major
    
    classification = "".join(re.findall(r'<th>Classification:</th>.*?<td>(.*?)</td>', details_html)).replace('&#39;', "'")
    print classification
    
    web_page = "".join(re.findall(r'<th>Web Page:</th>.*?<td>(.*?)</td>', details_html)).replace('&#39;', "'")
    print web_page
    
    phone = "".join(re.findall(r'<th>Office Phone:</th>.*?<td>(.*?)</td>', details_html))
    print phone
    
    email = "".join(re.findall(r'<th>Email Address:</th>.*?<td><a.*?>(.*?)</a></td>', details_html))
    print email
    
    return [first_name, last_name, title, work_department, major, classification, web_page, phone, email, 'Texas A&M University']

def get_details_url(search_url):
    details_url_list = []
    req = Request(search_url)
    response = urlopen(req)
    search_html = response.read().replace('\r', '').replace('\n', '')
    
    get_urls = re.findall(r'<a href="(/directory-search/people/.*?)">', search_html)
    for detail_url in get_urls:
        details_url_list.append('https://services.tamu.edu'+detail_url)
    
    return details_url_list

if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    
    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'ab'))
    #data_writer.writerow(['First Name', 'Last Name', 'Title', 'Work Department',
    #                      'Major', 'Classification', 'Web Page', 'Office Phone',
    #                      'Email Address', 'Institution'])
    
    last_name_list = open('last_names.txt', 'rb').readlines()
    for last_name in last_name_list:
        last_name_t = last_name.lower().strip()
        search_url = 'https://services.tamu.edu/directory-search/advanced/?csrfmiddlewaretoken=WbeymUHti9CwvQl7luY2JhQnRzIVT4id&givenName=&sn='+str(last_name_t)+'&cn=&tamuEduPersonClassification=&tamuEduPersonMajor=&title=&tamuEduPersonDepartmentName=&tamuEduCampusCode='
        profile_url_list = get_details_url(search_url)
        for detail_url in profile_url_list:
            print 'Extracting data from URL '+detail_url
            data_list = extract_details(detail_url)
            print "Writing data into CSV for last name ", last_name
            print data_list
            data_writer.writerow(data_list)
            print '*'*78
    """
    url = 'https://services.tamu.edu/directory-search/people/58c35015542f9eb7ce207c678bbf2fca/'
    extract_details(url)
    """