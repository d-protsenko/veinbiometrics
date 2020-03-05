import numpy as np
from argparse import ArgumentParser
import cv2

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
        img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4 + i * 2, 4 + i * 2)).apply(img)
    return img


def view_image(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    args = parse_arguments()

    img = cv2.imread(args.input_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.fastNlMeansDenoising(gray, gray, 2)

    mask = cv2.imread(args.mask, 0)
    clahed = multi_clahe(gray, defaultCLAHEValue)
    res = cv2.bitwise_and(clahed, clahed, mask=mask)
    cv2.imwrite(args.output_image, res)
    # view_image(res)
    # bash preprocess.sh 1.bmp


if __name__ == '__main__':
    main()
