import os
import re
import time

import h5py
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize
from nltk import ngrams
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn

# Transformers and related libraries
import transformers
from transformers import pipeline, AutoTokenizer, AutoModel

nltk.download("punkt")
from nltk import PunktTokenizer
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn

# Transformers and related libraries
import transformers
from transformers import pipeline, AutoTokenizer, AutoModel


# Read the data
JOBS_FP = "postings.csv"
ESCO_SKILLS_FP = "skills_en.csv"

df = pd.read_csv(JOBS_FP)

# print the columns of the dataframe

print(df.columns)

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
# Drop rows with missing values
df.drop_duplicates(subset=["description"], keep="first", inplace=True)

print(df.head())
esco_df = pd.read_csv(ESCO_SKILLS_FP)
# Remove "(text)" occurences
esco_df["label_cleaned"] = esco_df["preferredLabel"].apply(
    lambda x: re.sub(r"\([^)]*\)", "", x).strip()
)
# Count words in skills after cleaning
esco_df["word_cnt"] = esco_df["label_cleaned"].apply(lambda x: len(str(x).split()))
esco_df = pd.DataFrame(esco_df, columns=["label_cleaned", "altLabels", "word_cnt"])

import langdetect

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Drop rows with missing values in specified columns
required_columns = ["description", "location", "company_name", "original_listed_time"]
df = df.dropna(subset=required_columns)


# Function to detect language
def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


df = df.head(4000)
# Detect language of each job description
df["language"] = df["description"].apply(detect_language)

# Filter only English descriptions
df = df[df["language"] == "en"]

# Drop the language column if no longer needed
df = df.drop(columns=["language"])

# Display the cleaned dataframe
print(df.head())
print(len(df["description"]))


# Define the ESCO dataset class
class EscoDataset(Dataset):
    def __init__(self, df, skill_col, backbone):
        texts = df
        self.tokenizer = AutoTokenizer.from_pretrained(backbone)
        self.texts = texts[skill_col].values.tolist()

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        res = self.tokenizer(
            self.texts[idx],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=20,
        )
        return {k: v[0] for k, v in res.items()}


# Define the model class
class ClsPool(nn.Module):
    def forward(self, x):
        # batch * num_tokens * num_embedding
        return x[:, 0, :]


class BertModel(nn.Module):
    def __init__(self, backbone):
        super().__init__()

        self.backbone_name = backbone
        self.backbone = AutoModel.from_pretrained(backbone)
        self.pool = ClsPool()

    def forward(self, x):
        x = self.backbone(**x)["last_hidden_state"]
        x = self.pool(x)

        return x


# Define the model parameters
backbone = "jjzha/jobbert_skill_extraction"
emb_label = "jobbert"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the ESCO dataset and create a DataLoader
ds = EscoDataset(esco_df, "label_cleaned", backbone)
dl = DataLoader(ds, shuffle=False, batch_size=32)

# Build custom model
model = BertModel(backbone)
model.eval()
model.to(device)

# Get embeddings for each skill
embs = []
with torch.no_grad():
    for i, x in enumerate(dl):
        x = {k: v.to(device) for k, v in x.items()}
        out = model(x)
        embs.extend(out.detach().cpu())
# Add them to the DataFrame
esco_df[emb_label] = embs


# Define get_sentences function
def get_sentences(job):
    """
    Given a raw html job description, parse it into sentences
    by using nltk's sentence tokenization + new line splitting
    """
    # Parse the job description using BeautifulSoup
    soup = BeautifulSoup(job, "html.parser")
    # Found some ads using unicode bullet points
    # Remove them to avoid splitting sentences incorrectly
    for p in soup.find_all("p"):
        # Remove bullet points
        p.string = p.get_text().replace("•", "")
        # Remove empty lines
    text = soup.get_text()
    # Split the text into sentences
    st = sent_tokenize(text)
    sentences = []
    # Split sentences by new line
    for sent in st:
        # Split by new line
        sentences.extend([x for x in sent.split("\n") if x != ""])
    return sentences


