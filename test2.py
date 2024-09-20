import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import TrainingArguments, Trainer, AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
import numpy as np

# Load your data
job_data = pd.read_csv('new_job.csv')

# Step 1: Clean up the 'skills' column and create a mapping of unique skills
all_skills = set()
job_data['skills'].str.split(',').apply(all_skills.update)

# Create a mapping for skills to indices
# Check the skill mapping size
skill_mapping = {skill.strip(): idx for idx, skill in enumerate(sorted(all_skills))}
# Manually split the combined skill string into individual skills
corrected_skills = ['Writing skills', 'Content creation', 'SEO knowledge', 'Research skills', 'Grammar', 'Proofreading']

# Map these individual skills to valid indices
for skill in corrected_skills:
    if skill not in skill_mapping:
        skill_mapping[skill] = len(skill_mapping)  # Assign new indices if they don't exist

num_labels = len(skill_mapping)

# Split the data into training and testing sets
test_split = 0.1
train_df, test_df = train_test_split(
    job_data,
    test_size=test_split,
)

# Encode the 'skills' column as a binary vector of length num_labels
def encode_labels(skills_list, skill_mapping, num_labels):
    label_vectors = []
    for skills in skills_list:
        label_vector = np.zeros(num_labels)
        for skill in skills.split(','):
            label_vector[skill_mapping[skill.strip()]] = 1
        label_vectors.append(label_vector)
    return label_vectors

# Create encoded labels as binary vectors
train_labels = encode_labels(train_df['skills'].tolist(), skill_mapping, num_labels)
test_labels = encode_labels(test_df['skills'].tolist(), skill_mapping, num_labels)

# Extract job descriptions
train_texts = train_df['Job Description'].tolist()
eval_texts = test_df['Job Description'].tolist()

# Tokenize the text data
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

train_encodings = tokenizer(train_texts, padding="max_length", truncation=True, max_length=512)
eval_encodings = tokenizer(eval_texts, padding="max_length", truncation=True, max_length=512)

# Custom Dataset Class for Multi-Label Classification
class TextClassifierDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        # Convert binary label vector into tensor (multi-label classification)
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

# Prepare datasets
train_dataset = TextClassifierDataset(train_encodings, train_labels)
eval_dataset = TextClassifierDataset(eval_encodings, test_labels)

# Define the model for multi-label classification
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    problem_type="multi_label_classification",
    num_labels=num_labels
)

# Define training arguments
training_arguments = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
)

# Initialize the trainer
trainer = Trainer(
    model=model,
    args=training_arguments,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate()
