from tools.data_quality_tools import (
    check_missing_values,
    check_duplicates,
    check_quality_score,
    check_outliers,
    recommend_cleaning_steps,
    generate_dataset_summary,
)

from agent.llm_router import detect_intent

def get_last_interaction(context):
    history = context.get("context_history", [])

    if not history:
        return None

    return history[-1]


def resolve_follow_up_question(question, context):
    question_lower = question.lower().strip()
    last_interaction = get_last_interaction(context)

    if last_interaction is None:
        return question
    
    if (
        "why" in question_lower
        or "explain" in question_lower
        or "more detail" in question_lower
        or "more details" in question_lower
        or "tell me more" in question_lower
        or "elaborate" in question_lower
        ):
     return "__EXPLAIN_LAST_RECOMMENDATION__"
    

    if question_lower in ["why", "why?", "explain", "explain more", "more"]:
        last_tool = last_interaction["tool"]

        if last_tool == "recommend_cleaning_steps":
            return "__EXPLAIN_LAST_RECOMMENDATION__"

        if last_tool == "check_missing_values":
            return "__EXPLAIN_MISSING_VALUES__"

        if last_tool == "check_duplicates":
            return "__EXPLAIN_DUPLICATES__"

        if last_tool == "check_outliers":
            return "__EXPLAIN_OUTLIERS__"

        if last_tool == "check_quality_score":
            return "__EXPLAIN_QUALITY_SCORE__"

    if "what about duplicate" in question_lower or "duplicates" in question_lower:
        return "__EXPLAIN_DUPLICATES__"

    if "what about missing" in question_lower:
        return "missing values"

    if "what about outliers" in question_lower:
        return "outliers"

    if "and after that" in question_lower or "after that" in question_lower:
        return "__NEXT_CLEANING_STEP__"

    return question


def explain_last_recommendation(context):
    missing_df = context["missing_df"]
    recommendations = context["recommendations"]

    columns_with_missing = missing_df[
        missing_df["Missing Values"] > 0
    ].sort_values(
        by="Missing %",
        ascending=False
    )

    if not columns_with_missing.empty:
        top_issue = columns_with_missing.iloc[0]
        top_column = top_issue["Column"]
        top_missing_percent = top_issue["Missing %"]
    else:
        top_column = "the most problematic column"
        top_missing_percent = 0

    answer = f"""
The previous recommendation focused on the highest-priority issue in the dataset.

The column '{top_column}' should be cleaned first because it has the highest missing value percentage ({top_missing_percent}%).

This matters because missing values can:

- reduce data quality
- affect reports and dashboards
- create incorrect analysis results
- reduce machine learning model performance

Recommended cleaning order:

1. Handle missing values in '{top_column}'.
2. Remove duplicate rows.
3. Review possible outliers.
4. Re-run the data quality analysis.
5. Check whether the quality score improved.
"""

    if recommendations:
        answer += "\nAdditional detected issues:\n\n"
        for rec in recommendations:
            answer += f"- {rec}\n"

    return answer


def explain_missing_values(context):
    missing_df = context["missing_df"]

    columns_with_missing = missing_df[missing_df["Missing Values"] > 0]

    if columns_with_missing.empty:
        return "There are no missing values to explain in this dataset."

    answer = """
Missing values mean that some cells in the dataset are empty.

They are important because they can affect analysis, reporting, and machine learning results.

Columns affected:
"""

    for _, row in columns_with_missing.iterrows():
        answer += (
            f"- {row['Column']}: "
            f"{row['Missing Values']} missing values "
            f"({row['Missing %']}%)\n"
        )

    answer += """
Recommended actions:

1. If the column is important, fill missing values using a suitable method.
2. For numeric columns, use median or mean.
3. For text columns, use "Unknown" or investigate the source.
4. If a column has too many missing values, consider removing it.
"""

    return answer


def explain_duplicates(context):
    duplicate_rows = context["duplicate_rows"]

    if duplicate_rows == 0:
        return "There are no duplicate rows in this dataset."

    return f"""
The dataset contains {duplicate_rows} duplicate rows.

Duplicates are important because they can:

- inflate totals
- distort statistics
- affect reports
- bias machine learning models

Recommended action:

Remove duplicate rows before using this dataset for reporting, analysis, or machine learning.
"""


