from bs4 import BeautifulSoup
import requests, json
import sys, os
import time

_ = os.system("clear")

def getTweakersLink(ean):
    print("Loading product information...")
    tweakers_api = "https://tweakers.net/xmlhttp/xmlHttp.php?application=sitewidesearch&type=search&action=pricewatch&keyword="+ean+"&output=json"
    req = requests.get(tweakers_api)
    try:
        entity = json.loads(req.content)['entities'][0]
        return entity['name'],entity['link'].replace(".html","/specificaties")
    except:
        print("EAN not found")
        return False, False


def getArticleSpecs(url,driver):
    print("     * Scraping specifications...")
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
    print("     * Parsing specifications...")
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

print("Loading sneaky browser....")
options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
print("Sneaky browser loaded and sneaky")
print("Loading EAN database link...")
products = []

while True:
    _ = os.system("clear")
    print("**BENBELLEN Labeling system v0.1 [FOR INTERNAL USE ONLY]**")
    if len(products) > 0:
        print("You have the following items in your label basket...")
        for p in products:
            print(" - "+p['title']+" | "+p['price']+" | "+p['ean'])
        print("\n")
    try:
        ean = input("Scan EAN or hit enter to continue...\n ")
    except KeyboardInterrupt:
        driver.close()
        print("All done")
        raise
    if ean is "":
        break
    title, link = getTweakersLink(ean)
    if title:
        print("\n\nInsert price for | "+title+" | with EAN |"+ean+"|")
        products.append({"link":link,  "title":title,"specs":None,"price":input("Price: "),"ean":ean})

_ = os.system("clear")

print("Currently processing")
for i,p in enumerate(products):
    print("\n - "+p['title']+" | "+p['price']+" | "+p['ean'])
    specs = getArticleSpecs(p['link'],driver)
    products[i]['specs'] = specs

print("\nHiding sneaky browser...")
driver.close()


print("\n")
print("Generating PDF...")
generate_label(products)
_ = os.system("clear")
print("Fuck you Bjorn")
time.sleep(0.5)
_ = os.system("clear")
