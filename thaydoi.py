import cv2

img = cv2.imread("CNN letter Dataset/0/aug8041_0.jpg")
_,binary = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY_INV)
cv2.imshow("abc",binary)
cv2.waitKey()