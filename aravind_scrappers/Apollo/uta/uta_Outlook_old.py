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
        browser.find_element_by_id("cred_userid_inputtext").clear()
        browser.find_element_by_id("cred_userid_inputtext").send_keys("amin.patel@mavs.uta.edu")
        browser.find_element_by_id("cred_password_inputtext").clear()
        browser.find_element_by_id("cred_password_inputtext").send_keys("FCdallas786")
        time.sleep(5)
        browser.find_element_by_id("cred_sign_in_button").click()
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
            data_writer = csv.writer(open("uta.csv", "wb"))
            data_writer.writerow(['First Name', 'Middle Name', 'Last Name', 'Job Title', 'Email Address'])
            i = 1
            dir_item = browser.find_element_by_xpath("//div[@class='_ph_I2 scrollContainer']//div[@class='_ph_T2']["+str(i)+"]//span[@class='_pe_f _pe_B']")
            while dir_item:
                dir_item.click()
                time.sleep(7)
                item_name = browser.find_element_by_xpath("//div[@class='_ph_I2 scrollContainer']//div[@class='_ph_T2']["+str(i)+"]//span[@class='_pe_f _pe_B']/span").get_attribute('textContent').strip()
                try:
                    item_name_list = browser.find_elements_by_xpath("//div[contains(@aria-label,'"+str(item_name)+"')]//following::span[@class='_pe_d _pe_e _pe_o _pe_i1 owaimg presence presenceUnknown presenceSizeMedium']")
                    num = len(item_name_list)
                    print num
                    for a in range(num):
                        data_list = [] 
                        try:
                            name = browser.find_element_by_xpath("//span[@class='_pe_V ms-font-size-xxl ms-font-color-neutralPrimary _pe_j _pe_L bidi allowTextSelection _pe_l1 _pe_M ms-fwt-l']").get_attribute('textContent')
                            if ',' in name:
                                name_split = name.split(',')
                                first_second_name = name_split[0]
                                if " " in first_second_name:
                                    str_len = len(first_second_name)
                                    name_split_first = first_second_name.split(" ")
                                    first_name = name_split_first[0]
                                    second_name = " ".join(name_split_first[1:str_len])
                                    data_list.append(first_name.replace(u'\xe9', ''))
                                    data_list.append(second_name.replace(u'\xe9', ''))
                                else:
                                    data_list.append(first_second_name.replace(u'\xe9', ''))
                                    data_list.append("")
                                last_name = name_split[1]
                                data_list.append(last_name.replace(u'\xe9', ''))
                                
                            elif " " in name:
                                name_split = name.split(" ")
                                if len(name_split) >= 3:
                                    str_len_2 = len(name_split)
                                    data_list.append(name_split[0].replace(u'\xe9', ''))
                                    data_list.append(name_split[1].replace(u'\xe9', ''))
                                    data_list.append(" ".join(name_split[2:str_len_2]).replace(u'\xe9', ''))
                                else:
                                    data_list.append(name_split[0].replace(u'\xe9', ''))
                                    data_list.append("")
                                    data_list.append(name_split[1].replace(u'\xe9', ''))
                            else:
                                data_list.append(name.replace(u'\xe9', ''))
                                data_list.append("")
                                data_list.append("")
                        except:
                            data_list.append("---")
                            data_list.append("---")
                            data_list.append("---")
                        
                        try:
                            job_title = browser.find_element_by_xpath("//span[contains(text(),'Job title:')]/following-sibling::span[1]/span").get_attribute('textContent')
                            if job_title != "":
                                data_list.append(job_title.replace(u'\xa0', ''))
                            else:
                                data_list.append("---")                
                        except:
                            data_list.append("---")
                        
                        try:
                            email = browser.find_element_by_xpath("//span[contains(text(),'Email:')]/following-sibling::a[1]/span | //a[@class='o365button']/span[contains(text(),'@')]").get_attribute('textContent')
                            if email:
                                data_list.append(email)
                            else:
                                data_list.append('---')
                        except:
                            data_list.append("---")
                        
                        print data_list
                        try:
                            data_writer.writerow(data_list)
                        except:
                            pass
                        try:
                            browser.find_element_by_xpath("/descendant::span[@class='_pe_f _pe_B'][span[contains(text(),'"+str(name).strip()+"')]][last()]/following::span[@class='_pe_f _pe_B'][1]/span").click()
                            time.sleep(5)
                        except:
                            pass
                except:
                    pass
                time.sleep(5)
                i = i+1
                try:
                    dir_item = browser.find_element_by_xpath("//div[@class='_ph_T2'][not(following-sibling::div)]//span[@class='_pe_f _pe_B']/span")
                except:
                    pass
        except:
            pass
        
    """
    Starting method, open browser and passes browser object, starting URL to next method.
    """
    def main(self):
        starting_url = "https://login.microsoftonline.com/login.srf?wa=wsignin1.0&rpsnv=4&ct=1439096331&rver=6.6.6556.0&wp=MBI_SSL&wreply=https:%2F%2Foutlook.office365.com%2Fowa%2F%3Frealm%3Dmavs.uta.edu&id=260563&whr=mavs.uta.edu&CBCXT=out"
        browser = webdriver.Firefox()
        browser.maximize_window()
        self.login(starting_url, browser)
        browser.close()
    
if __name__ == "__main__":
    object_smu = smu()
    object_smu.main()
