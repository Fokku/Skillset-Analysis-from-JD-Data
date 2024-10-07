import pandas as pd
from datetime import datetime, timedelta

def convert_to_datetime(df, column_name):
    """
    Convert a column to datetime format.
    """
    print(f"{column_name} dtype:", df[column_name].dtype)
    print(f"{column_name} sample values:", df[column_name].head())

    # Try converting to datetime, assuming it's already in a recognizable format
    df['listed_date'] = pd.to_datetime(df[column_name], errors='coerce', unit='ms')

    # If conversion fails, try interpreting as days since a specific date (e.g., 1970-01-01)
    if df['listed_date'].isnull().all():
        print("Conversion failed, trying to convert as days since 1970-01-01")
        df['listed_date'] = pd.to_datetime('1970-01-01') + pd.to_timedelta(df[column_name], unit='D')

    print("Converted listed_date sample values:", df['listed_date'].head())
    return df

def filter_recent_dates(df, date_column, days=1):
    """
    Filter the dataframe to include only recent dates.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    return df[df[date_column] >= cutoff_date]

def group_by_time_and_skill(df, date_column, skill_column, freq='W'):
    """
    Group the dataframe by time (monthly) and skill, and return the top 5 skills.
    """
    # Ensure the date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Group by month and skill, count occurrences
    skills_over_time = df.groupby([df[date_column].dt.to_period(freq), skill_column]).size().unstack(fill_value=0)
    
    # Convert period index to datetime for better compatibility with Plotly
    skills_over_time.index = skills_over_time.index.to_timestamp()
    
    # Get top 5 skills
    top_5_skills = skills_over_time.sum().nlargest(5).index
    
    return skills_over_time, top_5_skills