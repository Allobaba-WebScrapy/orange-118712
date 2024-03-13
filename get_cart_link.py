from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from url_encrypted import encrypt_url

def link(driver, timeout=10):
    cart_link = []   

    WebDriverWait(driver, timeout).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'bi_denomination'))
    )
    
    div_links = driver.find_elements(By.CLASS_NAME, 'bi_denomination')
    for links in div_links:
        try:
            link = links.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            class_link = links.find_element(By.TAG_NAME, "span").get_attribute("class")
            take_link = re.search(r'adpJam_tgt_(.*)', class_link).group(1)
            encrypt = encrypt_url(take_link)
            link =encrypt.replace("//", "http://")
        if link not in cart_link:
            cart_link.append(link)
    return cart_link