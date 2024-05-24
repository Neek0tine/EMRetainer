<a href="https://github.com/Neek0tine/EMRetainer"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Neek0tine/Neek0tine/blob/main/stuff/EMRRdark.gif">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/Neek0tine/Neek0tine/blob/main/stuff/EMRR.gif">
  <img alt="EMRR Banner" src="https://github.com/Neek0tine/Neek0tine/blob/main/stuff/EMRR.gif">
</picture></a><br>

# Medical Record OCR Project

## Overview

This project focuses on the development of an Optical Character Recognition (OCR) system specifically designed for handwritten medical records from inpatients at Airlangga University Hospital (RSUA). The system aims to improve the digitization process of medical records by accurately recognizing and converting handwritten text into machine-readable format. The project involves data collection, preprocessing, OCR model fine-tuning, performance evaluation, and integration with a web-based interface.

## Methods

### Data Collection
Data in the form of handwritten medical record documents were collected from RSUA through manual scanning using smartphones or scanner devices. The data collection process was approved by the Faculty of Advanced Technology and Multidiscipline (FTMM) Airlangga University and carried out by submitting a formal data request to RSUA.

### Pre-Processing Data
The collected data is divided into two sets: 80% for validation and 20% for testing. The pre-processing steps include:

1. **Validation of Labeling Data:**
   - Labeling is done by reading handwriting on the image and adding the information in a separate document.
   - Matching the labels with the image files based on file names or other identification variables.
   - Ensuring the labeling format is consistent with the existing RSUA dataset if labels are already available.

2. **Data Augmentation:**
   - Performing image manipulations such as rotation, cropping, color changes, and brightness adjustments to increase the variety of data.
   - Ensuring the model can adapt to various image conditions and is robust to imperfect scans.

3. **Region of Interest (ROI) Search:**
   - Detecting handwriting areas where OCR will be applied using the Text Spotting Transformer (TESTR) model.
   - Obtaining coordinates of the bounding box for the area of interest and integrating these into the labeled dataset.

4. **Manual Resizing, Normalization, and Correction:**
   - Cleaning the final dataset to ensure high data quality.

### OCR Development
The OCR model was fine-tuned using a labeled medical record dataset to enhance text recognition accuracy. The pretrained Transformer OCR model proposed by Li (2021), which combines image and text processing using the Transformer architecture, was used for this purpose.

### Performance Evaluation
Performance was evaluated by calculating the Character Error Rate (CER). A maximum CER of 15% was set as the acceptable limit. If the CER exceeded this threshold, data correction or model adjustments were implemented.

### Spell Checker Integration
A spell checker was integrated to standardize drug names. It utilizes a combination of dictionary search, rule-based methods, and the Jaro-Winkler Similarity algorithm for correcting drug name spellings.

### Integration Website
The web interface was developed using the Flask framework as a Web Server Gateway Interface. It manages user data, result data, and web pages, forwarding the processed data to the Nginx server. The website allows users to:
- Upload PDF documents.
- Perform OCR conversions.
- Standardize drug names.
- Edit the converted text.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements
- Airlangga University Hospital (RSUA) for providing 
