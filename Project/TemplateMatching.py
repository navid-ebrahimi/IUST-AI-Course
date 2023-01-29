import numpy as np
import cv2
class TemplateMatching:
  def template_loc(self, img, template, type):
    h, w, a = template.shape
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
                cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
    if type=="car":
      method = methods[0]
    elif type=="turn_left":
      method = methods[0]
    elif type=="turn_right":
      method = methods[1]
    img2 = img.copy()
    result = cv2.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
      location = min_loc
    else:
      location = max_loc
    return location
