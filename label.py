from bs4 import BeautifulSoup
import requests, json
from datetime import datetime
import sys, os
import time
import hashlib

if len(sys.argv) > 1:
    os.system("rm *.pdf")
    sys.exit(0)

_ = os.system("clear")
def printFile(filename):
    printers = os.popen("lpstat -p | awk '$1 ~ /^printer/{print $2}'").read().split("\n")
    del printers[-1]
    print("Please select a printer")
    for i,p in enumerate(printers):
        print(" "+str(i+1)+") "+p)
    sel = input("\nEnter number: ")
    sel = int(sel)
    print("Printing on "+printers[sel-1])
    os.popen("lp -d "+printers[sel-1]+" "+filename)

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


def generate_label(products,filename):
    from blabel import LabelWriter
    label_writer = LabelWriter("item_template.html",default_stylesheets=("style.css",))
    records= [
        dict(sample_id="s01", sample_name="Sample 1"),
        dict(sample_id="s02", sample_name="Sample 2")
    ]

    label_writer.write_labels(products, target=filename+'.pdf',base_url='.')


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
file_label = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
file_label = hashlib.md5(file_label.encode('utf-8')).hexdigest()
generate_label(products,file_label)
print("Printing PDF...")
# os.system("lp "+file_label+'.pdf')
printFile(file_label+".pdf")
time.sleep(5)
_ = os.system("clear")
print("Fuck you Bjorn")
time.sleep(0.5)
_ = os.system("clear")
