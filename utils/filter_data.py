def filter_data(df, selected_countries, selected_industries, selected_skills=None):
    filtered_df = df

    if selected_countries:
        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    if selected_industries:
        if isinstance(selected_industries, str):
            selected_industries = [selected_industries]
        filtered_df = filtered_df[
            filtered_df["industry_name"].isin(selected_industries)
        ]

    if selected_skills:
        if isinstance(selected_skills, str):
            selected_skills = [selected_skills]
        filtered_df = filtered_df[filtered_df["skill_name"].isin(selected_skills)]

    return filtered_df