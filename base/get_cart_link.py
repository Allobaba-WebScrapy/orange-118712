from selenium.webdriver.support import expected_conditions as EC
import re
from url_encrypted import encrypt_url

def link(sb, timeout=10):
    cart_link = []   

    if  sb.is_element_visible("div.bi_denomination"):
        div_links = sb.find_elements("div.bi_denomination")
    
    for links in div_links:
        try:
            link = links.find_element("a").get_attribute("href")
        except:
            class_link = links.find_element("span").get_attribute("class")
            take_link = re.search(r'adpJam_tgt_(.*)', class_link).group(1)
            encrypt = encrypt_url(take_link)
            link =encrypt.replace("//", "http://")
        if link not in cart_link:
            cart_link.append(link)
            
    return cart_link