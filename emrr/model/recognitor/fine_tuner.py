from datasets import load_dataset, Dataset
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
from PIL import Image
import torch

# Define a function to load images
def load_image(image_path):
    return Image.open(image_path).convert("RGB")

# Load your dataset from a JSON file
dataset = load_dataset('json', data_files={'train': 'path/to/your/train_dataset.json', 'validation': 'path/to/your/val_dataset.json'})

# Initialize the processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten").to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# Preprocess the dataset
def preprocess(batch):
    images = [load_image(image_path) for image_path in batch["image_path"]]
    pixel_values = processor(images, return_tensors="pt", padding=True).pixel_values
    labels = processor.tokenizer(batch["text"], padding="max_length", truncation=True, return_tensors="pt").input_ids
    batch["pixel_values"] = pixel_values
    batch["labels"] = labels
    return batch

# Apply preprocessing
train_dataset = dataset["train"].map(preprocess, batched=True, remove_columns=["image_path", "text"])
val_dataset = dataset["validation"].map(preprocess, batched=True, remove_columns=["image_path", "text"])

# Define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    logging_dir="./logs",
    evaluation_strategy="epoch"
)

# Initialize Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Train the model
trainer.train()
