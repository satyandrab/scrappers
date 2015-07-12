#!/usr/bin/python

'''
Created on Jun 8, 2015

@author: satyandrababu
'''

import csv, re
from urllib2 import Request, urlopen

def get_email_id(details_url):
    try:
        print details_url
        req = Request(details_url)
        response = urlopen(req)
        details_html = response.read().replace('\r', '').replace('\n', '')
        
        #print details_html
        
        file_w = open('abc.html', 'wb')
        file_w.write(details_html)
        get_email = re.findall(r'email;charset=utf-8;type=internet;type=pref;type=.*?:(.*?@uh.edu) ', details_html)
        return get_email[0]
    except:
        return ""

def extract_details_link(search_url, data_writer):
    req = Request(search_url)
    response = urlopen(req)
    pagination_html = response.read().replace('\r', '').replace('\n', '')
    
    get_details = re.findall(r"<dt><a href='index.php\?emplid=(.*?)&loc=.*?dpt=.*?' >(.*?), (.*?)</a></dt>.*?<dd class=\"title\">(.*?)</dd>.*?<dd class=\"org\"><a.*?>(.*?)</a></dd>", pagination_html)
    for detail in get_details:
        detail_url = 'http://www.uh.edu/search/directory/api/vcard/?id='+str(detail[0])+'&type=perso'
        email = get_email_id(detail_url)
        first_name = detail[2]
        last_name = detail[1]
        title = detail[3].strip()
        department = detail[4]
        data_list = [first_name, last_name, department, title, email]
        print "writing data on csv for"
        print data_list
        data_writer.writerow(data_list)
        
        print '+'*78
        
if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    
    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['First Name', 'Last Name', 'Department', 'Title', 'Email'])
    
    char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    for char in char_list:
        search_url = "http://www.uh.edu/directory/proxy.php?submit=Search&loc=HR730&pos=faculty%7Cstaff%7Cstudent&letter="+str(char)+"&faculty=faculty&staff=staff&student=student"
        extract_details_link(search_url, data_writer)

    #search_url = "http://www.uh.edu/directory/proxy.php?submit=Search&loc=HR730&pos=faculty%7Cstaff%7Cstudent&letter=A&faculty=faculty&staff=staff&student=student"
    #extract_details_link(search_url, data_writer)
    
    #url = 'http://www.uh.edu/search/directory/api/vcard/?id=MTEzNDUyNw==&amp;type=perso'
    #get_email_id(url)