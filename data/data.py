import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import TruncatedSVD
# from sklearn.cluster import KMeans
# from sklearn.pipeline import make_pipeline

class Data:
    def __init__(self):
        self.cleaned_table = cleaned_table
        self.remaining_null_cols = remaining_null_cols
    
    def get_cleaned_table(self):
        return self.cleaned_table

    def get_remaining_null_cols(self):
        return self.remaining_null_cols
    
    def get_country_list(self):
        country_counts = self.cleaned_table['country'].value_counts()
        valid_countries = country_counts[(country_counts.index != '0') & (country_counts.index != "Not Specified")]
        return valid_countries.index.tolist()
    
    def get_industry_list(self):
        industry_counts = self.cleaned_table['industry_name'].value_counts()
        valid_industries = industry_counts[(industry_counts.index != '0') & (industry_counts.index != "Not Specified")]
        return valid_industries.index.tolist()
    
    def get_skills_list(self):
        return list(self.cleaned_table['skill_name'].unique())

rows_not_needed = [
    'pay_period',
    'remote_allowed',
    'job_posting_url',
    'application_url',
    'application_type',
    'expiry',
    'closed_time',
    'sponsored',
    'currency',
    'compensation_type',
    'zip_code_x',
    'fips',
    'inferred',
    'state',
    'zip_code_y',
    'address',
    'url',
    'industry_id',
    'posting_domain',
    'skill_abr',
    'time_recorded',
]

def fill_data(merged_all):

    # Define columns to fill with "Not Specified" and 0
    cols_fill_not_specified = ['skills_desc', 'type', 'pay_period', 'currency', 'compensation_type', 'posting_domain',
                            'application_url', 'formatted_experience_level', 'company_size', 'address',
                            'state', 'url', 'city', 'country', 'name']
    cols_fill_zero = ['applies', 'views', 'follower_count', 'employee_count']

    for col in cols_fill_not_specified:
        merged_all[col].fillna("Not Specified", inplace=True)

    for col in cols_fill_zero:
        merged_all[col].fillna(0, inplace=True)

    # Fill remote_allowed with "Unknown"
    merged_all['remote_allowed'].fillna("Unknown", inplace=True)

    # Fill missing job descriptions
    merged_all['description_x'].fillna("Not Specified", inplace=True)

    # Remove duplicate rows
    cleaned_table = merged_all.drop_duplicates()

    print(cleaned_table.head().columns.values.tolist())

    # Check remaining missing values
    remaining_null = merged_all.isnull().sum()
    remaining_null_cols = remaining_null[remaining_null > 0].sort_values(ascending=False)

    return cleaned_table, remaining_null_cols

