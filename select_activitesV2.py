from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ActivitesScraper:
    def __init__(self, driver):
        self.driver = driver

    def find_name_and_lien_of_activites(self):
        self.driver.get('https://www.118712.fr/')
        list_de_name_activites = []
        list_de_lien_activites = []
        
        list_activites = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdown-list"))
        ).find_elements(By.TAG_NAME, "li")

        for a in list_activites:
            a_elements = a.find_elements(By.TAG_NAME, "a")
            for a_element in a_elements:
                list_de_lien_activites.append(a_element.get_attribute("href"))
                list_de_name_activites.append(a_element.get_attribute("innerHTML").replace('\n', ''))
        
        return {"name": list_de_name_activites, "link": list_de_lien_activites}
