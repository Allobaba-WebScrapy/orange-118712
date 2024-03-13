from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
class INFOCART:
    def __init__(self, driver,link):
        self.driver = driver
        self.link = link
        self.cart = {"title": "", "category": "", "adress": "", "phone": [], "email": ""}

    def all_info_of_cart(self):
        self.driver.get(self.link)
        
        # number phone and email
        try:
            button_email = WebDriverWait(self.driver, 0).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/span[2]")))
            button_email.click()
        except:
            self.cart["email"] = "not found"
                
        try:    
            number_phone_div = self.driver.find_elements(By.CLASS_NAME, 'col-sm-4')
            for buttons in number_phone_div:
                button = WebDriverWait(buttons, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "span")))
                button.click()

        except:
            self.cart["phone"] = "not found"
            
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'button-inside-click'))
            )
            
            email_or_phone = self.driver.find_elements(By.CLASS_NAME, 'button-inside-click')
            for info in email_or_phone:
                info_test = info.get_attribute("href")
                
                if info_test.startswith("tel:"):
                    phone_number = info_test.replace("tel:", "")
                    self.cart["phone"].append(phone_number)
                else:
                    self.cart["email"] = info_test.replace("mailto:", "")

        except TimeoutException:
            print("Timeout while waiting for elements to be visible.")

        #---------title and category----------
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'teaser_bloc'))
            )
            
            div_title_category = self.driver.find_elements(By.CLASS_NAME, 'teaser_bloc')
            try:
                title = div_title_category[0].find_element(By.TAG_NAME, "h1").text
                self.cart["title"] = title
            except:
                self.cart["title"] = "not found"
            try:
                category = div_title_category[0].find_element(By.TAG_NAME, "p").text
                self.cart["category"] = category
            except:
                self.cart["category"] = "not found"
            
            self.cart["category"] = category
        except TimeoutException:
            print("Timeout while waiting for elements to be visible.")
            
        #---------adress----------
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'adress_label'))
            )
            
            adress = self.driver.find_element(By.CLASS_NAME, 'adress_label').text
            self.cart["adress"] = adress
        except TimeoutException:
            self.cart["adress"] = "not found"
        
        return self.cart
    