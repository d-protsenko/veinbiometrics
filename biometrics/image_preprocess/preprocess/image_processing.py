import cv2
from PIL import Image
import os

defaultCLAHEValue = 4
defaultDenoiseLevel = 4


# applies Contrast Limited Adaptive Histogram Equalization to the image
def multi_clahe(img, num):
    for i in range(num):
        img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4 + i * 2, 4 + i * 2)).apply(img)
    return img


# reads image by path
def read(path):
    return cv2.imread(path)


# saves image to path
def write(path, image):
    return cv2.imwrite(filename=path, img=image)


# image can be converted to PIL img array
def convert_cv_to_pil(img):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(img)


def preprocess(path,
               output_path,
               lower_thresh,
               upper_thresh,
               denoise_lvl=defaultDenoiseLevel,
               clahe_number=defaultCLAHEValue):
    # TODO: fix problem with path's
    input_img = read(path)
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  # convert image color to gray
    cv2.fastNlMeansDenoising(gray, gray, denoise_lvl)  # denoise image
    mask = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(gray,
                  thresh=lower_thresh,
                  maxval=upper_thresh,
                  type=cv2.THRESH_BINARY,
                  dst=mask)  # get mask by color threshold
    cv2.bitwise_not(mask, mask)  # revert mask
    clahed = multi_clahe(gray, clahe_number)
    final = cv2.bitwise_and(clahed, clahed, mask=mask)
    return write(output_path, final)