# Define the function to compute similarity between a vector and ESCO embeddings
def compute_similarity(vec, emb_type):
    """
    Compute vector similarity for a given vec and all the ESCO skills embeddings.
    If more embeddings were created, the type is specified by the input parameter.
    Return the ESCO skill id with max similarity
    """
    # Get the ESCO embeddings
    esco_embs = esco_df[emb_type]
    sims = []
    # Compute cosine similarities
    for i, esco_vec in enumerate(esco_embs):
        sims.append((i, cosine_similarity(vec, esco_vec.reshape(1, -1))))
    # Return max similarity and esco skill index
    idx, sim = max(sims, key=lambda x: x[1])
    return idx, sim.item()


# Define the function to compute similarity between a vector and ESCO embeddings
def compute_similarity_opt(emb_vec, emb_type):
    """
    Compute vector similarity for a given vec and all the ESCO skills embeddings
    by constructing a matrix from ESCO embeddings to process it faster.
    Return the ESCO skill id with max similarity.
    """
    # Extract ESCO embeddings for the given type
    esco_embs = [x for x in esco_df[emb_type]]
    esco_vectors = torch.stack(esco_embs)

    # Normalize the stacked embeddings and the input vector
    norm_esco_vectors = torch.nn.functional.normalize(esco_vectors, p=2, dim=1)
    norm_emb_vec = torch.nn.functional.normalize(emb_vec.T, p=2, dim=0)

    # Compute cosine similarities using matrix multiplication
    cos_similarities = torch.matmul(norm_esco_vectors, norm_emb_vec)

    # Return max similarity and ESCO skill index
    sim, idx = torch.max(cos_similarities, dim=0)
    return idx.item(), sim.item()


def compute_similarity_mat(emb_mat, emb_type):
    esco_embs = [x for x in esco_df[emb_type]]
    esco_vectors = torch.stack(esco_embs)
    emb_vectors = torch.stack(emb_mat)
    # Normalize the stacked embeddings and the input vectors
    norm_esco_vectors = torch.nn.functional.normalize(esco_vectors, p=2, dim=1)
    norm_emb_vecs = torch.nn.functional.normalize(emb_vectors.T, p=2, dim=0)
    # Compute cosine similarities
    cos_similarities = torch.matmul(norm_esco_vectors, norm_emb_vecs)
    # Return max similarity and esco skill index
    max_similarities, max_indices = torch.max(cos_similarities, dim=0)
    return max_indices.tolist(), max_similarities.tolist()


# Define the function to get the embeddings for a given text
def get_embedding(x):
    x = tokenizer(
        x, return_tensors="pt", padding="max_length", truncation=True, max_length=512
    )  # fix the code so that it does not exceed the size of tensor 512
    x = {k: v.to(device) for k, v in x.items()}
    return model(x).detach().cpu()


# Define the function to get the token classifiers
def get_classifiers(mtype):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if mtype == "jobbert":
        token_skill_classifier = pipeline(
            model="jjzha/jobbert_skill_extraction",
            aggregation_strategy="first",
            device=device,
            tokenizer=AutoTokenizer.from_pretrained(
                "jjzha/jobbert_skill_extraction", model_max_length=512
            ),
        )
        token_knowledge_classifier = pipeline(
            model="jjzha/jobbert_knowledge_extraction",
            aggregation_strategy="first",
            device=device,
            tokenizer=AutoTokenizer.from_pretrained(
                "jjzha/jobbert_knowledge_extraction", model_max_length=512
            ),
        )
    elif mtype == "xlmr":
        token_skill_classifier = pipeline(
            model="jjzha/escoxlmr_skill_extraction",
            aggregation_strategy="first",
            device=device,
        )
        token_knowledge_classifier = pipeline(
            model="jjzha/escoxlmr_knowledge_extraction",
            aggregation_strategy="first",
            device=device,
        )
    else:
        raise Exception("Unknown model name provided")
    return token_skill_classifier, token_knowledge_classifier


