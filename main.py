from playwright.sync_api import sync_playwright
import pandas as pd
import os 
import re


def create_r6s_files():
    if 'r6s_container' not in os.listdir():
        return os.mkdir('r6s_container')
    else:
        return False

def create_D_A_L_folders(base_path='r6s_container'):
    folders = ['Defender', 'Attacker', 'Legacy']
    
    for folder in folders:
        full_path = os.path.join(base_path, folder)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto('https://liquipedia.net/rainbowsix/Portal:Operators',wait_until='networkidle')
    page.wait_for_load_state('load')

    OperatorsInformation = {
        'operator'          :[ ],
        'real_name'         :[ ],
        'side'              :[ ],
        'bornDate'          :[ ],
        'Country'           :[ ],
        'City'              :[ ],
        'Age'               :[ ],
        'team'              :[ ],
        'operation role'    :[ ],
        'team_rainbow'      :[ ],
        'Affiliation'       :[ ],
        'Height'            :[ ],
        'Weight'            :[ ],
        'Armor/Health'      :[ ],
        'Speed'             :[ ],
        'Difficulty'        :[ ],
        'Biography'         :[ ],
        'Primary_1'         :[ ],
        'Type_1'            :[ ],
        'Primary_2'         :[ ], 
        'Type_2'            :[ ],
        'Secondary_1'       :[ ],
        'Type_3'            :[ ],
        'Secondary_2'       :[ ],
        'Type_4'            :[ ],
        'Gadget'            :[ ],
        'Unique_ability'    :[ ],
        
    }

    create_r6s_files()
    create_D_A_L_folders()

    links_selectors = {
        'DefenderLinks'     : '#mw-content-text > div > b:nth-child(4) > ul > li > div > div.thumb > div > a', 
        'AttackersLinks'    : '#mw-content-text > div > b:nth-child(2) > ul > li > div > div.thumb > div > a'
           
        }

    OperatorsInformation_selectors = {
        'operator'          : '#mw-content-text > div > div.fo-nttax-infobox-wrapper.infobox-rainbowsix > div.fo-nttax-infobox > div:nth-child(1) > div > a',
        'real name'         : ".infobox-description:text('Real Name:') + div",
        'team'              : '.infobox-description:text("Team:") + div',
        'born'              : '.infobox-description:text("Born:") + div',
        'OperationRole'     : '.infobox-description:text("Operator Role:") + div a',
        'flag'              : '.flag > a',
        'Team_Rainbow'      :  '.infobox-description:text("Team Rainbow:") + div a',
        'Affiliation'       : '.infobox-description:text("Affiliation:") + div a',
        'Height'            : '.infobox-description:text("Height:") + div',
        'Weight'            : '.infobox-description:text("Weight:") + div',
        'Armor/Health'      : '.infobox-description:text("Armor/Health:") + div', 
        'Speed'             : '.infobox-description:text("Speed:") + div',
        'Difficulty'           : '.infobox-description:text("Difficulty:") + div '

    }

    WeaponsInformation_selectors = {

        'primary'          : '.operator__loadout__category:nth-child(2) > div',
        'secondary'        : '.operator__loadout__category:nth-child(3) > div',
        'gadget'           : '.operator__loadout__category:nth-child(4) > div',
        'unique_Ability'   : '.operator__loadout__category:nth-child(5) > div'

    }

    Liquipedia_selectors = {

        'Biography_selector' : '.operator__biography__description'
    }
    
    for side, selector in links_selectors.items():
        links = page.locator(selector).all()

        
        for link in links:
            link.click()
            page.wait_for_load_state('load')
            
            countryextract = OperatorsInformation_selectors['flag']
            if page.locator(countryextract).count() > 0:
                country = page.locator(countryextract).first.get_attribute('title')
            else:
                country = 'N/A'


            born = OperatorsInformation_selectors['born']
            if page.locator(born).count() > 0:
                born = page.locator(born).all_text_contents()
  
                cleanText = re.sub(r"[(),]|age|\xa0", "", born[0]).strip()
                strippedText = cleanText.strip('\n').split()
                DOB = strippedText[:3]
                city = strippedText[3:-1]
                Age = strippedText[-1]
            else:
                DOB, city, Age = "N/A", "N/A", "N/A"


            real_name_selector = OperatorsInformation_selectors['real name']
            if page.locator(real_name_selector).count() > 0:
                real_name = page.locator(real_name_selector).inner_text()
            else:
                real_name = "N/A"


            operator_selector = OperatorsInformation_selectors['operator']
            if page.locator(operator_selector).count() > 0:
                Operator = page.locator(operator_selector).get_attribute('title')
            else:
                Operator = "N/A"

            teamselector = OperatorsInformation_selectors['team']
            if page.locator(teamselector).count() > 0:
                team = page.locator(teamselector).inner_text()
            else:
                team = "N/A"


            operationRole = OperatorsInformation_selectors['OperationRole']
            if page.locator(operationRole).count() > 0:
                operationrole = page.locator(operationRole).all_inner_texts()
            else:
                operationrole = 'N/A'

            teamRainbow = OperatorsInformation_selectors['Team_Rainbow']
            if page.locator(teamRainbow).count() > 0:
                teamrainbow = page.locator(teamRainbow).first.get_attribute('title')
            else:
                teamrainbow = 'N/A'

            affiliation = OperatorsInformation_selectors['Affiliation']
            if page.locator(affiliation).count() > 0: 
                affiliate = page.locator(affiliation).all_inner_texts()[-1]
            else:
                affiliate = 'N/A'

            Higt = OperatorsInformation_selectors['Height']
            Wigt = OperatorsInformation_selectors['Weight']
            if page.locator(Higt).count() > 0 and page.locator(Wigt).count() > 0:
                Hight = page.locator(Higt).inner_text()
                Wight = page.locator(Wigt).inner_text()

            else:
                Hight = 'N/A'
                Wight = 'N/A'

            Armor = OperatorsInformation_selectors['Armor/Health']
            if page.locator(Armor).count() > 0:
                armor = page.locator(Armor).all_text_contents()[0].strip().split(' ')[0]
                
            else:
                armor = 'N/A'

            speed = OperatorsInformation_selectors['Speed']
            if page.locator(speed).count() > 0:
                speeds = page.locator(speed).inner_text()
            else:
                speeds = 'N/A'

            Diff = OperatorsInformation_selectors['Difficulty']
            if page.locator(Diff).count() > 0:
                difficulty = page.locator(Diff).inner_text()

            else:
                difficulty = 'N/A'



            biography = 'N/A'
            # page.wait_for_load_state('domcontentloaded')
            bio_locator = page.locator(Liquipedia_selectors['Biography_selector'])
            background_locator = page.locator('.Background')

            if bio_locator.count() > 0 :
                biography = bio_locator.first.inner_text()
            else:
                biography = 'N/A'
            
            
            page.goto(f'https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators/{Operator.lower()}')
            page.wait_for_timeout(4000)
            primary_1 = primary_2 = type_1 = type_2 = 'N/A'
            
            #Primary Weabons 
            if page.locator(f"{WeaponsInformation_selectors['primary']} > div").count() > 0:
                p_names = page.locator('.operator__loadout__category:nth-child(2) > div > div > p:nth-child(1)')
                p_types = page.locator('.operator__loadout__category:nth-child(2) > div > div > p:nth-child(3)')
                if p_names.count() > 0:
                    primary_1 = p_names.nth(0).inner_text()
                    type_1 = p_types.nth(0).inner_text()
                if p_names.count() > 1:
                    primary_2 = p_names.nth(1).inner_text()
                    type_2 = p_types.nth(1).inner_text()
            page.wait_for_timeout(2000)

            #Secondary Weabons
            secondary_1 = secondary_2 = type_3 = type_4 = 'N/A'
            if page.locator(f"{WeaponsInformation_selectors['secondary']} > div").count() > 0:
                s_names = page.locator('.operator__loadout__category:nth-child(3) > div > div > p:nth-child(1)')
                s_types = page.locator('.operator__loadout__category:nth-child(3) > div > div > p:nth-child(3)')
                if s_names.count() > 0:
                    secondary_1 = s_names.nth(0).inner_text()
                    type_3 = s_types.nth(0).inner_text()
                if s_names.count() > 1:
                    secondary_2 = s_names.nth(1).inner_text()
                    type_4 = s_types.nth(1).inner_text()
            page.wait_for_timeout(2000)
            
            gadget_name = page.locator('.operator__loadout__category:nth-child(4) > div > div > p:nth-child(1)').all_inner_texts() if page.locator(WeaponsInformation_selectors['gadget']).count() > 0 else 'N/A'
            unique_ability = page.locator('.operator__loadout__category:nth-child(5) > div > div > p:nth-child(1)').inner_text() if page.locator(WeaponsInformation_selectors['unique_Ability']).count() > 0 else 'N/A'


            print(primary_1,primary_2,secondary_1,secondary_2)
            page.goto('https://liquipedia.net/rainbowsix/Portal:Operators',wait_until='load')



            OperatorsInformation['operator'].append(Operator)
            OperatorsInformation['real_name'].append(real_name)
            OperatorsInformation['side'].append(side.replace('Links', ''))
            OperatorsInformation['bornDate'].append(DOB)
            OperatorsInformation['City'].append(city)
            OperatorsInformation['Age'].append(Age)
            OperatorsInformation['operation role'].append(operationrole)
            OperatorsInformation['Country'].append(country)
            OperatorsInformation['team_rainbow'].append(teamrainbow)
            OperatorsInformation['Affiliation'].append(affiliate)
            OperatorsInformation['Weight'].append(Wight)
            OperatorsInformation['Height'].append(Hight)
            OperatorsInformation['Armor/Health'].append(armor)
            OperatorsInformation['Speed'].append(speeds)
            OperatorsInformation['Difficulty'].append(difficulty)
            OperatorsInformation['Biography'].append(biography)
            OperatorsInformation['Primary_1'].append(primary_1)
            OperatorsInformation['Type_1'].append(type_1)
            OperatorsInformation['Primary_2'].append(primary_2)
            OperatorsInformation['Type_2'].append(type_2)
            OperatorsInformation['Secondary_1'].append(secondary_1)
            OperatorsInformation['Type_3'].append(type_3)
            OperatorsInformation['Secondary_2'].append(secondary_2)
            OperatorsInformation['Type_4'].append(type_4)
            OperatorsInformation['Gadget'].append(gadget_name)
            OperatorsInformation['Unique_ability'].append(unique_ability)

    df = pd.DataFrame(data=OperatorsInformation)
    print(df)
    df.to_csv('main_r6s_v2.csv', index=False)

    page.close()
