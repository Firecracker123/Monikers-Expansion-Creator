from selenium import webdriver
from PIL import Image
import io
import os
import string
from unidecode import unidecode

class screenshotter:

    def __init__(self) -> None:    
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--window-size=400,600')
        options.add_argument(f"--force-device-scale-factor={3}") #increases dpi so text looks smoother
        driver = webdriver.Chrome(options=options)

        self.back_image = Image.open("back_of_card_image/card_back.tiff")
            

    def take_screenshot(self, url: str, output_file: str) -> None:
        try:
            screenshotter.driver.get(url)
            with Image.open(io.BytesIO(screenshotter.driver.get_screenshot_as_png())) as screenshot:
                screenshot.save(output_file, dpi=(300,300))
            print('Screenshot saved as:', output_file)
        except Exception as e:
            print('Failed to screenshot:', output_file)
            print('Error:', e)
    
    def quit(self):
        screenshotter.driver.quit()

    def makeBack(self, card_name :str, directory :str) -> None:
        self.back_image.save(f"{directory}/{card_name}")

def get_card_info(filename :str = 'card_info.csv') -> str:
    with open(filename) as f:
        file_text = f.read()

    card_text = file_text.split("\n\n") #Remove newlines characters and split into different cards
    cards_formated = []

    for card in card_text:
        i=0
        while not card[i].isdigit(): #Seperates each each card into Title, point value and description
            if i != len(card)-1 and card[i+1].isdigit():
                cards_formated.append([format_title(card[:i]), card[i+1:i+2], card[i+2:].replace("\n", "").replace("*","")])
            i += 1
    return cards_formated


def format_title(title):
    out_string = ""
    for char in title:
        if char != "*":
            out_string += char
    return out_string



def create_html(title :str,  points :int, description :str) -> None:
    points = int(points)
    point_colors = {1:"0e935c",2:"2bbaf1", 3:"6a226b", 4: "c71316"} #colours for different point values
    positions = {1: 65, 2: 62, 3: 62, 4:61} #Modified so the point value is still centred
    html = f"""
    <html>
<head>
    <link rel="stylesheet" href="Style.css">
</head>
        <body>
            <h1 id="head_title">{title}</h1>
            <div id="descriptionContainer">
                <p id="description">{description}</p>
            </div>
            <div id="dotContainer">
                <h2>.............</h2>
            </div>
                <div id="genreContainer">
                <p id="genre" style = "color: #{point_colors[points]}">Cards For Humanity</p>
            </div>
                <svg width="135" height="135" class="main-shape" xmlns="https://www.w3.org/2000/svg">
                    <path d="M116,100 
                        a7,7 0 1,0 -90,0 
                        l0,10000
                        Z" z
                    fill="#{point_colors[points]}" />
                    <text x="{positions[points]}" y="90" fill="white" font-size="30" id="points_num">{points}</text>
                    <text x="47" y="110" fill="white" font-size="20" id="points_word">POINTS</text>
                </svg>
                <svg height="40" width="120" class="rectangle" xmlns="https://www.w3.org/2000/svg">
                    <rect width="89.5" height="40" x="18.5" fill="#{point_colors[points]}"/>
                </svg>
        </body>
</html>"""
    with open('html_files/card_file.html', 'w') as f:
        f.write(html)


target_dir = "cards"
if target_dir not in [i.lower() for i in os.listdir('.')]:
    os.mkdir(target_dir)

html_screenshot_taker = screenshotter()
html_url = "".join([os.path.abspath("."),"\\html_files\\card_file.html"]) #Include absolute path to file with descriptions
cards = get_card_info()
for card in cards:
    filename = card[0].translate(str.maketrans('', '', string.punctuation)) #Removes punctuation from file name 
    output_file = f"{target_dir}/{unidecode(filename)}.jpg" #names file after card title and puts screenshot in Cards directory
    create_html(card[0], card[1], card[2]) #Passes Title, Points, Description in in that order
    html_screenshot_taker.take_screenshot(html_url, output_file) #Takes screenshot of created html file
    screenshotter.makeBack(filename, target_dir)

html_screenshot_taker.quit()#ends driver