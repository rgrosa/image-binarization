import argparse
import os
import cv2
import logging
import numpy as np
import uuid

def createMatrixList(img_list):
    logging.info('Creating matrix list')
    new_img_list = []
    for img in img_list:
        new_img_list.append(cv2.imread(img.get("img")))
    return new_img_list


def binarizeMatrixList(matrix_list):
    new_img_list = []
    logging.info('Start binary matrix transformation')
    for matrix in matrix_list:
        matrix_to_process = matrix
        for i in range(0, matrix_to_process.shape[0]):
            for j in range(0, matrix_to_process.shape[1]):
                if matrix_to_process[i][j][0] < 100:
                    matrix_to_process[i][j] = (255, 255, 255)
                else:
                    matrix_to_process[i][j] = (0, 0, 0)
        new_img_list.append(matrix_to_process)
    logging.info('Binary matrix transformation end with success')
    return new_img_list


def save_matrix_list(matrix_list):
    i = 1
    logging.info(f'Saving matrix list')
    for matrix in matrix_list:
     cv2.imwrite(f'image{i}-{uuid.uuid4()}.png', matrix)
     i = i + 1


def apply_closing(matrix_list):
    new_img_list = []
    logging.info('Start closing morphological operation')
    kernel = np.ones((5, 5), np.uint8)
    for matrix in matrix_list:
        matrix = cv2.morphologyEx(matrix, cv2.MORPH_CLOSE, kernel)
        new_img_list.append(cv2.dilate(matrix, kernel, iterations=2))
    return new_img_list


def count_pixel_quantity(matrix_list):
    logging.info("Count white pixels")
    i = 1
    for matrix in matrix_list:
        count = np.count_nonzero((matrix == [255, 255, 255]).all(axis=2))
        logging.info(f'The count of white pixels for image{i} is {count}')
        i = i + 1


def createImageList(files):
    img_list = []
    for file in files:
        img_list.append({"img": file})
    return img_list


def main():
    parser = argparse.ArgumentParser(description="Convert images to binary")
    parser.add_argument('-f', '--file', nargs='+', help='files location')
    parser.add_argument('-c', '--close', type=bool, help='add close operation to images', default=False)

    args = parser.parse_args()

    if args.file is None:
        logging.info(f'No files informed')
        exit(0)

    img_list = createImageList(args.file)

    matrix_list = createMatrixList(img_list)

    matrix_list_post_binarize = binarizeMatrixList(matrix_list)
    save_matrix_list(matrix_list_post_binarize)

    if args.close:
        logging.info(f'Apply close operation')
        matrix_list_post_binarize = apply_closing(matrix_list_post_binarize)
        save_matrix_list(matrix_list_post_binarize)

    count_pixel_quantity(matrix_list_post_binarize)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    main()
