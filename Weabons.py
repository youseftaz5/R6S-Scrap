import pandas as pd 
from playwright.sync_api import sync_playwright
import os 
import re 

# Function to eliminate any redundant snip of code 
# def extract_data(page, selector, default='N/A'):
#     loc = page.locator(selector)
#     return loc.inner_text() if loc.count() > 0 else default

WeaponsData = {
 
    'Weapon Name'    :  [],  
    'Type'           :  [],
    'Origin'         :  [],
    'Damage'         :  [],
    'Magazine'       :  [],
    'Ammunation'     :  [],
    'Reload Speed'   :  [],
    'Fire Rate'      :  [],
    # 'Side'           :  [],
    'Used By'        :  [],
    'Firing Mode'    :  [], 
    # 'Description'    :  [],
    'Sights'         :  [],
    'Barrels'        :  [],
    'Grips'          :  [],
    'Under Barrel'   :  [],
}

WeaponDataSelector = {
    'WeabonName':'#firstHeading > span > span',
    'WeaponOrigin' : '.infobox-cell-2.infobox-description:has-text("Origin:") + div ',
    'WeabonType':'.infobox-cell-2.infobox-description:has-text("Class:") + div',
    'Damage'    : '.infobox-cell-2.infobox-description:has-text("Base Damage:") + div',
    'MagazineSize' : '.infobox-cell-2.infobox-description:has-text("Magazine Size:") + div',
    'Ammo Capacity' : '.infobox-cell-2.infobox-description:has-text("Ammo Capacity:") + div',
    'Reload Speed'  : '.infobox-cell-2.infobox-description:has-text("Reload Speed:") + div',
    'Rate Of Fire'  : '.infobox-cell-2.infobox-description:has-text("Rate of Fire:") + div',
    # 'Side' : '.infobox-cell-2.infobox-description:has-text("Side:") + div',
    'FiringMode' : '.infobox-cell-2.infobox-description:has-text("Firing Mode:") + div',
    'UsedBy' : '.infobox-cell-2.infobox-description:has-text("Operators:") + div a',
    'Sights' : '.wikitable > tbody > tr:nth-child(1) > td:nth-child(2) > ul > li > a',
    'Barrels' : '.wikitable > tbody > tr:nth-child(2) > td:nth-child(2) > ul > li > a',
    'Grips' : '.wikitable > tbody > tr:nth-child(3) > td:nth-child(2) > ul > li > a',
    'Under Barrel' : '.wikitable > tbody > tr:nth-child(4) > td:nth-child(2) > ul > li > a'
}

Weabons_Type_Selectors = {
    'Ak-74' : 'div.show-when-light-mode > a',
    'PrimaryWeapons': '#mw-content-text > div > ul:nth-child(5) div > div.thumb > div > a',
    'SubMachineWeapons' : '#mw-content-text > div > ul:nth-child(10) div > div.thumb > div > a',
    'MarksmanWeapons' : ' #mw-content-text > div > ul:nth-child(16) div > div.thumb > div > a',
    'Light_Machine_Guns' : '#mw-content-text > div > ul:nth-child(19) div > div.thumb > div > a',
    'SecondaryWeapons' : '#mw-content-text > div > ul:nth-child(23) div > div.thumb > div > a',
    'MachinePistol' : '#mw-content-text > div > ul:nth-child(26) div > div.thumb > div > a',
    'Shotguns': '#mw-content-text > div > ul:nth-child(29) div > div.thumb > div > a'



}

