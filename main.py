from bs4 import BeautifulSoup
import requests
import lxml
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver = webdriver.Chrome(options=chrome_options)
CHROME_DRIVER_PATH = r"C:\Users\hasan\Development\chromedriver.exe"


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScKzUyT0dCohDmUKCL4maM1FvthSmgulYDaHhn1lLHGeSiR2g/viewform?usp=sf_link"
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

links_list = []
addresses_list = []
prices_list = []

response = requests.get(url=URL, headers=headers)
response.raise_for_status()
content = response.text
soup = BeautifulSoup(content, "html.parser")

links = soup.find_all(name="a", class_="property-card-link")
for link in links:
    if not link.get("href").startswith("http"):
        link = "https://www.zillow.com" + link.get("href")
        links_list.append(link)
    else:
        links_list.append(link.get("href"))

adresses = soup.find_all(class_="property-card-link")
for adress in adresses:
    try:
        addresses_list.append(adress.getText().split("|")[1].strip())
    except IndexError:
        addresses_list.append(adress.getText())
addresses_list = [item for item in addresses_list if item != ""]


prices = soup.find_all(class_="StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 bqsBln")
for price in prices:
    try:
        prices_list.append(price.getText().split("+")[0])
    except IndexError:
        prices_list.append(price.getText().split("/")[0])


service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

for i in range(len(prices_list)):
    driver.get(FORM_URL)
    time.sleep(2)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses_list[i])
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices_list[i])
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links_list[i])
    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit_btn.click()
    time.sleep(2)
    new_response_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    new_response_btn.click()
    time.sleep(2)
