from selenium import webdriver
import csv
from myconfig import *
import time


class twu():
    
    def Extract_Data(self, starting_url, browser):
        myfile = open('twu.csv', "wb")
        data_writer = csv.writer(myfile)
        data_writer.writerow(['First_Name','Last_Name', 'Email_Address'])
        browser.get(starting_url)
        time.sleep(10)
        browser.find_element_by_xpath("//a[contains(text(),'TWU Google Mail')]").click()
        time.sleep(3)
        browser.find_element_by_id('Email').clear()
        browser.find_element_by_id('Email').send_keys(username)
        browser.find_element_by_id('next').click()
        time.sleep(3)
        browser.find_element_by_id('Passwd').clear()
        browser.find_element_by_id('Passwd').send_keys(password)
        browser.find_element_by_id('signIn').click()
        time.sleep(12)
        browser.find_element_by_xpath("//div[@class='asT-asx aQS J-J5-Ji']").click()
        time.sleep(5)
        browser.find_element_by_xpath("//div[contains(text(),'Contacts')]").click()
        time.sleep(5)
        browser.find_element_by_xpath("//a[@title='Directory']").click()
        time.sleep(5)
        
        """
        Extracting details
        """
        
        contacts_list = browser.find_elements_by_xpath("//div[@class='nH' and @style='']//table//tr[contains(@id,':')]")
        i = 1
        length = len(contacts_list)
#        count = length
        while i <= length:
            data_list = []
            try:
                Name = browser.find_element_by_xpath("//div[@class='nH' and @style='']//table//tr[contains(@id,':')]["+str(i)+"]/td[4]/div/span").get_attribute('textContent')
                if " " in Name:
                    first_name = Name.rsplit(" ",1)[0].strip()
                    last_name = Name.rsplit(" ",1)[1].strip()
                    data_list.append(first_name)
                    data_list.append(last_name)
                else:
                    data_list.append(Name)
                    data_list.append('---')
            except:
                data_list.append('--')
                data_list.append('--')
                
            try:
                email = browser.find_element_by_xpath("//div[@class='nH' and @style='']//table//tr[contains(@id,':')]["+str(i)+"]/td[4]/div/span").get_attribute('email')
                if email:
                    data_list.append(email.strip())
                else:
                    data_list.append('--')
            except:
                data_list.append('--')
            print data_list
            data_writer.writerow(data_list)
            i = i+1
            if i > length:
                try:
                    browser.find_element_by_xpath("//div[@class='nH' and @style='']//div[@data-tooltip='Next']/img").click()
                    time.sleep(15)
                    i = 1
                    next_page_list = browser.find_elements_by_xpath("//div[@class='nH' and @style='']//table//tr[contains(@id,':')]")
                    Next_page_length = len(next_page_list)
                    length = Next_page_length
                except:
                    pass
            else:
                pass
                
                
    """
    Starting method, open browser and passes browser object, starting URL to next method.
    """
    def main(self):
        starting_url = "http://webmail.twu.edu/"
        browser = webdriver.Firefox()
        browser.maximize_window()
        self.Extract_Data(starting_url, browser)
#        browser.close()
    
    
if __name__ == "__main__":
    object_fmcsa = twu()
    object_fmcsa.main()