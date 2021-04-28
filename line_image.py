from PIL import ImageOps, Image
import cv2
import numpy as np
path = "fourier_image3.jpg"
with Image.open(path) as im:
    gray = im.convert('L')
    ocv = np.array(gray)
    threshold1 = 200
    threshold2 = 20
    edgec = cv2.Canny(ocv, threshold1, threshold2)
    edgec = Image.fromarray(edgec)
    edgec = ImageOps.invert(edgec)

Image._show(edgec)