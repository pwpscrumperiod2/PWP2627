import cv2 as cv
import numpy as np
import time

#saturate doesnt do much
def merge_lines(group):
    points = []
    lowY = []
    highY = []

    for x1, y1, x2, y2 in group:
        points.append([x1, y1])
        points.append([x2, y2])
        lowY.append(min(y1, y2))
        highY.append(max(y1, y2))

    points = np.array(points, dtype=np.float32)

    vx, vy, x, y = cv.fitLine(points, cv.DIST_L2, 0, 0.01, 0.01)
    vx, vy, x, y = float(vx[0]), float(vy[0]), float(x[0]), float(y[0])

    y1 = min(lowY)
    y2 = max(highY)
    x1 = int(x + (y1 - y) * vx / vy)
    x2 = int(x + (y2 - y) * vx / vy)

    return x1, y1, x2, y2

#image is a numpy array
def process_image(inputImage):    
#tips and tricks: use contrast and brightness and stuff
    # Loads an image for display purposes
    colorImage = inputImage #A NUMPY ARRAY

    #this image gets operated on
    #convert colorimage to grayscale
    image = cv.cvtColor(colorImage, cv.COLOR_BGR2GRAY)
    #Adjust contrast/brightness
    image = cv.convertScaleAbs(image, alpha=0.9, beta=0)


    #blurring and thresholding to help alievate background clutter
    """adjust parameters here to get better results"""
    #blurs to eliminate noise
    image = cv.GaussianBlur(
        image,
        ksize=(21, 21),
        sigmaX=0
    )

    #seperates object through thresholding, but not very well
    _, image = cv.threshold(
        image,
        thresh=127,
        maxval=255,
        type=cv.THRESH_TOZERO
    )

    ##canny edge detection to find edges
    image = cv.Canny(
        image,
        threshold1=100,
        threshold2=200,
        edges=None,
        apertureSize=3
    )

    #dilations to make lines thicker and more continuous, but also makes noise worse
    kernel = np.ones((3, 3), np.uint8)

    dst = cv.dilate(
        image,
        kernel=kernel,
        iterations=1
    )

    ########Region of interest: only look for lines in the bottom half of the image
    height, width = dst.shape
    vertices = np.array([[(0, height*0.5), (width, height*0.5), (width, height), (0, height)]], dtype=np.int32)

    roi = np.zeros_like(dst)
    cv.fillPoly(roi, vertices, 255)

    dst = cv.bitwise_and(dst, roi)

    ########
    """also adjust here"""
    #Hough transform to find lines in the image, returns a list of lines
    linesP = cv.HoughLinesP(
        image=dst,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        lines=None,
        minLineLength=100,
        maxLineGap=8
    )

    #tries to merge the tiny segments from each different lane
    left_lines = []
    right_lines = []
    for line in linesP:
        x1, y1, x2, y2 = line

        slope = (y2 - y1) / (x2 - x1 + 1e-6)

        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)

    lx1, ly1, lx2, ly2 = merge_lines(left_lines)
    cv.line(colorImage, (lx1, ly1), (lx2, ly2), (0,255,0), 3, cv.LINE_AA)

    rx1, ry1, rx2, ry2 = merge_lines(right_lines)
    cv.line(colorImage, (rx1, ry1), (rx2, ry2), (0,255,0), 3, cv.LINE_AA)

    #midpoint line display
    cv.line(colorImage, ((lx1+rx1)//2, (ly1+ry1)//2), ((lx2+rx2)//2, (ly2+ry2)//2), (255,0,0), 3, cv.LINE_AA)

    return colorImage
    