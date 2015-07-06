#!/usr/bin/python

'''
Created on Jun 8, 2015

@author: satyandrababu
'''

import csv, re
from urllib2 import Request, urlopen

def extract_details_link(search_url, school_data):
    category = 'University of Houston'
    school = school_data
    
    req = Request(search_url)
    response = urlopen(req)
    details_html = response.read().replace('\r', '').replace('\n', '')
    
    title = re.findall(r"<h1>((.*?) .*?) - ( .*?)</h1>", details_html)
    course_number = title[0][0].strip()
    course_category = title[0][1].strip()
    course_name = title[0][2].strip()
    
    return [category, school, course_number, course_category, course_name]

def get_details_url(url, data_writer, page):
    req = Request(url)
    response = urlopen(req)
    html = response.read().replace('\r', '').replace('\n', '').split('<td colspan="2"><br>')
    
    for splited_html in html:
        detail_urls = re.findall(r'<a href="(preview_course_nopop.php\?catoid=.*?&coid=.*?)"', splited_html)
        if len(detail_urls) > 0:
            school = "".join(re.findall(r'<p><b>(.*?)</b></p></td>', splited_html))
            
            for details_url in  detail_urls:
                d_url = 'http://catalog.uh.edu/'+details_url
                data_list = extract_details_link(d_url, school)
                print "Writing data to CSV for page ", str(page)
                print data_list
                data_writer.writerow(data_list)
                print '*'*78

if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    
    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'ab'))
    #data_writer.writerow(['First Name', 'Last Name', 'Department'])
    
    for page in range(29, 37):
        url = 'http://catalog.uh.edu/content.php?catoid=8&catoid=8&navoid=1557&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D='+str(page)
        print url
        get_details_url(url, data_writer, page)