import random

import cv2
from decimal import Decimal

import imutils
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from lena.utils.image_processing.filters_helper import try_threshold


def show(img):
    plt.imshow(img, cmap='gray')
    plt.show()

def get_contours_by_different_thresholds(grayscale_image, needs_to_remove_similar=False, block_size_min=3, block_size_max=11):
    binary_local, mean_binary, minimum_binary, otsu_binary, li_binary, isodata_binary, triangle_binary, yen_binary = try_threshold(grayscale_image, block_size_min, block_size_max)

    all_contours = []
    for binary_l in binary_local:
        try:
            contours, hierarchy = GetContoursByCanny(binary_l, 0, 255)
            all_contours.extend(contours)
        except:
            continue

    try:
        mean_binary_contours, _ = GetContoursByCanny(mean_binary, 0, 255)
        all_contours.extend(mean_binary_contours)
    except:
        print("error mean_binary_contours")

    try:
        minimum_binary_contours, _ = GetContoursByCanny(minimum_binary, 0, 255)
        all_contours.extend(minimum_binary_contours)
    except:
        print("error minimum_binary_contours")

    try:
        otsu_binary_contours, _ = GetContoursByCanny(otsu_binary, 0, 255)
        all_contours.extend(otsu_binary_contours)
    except:
        print("error otsu_binary_contours")

    try:
        li_binary_contours, _ = GetContoursByCanny(li_binary, 0, 255)
        all_contours.extend(li_binary_contours)
    except:
        print("error li_binary_contours")

    try:
        isodata_binary_contours, _ = GetContoursByCanny(isodata_binary, 0, 255)
        all_contours.extend(isodata_binary_contours)
    except:
        print("error isodata_binary_contours")

    try:
        triangle_binary_contours, _ = GetContoursByCanny(triangle_binary, 0, 255)
        all_contours.extend(triangle_binary_contours)
    except:
        print("error triangle_binary_contours")

    try:
        yen_binary_contours, _ = GetContoursByCanny(yen_binary, 0, 255)
        all_contours.extend(yen_binary_contours)
    except:
        print("error yen_binary_contours")


    #rectangles = np.zeros((len(all_contours), 4), dtype=np.int32)
    rectangles = []
    for i in range(len(all_contours)):
        x, y, w, h = cv2.boundingRect(all_contours[i])
        #rectangles[i] = (x, y, x + w, y + h)
        rectangles.append((x, y, w, h))
        #rectangles.append((x, y, x + w, y + h))

    #if(needs_to_remove_similar):
    #    rectangles = non_max_suppression(rectangles, probs=None, overlapThresh=0.9)

    #return all_contours, rectangles
    return all_contours

def get_contours(image_bw):
    contours, hierarchy = cv2.findContours(image_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy

def get_contours_external_only(image_bw):
    contours, hierarchy = cv2.findContours(image_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy
