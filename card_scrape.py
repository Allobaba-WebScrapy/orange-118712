class INFOCARD:
    def __init__(self, sb, link, type):
        self.sb = sb
        self.link = link
        self.type = type
        self.B2B = []
        self.B2C = []
        self.type_of_card = "B2C"
        self.card = {
            "title": "",
            "category": "",
            "adress": {"text": "", "link": ""},
            "phone": [],
            "email": "",
        }

    def all_info_of_card(self):
        self.sb.open(self.link)
        self.sb.wait_for_ready_state_complete(timeout=10)

        # number phone and email
        try:
            if self.sb.is_element_visible(
                "/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/span[2]"
            ):
                self.sb.click(
                    "/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/span[2]"
                )
        except:
            self.card["email"] = "not found"

        try:
            number_phone_div = self.sb.find_elements("div.col-sm-4")
            for button in number_phone_div:
                button.click()
        except:
            self.card["phone"] = "not found"

        try:
            if self.sb.is_element_visible("a.button-inside-click"):

                email_or_phone = self.sb.find_elements("a.button-inside-click")
                for info in email_or_phone:
                    info_test = info.get_attribute("href")

                    if info_test.startswith("tel:"):
                        phone_number = info_test.replace("tel:", "")
                        if (
                            (
                                phone_number.startswith("01")
                                or phone_number.startswith("02")
                            )
                            or phone_number.startswith("04")
                            or phone_number.startswith("05")
                        ):
                            self.type_of_card = "B2B"
                        self.card["phone"].append(phone_number)
                    else:
                        self.card["email"] = info_test.replace("mailto:", "")

        except:
            print("Timeout while waiting for email and phone number.")

        # ---------title and category----------
        try:
            try:
                if self.sb.is_element_visible("h1.h2"):
                    div_title_category = self.sb.find_element("h1.h2")

                    title = div_title_category.text
                    self.card["title"] = title
            except:
                self.card["title"] = "not found"

            try:
                if self.sb.is_element_visible("p.teaser_category"):

                    div_title_category = self.sb.find_element("p.teaser_category")

                    category = div_title_category.text
                    self.card["category"] = category
            except:
                self.card["category"] = "not found"

        except:
            print("Timeout while waiting for title and category.")

        # ---------adress----------
        try:
            if self.sb.is_element_visible("span.adress_label"):
                text = self.sb.find_element("span.adress_label").text
                link = self.sb.find_element(
                    "/html/body/div[2]/main/div[2]/div[1]/section[1]/div[1]/a"
                ).get_attribute("href")
                self.card["adress"]["text"] = text
                self.card["adress"]["link"] = link

        except:
            self.card["adress"]["text"] = "not found"
        # -------------------------
        if self.type_of_card == "B2B":
            self.B2B.append(self.card)
        else:
            self.B2C.append(self.card)

        if self.type == "B2C":
            if self.B2C == []:
                return None
            return self.B2C[0]
        elif self.type == "B2B":
            if self.B2B == []:
                return None
            return self.B2B[0]
        else:
            return self.card
