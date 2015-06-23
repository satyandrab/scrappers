from selenium import webdriver
import csv
from lxml import html
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class smu:
    
    """
    Login to outlook
    """
    def login (self, starting_url, browser):
        browser.get(starting_url)
        time.sleep(10)
        browser.find_element_by_id("userNameInput").clear()
        browser.find_element_by_id("userNameInput").send_keys("avenkatarama@smu.edu")
        browser.find_element_by_id("passwordInput").clear()
        browser.find_element_by_id("passwordInput").send_keys("Buy1Teach1$")
        browser.find_element_by_id("submitButton").click()
        time.sleep(10)
        try:
            if browser.find_element_by_xpath("//button[@class='refreshPageButton']"):
                browser.find_element_by_xpath("//button[@class='refreshPageButton']").click()
        except:
            pass
        time.sleep(10)
        self.Open_Address_Book(browser)
        
    """
    open the address book
    """
    def Open_Address_Book(self, browser):
        browser.find_element_by_id("O365_MainLink_NavMenu").click()
        time.sleep(5)
        browser.find_element_by_xpath("//span[@class='o365cs-nav-appTileIcon owaimg wf wf-size-x22 wf-o365-peoplelogo wf-family-o365 ms-fcl-w']").click()
        time.sleep(30)
        browser.find_element_by_xpath("//span[@title='Directory']").click()
        time.sleep(10)
        self.extract_data(browser) 
        
    """
    Create the blank csv file and extract data
    """
    def extract_data(self, browser):
        try:
            data_writer = csv.writer(open("smu.csv", "wb"))
            data_writer.writerow(['First Name', 'Last Name', 'Email Address', 'Job Title'])
            i = 1
            dir_item = browser.find_element_by_xpath("//div[@class='_ph_z2 scrollContainer']//div[@class='_ph_K2']["+str(i)+"]//span[@class='_pe_i _pe_C']")
            while dir_item:
                dir_item.click()
                time.sleep(5)
                item_name = dir_item.get_attribute('textContent').strip()
                try:
                    item_name_list = browser.find_elements_by_xpath("//div[contains(@aria-label,'"+str(item_name)+"')]//following::span[@class='_pe_R ms-fwt-sl ms-font-color-neutralPrimary _pe_p bidi _pe_q disableTextSelection']")
                    num = len(item_name_list)
                    print num
                    for a in range(num):
                        data_list = [] 
                        try:
                            name = browser.find_element_by_xpath("//span[@class='_pe_U ms-fwt-r ms-font-color-neutralPrimary _pe_z _pe_K bidi allowTextSelection _pe_q1 _pe_L']").get_attribute('textContent')
                            if ',' in name:
                                name_split = name.split(',')
                                first_name = name_split[1]
                                second_name = name_split[0]
                                data_list.append(first_name.replace(u'\xe9', ''))
                                data_list.append(second_name.replace(u'\xe9', ''))
                            else:
                                data_list.append(name.replace(u'\xe9', ''))
                                data_list.append("")
                        except:
                            pass
                            
                        try: 
                            email = browser.find_element_by_xpath("//div[@class='_rpc_C']//*[contains(text(),'@')] | //div[@class='_mg_D']//*[contains(text(),'@')]").get_attribute('textContent')
                            data_list.append(email)
                        except:
                            try:
                                email2 = browser.find_element_by_xpath("//div[@class='_pe_b _pe_A1']//*[contains(text(),'@')]").get_attribute('textContent')
                                if email2:
                                    data_list.append(email2)
                                else:
                                    data_list.append('---')
                            except:
                                pass
                        
                        try:
                            job_title = browser.find_element_by_xpath("//span[@class='_pe_U ms-fwt-r ms-font-color-neutralPrimary _pe_z _pe_K bidi allowTextSelection _pe_q1 _pe_L']/following-sibling::span[2] | //span[contains(text(),'Job title:')]/following-sibling::span[1]/span").get_attribute('textContent')
                            if job_title != "":
                                data_list.append(job_title.replace(u'\xa0', ''))
                            else:
                                data_list.append("---")                
                        except:
                            pass
                        
                        print data_list
                        try:
                            data_writer.writerow(data_list)
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath("/descendant::span[@class='_pe_i _pe_C'][span[contains(text(),'"+str(name).strip()+"')]][last()]/following::span[@class='_pe_i _pe_C'][1]/span").click()
                            time.sleep(5)
                        except:
                            pass
                except:
                    pass
                time.sleep(5)
                i = i+1
                try:
                    dir_item = browser.find_element_by_xpath("//div[@class='_ph_K2'][not(following-sibling::div)]//span[@class='_pe_R ms-fwt-sl ms-font-color-neutralPrimary _pe_p bidi _pe_q disableTextSelection']")
                except:
                    pass
        except:
            pass
        
    """
    Starting method, open browser and passes browser object, starting URL to next method.
    """
    def main(self):
        starting_url = "https://adfs.smu.edu/adfs/ls/?wa=wsignin1.0&wtrealm=urn:federation:MicrosoftOnline&wctx=wa%3Dwsignin1.0%26rpsnv%3D4%26ct%3D1433451891%26rver%3D6.6.6556.0%26wp%3DMBI_SSL%26wreply%3Dhttps:%252F%252Foutlook.office365.com%252Fowa%252F%253Frealm%253Dsmu.edu%2526authRedirect%253Dtrue%26id%3D260563%26whr%3Dsmu.edu%26CBCXT%3Dout"
        browser = webdriver.Firefox()
        browser.maximize_window()
        self.login(starting_url, browser)
        browser.close()
    
if __name__ == "__main__":
    object_smu = smu()
    object_smu.main()
