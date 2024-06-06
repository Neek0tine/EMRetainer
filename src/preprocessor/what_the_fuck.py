__author__ = "Nicholas Juan Kalvin P."
__copyright__ = "Copyright 2024, The EMRR Project"
__credits__ = ["Nicholas Juan Kalvin P.", "Muhammad Aulia H.", "Sukma Sekar Devita",
                    "Nabila Dien Jasmine"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Juan Kalvin P."
__email__ = "nicholas.juan.kalvin-2020@ftmm.unair.ac.id"
__status__ = "Development"

import cv2
import os
import numpy as np
import argparse
import csv

class ImageProcessor:
    def __init__(self, image_path: str, output_dir: str):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Image at path {image_path} could not be loaded.")
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def extract_rois(self, coordinates: dict) -> list:
        rois = []
        for name, (x1, y1, x2, y2) in coordinates.items():
            # Validate coordinates
            if x1 < 0 or y1 < 0 or x2 > self.image.shape[1] or y2 > self.image.shape[0]:
                print(f"Invalid coordinates for ROI '{name}': {(x1, y1, x2, y2)}")
                continue
            roi = self.image[y1:y2, x1:x2]
            rois.append(roi)
            roi_path = os.path.join(self.output_dir, f"{name}.png")
            cv2.imwrite(roi_path, roi)
        return rois

    def draw_boxes(self, coordinates: dict):
        image_with_boxes = self.image.copy()
        for name, (x1, y1, x2, y2) in coordinates.items():
            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image_with_boxes, name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image_with_boxes

    def save_image(self, image, output_path):
        cv2.imwrite(output_path, image)

def read_coords_file(coords_file: str) -> dict:
    coords = {}
    with open(coords_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            name, x1, y1, x2, y2 = row
            coords[name] = (int(x1), int(y1), int(x2), int(y2))
    return coords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an image to extract RoIs and draw boxes.')
    parser.add_argument('--image', required=True, help='Path to the input image.')
    parser.add_argument('--output', required=True, help='Directory to save the output images.')
    parser.add_argument('--coords', required=True, help='Path to the coordinates CSV file.')
    
    args = parser.parse_args()
    
    coordinates = read_coords_file(args.coords)
    
    processor = ImageProcessor(args.image, args.output)
    processor.extract_rois(coordinates)
    
    image_with_boxes = processor.draw_boxes(coordinates)
    processor.save_image(image_with_boxes, os.path.join(args.output, 'image_with_boxes.png'))
    
    print(f"Processed image and RoIs saved to {args.output}")
