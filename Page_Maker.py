import numpy as np
import cv2
from os import listdir
from unidecode import unidecode

class Page:
    rows = 6
    columns = 6
    def __init__(self) -> None:
        self.rows = [np.array([None for i in range(Page.columns)]) for i in range(Page.rows)]
        self.page_img = None
        self.current_row = 0
        self.current_col = 0
        self.full = False
    
    def create_page_img(self):
        row_cpy = self.rows.copy()
        row_imgs = []

        for row_num, row in enumerate(row_cpy):
            for img_num, img in enumerate(row):
                 #Replace any empty space on page with a transparent image
                 if img is None:                                        
                     self.rows[row_num][img_num] = cv2.imread('transparent_card.png')
            #Combine each image on current row
            row_imgs.append(np.concatenate(self.rows[row_num], axis=1)) 
        #Combine all rows of images
        self.page_img = np.concatenate(row_imgs, axis=0)                



    def write_page(self,page_name):
        cv2.imwrite(f"Pages/{page_name}.png", self.page_img)


    def add_image(self, img):
        
        #Adds image to current slot in page
        self.rows[self.current_row][self.current_col] = img
        self.current_col += 1

        #Goes to new row when column limit has been reached
        if (self.current_col  != 0 and self.current_col % Page.columns == 0):
            self.current_row += 1
            self.current_col = 0
        
            #Page is full if row limit is exceeded
            if self.current_row >= len(self.rows):
                self.full = True


    def is_full(self):
        return self.full

def create_card_back(page_name):
    background_image = cv2.imread("back_card_image.png")
    background_page = Page()

    while not background_page.is_full():
        background_page.add_image(background_image)

    background_page.create_page_img()
    background_page.write_page(f"{page_name}_background")          

#Get file names of all card images
card_dirs = listdir('Cards')

#track the number of cards made
num_cards = 0
num_pages = 0

while num_cards < len(card_dirs)-1:
    current_page = Page()
    #Add images to page until page is full then create an image and then write the file
    while not current_page.is_full() and num_cards < len(card_dirs):
        current_page.add_image(cv2.imread(unidecode(f"Cards/{card_dirs[num_cards]}"))) 
        num_cards += 1    
    current_page.create_page_img()
    num_pages += 1
    current_page.write_page(f"Page {num_pages}")
    create_card_back(f"Page {num_pages}")
