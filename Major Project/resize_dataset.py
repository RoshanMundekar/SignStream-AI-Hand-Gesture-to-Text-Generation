from PIL import Image

def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.LANCZOS)
    img.save(imageName)

import os
all_folders = os.listdir("Dataset")


for i in all_folders:
    for j in os.listdir("Dataset/"+i):
        resizeImage("Dataset/"+i+"/"+j)
        print("[Info] "+"Dataset/"+i+"/"+j+" completed")
        



# for i in range(0, 1000):
#     # Mention the directory in which you wanna resize the images followed by the image name
#     resizeImage("Dataset/HelloImages/hello_" + str(i) + '.png')


