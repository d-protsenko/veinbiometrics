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

    return parser.parse_args()


def multi_clahe(img, num):
    for i in range(num):
        img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4 + i * 2, 4 + i * 2)).apply(img)
    return img


def main():
    args = parse_arguments()

    img = cv2.imread(args.input_image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.fastNlMeansDenoising(gray, gray, 4)
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(gray, thresh=240, maxval=255, type=cv2.THRESH_BINARY, dst=mask)

    # im_thresh_gray = cv2.bitwise_and(gray, mask)
    # mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) #back to 3 channel img -> bitwise_and(...)

    cv2.imwrite('mask.png', mask)
    cv2.imwrite('mask_inverted.png', cv2.bitwise_not(mask))
    final = multi_clahe(gray, defaultCLAHEValue)

    cv2.imwrite(args.output_image, final)

    # cv2.imshow('image', final)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # bash preprocess.sh ./from_db/orig/101_3_f2_1.bmp finger_test.png


if __name__ == '__main__':
    main()