def explain_outliers(context):
    df = context["df"]
    outlier_summary = check_outliers(df)

    return f"""
Outliers are values that are unusually high or unusually low compared to the rest of the data.

Detected outliers:

{outlier_summary}

Outliers matter because they can:

- distort averages
- affect visualizations
- reduce model accuracy
- indicate data entry errors

Recommended action:

Review the outlier values before removing them. Some outliers may be valid business cases, while others may be mistakes.
"""


def explain_quality_score(context):
    quality_score = context["quality_score"]
    missing_cells = context["missing_cells"]
    duplicate_rows = context["duplicate_rows"]

    return f"""
The current data quality score is {quality_score}/100.

This score is affected by:

- Missing cells: {missing_cells}
- Duplicate rows: {duplicate_rows}

A higher score means the dataset is cleaner and more reliable.

To improve the score:

1. Fill or remove missing values.
2. Remove duplicate rows.
3. Review outliers.
4. Re-run the quality analysis after cleaning.
"""


def next_cleaning_step(context):
    missing_df = context["missing_df"]
    duplicate_rows = context["duplicate_rows"]
    df = context["df"]

    columns_with_missing = missing_df[
        missing_df["Missing Values"] > 0
    ].sort_values(
        by="Missing %",
        ascending=False
    )

    if not columns_with_missing.empty:
        top_issue = columns_with_missing.iloc[0]

        return (
            f"The next best step is to clean the column "
            f"'{top_issue['Column']}' because it has "
            f"{top_issue['Missing %']}% missing values."
        )

    if duplicate_rows > 0:
        return (
            f"The next best step is to remove the "
            f"{duplicate_rows} duplicate rows."
        )

    outlier_result = check_outliers(df)

    if "No major outliers" not in outlier_result:
        return (
            "The next best step is to review the detected outliers:\n\n"
            f"{outlier_result}"
        )

    return "No major cleaning step is needed right now."

def explain_ml_readiness(context):
    quality_score = context["quality_score"]
    missing_cells = context["missing_cells"]
    duplicate_rows = context["duplicate_rows"]
    missing_df = context["missing_df"]

    columns_with_missing = missing_df[missing_df["Missing Values"] > 0]

    answer = f"""
Machine Learning Readiness Assessment:

Current quality score: {quality_score}/100

Main concerns:
- Missing cells: {missing_cells}
- Duplicate rows: {duplicate_rows}
- Columns with missing values: {len(columns_with_missing)}

Assessment:
"""

    if quality_score >= 85 and missing_cells == 0 and duplicate_rows == 0:
        answer += """
This dataset looks mostly ready for machine learning.

Recommended next steps:
1. Encode categorical variables.
2. Scale numeric features if needed.
3. Split data into train and test sets.
"""
    else:
        answer += """
This dataset is not fully ready for machine learning yet.

Recommended next steps:
1. Handle missing values.
2. Remove duplicate rows.
3. Review outliers.
4. Encode categorical columns.
5. Scale numeric features if the model requires it.
"""

    return answer


def recommend_preprocessing_steps(context):
    df = context["df"]
    missing_df = context["missing_df"]
    duplicate_rows = context["duplicate_rows"]

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    text_cols = df.select_dtypes(include=["object"]).columns

    answer = """
Recommended preprocessing steps:

"""

    if duplicate_rows > 0:
        answer += "1. Remove duplicate rows.\n"

    columns_with_missing = missing_df[missing_df["Missing Values"] > 0]

    if not columns_with_missing.empty:
        answer += "2. Handle missing values:\n"

        for _, row in columns_with_missing.iterrows():
            answer += (
                f"   - {row['Column']}: "
                f"{row['Missing Values']} missing values "
                f"({row['Missing %']}%)\n"
            )

    if len(text_cols) > 0:
        answer += "3. Encode categorical/text columns before machine learning.\n"

    if len(numeric_cols) > 0:
        answer += "4. Scale numeric columns if using distance-based models.\n"

    answer += "5. Recalculate the data quality score after preprocessing.\n"

    return answer


def identify_problematic_columns(context):
    missing_df = context["missing_df"]

    problem_columns = missing_df[
        missing_df["Missing Values"] > 0
    ].sort_values(
        by="Missing %",
        ascending=False
    )

    if problem_columns.empty:
        return "No problematic columns were detected based on missing values."

    answer = """
Most problematic columns based on missing values:

"""

    for _, row in problem_columns.iterrows():
        answer += (
            f"- {row['Column']}: "
            f"{row['Missing Values']} missing values "
            f"({row['Missing %']}%)\n"
        )

    return answer


