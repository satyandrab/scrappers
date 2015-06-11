#!/usr/bin/python

'''
Created on 10-Jun-2015

@author: satyandra
'''

import csv, re
from urllib2 import Request, urlopen

def extract_details(url, school_p, cource_category, data_writer):
    category = 'Texas A&M University'
    school = school_p
    req = Request(url)
    response = urlopen(req)
    details_html = response.read().replace('\r', '').replace('\n', '')
    
    cource_titles = re.findall(r'<TH CLASS="ddtitle" scope="colgroup" ><A HREF=".*?">(.*?)</A></TH>', details_html)
    for cource_title in cource_titles:
        splitted_title = cource_title.split('-')
        cource_number = splitted_title[-2].strip()
        cource_name = splitted_title[0].strip()
        data_list = [category, school, cource_category, cource_number, cource_name]
        print data_list
        data_writer.writerow(data_list)
        print '*'*78
    
if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'
    
    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['Category', 'School', 'Title', 'Course Number',
                          'Course Name'])
    
    
    cource_file = open('cources.txt', 'rb').readlines()
    for cource in cource_file:
        splitted_cource =  cource.strip().split(' - ')
        category = splitted_cource[0]
        school = splitted_cource[1]
        url = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=201531&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj='+str(category)+'&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
        extract_details(url, school, category, data_writer)
    
    #url = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=201531&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=ACCT&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
    #extract_details(url, 'Accounting', 'ACCT', data_writer)
    
    
    
"""
https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=201531&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=
dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=ACCT&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=
&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a

Search By Term: 
Fall 2015- College Station -- 201531
Spring 2015- College Station -- 201511
"""

