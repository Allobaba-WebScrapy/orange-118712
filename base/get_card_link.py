import re
from url_encrypted import encrypt_url

def link(sb):

    if  sb.wait_for_element_visible("div.bi_denomination"):
        card_link = []  
                
        div_links = sb.find_elements("div.bi_denomination  a")
        div_links2 = sb.find_elements("div.bi_denomination  span")

        for links in div_links:
            link = links.get_attribute("href")
            if link not in card_link:
                card_link.append(link)
        for links in div_links2:
            class_link = links.get_attribute("class")
            take_link = re.search(r'adpJam_tgt_(.*)', class_link).group(1)
            encrypt = encrypt_url(take_link)
            link =encrypt.replace("//", "http://")
            if link not in card_link:
                card_link.append(link)
        
                
        return card_link
