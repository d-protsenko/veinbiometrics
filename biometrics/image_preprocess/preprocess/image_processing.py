import cv2
from PIL import Image
import numpy as np

defaultCLAHEValue = 4
defaultDenoiseLevel = 4
default_gauss_block_size = 27
default_gauss_constant = 8


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


def gauss_process(image, gauss_block_size, gauss_constant):
    img = cv2.medianBlur(image, 5)
    th_gauss = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, gauss_block_size, gauss_constant)
    return th_gauss


def grabcut_process(img, rect=(20, 20, 510, 200)):
    newmask = cv2.imread('./image_preprocess/preprocessed/mask.bmp', 0)
    mask = np.zeros(img.shape[:2], np.uint8)
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, rect, background_model, foreground_model, 4, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    mask[newmask == 0] = 0
    cv2.grabCut(img, mask, None, background_model, foreground_model, 5, cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    return img


def default_preprocess(input_img,
                       lower_thresh,
                       upper_thresh,
                       denoise_lvl,
                       clahe_lvl):
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  # convert image color to gray
    cv2.fastNlMeansDenoising(gray, gray, denoise_lvl)  # denoise image
    mask = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(gray,
                  thresh=lower_thresh,
                  maxval=upper_thresh,
                  type=cv2.THRESH_BINARY_INV,
                  dst=mask)  # get mask by color threshold
    clahed = multi_clahe(gray, clahe_lvl)
    final = cv2.bitwise_and(clahed, clahed, mask=mask)
    return final


def threshold(input_img, lower_thresh, upper_thresh):
    mask = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(input_img,
                  thresh=lower_thresh,
                  maxval=upper_thresh,
                  type=cv2.THRESH_BINARY_INV,
                  dst=mask)  # get mask by color threshold
    return mask


def masking(input_img, mask):
    masked = cv2.bitwise_and(input_img, input_img, mask=mask)
    return masked


def denoise(input_img, denoise_lvl):
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  # convert image color to gray
    cv2.fastNlMeansDenoising(gray, gray, denoise_lvl)  # denoise image
    return gray


def preprocess(input_path,
               preprocessed_path,
               gauss_path,
               grabcut_path,
               grabcut_gauss_output_path,
               lower_thresh,
               upper_thresh,
               denoise_lvl=defaultDenoiseLevel,
               clahe_lvl=defaultCLAHEValue,
               gauss_block_size=default_gauss_block_size,
               gauss_constant=default_gauss_constant
               ):
    # TODO: fix problem with path's
    # TODO: check possibility of loading files with not only english names
    # or add an regexp check on field

    input_img = read(input_path)
    final = default_preprocess(input_img, lower_thresh, upper_thresh, denoise_lvl, clahe_lvl)
    write(preprocessed_path, final)
    write(gauss_path, gauss_process(final, gauss_block_size, gauss_constant))

    input_grab = read(input_path)
    # denoised = denoise(input_grab, denoise_lvl)
    # grabbed = grabcut_process(denoised)
    # clahed_grab = multi_clahe(grabbed, clahe_lvl)

    grabcut_processed = default_preprocess(
        grabcut_process(img=input_grab),
        lower_thresh,
        upper_thresh,
        denoise_lvl,
        clahe_lvl
    )

    write(
        grabcut_path,
        grabcut_processed
    )
    write(grabcut_gauss_output_path, gauss_process(grabcut_processed, gauss_block_size, gauss_constant))
