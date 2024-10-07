from PIL import Image
from os import listdir

target_dir = "Tiffs"
files = [i for i in listdir(target_dir) if i.endswith(".jpg")]

back_im = Image.open("back_image.jpg")

for file in files:
    back_im.save(f"{target_dir}/{file[:-4]}_back.jpg", dpi=(300,300))