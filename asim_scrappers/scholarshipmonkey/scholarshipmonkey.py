#!/usr/bin/python

'''
Created on Jul 11, 2015

@author: satyandrababu
'''

from urllib2 import Request, urlopen, URLError
import urllib
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

def extract_details(url, data_writer):
    print url
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    details_html = html_source.replace('\n', '').replace('\r', '')
    
    scholarship = "".join(re.findall(r'<strong>Scholarship:</strong>(.*?)<', details_html)).strip()
    print scholarship
    
    school = re.findall(r'<strong>School:</strong> <a href="(/school/.*?)" target="_blank">(.*?)</a>', details_html)
    school_url =  'http://www.scholarshipmonkey.com'+str(school[0][0])
    school_name = school[0][1].strip()
    print school_url
    print school_name
    
    deadline = "".join(re.findall(r'<strong>Deadline:</strong>(.*?)<', details_html)).strip()
    print deadline
    
    amount = "".join(re.findall(r'<strong>Amount:</strong>(.*?)<', details_html)).strip()
    print amount
    
    sat = "".join(re.findall(r'<strong>SAT:</strong>(.*?)<', details_html)).strip()
    print sat
    
    gpa = "".join(re.findall(r'<strong>GPA:</strong>(.*?)<', details_html)).strip()
    print gpa
    
    majors = "".join(re.findall(r'<strong>Majors:</strong>(.*?)<', details_html)).strip()
    print majors
    
    website = "".join(re.findall(r'<strong>Website:</strong> <a href=".*?" target="_blank">(.*?)</a>', details_html)).strip()
    print website
    
    description = "".join(re.findall(r'<strong>Description:</strong>(.*?)<br><br>', details_html)).strip()
    print description
    
    data_list = [url, scholarship, school_url, school_name, deadline, amount, sat, gpa, majors, website, description]
    print data_list
    
    data_writer.writerow(data_list)

def extract_details_url(scholerships_list_url):
    print scholerships_list_url
    br_instance = mechanize_br()
    html_response = br_instance.open(scholerships_list_url)
    html_source = html_response.read()
    details_html = html_source.replace('\n', '').replace('\r', '')
    
    a = re.findall(r'<div class="hit">', details_html)
    print a
    
if __name__ == '__main__':
    """
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['URL', 'Scholarship', 'School URL', 'School Name', 'Deadline', 'Amount', 'SAT', 'GPA',
                          'Majors', 'Website', 'Description'])
    
    url = 'http://www.scholarshipmonkey.com/scholarship/410050ED-D0A3-71D4-5C3991FB22BAEE1D'
    extract_details(url, data_writer)
    """
    
    scholerships_list_url = 'http://www.scholarshipmonkey.com/list?list=Accounting%20Finance'
    extract_details_url(scholerships_list_url)