def run_data_quality_agent(question, context):
    resolved_question = resolve_follow_up_question(question, context)
    question_lower = resolved_question.lower()

    try:
        llm_intent = detect_intent(resolved_question)
    except Exception:
        llm_intent = None

    if resolved_question == "__EXPLAIN_LAST_RECOMMENDATION__":
        tool_used = "context_explanation"
        answer = explain_last_recommendation(context)

    elif resolved_question == "__EXPLAIN_MISSING_VALUES__":
        tool_used = "context_explanation_missing_values"
        answer = explain_missing_values(context)

    elif resolved_question == "__EXPLAIN_DUPLICATES__":
        tool_used = "context_explanation_duplicates"
        answer = explain_duplicates(context)

    elif resolved_question == "__EXPLAIN_OUTLIERS__":
        tool_used = "context_explanation_outliers"
        answer = explain_outliers(context)

    elif resolved_question == "__EXPLAIN_QUALITY_SCORE__":
        tool_used = "context_explanation_quality_score"
        answer = explain_quality_score(context)

    elif resolved_question == "__NEXT_CLEANING_STEP__":
        tool_used = "next_cleaning_step"
        answer = next_cleaning_step(context)
    elif llm_intent == "missing_values":
        tool_used = "llm_router_missing_values"
        answer = check_missing_values(context["missing_df"])

    elif llm_intent == "duplicates":
        tool_used = "llm_router_duplicates"
        answer = check_duplicates(context["duplicate_rows"])

    elif llm_intent == "outliers":
        tool_used = "llm_router_outliers"
        answer = check_outliers(context["df"])

    elif llm_intent == "quality_score":
        tool_used = "llm_router_quality_score"
        answer = check_quality_score(context["quality_score"])

    elif llm_intent == "recommendations":
        tool_used = "llm_router_recommendations"
        answer = recommend_cleaning_steps(
            context["recommendations"],
            context["missing_df"]
        )

    elif llm_intent == "summary":
        tool_used = "llm_router_summary"
        answer = generate_dataset_summary(
            context["df"],
            context["duplicate_rows"],
            context["missing_cells"],
            context["quality_score"],
        )

    elif llm_intent == "ml_readiness":
        tool_used = "llm_router_ml_readiness"
        answer = explain_ml_readiness(context)

    elif llm_intent == "preprocessing":
        tool_used = "llm_router_preprocessing"
        answer = recommend_preprocessing_steps(context)

    elif llm_intent == "problematic_columns":
        tool_used = "llm_router_problematic_columns"
        answer = identify_problematic_columns(context)

    elif "missing" in question_lower or "null" in question_lower:
        tool_used = "check_missing_values"
        answer = check_missing_values(context["missing_df"])

    elif "duplicate" in question_lower or "duplicates" in question_lower:
        tool_used = "check_duplicates"
        answer = check_duplicates(context["duplicate_rows"])

    elif "quality" in question_lower or "score" in question_lower:
        tool_used = "check_quality_score"
        answer = check_quality_score(context["quality_score"])

    elif "outlier" in question_lower or "outliers" in question_lower:
        tool_used = "check_outliers"
        answer = check_outliers(context["df"])

    elif (
        "recommend" in question_lower
        or "clean" in question_lower
        or "fix" in question_lower
        or "what should" in question_lower
        or "priority" in question_lower
    ):
        tool_used = "recommend_cleaning_steps"
        answer = recommend_cleaning_steps(
            context["recommendations"],
            context["missing_df"]
        )

    elif "summary" in question_lower or "overview" in question_lower:
        tool_used = "generate_dataset_summary"
        answer = generate_dataset_summary(
            context["df"],
            context["duplicate_rows"],
            context["missing_cells"],
            context["quality_score"],
        )

    else:
        tool_used = "fallback"
        answer = (
            "I can help with missing values, duplicates, outliers, "
            "quality score, recommendations, cleaning steps, and dataset summary."
        )

    return {
        "tool_used": tool_used,
        "answer": answer,
        "resolved_question": resolved_question,
    }