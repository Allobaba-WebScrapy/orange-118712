
from seleniumbase import SB
from selenium.common.exceptions import TimeoutException

class ActivitesScraper:

    def find_name_and_lien_of_activites(self,sb):
        
        list_de_name_activites = []
        list_de_lien_activites = []
        
        if  sb.wait_for_element("ul.dropdown-list",timeout=20):
            list_activites = sb.find_elements("ul.dropdown-list li")
            for a in list_activites:
                a_elements = a.find_elements("a")
                for a_element in a_elements:
                    list_de_lien_activites.append(a_element.get_attribute("href"))
                    list_de_name_activites.append(a_element.get_attribute("innerHTML").replace('\n', ''))
            
            return {"name": list_de_name_activites, "link": list_de_lien_activites}