# Define the function to extract skills from a job description
def extract_skills(
    job,
    token_skill_classifier,
    token_knowledge_classifier,
    out_treshold=0.3,
    sim_threshold=0.3,
):
    """
    Extract skills from a job description using token classifiers and compute similarity with ESCO skills.
    Handles token classification outputs and filters based on vector similarity.
    """
    sentences = get_sentences(job)
    pred_labels = []
    res = []
    skill_embs = []
    skill_texts = []

    # Process each sentence in the job description
    for sent in sentences:
        skills = ner(sent, token_skill_classifier, token_knowledge_classifier)

        for entity in skills["entities"]:
            text = entity["word"]
            if entity["score"] > out_treshold:
                embedding = get_embedding(text).squeeze()

                # Ensure embedding is valid (non-empty)
                if embedding is not None and embedding.numel() > 0:
                    skill_embs.append(embedding)
                    skill_texts.append(text)
                else:
                    print(f"Warning: Empty embedding for text: {text}")

    # If no skills are found, return empty results
    if len(skill_embs) == 0:
        print("No valid skills extracted.")
        return [], []

    # Compute similarity matrix
    idxs, sims = compute_similarity_mat(skill_embs, emb_label)

    # Filter results based on similarity threshold
    for i in range(len(idxs)):
        if sims[i] > sim_threshold:
            pred_labels.append(idxs[i])
            res.append(
                (skill_texts[i], esco_df.iloc[idxs[i]]["label_cleaned"], sims[i])
            )

    return pred_labels, res


def aggregate_span(results):
    new_results = []
    current_result = results[0]

    for result in results[1:]:
        if result["start"] == current_result["end"] + 1:
            current_result["word"] += " " + result["word"]
            current_result["end"] = result["end"]
        else:
            new_results.append(current_result)
            current_result = result

    new_results.append(current_result)

    return new_results


def ner(text, token_skill_classifier, token_knowledge_classifier):
    output_skills = token_skill_classifier(text)
    for result in output_skills:
        if result.get("entity_group"):
            result["entity"] = "Skill"
            del result["entity_group"]

    output_knowledge = token_knowledge_classifier(text)
    for result in output_knowledge:
        if result.get("entity_group"):
            result["entity"] = "Knowledge"
            del result["entity_group"]

    if len(output_skills) > 0:
        output_skills = aggregate_span(output_skills)
    if len(output_knowledge) > 0:
        output_knowledge = aggregate_span(output_knowledge)

    skills = []
    skills.extend(output_skills)
    skills.extend(output_knowledge)
    return {"text": text, "entities": skills}


def process_sentence(sent):
    emb = get_embedding(sent)
    return compute_similarity_opt(emb, emb_label)


def extract_and_store_skills(row):
    description = row["description"]
    pred_labels, res = extract_skills(description, tsc, tkc)

    # Extract the ESCO skills from the result
    extracted_skills = [
        skill_info[1] for skill_info in res
    ]  # skill_info[1] is the ESCO skill name
    return extracted_skills


tokenizer = AutoTokenizer.from_pretrained(backbone)
model = BertModel(backbone)
model.to(device)
model.eval()


# Used in performance optimization and output example
job_sample = df.iloc[15]["description"]
print(job_sample)
threshold = 0.8

sentences = get_sentences(job_sample)

sim_start_time = time.time()
sent_embs = []
for sent in sentences:
    x = tokenizer(sent, return_tensors="pt")
    x = {k: v.to(device) for k, v in x.items()}
    emb = model(x).detach().cpu()
    sent_embs.append(emb.squeeze())
idxs, sims = compute_similarity_mat(sent_embs, emb_label)
# Calculate job description processing time
sim_end_time = time.time()
execution_time = sim_end_time - sim_start_time
print(f"Execution time: {execution_time:.4f} seconds")
tsc, tkc = get_classifiers("jobbert")


# Define the function to extract skills for each row
def extract_and_store_skills(row):
    description = row["description"]
    pred_labels, res = extract_skills(description, tsc, tkc)

    # Extract the ESCO skills from the result
    extracted_skills = [
        skill_info[1] for skill_info in res
    ]  # skill_info[1] is the ESCO skill name
    return extracted_skills


# Slice the DataFrame for rows 0 to 9
df_subset = df  # Use .copy() to avoid the SettingWithCopyWarning

# Apply the function to store skills in the 'skills' column using .loc[]
df_subset.loc[:, "skills"] = df_subset.apply(extract_and_store_skills, axis=1)

# Display the DataFrame to check the new 'skills' column
print(df_subset[["description", "skills"]])

# Export the subset to a JSON file
df_subset.to_json("test3.json", orient="records", lines=True)

# This will save the file 'extracted_skills_subset.json' containing the first 10 rows with their extracted skills
