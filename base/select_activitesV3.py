from seleniumbase import SB 
from selenium.common.exceptions import TimeoutException

class ActivitesScraper:
    def __init__(self, sb):
         self.sb = sb
    def find_name_and_lien_of_activites(self):
        list_de_name_activites = []
        list_de_lien_activites = []
        try:
            if self.sb.wait_for_element_visible("section.homeHero-container", timeout=20):
                yield {"type": "progress","message":"verefivation passed"}
        except:
            print("Page Jaune not found!")
            return
        
        if  self.sb.is_element_present("ul.dropdown-list"):
            list_activites = self.sb.find_elements("ul.dropdown-list li a")

            for a in list_activites:
                list_de_lien_activites.append(a.get_attribute("href"))
                list_de_name_activites.append(a.get_attribute("innerHTML").replace('\n', ''))
                
        return {"name": list_de_name_activites, "link": list_de_lien_activites}




# with SB(
#              uc_cdp=True,
#             guest_mode=True,
#             headless=False,
#             undetected=True,
#             timeout_multiplier=1,
#         ) as sb:
#             sb = sb
#             try:
#                 sb.open("https://www.118712.fr/")
#                 sb.wait_for_ready_state_complete(timeout=20)
#             except TimeoutException:
#                 print("Page Jaune not found!")
#             scrape = ActivitesScraper(sb)
#             print(scrape.find_name_and_lien_of_activites())
