import pandas as pd


def check_missing_values(missing_df):
    columns_with_missing = missing_df[missing_df["Missing Values"] > 0]

    if columns_with_missing.empty:
        return "No missing values found in this dataset."

    result = "Columns with missing values:\n\n"

    for _, row in columns_with_missing.iterrows():
        result += (
            f"- {row['Column']}: "
            f"{row['Missing Values']} missing values "
            f"({row['Missing %']}%)\n"
        )

    return result


def check_duplicates(duplicate_rows):
    return f"The dataset contains {duplicate_rows} duplicate rows."


def check_quality_score(quality_score):
    return f"The overall data quality score is {quality_score}/100."


def check_outliers(df):
    outlier_results = []
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        clean_col = df[col].dropna()

        if clean_col.empty:
            continue

        q1 = clean_col.quantile(0.25)
        q3 = clean_col.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        if len(outliers) > 0:
            outlier_results.append(
                f"{col}: {len(outliers)} outliers detected"
            )

    if not outlier_results:
        return "No major outliers detected."

    return "\n".join(outlier_results)


def recommend_cleaning_steps(recommendations, missing_df):
    columns_with_missing = missing_df[
        missing_df["Missing Values"] > 0
    ].sort_values(
        by="Missing %",
        ascending=False
    )

    response = ""

    if not columns_with_missing.empty:
        top_issue = columns_with_missing.iloc[0]

        response += (
            f"Priority 1: Clean column '{top_issue['Column']}' "
            f"because it has the highest missing value percentage "
            f"({top_issue['Missing %']}%).\n\n"
        )

    if recommendations:
        response += "Additional recommendations:\n\n"

        for rec in recommendations:
            response += f"- {rec}\n"

    return response


def generate_dataset_summary(df, duplicate_rows, missing_cells, quality_score):
    return f"""
Dataset Summary:
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Duplicate rows: {duplicate_rows}
- Missing cells: {missing_cells}
- Quality score: {quality_score}/100
"""