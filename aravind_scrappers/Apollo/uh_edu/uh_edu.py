#!/usr/bin/python

'''
Created on Jun 8, 2015

@author: satyandrababu
'''

import csv, re
from urllib2 import Request, urlopen

def extract_details_link(search_url, data_writer):
    req = Request(search_url)
    response = urlopen(req)
    pagination_html = response.read().replace('\r', '').replace('\n', '')
    
    get_details = re.findall(r"<dt><a href='(.*?)' >(.*?), (.*?)</a></dt>.*?<dd class=\"title\">(.*?)</dd>.*?<dd class=\"org\"><a.*?>(.*?)</a></dd>", pagination_html)
    for detail in get_details:
        first_name = detail[2]
        last_name = detail[1]
        title = detail[3].strip()
        department = detail[4]
        data_list = [first_name, last_name, department, title]
        print "writing data on csv for"
        print data_list
        data_writer.writerow(data_list)
        print '+'*78
        
if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    
    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['First Name', 'Last Name', 'Department', 'Title'])
    
    char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    for char in char_list:
        search_url = "http://www.uh.edu/directory/proxy.php?submit=Search&loc=HR730&pos=faculty%7Cstaff%7Cstudent&letter="+str(char)+"&faculty=faculty&staff=staff&student=student"
        extract_details_link(search_url, data_writer)
    
    """
    search_url = "http://www.uh.edu/directory/proxy.php?submit=Search&loc=HR730&pos=faculty%7Cstaff%7Cstudent&letter=A&faculty=faculty&staff=staff&student=student"
    extract_details_link(search_url)#, data_writer)
    """