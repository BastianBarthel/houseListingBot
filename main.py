import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

CHROME_DRIVER_PATH = "/Applications/chromedriver"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeK3v1iZL8x_84Ob1vtzKZ5uJsQ0w7qrfub7Sjwrr32hC-Jbg/viewform?usp=sf_link"
ZILLOW = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds" \
         "%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37" \
         ".626703706369355%2C%22north%22%3A37.923581166124535%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C" \
         "%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf" \
         "%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000" \
         "%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value" \
         "%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22" \
         "%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D "

headers = {
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
}

# Scraping the listings from Zillow
response = requests.get(ZILLOW, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

addresses = [address.text for address in soup.find_all(name="address", class_="list-card-addr")]

prices = []
for price in soup.find_all(name="div", class_="list-card-price"):
    if "/" in price.text:
        prices.append(price.text.split("/")[0])
    else:
        prices.append(price.text.split("+")[0])

link_elements = soup.select(".list-card-top a")
links = []
for link in link_elements:
    href = link["href"]
    if "http" not in href:
        links.append(f"https://www.zillow.com{href}")
    else:
        links.append(href)

# Filling in the Google Forms
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM)

for n in range(len(addresses)-1):
    first_answer = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    second_answer = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    third_answer = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    first_answer.send_keys(addresses[n])
    second_answer.send_keys(prices[n])
    third_answer.send_keys(links[n])
    submit_button.click()
    time.sleep(1)
    send_more = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    send_more.click()
    time.sleep(2)

# Closing the browser
driver.quit()
