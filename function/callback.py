

import cv2


global plotted_img

def callback_test(self):
    try:
        cv2.imshow("callback_plotted",self.plotted_img)
    except:
        pass
