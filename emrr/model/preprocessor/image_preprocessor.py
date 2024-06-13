__author__ = "Nicholas Juan Kalvin P., Muhammad Aulia, and Peter Maxwell"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
                    "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"

import cv2
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

class ImagePreprocessor:
    def __init__(self, size=(1080, 1920), beta_value=50):
        self.size = size
        self.beta_value = beta_value

    def resize_image(self, image_path, output_path):
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, self.size)
        cv2.imwrite(output_path, resized_image)

    def deskew_image(self, image_path, output_path):
        image = cv2.imread(image_path, 0)
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(output_path, deskewed_image)

    def binarize_image(self, image_path, output_path):
        image = cv2.imread(image_path, 0)
        binarized_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 2)
        cv2.imwrite(output_path, binarized_image)

    def greyscale_image(self, image_path, output_path):
        image = cv2.imread(image_path)
        greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_path, greyscale_image)
        
    def delete_jpg_files(self, directory):
        files = glob.glob(os.path.join(directory, '*.png'))
        for f in files:
            os.remove(f)

    def apply_bilateral_filter(self, image_path, output_path, d=15, sigmaColor=50, sigmaSpace=50):
        image = cv2.imread(image_path)
        filtered_image = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
        cv2.imwrite(output_path, filtered_image)


if __name__ == "__main__":
    preprocessor = ImagePreprocessor()
    print(os.getcwd())
    inputimg = "emrr/model/preprocessor/data/form1/diagnosis_utama_icd_10.png"
    outputdir = "src/preprocessor/results/"
    # preprocessor.delete_jpg_files(outputdir)
    preprocessor.greyscale_image(inputimg, (outputdir + "greyscaled" + ".png"))
    preprocessor.apply_bilateral_filter(image_path=(outputdir + "greyscaled" + ".png"), output_path=(outputdir + "bilateral" + ".png"))
    preprocessor.binarize_image((outputdir + "bilateral" + ".png"), (outputdir + "form1_final" + ".png"))
    