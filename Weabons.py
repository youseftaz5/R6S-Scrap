import pandas as pd 
from playwright.sync_api import sync_playwright
import os 
import re 


WeabonsData = {
 
    'Weapon Name'    :  [],  
    'Description'    :  [],
    'Type'           :  [],
    'Damage'         :  [],
    'Fire Rate'      :  [],
    'Ammunation'     :  [],
    'Sights'         :  [],
    'Barrels'        :  [],
    'Grips'          :  [],
    'Under Barrel'   :  [],
    'Used By'        :  []
}

WeaponDataSelector = {
    'WeabonName':'#firstHeading > span > span',
    'WeabonType':'.infobox-cell-2.infobox-description:has-text("Class:") + div'
}

Weabons_Type_Selectors = {
    'PrimaryWeabons': '#mw-content-text > div > ul:nth-child(5) div > div.thumb > div > a'
}

with sync_playwright() as p: 
    browser = p.firefox.launch(headless=False)
    page    = browser.new_page()
    page.goto('https://liquipedia.net/rainbowsix/Portal:Weapons', wait_until='load',timeout=50000)

    # Primary_Weabons_Selector
    
    # PWS = page.locator(WeabonsSelectors['PrimaryWeabons']).all()
    for Type,selector in Weabons_Type_Selectors.items():
        links = page.locator(selector).all()
        
        print(len(links))
        for link in links:
            link.click()
            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['WeabonName']).count() > 0:
                wbn = page.locator(WeaponDataSelector['WeabonName']).inner_text()
                print(wbn)
            else:
                print('N/A')
            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['WeabonType']).count() > 0:
                Typeis = page.locator(WeaponDataSelector['WeabonType']).inner_text()
                print(Typeis)
            else:
                print('n/a')

    
            page.go_back()

