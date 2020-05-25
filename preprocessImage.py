from argparse import ArgumentParser
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

defaultCLAHEValue = 4


def parse_arguments():
    parser = ArgumentParser(description='Preprocess image')
    parser.add_argument('-in', '--input',
                        type=str,
                        dest='input_image',
                        default='img.png',
                        help='Name of the input image, default is img.png'
                        )
    parser.add_argument('-out', '--output',
                        type=str,
                        dest='output_image',
                        default='image.png',
                        help='Name of the input image, default is image.png'
                        )
    parser.add_argument('-mask',
                        type=str,
                        dest='mask',
                        default='mask.png',
                        help='Name of the image mask file, default is mask.png'
                        )

    return parser.parse_args()


def multi_clahe(img, num):
    for i in range(num):
        img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(6 + i * 2, 6 + i * 2)).apply(img)
    return img


def view_image(image, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def gauss_process(image):
    img = cv2.medianBlur(image, 5)
    th_gauss = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    cv2.fastNlMeansDenoising(th_gauss, th_gauss, 4)
    view_image(th_gauss, 'gauss image')


def main(img):
    args = parse_arguments()
    # img = cv2.imread('./image.bmp')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.fastNlMeansDenoising(gray, gray, 4)
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    view_image(gray, '')
    cv2.threshold(gray, thresh=180, maxval=255, type=cv2.THRESH_BINARY_INV, dst=mask)
    # cv2.bitwise_not(mask, mask)
    view_image(mask, 'mask')
    clahed = multi_clahe(gray, defaultCLAHEValue)
    final = cv2.bitwise_and(clahed, clahed, mask=mask)
    # cv2.imwrite(final, args.output_image)
    view_image(final, 'preprocessed image')
    return final


def grabcut(img, rect=(0, 0, 510, 200)):
    newmask = cv2.imread('./mask.bmp', 0)

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
    plt.imshow(img), plt.colorbar(), plt.show()
    return img


if __name__ == '__main__':
    img = cv2.imread('./image.bmp')
    main(grabcut(img))
    gauss_process(main(grabcut(img)))
