from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image
import random
import glob

# Check if CUDA is available and set device accordingly
device = torch.device("cuda")

# Load the processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten").to(device)

# processor = TrOCRProcessor.from_pretrained("./results")
# model = VisionEncoderDecoderModel.from_pretrained("./results")


# Load image from local dataset
image = Image.open("src/detectors/Hi-SAM/demo/final_rois/final_roi_1.png").convert("RGB")

# Process the image and move pixel values to the GPU
pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

# Generate the text from the image
generated_ids = model.generate(pixel_values)

# Decode the generated text
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True, max_new_tokens=4000)[0]

# Print and show the results
print(generated_text)
image.show()