with sync_playwright() as p: 
    browser = p.firefox.launch(headless=False)
    page    = browser.new_page()
    page.goto('https://liquipedia.net/rainbowsix/Portal:Weapons', wait_until='load',timeout=60000)

    # Primary_Weabons_Selector
    

    for Type,selector in Weabons_Type_Selectors.items():
        links = page.locator(selector).all()
    
        print(len(links))
        
        for link in links:
            link.scroll_into_view_if_needed()
            link.click()
            page.wait_for_load_state('load')

            if page.locator(WeaponDataSelector['WeabonName']).count() > 0:                
                WeaponName = page.locator(WeaponDataSelector['WeabonName']).inner_text()
                print(WeaponName)
            else:
                WeaponName = 'N/A'

            if page.locator(WeaponDataSelector['WeaponOrigin']).count() > 0:
                Origin = page.locator(WeaponDataSelector['WeaponOrigin']).inner_text()
                print(Origin)
            else:
                Origin = 'N/A'

            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['WeabonType']).count() > 0:
                Type = page.locator(WeaponDataSelector['WeabonType']).inner_text()
                print(Type)
            else:
                Type = 'N/A'

            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['Damage']).count() > 0:
                Damage = page.locator(WeaponDataSelector['Damage']).inner_text()
                print(Damage)
            else:
                Damage = 'N/A'

            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['MagazineSize']).count() > 0:
                Magazine = page.locator(WeaponDataSelector['MagazineSize']).inner_text()
                print(Magazine)
            else:
                Magazine = 'N/A'
            
            if page.locator(WeaponDataSelector['Ammo Capacity']).count() > 0: 
                Ammo = page.locator(WeaponDataSelector['Ammo Capacity']).inner_text()
            else:
                Ammo = 'N/A'
            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['Reload Speed']).count() > 0: 
                ReloadSpeed = page.locator(WeaponDataSelector['Reload Speed']).inner_text()
            else:
                ReloadSpeed = 'N/A'
            
            
            if page.locator(WeaponDataSelector['Rate Of Fire']).count() > 0: 
                RateOfFire = page.locator(WeaponDataSelector['Rate Of Fire']).inner_text()
            else:
                RateOfFire = 'N/A'
            
            page.wait_for_load_state('load')
            if page.locator(WeaponDataSelector['UsedBy']).count() > 0:
                    usedby_elements = page.locator(WeaponDataSelector['UsedBy']).all()
                    usedby = []
                    for element in usedby_elements:
                        title = element.get_attribute('title')
                        if title:
                            usedby.append(title)
                        else:
                            alt = element.locator('img').get_attribute('alt')
                            if alt:
                                usedby.append(alt)

                    print(usedby)
            else:
                usedby = 'N/A'

            if page.locator(WeaponDataSelector['FiringMode']).count() > 0:
                Fire_Mode = page.locator(WeaponDataSelector['FiringMode']).all_inner_texts()
                print(Fire_Mode)
            else:
                Fire_Mode = 'N/A'
            

            if page.locator(WeaponDataSelector['Sights']).count() > 0:
                sights = page.locator(WeaponDataSelector['Sights']).all_inner_texts()
                print(sights)
            else:
                sights = 'N/A'

            if page.locator(WeaponDataSelector['Barrels']).count() > 0:
                barrels = page.locator(WeaponDataSelector['Barrels']).all_inner_texts()
                print(barrels)
            else:
                barrels = 'N/A'

            if page.locator(WeaponDataSelector['Grips']).count() > 0:
                grips = page.locator(WeaponDataSelector['Grips']).all_inner_texts()
                print(grips)
            else:
                grips = 'N/A'

            if page.locator(WeaponDataSelector['Under Barrel']).count() > 0:
                under_barrel = page.locator(WeaponDataSelector['Under Barrel']).all_inner_texts()
                print(under_barrel)
            else:
                under_barrel = 'N/A'
            
            page.go_back()
            WeaponsData['Weapon Name'].append(WeaponName)
            WeaponsData['Type'].append(Type)
            WeaponsData['Origin'].append(Origin)
            WeaponsData['Damage'].append(Damage)
            WeaponsData['Magazine'].append(Magazine)
            WeaponsData['Ammunation'].append(Ammo)
            WeaponsData['Reload Speed'].append(ReloadSpeed)
            WeaponsData['Firing Mode'].append(Fire_Mode)
            WeaponsData['Fire Rate'].append(RateOfFire)
            WeaponsData['Used By'].append(usedby)
            WeaponsData['Sights'].append(sights)
            WeaponsData['Barrels'].append(barrels)
            WeaponsData['Grips'].append(grips)
            WeaponsData['Under Barrel'].append(under_barrel)
    
        df = pd.read_excel('main_r6s_v2_.xlsx')
        df = pd.DataFrame(WeaponsData)
        df.to_excel('main_r6s_v2_.xlsx', sheet_name='Weapons', index=False)
    page.close()

