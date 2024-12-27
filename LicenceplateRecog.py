import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Reading the image
img = cv2.imread('car2.jpg')
cv2.imshow('Original Image', img)

# Converting the image to grayscale
gray_img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', gray_img)

# Canny Edge Detection
canny_edges = cv2.Canny(gray_img, 170, 200) # thresholds for canny edge detection (lower, upper)
cv2.imshow('Canny Edges', canny_edges)

# Finding contours
contours, hierarchy = cv2.findContours(canny_edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]


# initializing  license plate contour and x,y,w,h coordinates
contour_with_license_plate = None
license_plate = None

x=None
y=None
w=None
h=None

#creating a blank canvas to draw contours on
contour_imges=img.copy()

#Drawing contours on the canvas
cv2.drawContours(contour_imges, contours, -1, (0,255,0), 2)

#Displaying the canvas
cv2.imshow('Image with Contours', contour_imges)
# cv2.imwrite('contour_imges.jpg', contour_imges)

for cnt in contours:
    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.01*perimeter, True)
    print("Approx polygon is ", approx)
    if len(approx) == 4:
        contour_with_license_plate = approx
        x,y,w,h = cv2.boundingRect(cnt)
        license_plate = gray_img[y:y+h, x:x+w]
        break

(thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('License Plate', license_plate)
# cv2.imwrite('license_plate.jpg', license_plate)

#removing noise from license plate
license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)

#text recognition
text = pytesseract.image_to_string(license_plate)


#Drawing text on the image
img=cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
img = cv2.putText(img, text, (x-100, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.imshow('Image with License Plate', img)
cv2.imwrite('license_plate with text22.jpg', img)

print(text)

# cv2.waitKey(0)





