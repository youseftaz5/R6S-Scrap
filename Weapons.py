import pandas as pd 
from playwright.sync_api import sync_playwright
import os 


WeaponsData = {
 
    'Weapon Name'       :  [],  
    'Type'              :  [],
    'Origin'            :  [],
    'Damage'            :  [],
    'Magazine'          :  [],
    'Ammunation'        :  [],
    'Reload Speed'      :  [],
    'Fire Rate'         :  [],
    'Used By'           :  [],
    'Firing Mode'       :  [], 
    'Sights'            :  [],
    'Barrels'           :  [],
    'Grips'             :  [],
    'Under Barrel'      :  [],
}

WeaponDataSelector = {
    'WeabonName'        :'#firstHeading > span > span',
    'WeaponOrigin'      : '.infobox-cell-2.infobox-description:has-text("Origin:") + div ',
    'WeabonType'        :'.infobox-cell-2.infobox-description:has-text("Class:") + div',
    'Damage'            : '.infobox-cell-2.infobox-description:has-text("Base Damage:") + div',
    'MagazineSize'      : '.infobox-cell-2.infobox-description:has-text("Magazine Size:") + div',
    'Ammo Capacity'     : '.infobox-cell-2.infobox-description:has-text("Ammo Capacity:") + div',
    'Reload Speed'      : '.infobox-cell-2.infobox-description:has-text("Reload Speed:") + div',
    'Rate Of Fire'      : '.infobox-cell-2.infobox-description:has-text("Rate of Fire:") + div',
    'FiringMode'        : '.infobox-cell-2.infobox-description:has-text("Firing Mode:") + div',
    'UsedBy'            : '.infobox-cell-2.infobox-description:has-text("Operators:") + div a',
    'Sights'            : '.wikitable > tbody > tr:nth-child(1) > td:nth-child(2) > ul > li > a',
    'Barrels'           : '.wikitable > tbody > tr:nth-child(2) > td:nth-child(2) > ul > li > a',
    'Grips'             : '.wikitable > tbody > tr:nth-child(3) > td:nth-child(2) > ul > li > a',
    'Under Barrel'      : '.wikitable > tbody > tr:nth-child(4) > td:nth-child(2) > ul > li > a'
}

Weabons_Type_Selectors = {
    'Ak-74'             : 'div.show-when-light-mode > a',
    'PrimaryWeapons'    : '#mw-content-text > div > ul:nth-child(5) div > div.thumb > div > a',
    'SubMachineWeapons' : '#mw-content-text > div > ul:nth-child(10) div > div.thumb > div > a',
    'MarksmanWeapons'   : ' #mw-content-text > div > ul:nth-child(16) div > div.thumb > div > a',
    'Light_Machine_Guns': '#mw-content-text > div > ul:nth-child(19) div > div.thumb > div > a',
    'SecondaryWeapons'  : '#mw-content-text > div > ul:nth-child(23) div > div.thumb > div > a',
    'MachinePistol'     : '#mw-content-text > div > ul:nth-child(26) div > div.thumb > div > a',
    'Shotguns'          : '#mw-content-text > div > ul:nth-child(29) div > div.thumb > div > a'



}


def get_text(page, selector, multiple=False, default='N/A'):
    if page.locator(selector).count() > 0:
        return page.locator(selector).all_inner_texts() if multiple else page.locator(selector).inner_text()
    return default

def get_used_by(page, selector):
    if page.locator(selector).count() > 0:
        elements = page.locator(selector).all()
        used_by = []
        for element in elements:
            title = element.get_attribute('title')
            if title:
                used_by.append(title)
            else:
                alt = element.locator('img').get_attribute('alt')
                if alt:
                    used_by.append(alt)
        return used_by
    return 'N/A'

with sync_playwright() as p: 
    browser = p.firefox.launch(headless=False)
    page    = browser.new_page()
    page.goto('https://liquipedia.net/rainbowsix/Portal:Weapons', wait_until='load',timeout=60000)

    
    for Type,selector in Weabons_Type_Selectors.items():
        links = page.locator(selector).all()
    

        
        for link in links:
            link.scroll_into_view_if_needed()
            link.click()
            page.wait_for_load_state('load')
            

            weapon_name     = get_text(page, WeaponDataSelector['WeabonName'])
            origin          = get_text(page, WeaponDataSelector['WeaponOrigin'])
            w_type          = get_text(page, WeaponDataSelector['WeabonType'])
            damage          = get_text(page, WeaponDataSelector['Damage'])
            magazine        = get_text(page, WeaponDataSelector['MagazineSize'])
            ammo            = get_text(page, WeaponDataSelector['Ammo Capacity'])
            reload_speed    = get_text(page, WeaponDataSelector['Reload Speed'])
            fire_rate       = get_text(page, WeaponDataSelector['Rate Of Fire'])
            used_by         = get_used_by(page, WeaponDataSelector['UsedBy'])
            firing_mode     = get_text(page, WeaponDataSelector['FiringMode'], multiple=True)
            sights          = get_text(page, WeaponDataSelector['Sights'], multiple=True)
            barrels         = get_text(page, WeaponDataSelector['Barrels'], multiple=True)
            grips           = get_text(page, WeaponDataSelector['Grips'], multiple=True)
            under_barrel    = get_text(page, WeaponDataSelector['Under Barrel'], multiple=True)
            
            page.go_back()
            WeaponsData['Weapon Name'].append(weapon_name)
            WeaponsData['Type'].append(w_type)
            WeaponsData['Origin'].append(origin)
            WeaponsData['Damage'].append(damage)
            WeaponsData['Magazine'].append(magazine)
            WeaponsData['Ammunation'].append(ammo)
            WeaponsData['Reload Speed'].append(reload_speed)
            WeaponsData['Fire Rate'].append(fire_rate)
            WeaponsData['Used By'].append(used_by)
            WeaponsData['Firing Mode'].append(firing_mode)
            WeaponsData['Sights'].append(sights)
            WeaponsData['Barrels'].append(barrels)
            WeaponsData['Grips'].append(grips)
            WeaponsData['Under Barrel'].append(under_barrel)
    
        df = pd.read_excel('main_r6s_v2_.xlsx')
        df = pd.DataFrame(WeaponsData)
        df.to_excel('main_r6s_v2_.xlsx', sheet_name='Weapons', index=False)
    page.close()

