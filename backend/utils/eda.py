def describe_table(df):
    summary = df.describe(include='all').to_dict()
    return summary
