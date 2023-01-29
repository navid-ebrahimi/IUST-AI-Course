import numpy as np
import cv2
class LineDetection:
  def __init__(self, low_threshold, high_threshold, rho, theta, threshold, min_line_length, max_line_gap):
    self.low_threshold = low_threshold
    self.high_threshold = high_threshold
    self.rho = rho
    self.theta = theta
    self.threshold = threshold
    self.min_line_length = min_line_length
    self.max_line_gap = max_line_gap

  def detect_lines(self, state):
    frame = state
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(frame1, self.low_threshold, self.high_threshold)
    lines = cv2.HoughLinesP(edges, self.rho, self.theta, self.threshold, np.array([]),self.min_line_length, self.max_line_gap)
    return lines
