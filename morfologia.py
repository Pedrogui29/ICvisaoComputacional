import cv2


# ----- Morfologia de imagens _____
img = cv2.imread('piramide.jpg')
img = cv2.resize(img,(400,300))
imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgCinza,(7,7),8)
imgCanny = cv2.Canny(img, 50,100)
imgDilat = cv2.dilate(imgCanny,(5,5), iterations= 5)
imgErode = cv2.erode(imgCanny,(5,5), iterations= 2)

cv2.imshow('Img Original', img)
cv2.imshow('Img Cinza', imgCinza)
cv2.imshow('Img Blur', imgBlur)
cv2.imshow('Img Canny', imgCanny)
cv2.imshow('Img Dilat', imgDilat)
cv2.imshow('Img Erode', imgErode)
cv2.waitKey(0)
