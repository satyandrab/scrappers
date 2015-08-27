import csv, random
import re, csv, mechanize, cookielib
from lxml import html
data_writer = csv.writer(open('twu final.csv', 'ab'))
done_emails_t = open('done_emails.txt', 'ab')
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


def check_faculty(line):
    with open('done_emails.txt', 'rb') as profid_file_r:
            mylist = profid_file_r.read().splitlines()
            
    if line[2] in temp_list or line[2] in mylist:
        pass
    else:
        first_name = line[0].lower().strip()
        last_name = line[1].lower().strip()
        
        faculty_file = open('faculty_file.txt').read().lower()
        
        form_string = last_name+', '+first_name
        if form_string in str(faculty_file).lower():
            print "Faculty found"
            pass
        else:
            print "writing data for", line 
            data_writer.writerow(line)
        done_emails_t.write(str(line[2]))
        done_emails_t.write('\n')
        temp_list.append(line[2])
    
    #states_urls = parsed_source.xpath("//div[@class='span3']/ul/li/a/@href")
    #return states_urls

if __name__ == '__main__':
    read_data_file = csv.reader(open('twu.csv', 'rb'))
    for line in read_data_file:
        print line
        check_faculty(line)
        print '*'*78