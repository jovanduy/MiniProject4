#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2, math
import numpy as np

class ColourTracker:
  def __init__(self):
    cv2.namedWindow("ColourTrackerWindow", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("ColourTrackerWindow", 640, 480)
    self.capture = cv2.VideoCapture(0)
    self.scale_down = 1
    self.points = ((0, 0), (0, 0), (0, 0), (0, 0))
    self.past = []

  def run(self):
    while True:
      f, orig_img = self.capture.read()
      orig_img = cv2.flip(orig_img, 1)
      img = cv2.GaussianBlur(orig_img, (5,5), 0)
      img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
      img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
      red_lower = np.array([120, 50, 50],np.uint8)
      red_upper = np.array([145, 255, 255],np.uint8)
      red_binary = cv2.inRange(img, red_lower, red_upper)
      dilation = np.ones((15, 15), "uint8")
      red_binary = cv2.dilate(red_binary, dilation)
      contours, hierarchy = cv2.findContours(red_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      max_area = 0
      largest_contour = None
      for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
          max_area = area
          largest_contour = contour
      if not largest_contour == None:
        moment = cv2.moments(largest_contour)
        if moment["m00"] > 1000 / self.scale_down:
          rect = cv2.minAreaRect(largest_contour)
          rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
          box = cv2.cv.BoxPoints(rect)
          self.points = box
          self.find_center()

          box = np.int0(box)
          cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)
          cv2.imshow("ColourTrackerWindow", orig_img)
          if cv2.waitKey(10) == 27:
            cv2.destroyWindow("ColourTrackerWindow")
            self.capture.release()
            break

  def find_center(self):
    # print self.points[0], self.points[1], self.points[2], self.points[3]
    p0 = self.points[0]
    p1 = self.points[1]
    p2 = self.points[2]
    p3 = self.points[3]
    center = [np.mean([p0[0], p1[0], p2[0], p3[0]]), np.mean([p0[1], p1[1], p2[1], p3[1]])]

    if center[1] > center[0] - 80 and center[1] < -center[0] + 480 + 80 and center[0] < (320 - 60):
      print "L"
    elif center[0] < center[1] + 80 and center[0] > -center[1] + 480 + 80 and center[1] > (240 + 60):
      print "D"
    elif center[0] > center[1] + 80 and center[0] < -center[1] + 480 + 80 and center[1] < (240 - 60):
      print "U"
    elif center[1] < center[0] - 80 and center[1] > -center[0] + 480 + 80 and center[0] > (320 + 60):
      print "R"
    else:
      print "C"

    # print center
    # if len(self.past) < 100:
    #   self.past += center
    # else:
    #   self.past = self.past[1:]
    #   self.past.append(center)
    #   if (self.past[15:][0] - self.past[:5][0]) > 100:
    #     print "R"
    #   elif (self.past[15:][0] - self.past[:5][0]) < 100:
    #     print "L"
    #   elif (self.past[15:][1] - self.past[:5][1]) > 100:
    #     print "D"
    #   elif (self.past[15:][1] - self.past[:5][1]) < 100:
    #     print "U"
    #   self.track()

  def track(self):
    pass

if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.run()
