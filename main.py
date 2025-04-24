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
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto('https://liquipedia.net/rainbowsix/Portal:Operators')
    page.wait_for_load_state('load')

    OperatorsInformation = {
        'operator' :       [],
        'real_name':       [],
        'side'     :       [],
        'bornDate' :       [],
        'Country'  :       [],
        'City'     :       [],
        'Age'      :       [],
        'team'     :       [],
        'operation role':  [],
        'team_rainbow' :   [],
        'Affiliation':     [],
        'Height':          [],
        'Weight' :         [],
        'Armor/Health' :   [],
        'Speed':           [],
        'Difficulty':      []

    }

    create_r6s_files()
    create_D_A_L_folders()

    links_selectors = {
        'DefenderLinks': '#mw-content-text > div > b:nth-child(4) > ul > li > div > div.thumb > div > a', 
        'AttackersLinks': '#mw-content-text > div > b:nth-child(2) > ul > li > div > div.thumb > div > a'
           
        }

    OperatorsInformation_selectors = {
        'operator' : '#mw-content-text > div > div.fo-nttax-infobox-wrapper.infobox-rainbowsix > div.fo-nttax-infobox > div:nth-child(1) > div > a',
        'real name': ".infobox-description:text('Real Name:') + div",
        'team'     : '.infobox-description:text("Team:") + div',
        'born'     : '.infobox-description:text("Born:") + div',
        'OperationRole' : '.infobox-description:text("Operator Role:") + div a',
        'flag' : '.flag > a',
        'Team_Rainbow' :  '.infobox-description:text("Team Rainbow:") + div a',
        'Affiliation' : '.infobox-description:text("Affiliation:") + div a',
        'Height': '.infobox-description:text("Height:") + div',
        'Weight': '.infobox-description:text("Weight:") + div',
        'Armor/Health' : '.infobox-description:text("Armor/Health:") + div', 
        'Speed' : '.infobox-description:text("Speed:") + div',
        'Difficulty' : '.infobox-description:text("Difficulty:") + div '

    }

    WeaponsInformation_selectors = {

        'primary': '#mw-content-text > div > div:nth-child(6) > div > div > div ',
        'secondary': '#mw-content-text > div > div:nth-child(10) div ',
        'equipment' : '#mw-content-text > div > div:nth-child(12) div', 
    }
    
    for side, selector in links_selectors.items():
        links = page.locator(selector).all()

        
        for link in links:
            link.click()
            page.wait_for_load_state('networkidle')
            
            countryextract = OperatorsInformation_selectors['flag']
            if page.locator(countryextract).count() > 0:
                country = page.locator(countryextract).first.get_attribute('title')
                print(country)
            else:
                country = 'N/A'


            born = OperatorsInformation_selectors['born']
            if page.locator(born).count() > 0:
                born = page.locator(born).all_text_contents()
                print(born)
                cleanText = re.sub(r"[(),]|age|\xa0", "", born[0]).strip()
                strippedText = cleanText.strip('\n').split()
                DOB = strippedText[:3]
                city = strippedText[3:-1]
                Age = strippedText[-1]
                print(DOB, city, Age)
            else:
                DOB, city, Age = "N/A", "N/A", "N/A"


            real_name_selector = OperatorsInformation_selectors['real name']
            if page.locator(real_name_selector).count() > 0:
                real_name = page.locator(real_name_selector).inner_text()
                print(real_name)
            else:
                real_name = "N/A"


            operator_selector = OperatorsInformation_selectors['operator']
            if page.locator(operator_selector).count() > 0:
                Operator = page.locator(operator_selector).get_attribute('title')
                print(Operator)
            else:
                Operator = "N/A"

            teamselector = OperatorsInformation_selectors['team']
            if page.locator(teamselector).count() > 0:
                team = page.locator(teamselector).inner_text()
                print(team)
            else:
                team = "N/A"


            operationRole = OperatorsInformation_selectors['OperationRole']
            if page.locator(operationRole).count() > 0:
                operationrole = page.locator(operationRole).all_inner_texts()
                print(operationrole)
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


            # pr_weapons = WeaponsInformation_selectors['primary']
            # if page.locator(pr_weapons).count() > 0:
            #     AllPrWeapons = page.locator(pr_weapons).all_inner_texts()
            #     print(AllPrWeapons)
            # else:
            #     print('N/A')


            OperatorsInformation['operator'].append(Operator)
            OperatorsInformation['real_name'].append(real_name)
            OperatorsInformation['side'].append(side.replace('Links', ''))  # Set side (Defender, Attacker, Legacy)
            OperatorsInformation['team'].append(team)
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


            page.go_back()


    df = pd.DataFrame(data=OperatorsInformation)
    print(df)
    df.to_csv('main_r6s.csv', index=False)


    page.close()
