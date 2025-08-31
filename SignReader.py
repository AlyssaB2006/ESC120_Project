#ISOLATE COLOR

import cv2
import numpy as np

imag = cv2.imread('poc1.jpg') #read image
hsv = cv2.cvtColor(imag, cv2.COLOR_BGR2HSV)  #convert to hsv color space

lower_yell = np.array([15, 35, 140]) 
upper_yell = np.array([30, 255, 255])

mask = cv2.inRange(hsv, lower_yell, upper_yell) #color isolating mask (BW)

cmask = cv2.bitwise_and(imag, imag, mask = mask) #apply mask to original image (yellow mask)
  
cv2.imshow('input', imag) #og display
cv2.imshow('bw mask', mask) 
cv2.imshow('color mask', cmask) #color mask display
      
# FIND SHAPES

img = cmask

ret , thrash = cv2.threshold(mask, 240 , 255, cv2.CHAIN_APPROX_SIMPLE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:

    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (36, 255, 12), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5

    if len(approx) == 3:
        cv2.putText( img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12) )
        print("\ntriangle:\n")
    elif len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12))
            print("\nsquare:\n")
            
        else:
            cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12))
            print("rectangle:\n")
            
    elif len(approx) == 5 :
        cv2.putText(img, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12))
        print("\npentagon:\n")
    elif len(approx) == 7 :
        cv2.putText(img, "arrow", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12))
        print("\narrow:\n")
    elif len(approx) >= 10 :
        cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (36, 255, 12))
        print("\ncircle:\n")

cv2.imshow('output', img)

# READ TEXT

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\users\alyss\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Perform OCR on the mask
text = pytesseract.image_to_string(mask)

# Print the extracted text
print(text)

# WAIT THEN EXIT

cv2.waitKey(0)
cv2.destroyAllWindows()
