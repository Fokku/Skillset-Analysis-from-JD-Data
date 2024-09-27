import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import TruncatedSVD
# from sklearn.cluster import KMeans
# from sklearn.pipeline import make_pipeline

from fill import fill_data

class Data:
    def __init__(self) -> pd.DataFrame:
        self.cleaned_table = cleaned_table
        self.remaining_null_cols = remaining_null_cols
    
    def get_cleaned_table(self):
        return self.cleaned_table

    def get_remaining_null_cols(self):
        return self.remaining_null_cols
    
    def get_country_data(self):
        return self.cleaned_table['country'].unique()
    
    def get_industries_data(self):
        return self.cleaned_table['industries'].unique()
    


# Load datasets
try:
    job_postings = pd.read_csv('archive/postings.csv')
    benefits = pd.read_csv('archive/jobs/benefits.csv')
    job_industries = pd.read_csv('archive/jobs/job_industries.csv')
    job_skills = pd.read_csv('archive/jobs/job_skills.csv')
    # Not using salary data as it is unreliable.
    # job_salaries = pd.read_csv('/archive/jobs/salaries.csv')
    companies = pd.read_csv('archive/companies/companies.csv')
    employee_counts = pd.read_csv('archive/companies/employee_counts.csv')
    company_industries = pd.read_csv('archive/companies/company_industries.csv')
    company_specialities = pd.read_csv('archive/companies/company_specialities.csv')
except FileNotFoundError as error:
    print(error)
    print("Please ensure that all datasets are within the archive folder.")
    exit(1)

# Check unique values
unique_values = {
    'job_postings': job_postings['job_id'].nunique(),
    'benefits': benefits['job_id'].nunique(),
    'job_industries': job_industries['job_id'].nunique(),
    'job_skills': job_skills['job_id'].nunique(),
    'companies': companies['company_id'].nunique(),
    'employee_counts': employee_counts['company_id'].nunique(),
    'company_industries': company_industries['company_id'].nunique(),
    'company_specialities': company_specialities['company_id'].nunique()
}
for i in unique_values:
    print("Unique values for {}: {}".format(i, unique_values[i]))

# Merge datasets
merged_jobs = pd.merge(job_postings, benefits, on='job_id', how='left')
merged_companies = pd.merge(companies, employee_counts, on='company_id', how='left')
merged_all = pd.merge(merged_jobs, merged_companies, on='company_id', how='left')

# Check for missing values
missing_values = merged_all.isnull().sum()
print(missing_values[missing_values > 0].sort_values(ascending=False))

# Fill missing values
cleaned_table, remaining_null_cols = fill_data(merged_all)


