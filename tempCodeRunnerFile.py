import cv2
import numpy as np
from match_vil import match_vil
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract.exe'

ingame_screenshot = cv2.imread("./assets/images/jap.png")

# Use Tesseract
custom_config = r'--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(ingame_screenshot[900:, 0:190],config=custom_config, lang='eng')
print(text)


# print(match_vil(ingame_screenshot))


cv2.imshow('cwel',ingame_screenshot[900:, 0:190] )
cv2.waitKey(0)
cv2.destroyAllWindows()
