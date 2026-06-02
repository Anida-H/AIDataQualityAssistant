import pandas as pd
from agent.dataset_chat_router import detect_dataset_chat_intent

def answer_dataset_question(question, df):
    question_lower = question.lower()

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    try:
        llm_intent = detect_dataset_chat_intent(question, df.columns.tolist())
    except Exception:
        llm_intent = None


    # Numeric columns
    if llm_intent == "numeric_columns" or ("numeric" in question_lower and "column" in question_lower):
        return f"Numeric columns are: {', '.join(numeric_cols)}"

    # Column list
    if llm_intent == "column_list" or "columns" in question_lower or "column names" in question_lower:
        return f"The dataset columns are: {', '.join(df.columns)}"

    # Row count
    if llm_intent == "row_count" or "how many rows" in question_lower or "number of rows" in question_lower:
        return f"The dataset contains {df.shape[0]} rows."

    # Average / Mean
    if llm_intent == "average" or "average" in question_lower or "mean" in question_lower:
        for col in numeric_cols:
            if col.lower() in question_lower:
                avg_value = df[col].mean()
                return f"The average value of '{col}' is {avg_value:.2f}."

        return f"Please specify one numeric column. Available numeric columns: {', '.join(numeric_cols)}"

    # Maximum / Highest
    if llm_intent == "maximum" or "maximum" in question_lower or "max" in question_lower or "highest" in question_lower:
        for col in numeric_cols:
            if col.lower() in question_lower:
                max_value = df[col].max()
                return f"The maximum value of '{col}' is {max_value}."

    # Minimum / Lowest
    if llm_intent == "minimum" or "minimum" in question_lower or "min" in question_lower or "lowest" in question_lower:
        for col in numeric_cols:
            if col.lower() in question_lower:
                min_value = df[col].min()
                return f"The minimum value of '{col}' is {min_value}."

    # Count by category value
    if llm_intent == "category_count" or "how many" in question_lower:
        for col in categorical_cols:
            for value in df[col].dropna().unique():
                if str(value).lower() in question_lower:
                    count = df[
                        df[col].astype(str).str.lower() == str(value).lower()
                    ].shape[0]

                    return f"There are {count} rows where '{col}' is '{value}'."

    # Most frequent category
    if llm_intent == "most_frequent" or "most frequent" in question_lower or "appears most" in question_lower:
        for col in categorical_cols:
            if col.lower() in question_lower:
                top_value = df[col].mode().iloc[0]
                count = df[col].value_counts().iloc[0]

                return (
                    f"The most frequent value in '{col}' is "
                    f"'{top_value}' with {count} rows."
                )

    # Which category spends the most / highest total
    if llm_intent == "group_total" or (
        "spends the most" in question_lower
        or "highest spending" in question_lower
        or "highest total" in question_lower
        or "most spent" in question_lower
    ):
        amount_col = find_amount_column(numeric_cols)

        if amount_col is None:
            return "I could not find a numeric spending/amount column."

        group_col = find_group_column(question_lower, categorical_cols)

        if group_col is None:
            return (
                "Please specify the grouping column, for example: "
                "'Which country spends the most?'"
            )

        grouped = (
            df.groupby(group_col)[amount_col]
            .sum()
            .sort_values(ascending=False)
        )

        top_group = grouped.index[0]
        top_value = grouped.iloc[0]

        return (
            f"The '{group_col}' with the highest total '{amount_col}' is "
            f"'{top_group}' with {top_value:.2f}."
        )

    # Highest average spending by group
    if llm_intent == "group_average" or (
        "highest average" in question_lower
        or "average spending" in question_lower
        or "average spent" in question_lower
    ):
        amount_col = find_amount_column(numeric_cols)

        if amount_col is None:
            return "I could not find a numeric spending/amount column."

        group_col = find_group_column(question_lower, categorical_cols)

        if group_col is None:
            return (
                "Please specify the grouping column, for example: "
                "'Which country has the highest average spending?'"
            )

        grouped = (
            df.groupby(group_col)[amount_col]
            .mean()
            .sort_values(ascending=False)
        )

        top_group = grouped.index[0]
        top_value = grouped.iloc[0]

        return top_rows[display_cols]

    # Top N rows by numeric column
    if llm_intent == "top_n" or "top" in question_lower:
        n = extract_top_n(question_lower)

        target_numeric_col = None

        for col in numeric_cols:
            if col.lower() in question_lower:
                target_numeric_col = col
                break

        if target_numeric_col is None:
            target_numeric_col = find_amount_column(numeric_cols)

        if target_numeric_col is None:
            return "Please specify a numeric column for the top results."

        top_rows = df.sort_values(
            by=target_numeric_col,
            ascending=False
        ).head(n)

        display_cols = select_display_columns(df, target_numeric_col)

        return (
            f"Top {n} rows by '{target_numeric_col}':\n\n"
            f"{top_rows[display_cols].to_string(index=False)}"
        )

    return (
        "I can answer questions about rows, columns, numeric columns, "
        "average, min, max, category counts, top values, and group-based spending."
    )


def find_amount_column(numeric_cols):
    preferred_keywords = [
        "spent",
        "spending",
        "amount",
        "price",
        "sales",
        "revenue",
        "total",
        "cost",
        "value"
    ]

    for keyword in preferred_keywords:
        for col in numeric_cols:
            if keyword in col.lower():
                return col

    if numeric_cols:
        return numeric_cols[-1]

    return None


def find_group_column(question_lower, categorical_cols):
    for col in categorical_cols:
        if col.lower() in question_lower:
            return col

    common_group_words = {
        "country": ["country", "countries"],
        "city": ["city", "cities"],
        "customer": ["customer", "customers", "name"],
        "category": ["category", "categories"],
        "product": ["product", "products"],
    }

    for col in categorical_cols:
        col_lower = col.lower()

        for _, keywords in common_group_words.items():
            if any(keyword in question_lower for keyword in keywords):
                if any(keyword in col_lower for keyword in keywords):
                    return col

    return None


def extract_top_n(question_lower):
    words = question_lower.split()

    for word in words:
        if word.isdigit():
            return int(word)

    return 5


def select_display_columns(df, target_numeric_col):
    possible_id_cols = [
        "customer_id",
        "id",
        "name",
        "customer",
        "country",
        target_numeric_col
    ]

    display_cols = []

    for col in possible_id_cols:
        if col in df.columns and col not in display_cols:
            display_cols.append(col)

    if target_numeric_col not in display_cols:
        display_cols.append(target_numeric_col)

    return display_cols