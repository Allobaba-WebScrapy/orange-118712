from selenium.webdriver.support import expected_conditions as EC
import re
from url_encrypted import encrypt_url
from seleniumbase import SB 
from selenium.common.exceptions import TimeoutException

def link(sb):

    if  sb.wait_for_element_visible("div.bi_denomination"):
        cart_link = []  
                
        div_links = sb.find_elements("div.bi_denomination  a")
        div_links2 = sb.find_elements("div.bi_denomination  span")

        for links in div_links:
            link = links.get_attribute("href")
            if link not in cart_link:
                cart_link.append(link)
        for links in div_links2:
            class_link = links.get_attribute("class")
            take_link = re.search(r'adpJam_tgt_(.*)', class_link).group(1)
            encrypt = encrypt_url(take_link)
            link =encrypt.replace("//", "http://")
            if link not in cart_link:
                cart_link.append(link)
        
                
        return cart_link
                
# with SB(
#              uc_cdp=True,
#             guest_mode=True,
#             headless=False,
#             undetected=True,
#             timeout_multiplier=1,
#         ) as sb:
#             sb = sb
#             try:
#                 sb.open("https://www.118712.fr/activite/fleuristes")
#                 sb.wait_for_ready_state_complete(timeout=20)
#             except TimeoutException:
#                 print("Page Jaune not found!")
#             print(link(sb))