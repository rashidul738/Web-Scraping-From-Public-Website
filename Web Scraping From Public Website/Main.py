import os
import csv
import tqdm
from csv import reader
from time import sleep
from random import randint
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()
driver.get('https://qpublic.schneidercorp.com/Application.aspx?App=ForsythCountyGA&PageType=Search')
sleep(3)

driver.find_element_by_xpath('//div[@class="modal-footer"]/a[@class="btn btn-primary button-1"]').click()
sleep(1)

ParcelID = []

with open('ParcelID.csv', 'r') as f:
    csv_reader = reader(f)
    for row in csv_reader:
        ParcelID.append(row[0])
        

details = []
for id in ParcelID:
    input_parcel=driver.find_element_by_xpath('//input[@placeholder="enter parcel number..."]')
    input_parcel.send_keys(id)
    sleep(1)
    input_parcel.send_keys(Keys.RETURN)
    sleep(randint(5,15))
    
    sel = Selector(text=driver.page_source)
    Location_1 = sel.xpath('//th/strong[text()="Location Address"]/following::td[1]/span/text()').get()
    Location_2 = sel.xpath('//th/strong[text()="Location Address"]/following::td[1]/span/text()[2]').get()
    Location = Location_1 + Location_2
    
    OwnerFastName = sel.xpath('//div[@class="four-column-blocks"]/span[2]/text()').get()
    OwnerLastName = sel.xpath('//div[@class="four-column-blocks"]/span[3]/text()').get()

    OwnerAddress_1 = sel.xpath('//span[@id="ctlBodyPane_ctl02_ctl01_lblAddress1"]/text()').get()
    OwnerAddress_2 = sel.xpath('//span[@id="ctlBodyPane_ctl02_ctl01_lblCityStZip"]/text()').get()
    OwnerAddress = OwnerAddress_1 + OwnerAddress_2
    
    StartCode = sel.xpath('//tr/th[text()="Class"]/following-sibling::td/text()').get()
    LandValue = sel.xpath('//tr/th[text()="Land Value"]/following-sibling::td[1]/text()').get()
    BuildingValue = sel.xpath('//tr/th[text()="Building Value"]/following-sibling::td[1]/text()').get()
    Acres = sel.xpath('//th[text()="SINGLE FAMILY RESIDENTIAL"]/following-sibling::td[4]/text()').get()
    Bedrooms = sel.xpath('//th/strong[text()="Bedrooms"]/following::td[1]/span/text()').get()
    MostRecentSalesDate = sel.xpath('//tr/th[text()="Sale Date"]/following::tbody/tr/th/text()').get()
    MostRecentSalesAmount = sel.xpath('//tr/th[text()="Sale Date"]/following::tbody/tr[1]/td[1]/text()').get()

    info = {
        'Location': Location,
        'OwnerFastName': OwnerFastName,
        'OwnerLastName': OwnerLastName,
        'OwnerAddress': OwnerAddress,
        'StartCode': StartCode,
        'LandValue': LandValue,
        'BuildingValue': BuildingValue,
        'Acres': Acres,
        'Bedrooms': Bedrooms,
        'MostRecentSalesDate': MostRecentSalesDate,
        'MostRecentSalesAmount': MostRecentSalesAmount,
        'Parcel ID': id
        }
    print(info)
    print("#"*120)
    details.append(info)
    
    
    with open('Dataset.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Location', 'OwnerFastName', 'OwnerLastName', 'OwnerAddress', 'StartCode', 'LandValue', 'BuildingValue', 'Acres', 'Bedrooms', 'MostRecentSalesDate', 'MostRecentSalesAmount', 'Parcel ID'])
            writer.writeheader()
            writer.writerows(details)
    
    driver.back()
    sleep(3)          
driver.close()
