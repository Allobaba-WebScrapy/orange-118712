from seleniumbase import SB
from selenium.common.exceptions import TimeoutException
import re
from select_activitesV2 import ActivitesScraper
from cart_scrape import INFOCART
from flask import Flask, jsonify , Response, request
from flask_cors import CORS
import json
from get_cart_link import link

app = Flask(__name__)
CORS(app)

class Scraper:
    def __init__(self,activites_name,type,number_of_pages):
        self.activites_name = activites_name
        self.number_of_pages = number_of_pages
        self.type = type

        self.carts = []
        self.links = []
        self.links_scrape = []

    # Wait for the body element to be visible
    def click_button_and_get_data(self, onclick_value,first_link,sb):
        try:
            if sb.is_element_visible(f"xpath://button[@onclick='{onclick_value}']"):
                sb.click(f"xpath://button[@onclick='{onclick_value}']")
        except TimeoutException:
            print("next page timeout")

        try:
            cart_links = link(sb)
            for cart_link in cart_links:
                if cart_link not in self.links:
                    self.links.append(cart_link)
                    self.links_scrape.append(cart_link)
            for i in range(0,len(self.links_scrape)):
                cart = INFOCART(sb, self.links_scrape[i],self.type).all_info_of_cart()
                if cart != None:
                    self.carts.append(cart)
                    yield self.carts[-1]
                else:
                    continue
            self.links_scrape = []
            sb.open(first_link)


        except TimeoutException:
            print("carts timeout")

    def scrape_activites(self):
        with SB(
            uc_cdp=True,
            guest_mode=True,
            headless=False,
            undetected=True,
            timeout_multiplier=1,
            agent="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36"
        ) as sb:
            self.sb = sb
            try:
                self.sb.open("https://www.118712.fr/")
                self.sb.wait_for_ready_state_complete(timeout=20)
            except TimeoutException:
                print("Page Jaune not found!")

            activites = ActivitesScraper(self.sb).find_name_and_lien_of_activites()

            index_name = activites['name'].index(self.activites_name)
            links = activites['link']
            link = links[index_name]

            self.sb.wait_for_ready_state_complete(timeout=30)

            self.sb.open(link)
            # click button of cookies
            if self.sb.wait_for_element_visible("button.btn-primary",timeout=5):
                self.sb.click("button.btn-primary")   

            #find class name of last page
            j = 1
            if self.sb.find_elements('button.len3'):
                page_next = self.sb.find_elements('button.len3')
            elif self.sb.find_elements('button.len2'):
                page_next = self.sb.find_elements('button.len2')
            else:
                page_next = self.sb.find_elements('button.len1')
                j = 2

            # get the number of pages
            num_of_button_pageNext = len(page_next)
            event_name = page_next[num_of_button_pageNext - j].get_attribute("onclick")
            number_of_pages = int(re.search(r'\d+', event_name).group())

            #send the pages to the function click_button_and_get_data
            print(self.number_of_pages)
            for i in range(1, self.number_of_pages):
                yield from self.click_button_and_get_data(f'changePageUseCurrentBounds({i})',link,self.sb)
# Usage:


@app.route('/')
def index():
    return "Hello World!"

# @app.route('/setup', methods=['POST'])
# def setup():
#     global scraper
#     data = request.get_json()
#     activites_name = data['activites_name']
#     type = data['type']
#     number_of_pages = int(data['number_of_pages'])
#     scraper = Scraper("Fleuristes","b_to_b",2)
#     return jsonify("ok")


@app.route('/scrape')
def scrape():
    def generate():
        print("scraping")
        scraper = Scraper("Fleuristes","b_to_b",2)
        for cart in scraper.scrape_activites():
            yield f"data: {json.dumps(cart)}\n\n"
        yield "event: done\ndata: Done\n\n"
    return Response(generate(), mimetype='text/event-stream')
    


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=5500)

