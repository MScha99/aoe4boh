import cv2
import numpy as np
from match_vil import match_vil
import easyocr


ingame_screenshot=cv2.imread("jap.png")
#print(match_vil(ingame_screenshot))


# cv2.imshow('cwel',ingame_screenshot[900:, 0:190] )
# cv2.waitKey(0)
# cv2.destroyAllWindows()

reader = easyocr.Reader(['en'], gpu=False) # specify the language  
result = reader.readtext(ingame_screenshot[900:, 0:190])

for (bbox, text, prob) in result:
    print(f'Text: {text}, Probability: {prob}')

