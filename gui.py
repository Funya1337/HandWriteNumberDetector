from neural_network import *
import runpy
from tkinter import *
import numpy as np
import cv2
from PIL import ImageGrab
from PIL import Image, ImageFilter

def imageprepare(argv):
	im = Image.open(argv).convert('L')
	width = float(im.size[0])
	height = float(im.size[1])
	newImage = Image.new('L', (28, 28), (255))

	if width > height:
		nheight = int(round((20.0 / width * height), 0))
		if (nheight == 0):
			nheight = 1
		img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
		wtop = int(round(((28 - nheight) / 2), 0))
		newImage.paste(img, (4, wtop))
	else:
		nwidth = int(round((20.0 / height * width), 0))
		if (nwidth == 0):
			nwidth = 1

		img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
		wleft = int(round(((28 - nwidth) / 2), 0))
		newImage.paste(img, (wleft, 4))

	tv = list(newImage.getdata())

	tva = [(255 - x) * 1.0 / 255.0 for x in tv]
	print(tva)
	print(len(tva))
	return tva

def activate_paint(position):
    global lastx, lasty
    canvas.bind('<B1-Motion>', paint)
    lastx, lasty = position.x, position.y

def paint(position):
    global lastx, lasty
    canvas.create_line((lastx, lasty, position.x, position.y), fill = 'black', width = 30.0, capstyle = ROUND, smooth = TRUE, splinesteps = 36)
    lastx, lasty = position.x, position.y

def Erase(my_text):
    canvas.delete("all")
    my_text.set("Answer : ")

def Execute():
	ImageGrab.grab().crop((canvas.winfo_rootx() + 2, canvas.winfo_rooty() + 2, canvas.winfo_rootx() + 640, canvas.winfo_rooty() + 480)).save("my_drawing.png", quality = 100)
	img = Image.open('my_drawing.png')
	img = img.resize((28, 28))
	img.save('new.png')
	hand_write_data_check(imageprepare('new.png'))

root = Tk()
root.title("Handwritten number recognition with characteristic")
lastx, lasty = None, None
my_text = StringVar()
my_text.set("Answer : ")
canvas = Canvas(root, width = 640, height = 480, bg = 'white')
canvas.bind('<1>', activate_paint)
canvas.pack(expand = YES, fill = BOTH)
button_frame = Frame(root)
button_frame.pack()
Button(button_frame, text = "Erase", command = lambda:Erase(my_text)).pack(side = LEFT)
Button(button_frame, text = "Execute", command = Execute).pack(side = LEFT)
Label(root, textvariable = my_text).pack()
root.mainloop()