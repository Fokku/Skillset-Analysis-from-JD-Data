# Visualizing job data & it's evolution across the years.

This project analyzes job descriptions from various industries and job levels (entry, mid, and senior) to extract and categorize key skillsets using Natural Language Processing (NLP) techniques in Python. The goal is to provide insights into the most in-demand skills across different position levels, industries, and regions by analyzing job listings from an external API.

## Features:

Data Collection: Automated job description retrieval via API integration.
NLP-Based Skill Extraction: Extraction of both hard and soft skills from job descriptions using NLP.
Skillset Categorization: Classification of skills based on job levels and industries.
Interactive Visualizations: Dashboard showcasing skill frequency, industry-specific demands, and trends across job levels.
Trend Analysis: Visualize emerging skills and evolving trends over time.
User Filters: Allow users to explore data based on industry, job level, and region.

## Tech Stack:

Language: Python
Libraries: NTLK, Plotly, Dash, Pandas
Data Source: Kaggle
Visualization Tools: Interactive dashboards powered by Plotly Express, Dash

## Setup:

- Clone the repository.

  ```bash
  git clone https://github.com/Fokku/Skillset-Analysis-from-JD-Data
  ```

- Install required dependencies.

  ```bash
  pip install -r requirements.txt
  ```

- Download [Linkedin Job Dataset from Kaggle] (https://www.kaggle.com/datasets/arshkon/linkedin-job-postings).
- Place `archive` folder into project root directory.
- Run data cleansing scripts if needed.

> [!IMPORTANT]
> If the archive folder is not detected, random data will be generated instead.
> In the case of a server deployment, data will be randomly generated as the dataset is too large to be hosted without paid options.

## TO-DO

## Footnotes:

[^1]: Fill in
[^2]: Fill in
