import pandas as pd
from datetime import datetime, timedelta


def convert_to_datetime(df, column_name):
    """
    Convert a column to datetime format.
    """
    df["listed_date"] = pd.to_datetime(df[column_name], unit="ms")
    df['day'] = df['listed_date'].dt.to_period('D')
    return df


def filter_recent_dates(df, date_column, days=210):
    """
    Filter the dataframe to include only recent dates.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    return df[df[date_column] >= cutoff_date]


def group_by_time_and_skill(df, time_column, skill_column):
    df['date'] = pd.to_datetime(df[time_column]).dt.date
    skill_counts = df.groupby(['date', skill_column]).size().unstack(fill_value=0)
    # get the top 3 skills and the lowest 3 skills
    varying_6_skills = skill_counts.sum().nlargest(3).index.tolist() + skill_counts.sum().nsmallest(3).index.tolist()
    return skill_counts, varying_6_skills
