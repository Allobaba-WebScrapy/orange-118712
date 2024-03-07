from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import re
from select_activites import link

#----------------------------------------------------------
def click_button_and_scrap_page(driver, onclick_value, timeout=10):

    # Click the button of next page by the function name
    try:
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[@onclick='{onclick_value}']"))
        )
        button.click()
    except TimeoutException:
        print("Timeout while waiting for the button")

    # Wait for new elements to load after clicking the button
    try:
        # Wait for elements with class 'h4' to be visible
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'h4'))
        )
        # Scraping the page
        titles = driver.find_elements(By.CLASS_NAME, 'h4')
        for title in titles:
            if(title.text not in cart):
                cart.append(title.text)
    except TimeoutException:
        print("Timeout while waiting for elements to be visible.")

#----------------------------------------------------------

# Initialize the WebDriver
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome()
driver.get(link)


# Click the button of coockies
button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn')))
button2.click()

j = 1
# How many button in next page button
if(driver.find_elements(By.CLASS_NAME, 'len3')):
    page_next = driver.find_elements(By.CLASS_NAME, 'len3')
elif(driver.find_elements(By.CLASS_NAME, 'len2')):
    page_next = driver.find_elements(By.CLASS_NAME, 'len2')
else:
    page_next = driver.find_elements(By.CLASS_NAME, 'len1')
    j = 2

num_of_button_pageNext = len(page_next)
event_name = page_next[num_of_button_pageNext - j].get_attribute("onclick")

number_of_pages = int(re.search(r'\d+', event_name).group()) # changePageUseCurrentBounds(50) ---> 50

cart =[] #array of tittle cart
# function of scraping all page in one activites
for i in range(1,number_of_pages+1):
    click_button_and_scrap_page(driver, f'changePageUseCurrentBounds({i})')

print(cart)


driver.quit()