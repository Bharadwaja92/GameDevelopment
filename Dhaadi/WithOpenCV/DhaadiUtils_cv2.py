import cv2
import numpy as np

""" First create an empty canvas """


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x=', x, ' y=', y)
        # cv2.circle(img=)


def createEmptyCanvas():
    height, width = 400, 600
    blank_image = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    blank_image[:] = (255, 255, 255)
    p1x, p1y, p2x, p2y = 100, 50, 450, 360
    p1 = (p1x, p1y)
    p2 = ((p1x + p2x) // 2, p1y)
    p3 = (p2x, p1y)
    p4 = (p1x, (p1y + p2y) // 2)
    p5 = ((p1x + p2x) // 2, (p1y + p2y) // 2)
    p6 = (p2x, (p1y + p2y) // 2)
    p7 = (p1x, p2y)
    p8 = ((p1x + p2x) // 2, p2y)
    p9 = (p2x, p2y)
    cv2.rectangle(img=blank_image, pt1=(p1x, p1y), pt2=(p2x, p2y), color=(0, 0, 0), thickness=2)
    cv2.line(img=blank_image, pt1=p2, pt2=p8, color=(0, 0, 0), thickness=2)
    cv2.line(img=blank_image, pt1=p4, pt2=p6, color=(0, 0, 0), thickness=2)
    cv2.line(img=blank_image, pt1=p1, pt2=p9, color=(0, 0, 0), thickness=2)
    cv2.line(img=blank_image, pt1=p3, pt2=p7, color=(0, 0, 0), thickness=2)

    cv2.namedWindow(winname='Dhaadi')
    cv2.setMouseCallback('Dhaadi', onMouse)

    cv2.imshow('Dhaadi', blank_image)
    cv2.waitKey(0)


createEmptyCanvas()




