import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

operators = [
    "Sentry", "Smoke", "Mute", "Castle", "Pulse", "Doc", "Rook", "Kapkan", "Tachanka", "Jäger", "Bandit",
    "Frost", "Valkyrie", "Caveira", "Echo", "Mira", "Lesion", "Ela", "Vigil", "Alibi", "Maestro", "Clash",
    "Kaid", "Mozzie", "Warden", "Goyo", "Wamai", "Oryx", "Melusi", "Aruni", "Thunderbird", "Thorn", "Azami",
    "Solis", "Fenrir", "Tubarao", "Skopós", "Striker", "Sledge", "Thatcher", "Ash", "Thermite", "Twitch",
    "Montagne", "Glaz", "Fuze", "Blitz", "IQ", "Buck", "Blackbeard", "Capitão", "Hibana", "Jackal", "Ying",
    "Zofia", "Dokkaebi", "Lion", "Finka", "Maverick", "Nomad", "Gridlock", "Nøkk", "Amaru", "Kali", "Iana",
    "Ace", "Zero", "Flores", "Osa", "Sens", "Grim", "Brava", "Ram", "Deimos", "Rauora"
]

def get_bio(operator):
    slug = operator.lower()
    url = f"https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators/{slug}"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the <h3>BIOGRAPHY</h3> tag
        bio_header = soup.find("h3", string=lambda t: t and "biography" in t.lower())
        if not bio_header:
            return "N/A"

        # Collect all <p> tags directly after the <h3> until non-<p> tag
        paragraphs = []
        next_tag = bio_header.find_next_sibling()
        while next_tag and next_tag.name == "p":
            paragraphs.append(next_tag.get_text(strip=True))
            next_tag = next_tag.find_next_sibling()

        return " ".join(paragraphs) if paragraphs else "N/A"

    except Exception as e:
        print(f" Error scraping {operator}: {e}")
        return "N/A"


bios = []
for op in operators:
    print(f" Scraping {op}...")
    bio = get_bio(op)
    bios.append({"Operator": op, "Biography": bio})
    time.sleep(1)  

df = pd.DataFrame(bios)
df.to_excel("Dataset/R6S_Operators_Biographies.xlsx", index=False)
print("Done! File saved")
