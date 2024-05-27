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

class ImagePreprocessor:
    def __init__(self, size=(1080, 1920), beta_value=50):
        self.size = size
        self.beta_value = beta_value

    def resize_image(self, image_path, output_path):
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, self.size)
        cv2.imwrite(output_path, resized_image)

    def denoise_image(self, image_path, output_path):
        image = cv2.imread(image_path)
        denoised_image = cv2.GaussianBlur(image, (5, 5), 0)
        cv2.imwrite(output_path, denoised_image)

    def adjust_contrast(self, image_path, output_path):
        image = cv2.imread(image_path, 0)  # Read the image in grayscale
        equalized_image = cv2.equalizeHist(image)
        cv2.imwrite(output_path, equalized_image)

    def adjust_brightness(self, image_path, output_path):
        image = cv2.imread(image_path)
        brightened_image = cv2.convertScaleAbs(image, beta=self.beta_value)
        cv2.imwrite(output_path, brightened_image)

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

    def perspective_correction(self, image_path, output_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200, 255)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            print("No suitable quadrilateral found.")
            # Optionally, save the original image if no correction is possible
            cv2.imwrite(output_path, image)
            return

        pts = screenCnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        corrected_image = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        cv2.imwrite(output_path, corrected_image)

    def crop_to_largest_square(self, image_path, output_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                square_side = min(w, h)
                cropped_image = image[y:y+square_side, x:x+square_side]
                cv2.imwrite(output_path, cropped_image)
                return

        # If no square is found, save the original image
        cv2.imwrite(output_path, image)

    def binarize_image(self, image_path, output_path):
        image = cv2.imread(image_path, 0)
        binarized_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(output_path, binarized_image)

    def greyscale_image(self, image_path, output_path):
        image = cv2.imread(image_path)
        greyscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_path, greyscale_image)

    def histogram_equalization(self, image_path, output_path):
            image = cv2.imread(image_path, 0)  # Read the image in grayscale
            equalized_image = cv2.equalizeHist(image)
            cv2.imwrite(output_path, equalized_image)

    def clahe(self, image_path, output_path):
            image = cv2.imread(image_path, 0)  # Read the image in grayscale
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            clahe_image = clahe.apply(image)
            cv2.imwrite(output_path, clahe_image)

    def unsharp_masking(self, image_path, output_path):
        image = cv2.imread(image_path)
        gaussian_blurred = cv2.GaussianBlur(image, (9, 9), 10.0)
        unsharp_image = cv2.addWeighted(image, 1.5, gaussian_blurred, -0.5, 0)
        cv2.imwrite(output_path, unsharp_image)
        
    def delete_jpg_files(self, directory):
        files = glob.glob(os.path.join(directory, '*.jpg'))
        for f in files:
            os.remove(f)

# Usage Example
if __name__ == "__main__":
    preprocessor = ImagePreprocessor()

    inputimg = "src/preprocessor/data/10.jpg"
    outputdir = "src/preprocessor/results/"
    

    # preprocessor.resize_image(inputimg, (outputdir + "output_resized" + ".jpg"))
        # preprocessor.adjust_contrast(inputimg, (outputdir + "output_contrast" + ".jpg"))
    # preprocessor.adjust_brightness(inputimg, (outputdir + "output_brightness" + ".jpg"))
    # preprocessor.deskew_image(inputimg, (outputdir + "output_deskew" + ".jpg"))
    # preprocessor.perspective_correction(inputimg, (outputdir + "output_perspective" + ".jpg"))
    # preprocessor.crop_to_largest_square(inputimg, (outputdir + "output_autocrop" + ".jpg"))
    # preprocessor.greyscale_image(inputimg, (outputdir + "output_greyscaled" + ".jpg"))
    # preprocessor.adjust_contrast((outputdir + "output_brightness" + ".jpg"), (outputdir + "output_contrast" + ".jpg"))
    preprocessor.histogram_equalization(inputimg, (outputdir + "he" + ".jpg"))
    preprocessor.clahe(inputimg, (outputdir + "clahe" + ".jpg"))
    preprocessor.unsharp_masking((outputdir + "clahe" + ".jpg"), (outputdir + "um" + ".jpg"))
    preprocessor.adjust_brightness((outputdir + "um" + ".jpg"), (outputdir + "output_brightness" + ".jpg"))
    preprocessor.binarize_image(inputimg, (outputdir + "output_binarized" + ".jpg"))
    # preprocessor.denoise_image((outputdir + "output_binarized" + ".jpg"), (outputdir + "output_denoised" + ".jpg"))
    