from bs4 import BeautifulSoup
import requests, json
import sys
# Set headers
headers = requests.utils.default_headers()
# headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
def getTweakersLink(ean):

    tweakers_api = "https://tweakers.net/xmlhttp/xmlHttp.php?application=sitewidesearch&type=search&action=pricewatch&keyword="+ean+"&output=json"
    req = requests.get(tweakers_api)
    try:
        entity = json.loads(req.content)['entities'][0]
        print(entity['name'])
        return entity['name'],entity['link'].replace(".html","/specificaties")
    except:
        print("Not found")
        return
def getArticleSpecs(url,driver):
    if not url:
        return
    driver.get(url)
    elem = None
    try:
        elem = driver.find_element_by_name('decision')
    except:
        pass
    if elem:
        elem.click()
    # title=driver.find_elements_by_tag_name("h1")[0].find_elements_by_tag_name("a")[0]
    table = driver.find_element_by_class_name('popularSpecs')
    specs=[]
    for row in table.find_elements_by_xpath(".//tr"):
        specs.append([td.text.split('\n')[0] for td in row.find_elements_by_xpath(".//td")])
    return specs

def generate_label(products):
    from blabel import LabelWriter
    label_writer = LabelWriter("item_template.html",default_stylesheets=("style.css",))
    records= [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2")
    ]

    label_writer.write_labels(products, target='logo_and_datamatrix.pdf',base_url='.')



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox()
# options=options)
products = []
ean = "4038986146494"
title, link = getTweakersLink(ean)
specs = getArticleSpecs(link,driver)
driver.close()

if title:
    # products.append({"title":title,"specs":specs,"price":input("Price: "),"ean":ean})
    products.append({"title":title,"specs":specs,"price":"229,-","ean":ean})
generate_label(products)
