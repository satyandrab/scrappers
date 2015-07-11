from selenium import webdriver
import csv
from lxml import html
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class scholarshipmonkey():
    
    def Extract_data(self, starting_url, browser):
        data_writer = csv.writer(open("scholarship_monkey.csv", "wb"))
        data_writer.writerow(['SholarShip_Page URL', 'Scholarship URL', 'Scholarship', 'School URL', 'School Name', 'Deadline', 'Amount', 'SAT', 'GPA', 'Majors', 'Website', 'Description'])
        browser.get(starting_url)
        time.sleep(2)
        window_before = browser.window_handles[0]
        scholarship_links_list = browser.find_elements_by_xpath("//div[@class='small-4 columns']/a")
        print len(scholarship_links_list)
        i = 0
        for a in scholarship_links_list:
            scholarship_links_list = browser.find_elements_by_xpath("//div[@class='small-4 columns']/a")
            page_link = scholarship_links_list[i].get_attribute("href")
            scholarship_links_list[i].click()
            time.sleep(2)
            scholarship_links = browser.find_elements_by_xpath("//div[@class='hit']/a")
            print len(scholarship_links)
            j=0
            for item in scholarship_links:
                data_list = []
                current_url = browser.current_url
                print current_url
                scholarship_links = browser.find_elements_by_xpath("//div[@class='hit']/a")
                data_list.append(page_link)
                
                data_list.append(scholarship_links[j].get_attribute("href"))
                
                scholarship_links[j].click()
                time.sleep(2)
                
                window_after = browser.window_handles[1]
                browser.switch_to_window(window_after)
                
                current_url_new = browser.current_url
                parsed_source = browser.page_source
                final_page_source = html.fromstring(parsed_source, current_url)
#                f = open('abc.html', 'w+')
#                f.write(parsed_source)
                
                try:
                    Scholarship = final_page_source.xpath("//strong[contains(text(),'Scholarship:')]/following-sibling::text()[1]")
                    if Scholarship:
                        print Scholarship
                        data_list.append("".join(Scholarship).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    School_url = final_page_source.xpath("//strong[contains(text(),'School:')]/following-sibling::a[1]/@href")
                    if School_url:
                        url = "".join(School_url)
                        data_list.append("http://www.scholarshipmonkey.com"+url)
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    School_name = final_page_source.xpath("//strong[contains(text(),'School:')]/following-sibling::a[1]/text()")
                    if School_name:
                        data_list.append("".join(School_name).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    Deadline = final_page_source.xpath("//strong[contains(text(),'Deadline:')]/following-sibling::text()[1]")
                    if Deadline:
                        data_list.append("".join(Deadline).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    Amount = final_page_source.xpath("//strong[contains(text(),'Amount:')]/following-sibling::text()[1]")
                    if Amount:
                        data_list.append("".join(Amount).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    SAT = final_page_source.xpath("//strong[contains(text(),'SAT:')]/following-sibling::text()[1]")
                    if SAT:
                        data_list.append("".join(SAT).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    GPA = final_page_source.xpath("//strong[contains(text(),'GPA:')]/following-sibling::text()[1]")
                    if GPA != "":
                        data_list.append("".join(GPA).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    Majors = final_page_source.xpath("//strong[contains(text(),'Majors:')]/following-sibling::text()[1]")
                    if Majors:
                        data_list.append("".join(Majors).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    Website = final_page_source.xpath("//strong[contains(text(),'Website:')]/following-sibling::a[1]/text()")
                    if Website:
                        data_list.append("".join(Website).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                try:
                    Description = final_page_source.xpath("//strong[contains(text(),'Description:')]/following-sibling::text()")
                    if Description:
                        data_list.append(" ".join(Description).strip())
                    else:
                        data_list.append("---")                
                except:
                    pass
                
                print data_list
                data_writer.writerow(data_list)

                browser.close()              
                browser.switch_to_window(window_before)
                browser.get(current_url)
                time.sleep(2)
                j = j+1
            browser.get(starting_url)
            time.sleep(1)
            i = i+1
    
    """
    Starting method, open browser and passes browser object, starting URL to next method.
    """
    def main(self):
        starting_url = "http://www.scholarshipmonkey.com/lists"
        browser = webdriver.Firefox()
        browser.maximize_window()
        self.Extract_data(starting_url, browser)
        browser.close()
    
    
if __name__ == "__main__":
    object_scholarshipmonkey = scholarshipmonkey()
    object_scholarshipmonkey.main()