from argparse import ArgumentParser
import cv2
import os

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


def view_image(image, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main_gauss():
    args = parse_arguments()
    img = cv2.imread('./image.bmp', 0)
    img = cv2.medianBlur(img, 5)
    th_gauss = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    view_image(th_gauss, 'gauss')


def main():
    args = parse_arguments()
    img = cv2.imread(args.input_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.fastNlMeansDenoising(gray, gray, 4)
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(gray, thresh=145, maxval=255, type=cv2.THRESH_BINARY, dst=mask)
    cv2.bitwise_not(mask, mask)
    clahed = multi_clahe(gray, defaultCLAHEValue)
    final = cv2.bitwise_and(clahed, clahed, mask=mask)
    cv2.imwrite(final, args.output_image)
    # view_image(final, 'processed image')



if __name__ == '__main__':
    main()
