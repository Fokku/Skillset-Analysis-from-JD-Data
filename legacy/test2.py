import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, pipeline
import nltk

nltk.download("punkt")

# Read the data
JOBS_FP = "postings.csv"
ESCO_SKILLS_FP = "skills_en.csv"

df = pd.read_csv(JOBS_FP)
esco_df = pd.read_csv(ESCO_SKILLS_FP)

# Drop columns that are not needed
df = df.drop(
    columns=[
        "job_id",
        "pay_period",
        "company_id",
        "views",
        "med_salary",
        "formatted_work_type",
        "remote_allowed",
        "application_url",
        "applies",
        "application_type",
        "expiry",
        "closed_time",
        "skills_desc",
        "posting_domain",
        "sponsored",
        "currency",
        "compensation_type",
        "zip_code",
        "fips",
    ]
)

# Use only the first 5000 rows
df = df.head(5000)

# Tokenize job descriptions
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
df["tokens"] = df["description"].apply(
    lambda x: tokenizer.encode(x, truncation=True, padding="max_length", max_length=512)
)

# Use a pre-trained model to extract skills from job descriptions
skill_extractor = pipeline("ner", model="dslim/bert-base-NER")
df["extracted_skills"] = df["description"].apply(
    lambda x: [
        entity["word"]
        for entity in skill_extractor(x)
        if entity["entity"].startswith("B-")
    ]
)


class JobDataset(Dataset):
    def __init__(self, descriptions, skills):
        self.descriptions = descriptions
        self.skills = skills

    def __len__(self):
        return len(self.descriptions)

    def __getitem__(self, idx):
        return torch.tensor(self.descriptions[idx]), torch.tensor(self.skills[idx])


# Convert extracted skills to a binary matrix
all_skills = list(set(skill for skills in df["extracted_skills"] for skill in skills))
skill_to_idx = {skill: idx for idx, skill in enumerate(all_skills)}
df["skills_vector"] = df["extracted_skills"].apply(
    lambda skills: [1 if skill in skills else 0 for skill in all_skills]
)

# Split the data into training and validation sets
train_df = df.iloc[:4000]
val_df = df.iloc[4000:]

train_dataset = JobDataset(
    train_df["tokens"].tolist(), train_df["skills_vector"].tolist()
)
val_dataset = JobDataset(val_df["tokens"].tolist(), val_df["skills_vector"].tolist())

train_dataloader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=16, shuffle=False)

import torch.nn as nn
import torch.optim as optim
from transformers import AutoModel


class SkillPredictor(nn.Module):
    def __init__(self):
        super(SkillPredictor, self).__init__()
        self.bert = AutoModel.from_pretrained("bert-base-uncased")
        self.fc = nn.Linear(768, len(all_skills))  # Number of skills

    def forward(self, input_ids):
        outputs = self.bert(input_ids)
        cls_output = outputs.last_hidden_state[:, 0, :]  # CLS token output
        skill_logits = self.fc(cls_output)
        return skill_logits


model = SkillPredictor()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 5

for epoch in range(num_epochs):
    model.train()
    for descriptions, skills in train_dataloader:
        optimizer.zero_grad()
        outputs = model(descriptions)
        loss = criterion(outputs, skills.float())
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# Save the trained model
torch.save(model.state_dict(), "skill_predictor.pth")

model.eval()
total_loss = 0
with torch.no_grad():
    for descriptions, skills in val_dataloader:
        outputs = model(descriptions)
        loss = criterion(outputs, skills.float())
        total_loss += loss.item()

print(f"Validation Loss: {total_loss / len(val_dataloader)}")

# Load the trained model
model = SkillPredictor()
model.load_state_dict(torch.load("skill_predictor.pth"))
model.eval()

# Load the original data
df = pd.read_csv(JOBS_FP)

# Drop columns that are not needed
df = df.drop(
    columns=[
        "job_id",
        "pay_period",
        "company_id",
        "views",
        "med_salary",
        "formatted_work_type",
        "remote_allowed",
        "application_url",
        "applies",
        "application_type",
        "expiry",
        "closed_time",
        "skills_desc",
        "posting_domain",
        "sponsored",
        "currency",
        "compensation_type",
        "zip_code",
        "fips",
    ]
)

# Select the next 1000 rows (from index 4000 to 4999)
new_df = df.iloc[4000:5000]

# Tokenize new job descriptions
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
new_df["tokens"] = new_df["description"].apply(
    lambda x: tokenizer.encode(x, truncation=True, padding="max_length", max_length=512)
)

# Convert tokens to tensor
new_tokens = new_df["tokens"].tolist()
new_tokens_tensor = torch.tensor(new_tokens)

# Create a DataLoader for the new job descriptions
new_dataset = JobDataset(
    new_df["tokens"].tolist(), [[0] * len(all_skills)] * len(new_df)
)  # Dummy skills vector
new_dataloader = DataLoader(new_dataset, batch_size=16, shuffle=False)

# Make predictions
predicted_skills = []
model.eval()
with torch.no_grad():
    for descriptions, _ in new_dataloader:
        outputs = model(descriptions)
        predicted_skills.append(torch.sigmoid(outputs).round().int())

# Concatenate all predictions
predicted_skills = torch.cat(predicted_skills, dim=0)

# Map indices to skill names
idx_to_skill = {idx: skill for skill, idx in skill_to_idx.items()}

# Convert binary predictions to skill names
predicted_skill_names = []
for skill_vector in predicted_skills:
    skills = [idx_to_skill[idx] for idx, val in enumerate(skill_vector) if val == 1]
    predicted_skill_names.append(skills)

# Add the predicted skills to the DataFrame
new_df["predicted_skills"] = predicted_skill_names

# Export the DataFrame to a JSON file
new_df[["description", "predicted_skills"]].to_json(
    "predicted_skills.json", orient="records", lines=True
)

# Print confirmation
print("Predicted skills have been exported to 'predicted_skills.json'")
