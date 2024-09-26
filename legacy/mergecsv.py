import pandas as pd

# Read the CSV files
company_specialities = pd.read_csv("kaggle/company_specialities.csv")
company_industries = pd.read_csv("kaggle/company_industries.csv")
job_industries = pd.read_csv("kaggle/job_industries.csv")
industry_mappings = pd.read_csv("kaggle/industries.csv")
skill_mappings = pd.read_csv("kaggle/skills.csv")
postings = pd.read_csv("kaggle/postings.csv")
salaries = pd.read_csv("kaggle/salaries.csv")

# Merge the job industries with industry mappings
industries_df = job_industries.merge(industry_mappings, on="industry_id")

# Merge the postings with all the provided infos
postings = postings\
    .merge(salaries, on="job_id")\
    .merge(industries_df, on="job_id")\
    .merge(company_specialities, on="company_id")

# Filter out rows where pay_period is "HOURLY" or work_type is not "FULL_TIME"
postings = postings[(postings['pay_period_x'] != 'HOURLY') & (postings['work_type'] == 'FULL_TIME')]

# Print columns of the merged DataFrame to debug
print("Columns in merged DataFrame:", postings.columns)

# Group by job_id and aggregate the required columns
postings = postings.groupby('job_id').agg(
    description=('description', 'first'),
    company_name=('company_name', 'first'),
    work_type=('work_type', 'first'),
    min_salary=('min_salary_x', 'first'),
    max_salary=('max_salary_x', 'first'),
    pay_period=('pay_period_x', 'first'),
    location=('location', 'first'),
    original_list_date=('original_listed_time', 'first'),
    job_posting_url=('job_posting_url', 'first'),
    title=('title', 'first'),
    speciality_set=('speciality', set),
    industry_set=('industry_name', set)
).reset_index()

# Print the first few rows of the aggregated DataFrame
print(postings.head())

# Export the postings DataFrame to a CSV file
postings.to_csv("kaggle/postings_export.csv", index=False)

# Print confirmation
print("Postings have been exported to 'kaggle/postings_export.csv'")