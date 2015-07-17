#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize, cookielib, random, csv, re
from lxml import html

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
    br.set_handle_equiv(True)
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
    br.addheaders = [('User-agent', 'Mozilla/'+(random.choice(version_list))+' (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    return br

def extract_details(url, data_writer):
    try:
        print url
        br_instance = mechanize_br()
        html_response = br_instance.open(url)
        html_source = html_response.read()
        result = html_source.replace('\n', '').replace('\r', '')
        parsed_source = html.fromstring(result, 'http://store.steampowered.com/')
        parsed_source.make_links_absolute()
        
        game_name = "".join(parsed_source.xpath("//div[@class='apphub_AppName']/text()")).encode("utf-8").strip()
        game_name = unicode(game_name, 'utf8')
        if len(game_name) > 0:
        
            game_genre = re.sub(r'<.*?>', '', "".join(re.findall(r'<b>Genre:</b>(.*?)<br>', result))).strip().encode("utf-8").strip()
            #print game_genre
            
            developer_name = "".join(re.findall(r'<b>Developer:</b>.*?<a href="http://store.steampowered.com/search/\?developer=.*?">(.*?)</a>.*?<br>', result))#.encode("utf-8").strip()
            developer_name = unicode(developer_name, 'utf8')
            developer_url = "".join(re.findall(r'<div class="details_block">.*?<a class="linkbar" href="(.*?)" target="_blank">.*?Visit the website', result))#.encode("utf-8").strip()
            #print developer_name
            #print developer_url
            
            try:
                publisher_details = re.findall(r'<b>Publisher:</b>.*?<a href="(http://store.steampowered.com/search/\?publisher=.*?)">(.*?)</a>', result)
                publisher_url = publisher_details[0][0].encode("utf-8").strip()
                publisher_name = publisher_details[0][1].encode("utf-8").strip()
                #print publisher_url
                #print publisher_name
            except:
                publisher_url = ''
                publisher_name = ''
                
            app_id = url.split('/')[-1]
        #    print app_id
            
            try:
                user_review_score = "".join(parsed_source.xpath("//div[@itemprop='aggregateRating']/@data-store-tooltip"))
                if len(user_review_score) > 0:
                    user_review_score = user_review_score.split(' ')[0].replace('%', '')
                #print user_review_score
            except:
                user_review_score = ''
            
            release_date = "".join(parsed_source.xpath("//span[@class='date']/text()")).encode("utf-8").strip()
        #    print release_date
            
            try:
                last_update_date = parsed_source.xpath("//div[@class='container']/h2/text()")[0]
            except:
                last_update_date = 'Unknown'
        #    print last_update_date
            
            supported_languages = parsed_source.xpath("//td[@class='ellipsis']/text()")
            languages = ", ".join([x.strip() for x in supported_languages])
        #    print languages
            
            system_supported = parsed_source.xpath("//div[@class='sysreq_tabs']/div/text()")
            systems = ", ".join([y.strip() for y in system_supported])
            if len(systems) > 0:
                systems = systems
            elif len(systems) == 0:
                system_supported = parsed_source.xpath("//div[@class='sysreq_contents']/div/@data-os")
                if "".join(system_supported) == 'win':
                    systems = 'Windows'
        #    print systems
            
            data_list = [url, game_name, game_genre, developer_name, developer_url, publisher_name, publisher_url, app_id,
                         user_review_score, release_date, last_update_date, languages, systems]
            
            print data_list
            data_writer.writerow([unicode(s).encode("utf-8") for s in data_list])
        else:
            pass
    except:
        extract_details(url, data_writer)
    
if __name__ == "__main__":
    
    file_name = raw_input('Enter name of file to save data(need not to enter file extension)......\n')
    csv_file_name = file_name+'.csv'

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'ab'))
    data_writer.writerow(['URL', 'Game name', 'Game genre', 'Developer name', 'Developer URL', 'Publisher name',
                          'Publisher URL', 'App ID', 'User review scores', 'Release date', 'Last update date',
                          'Supported languages', 'platform/systems'])
    
    id_file = csv.reader(open('imported_data/id_file.csv', 'rb'))
    for id in id_file:
        app_id = id[1]
        app_type = id[3]
        if app_type == 'Game':
            game_details_url = 'http://store.steampowered.com/app/'+str(app_id.strip())
            print game_details_url
            extract_details(game_details_url, data_writer)
            print '+'*78

    """
    url = 'http://store.steampowered.com/app/17520'
    #detail_url = 'http://store.steampowered.com/app/370920/'
    extract_details(url, data_writer)
    """
    