if not os.path.exists('data/cleaned_table.csv'):
    print("Cache Data not found, formatting data...")

    if not os.path.exists('archive'):
        # Load datasets
        try:
            job_postings = pd.read_csv('archive/postings.csv')
            benefits = pd.read_csv('archive/jobs/benefits.csv')
            job_industries = pd.read_csv('archive/jobs/job_industries.csv')
            job_industries_mapping = pd.read_csv('archive/mappings/industries.csv')
            job_skills = pd.read_csv('archive/jobs/job_skills.csv')
            job_skills_mapping = pd.read_csv('archive/mappings/skills.csv')
            # Salary data is not accurate, leave for now
            # job_salaries = pd.read_csv('archive/jobs/salaries.csv')
            companies = pd.read_csv('archive/companies/companies.csv')
            employee_counts = pd.read_csv('archive/companies/employee_counts.csv')
            company_industries = pd.read_csv('archive/companies/company_industries.csv')
            company_specialities = pd.read_csv('archive/companies/company_specialities.csv')
            # Test for columns in dataframes
            # for i in [job_postings, benefits, job_industries, job_skills, companies, employee_counts, company_industries, company_specialities]:
            #     print(i.head().columns.values.tolist())
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

        # Merge datasets (Mappings)
        merged_job_industries = pd.merge(job_industries, job_industries_mapping, on='industry_id', how='left')
        merged_job_skills = pd.merge(job_skills, job_skills_mapping, on='skill_abr', how='left')
        merged_companies = pd.merge(companies, employee_counts, on='company_id', how='left')

        # Merge datasets
        merged_benefits = pd.merge(job_postings, benefits, on='job_id', how='left')
        merged_industries = pd.merge(merged_benefits, merged_job_industries, on='job_id', how='left')
        merged_skills = pd.merge(merged_industries, merged_job_skills, on='job_id', how='left')

        merged_all = pd.merge(merged_skills, merged_companies, on='company_id', how='left')

        # Check for missing values
        missing_values = merged_all.isnull().sum()
        print(missing_values[missing_values > 0].sort_values(ascending=False))

        # Fill missing values
        cleaned_table, remaining_null_cols = fill_data(merged_all)

        # Drop columns not needed
        cleaned_table.drop(columns=rows_not_needed, inplace=True)
        
        # Save cleaned table to CSV for quality assurance :)
        cleaned_table.to_csv('data/cleaned_table.csv', index=False)
        cleaned_table.iloc[0].to_json('data/data-format.json')

    else:
        print("Archive folder not found. Creating fake data for testing...")
        # Create fake data
        num_rows = 10000
        current_time = datetime.now()
        
        fake_data = {
            'job_id': range(1, num_rows + 1),
            'company_name': np.random.choice(['Company A', 'Company B', 'Company C', 'Company D', 'Company E'], num_rows),
            'title': np.random.choice(['Software Engineer', 'Data Scientist', 'Product Manager', 'Sales Representative', 'Marketing Specialist'], num_rows),
            'description_x': ['Fake job description ' + str(i) for i in range(1, num_rows + 1)],
            'max_salary': np.random.uniform(50000, 200000, num_rows).round(2),
            'location': np.random.choice(['New York, NY', 'San Francisco, CA', 'London, UK', 'Berlin, Germany', 'Toronto, Canada'], num_rows),
            'company_id': np.random.randint(1000000, 9999999, num_rows),
            'views': np.random.randint(0, 1000, num_rows),
            'med_salary': np.random.uniform(40000, 150000, num_rows).round(2),
            'min_salary': np.random.uniform(30000, 100000, num_rows).round(2),
            'formatted_work_type': np.random.choice(['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship'], num_rows),
            'applies': np.random.randint(0, 100, num_rows),
            'original_listed_time': [int((current_time - timedelta(days=np.random.randint(1, 30))).timestamp() * 1000) for _ in range(num_rows)],
            'formatted_experience_level': np.random.choice(['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive'], num_rows),
            'skills_desc': ['Required skills: ' + ', '.join(np.random.choice(['Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis', 'Project Management'], 3, replace=False)) for _ in range(num_rows)],
            'listed_time': [int((current_time - timedelta(days=np.random.randint(1, 30))).timestamp() * 1000) for _ in range(num_rows)],
            'work_type': np.random.choice(['FULL_TIME', 'PART_TIME', 'CONTRACT', 'TEMPORARY', 'INTERNSHIP'], num_rows),
            'normalized_salary': np.random.uniform(30000, 200000, num_rows).round(2),
            'type': np.random.choice(['Permanent', 'Contract', 'Temporary', 'Internship', 'Not Specified'], num_rows),
            'industry_name': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing'], num_rows),
            'skill_name': np.random.choice(['Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis', 'Project Management'], num_rows),
            'name': np.random.choice(['Company A', 'Company B', 'Company C', 'Company D', 'Company E'], num_rows),
            'description_y': ['Company description for ' + str(i) for i in range(1, num_rows + 1)],
            'company_size': np.random.choice(['1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5001-10000', '10001+'], num_rows),
            'country': np.random.choice(['US', 'UK', 'CA', 'DE', 'FR', 'Not Specified'], num_rows),
            'city': np.random.choice(['New York', 'San Francisco', 'London', 'Berlin', 'Toronto', 'Not Specified'], num_rows),
            'employee_count': np.random.randint(10, 100000, num_rows),
            'follower_count': np.random.randint(0, 1000000, num_rows)
        }
        
        cleaned_table = pd.DataFrame(fake_data)
        remaining_null_cols = pd.Series(dtype=int)  # Empty series for remaining null columns
        
        # Save fake data to CSV
        cleaned_table.to_csv('data/cleaned_table.csv', index=False)
        print("Fake data created and saved to data/cleaned_table.csv")

        # Save a sample row as JSON for data format reference
        cleaned_table.iloc[0].to_json('data/data-format.json', indent=2)
        print("Sample data format saved to data/data-format.json")

else:
    print("Cache Data found, loading data...")
    cleaned_table = pd.read_csv('data/cleaned_table.csv')
    remaining_null_cols = None
    print("Cache Data loaded successfully.")

# Create an instance of the Data class after loading the data
# data = Data()