def fill_data(merged_all):

    # Define columns to fill with "Not Specified" and 0
    cols_fill_not_specified = [
        "skills_desc",
        "type",
        "pay_period",
        "currency",
        "compensation_type",
        "posting_domain",
        "application_url",
        "formatted_experience_level",
        "company_size",
        "zip_code",
        "address",
        "state",
        "url",
        "city",
        "country",
        "name",
    ]
    cols_fill_zero = ["applies", "views", "follower_count", "employee_count"]

    for col in cols_fill_not_specified:
        merged_all[col].fillna("Not Specified", inplace=True)

    for col in cols_fill_zero:
        merged_all[col].fillna(0, inplace=True)

    # Fill remote_allowed with "Unknown"
    merged_all["remote_allowed"].fillna("Unknown", inplace=True)

    # Fill missing job descriptions
    merged_all["description_x"].fillna("Not Specified", inplace=True)

    # Remove duplicate rows
    cleaned_table = merged_all.drop_duplicates()

    # Check remaining missing values
    remaining_null = merged_all.isnull().sum()
    remaining_null_cols = remaining_null[remaining_null > 0].sort_values(
        ascending=False
    )

    return cleaned_table, remaining_null_cols
