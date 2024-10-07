import pandas as pd
from datetime import datetime, timedelta


def convert_to_datetime(df, column_name):
    """
    Convert a column to datetime format.
    """
    df["listed_date"] = pd.to_datetime(df[column_name], unit="ms")
    return df


def filter_recent_dates(df, date_column, days=210):
    """
    Filter the dataframe to include only recent dates.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    return df[df[date_column] >= cutoff_date]


def group_by_time_and_skill(df, date_column, skill_column, freq="W"):
    """
    Group the dataframe by time (weekly) and skill, and return the top 5 skills.
    """
    df[date_column] = pd.to_datetime(df[date_column])

    skills_over_time = (
        df.groupby([pd.Grouper(key=date_column, freq=freq), skill_column])
        .size()
        .unstack(fill_value=0)
    )

    top_5_skills = skills_over_time.sum().nlargest(5).index

    return skills_over_time, top_5_skills
