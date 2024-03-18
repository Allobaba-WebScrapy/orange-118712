from selenium.common.exceptions import TimeoutException

class INFOCART:
    def __init__(self, sb,link,type):
        self.sb = sb
        self.link = link
        self.type = type
        self.b_to_b = []
        self.b_to_c = []
        self.type_of_cart = "b_to_c"
        self.cart = {"title": "", "category": "", "adress": "", "phone": [], "email": ""}

    def all_info_of_cart(self):
        self.sb.open(self.link)

        # number phone and email
        try:
            if self.sb.is_element_visible("c/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/span[2]"):
                self.sb.click(xpath= "xpath:/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/span[2]")
        except:
            self.cart["email"] = "not found"
                
        try:
            number_phone_div = self.sb.find_elements('div.col-sm-4')
            for buttons in number_phone_div:
                if self.sb.is_element_visible(f"{buttons} span"):
                    self.sb.click(f"{buttons} span")

        except:
            self.cart["phone"] = "not found"
            
        try:
            if self.sb.is_element_visible("a.button-inside-click"):

                email_or_phone = self.sb.find_elements('a.button-inside-click')
                for info in email_or_phone:
                    info_test = info.get_attribute("href")
                    
                    if info_test.startswith("tel:"):
                        phone_number = info_test.replace("tel:", "")
                        if (phone_number.startswith("01") or phone_number.startswith("02")) or phone_number.startswith("04") or phone_number.startswith("05"):
                            self.type_of_cart = "b_to_b"
                        self.cart["phone"].append(phone_number)
                    else:
                        self.cart["email"] = info_test.replace("mailto:", "")

        except TimeoutException:
            print("Timeout while waiting for email and phone number.")

        #---------title and category----------
        try:
            if self.sb.is_element_visible("div.teaser_bloc"):
                try:
                    div_title_category = self.sb.find_elements('div.teaser_bloc h1')
                
                    title = div_title_category.text
                    self.cart["title"] = title
                except:
                    self.cart["title"] = "not found"

                try:
                    div_title_category = self.sb.find_elements('div.teaser_bloc p')

                    category = div_title_category.text
                    self.cart["category"] = category
                except:
                    self.cart["category"] = "not found"
                
        except TimeoutException:
            print("Timeout while waiting for title and category.")
            
        #---------adress----------
        try:
            if self.sb.is_element_visible("span.adress_label"):
                adress = self.sb.find_element('span.adress_label').text
                self.cart["adress"] = adress
        except TimeoutException:
            self.cart["adress"] = "not found"
        
        if self.type_of_cart == "b_to_b":
            self.b_to_b.append(self.cart)
        else:
            self.b_to_c.append(self.cart)
        
        if self.type == "b_to_c":
            if self.b_to_c == []:
                return None
            return self.b_to_c[0]
        elif self.type == "b_to_b":
            if self.b_to_b == []:
                return None
            return self.b_to_b[0]
        else:
            return self.cart