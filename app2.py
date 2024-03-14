from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from select_activitesV2 import ActivitesScraper
from cart_scrape import INFOCART
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify , Response, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
from get_cart_link import link

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
socketio = SocketIO(app, cors_allowed_origins='*')

class Scraper:
    def __init__(self,activites_name,type,number_of_pages):
        self.activites_name = activites_name
        self.number_of_pages = number_of_pages
        self.type = type
        chrome_options = Options()
        chrome_options.add_argument('--user-agent=Chrome/123.0.6312.31')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)

        self.carts = []

    # Wait for the body element to be visible
    def click_button_and_get_data(self, onclick_value, timeout=10):
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@onclick='{onclick_value}']"))
            )
            button.click()
        except TimeoutException:
            print("Timeout while waiting for the button")

        try:
            cart_link = link(self.driver)
            for i in range(0,len(cart_link)):
                cart = INFOCART(self.driver, cart_link[i],self.type).all_info_of_cart()
                if cart != None:
                    self.carts.append(cart)
                    yield self.carts[-1]
                else:
                    continue

        except TimeoutException:
            print("Timeout while waiting for elements to be visible.")

    def scrape_activites(self):
        activites = ActivitesScraper(self.driver).find_name_and_lien_of_activites()

        index_name = activites['name'].index(self.activites_name)
        links = activites['link']
        link = links[index_name]

        self.driver.get(link)
        
        # click button of cookies
        button2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn')))
        button2.click()

        #find class name of last page
        j = 1
        if self.driver.find_elements(By.CLASS_NAME, 'len3'):
            page_next = self.driver.find_elements(By.CLASS_NAME, 'len3')
        elif self.driver.find_elements(By.CLASS_NAME, 'len2'):
            page_next = self.driver.find_elements(By.CLASS_NAME, 'len2')
        else:
            page_next = self.driver.find_elements(By.CLASS_NAME, 'len1')
            j = 2

        # get the number of pages
        num_of_button_pageNext = len(page_next)
        event_name = page_next[num_of_button_pageNext - j].get_attribute("onclick")
        number_of_pages = int(re.search(r'\d+', event_name).group())

        #send the pages to the function click_button_and_get_data
        for i in range(1, self.number_of_pages):
            yield from self.click_button_and_get_data(f'changePageUseCurrentBounds({i})')
        self.driver.quit()

# Usage:
# @app.route('/')
# def index():
#     return "Hello World!"

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     data = request.json
#     activity_name = data['activityName']
#     activity_type = data['activityType']
#     number_of_pages = int(data['numberOfPages'])
#     scraper = Scraper(activity_name, activity_type, number_of_pages)
    
#     def generate():
#         for cart in scraper.scrape_activites():
#             yield json.dumps({"Cart": cart}) + "\n"

#     return Response(generate(), mimetype='text/event-stream')


# if __name__ == "__main__":
#     app.run(host = '0.0.0.0',port=5000)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    activity_name = data['activityName']
    activity_type = data['activityType']
    number_of_pages = int(data['numberOfPages'])
    scraper = Scraper(activity_name, activity_type, number_of_pages)
    
    def generate():
        for cart in scraper.scrape_activites():
            yield json.dumps({"Cart": cart}) + "\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)