#!/usr/bin/env python
"Idenitfy clouds in images of sky"
import sys, cv2
import numpy as np

if len(sys.argv) < 2:
    print sys.stderr, "Error: ", sys.argv[0]
    sys.exit(1)

#Process files given on command line
for fname in sys.argv[1:]:
    #read file in, convert to grayscale
    img = cv2.imread(fname)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #mask for non cloud and non sky objects
    WHITE = np.array([255,255,255])
    WHITE_MAX = np.array([30,30,30])
    mask = cv2.inRange(img, WHITE_MAX, WHITE)
    #mask for sky but not cloud
    BLUE_MIN = np.array([90,10,0])
    BLUE_MAX = np.array([190,255,255])
    dst = cv2.inRange(img_hsv, BLUE_MIN, BLUE_MAX)
    dst = cv2.bitwise_not(dst)

    #combine masks
    maskcomb = cv2.bitwise_and(dst, mask)
    maskfinal = cv2.bitwise_not(maskcomb)
    #overlay mask on image
    res = cv2.bitwise_and(img,img,mask = maskfinal)

    #make black mask yellow
    res[np.where((res==[0,0,0]).all(axis=2))] = [25,150,150]

    #combine images into one window
    both = np.hstack((img,res))
    cv2.imshow('cloudpic', both)
    cv2.moveWindow('cloudpic', 40, 40)
    cv2.waitKey(2000)
    cv2.destroyWindow(fname)
