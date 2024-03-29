from seleniumbase import SB
import re
from card_scrape import INFOCARD
from flask import Flask, jsonify , Response, request
from flask_cors import CORS
import json
from get_card_link import link

app = Flask(__name__)
CORS(app)

class Scraper:
    def __init__(self,activites_name,type,start_page,limit_page):
        self.activites_name = activites_name
        self.start_page = start_page
        self.limit_page = limit_page
        self.type = type

        self.cards = []
        self.links = []
        self.links_scrape = []

    # Wait for the body element to be visible
    def click_button_and_get_data(self, onclick_value,first_link,sb,index):

        yield {"type": "progress","message":f"Scrape Page {index}/{self.limit_page}"}

        try:
            if sb.is_element_visible(f"xpath://button[@onclick='{onclick_value}']"):
                sb.click(f"xpath://button[@onclick='{onclick_value}']")
        except:
            print("next page timeout")

        try:
            card_links = link(sb)
            yield {"type": "progress","message":"Get Non Deplicate Card","card_progress":{"nCard":0, "length":0}}
            for card_link in card_links:
                if card_link not in self.links:
                    self.links.append(card_link)
                    self.links_scrape.append(card_link)
            number_cards = len(self.links_scrape)
            if number_cards == 0:
                yield {"type": "progress","message":"All Card is Duplicate"}

            card_that_scrape = 0
            for i in range(0,number_cards):
                card = INFOCARD(sb, self.links_scrape[i],self.type).all_info_of_card()
                print(card)
                if card != None:
                    self.cards.append(card)
                    card_that_scrape += 1
                    yield {"type":"response","message":self.cards[-1],"process":{"nCard":i+1, "length":number_cards}}
                else:
                    yield {"type":"response","process":{"nCard":i+1, "length":number_cards}}

            yield {"type": "progress","message":f"{card_that_scrape} {self.type} cards successfully scraped"}
            self.links_scrape = []
            sb.open(first_link)
        except:
            yield {"type":"error","message":"Error in scraping cards"}

    def scrape_activites(self):
        with SB(
            uc_cdp=True,
            guest_mode=True,
            headless=True,
            undetected=True,
            timeout_multiplier=1,
        ) as sb:
            self.sb = sb
            self.sb.open("https://www.118712.fr/")
            self.sb.wait_for_ready_state_complete(timeout=10)
            
            # def find_name_and_lien_of_activites(self):
            list_de_name_activites = []
            list_de_lien_activites = []
            try:
                if self.sb.wait_for_element_visible("section.homeHero-container",timeout=10):
                    yield {"type": "progress","message":"Verefivation passed"}
            except:
                print("verefecation fails")
            
            if  self.sb.is_element_present("ul.dropdown-list"):
                list_activites = self.sb.find_elements("ul.dropdown-list li a")

                for a in list_activites:
                    list_de_lien_activites.append(a.get_attribute("href"))
                    list_de_name_activites.append(a.get_attribute("innerHTML").replace('\n', ''))

            try:
                index_name = list_de_name_activites.index(self.activites_name)
                links = list_de_lien_activites
                link = links[index_name]
                self.sb.open(link)

                # click button of cookies
                if self.sb.wait_for_element_visible("button.btn-primary",timeout=10):
                    self.sb.click("button.btn-primary")
                # yield {"type": "progress","message":"Cockies accepted"}

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
                if (self.start_page > number_of_pages):
                    yield {"type":"error","message":"The start page is greater than the number of pages"}
                    return
                elif (self.start_page + self.limit_page > number_of_pages + 1):
                    self.limit_page = number_of_pages - self.start_page + 1
                    yield {"type":"progress","message":f"Limit number is greater than the total page number! Adjusted to {self.limit_page}"}

                #send the pages to the function click_button_and_get_data
                for index,i in enumerate(range(self.start_page, self.start_page + self.limit_page)):
                    if  (i <= number_of_pages):
                        yield from self.click_button_and_get_data(f'changePageUseCurrentBounds({i})',link,self.sb,index+1)
            except:
                yield {"type":"error","message":"Verification failed"}
# Usage:


@app.route('/')
def index():
    return "Hello World!"

@app.route('/setup', methods=['POST'])
def setup():
    global scraper
    data = request.get_json()
    activites_name = data['activites_name']
    type = data['type']
    start_pages = int(data['start_pages'])
    limit_pages = int(data['limit_pages'])
    scraper = Scraper(activites_name,type,start_pages,limit_pages)
    return jsonify("ok")


@app.route('/scrape')
def scrape():
    def generate():
        results = []
        yield f"data: {json.dumps({'type': 'progress', 'message': 'Scraping Starting...'})}\n\n"
        # scraper = Scraper("Fleuristes","B2C",1,1)

        for result in scraper.scrape_activites():
            if(result["type"]=="response"):
                results.append(result)
            yield f"data: {json.dumps(result)}\n\n"
        if(results):
            yield "event: done\ndata: Done\n\n"
        else:
            yield f"event: error\ndata:{json.dumps({'type':'error', 'message':'Verification failed No result'})}\n\n"
    return Response(generate(), mimetype='text/event-stream')
    


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=4933)

