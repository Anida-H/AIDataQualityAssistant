import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from agent.data_quality_agent import run_data_quality_agent
from agent.dataset_chat import answer_dataset_question


def safe_dataframe(dataframe):
    return dataframe.astype(str)


st.set_page_config(page_title="AI Data Quality Assistant", layout="wide")
st.markdown("""
<style>

/* Primary buttons */
div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Text input styling */
.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("AI Data Quality Assistant")
st.write("Upload a CSV file to analyze its data quality and interact with AI agents.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing %": missing_percent.round(2).values
    })

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    missing_penalty = (missing_cells / total_cells) * 50
    duplicate_penalty = (duplicate_rows / len(df)) * 30

    quality_score = 100 - missing_penalty - duplicate_penalty
    quality_score = max(0, round(quality_score, 2))

    data_types = df.dtypes.astype(str).reset_index()
    data_types.columns = ["Column", "Data Type"]

    recommendations = []

    high_missing = missing_df[missing_df["Missing %"] > 20]

    for _, row in high_missing.iterrows():
        recommendations.append(
            f"Column '{row['Column']}' has {row['Missing %']}% missing values. "
            f"Consider cleaning or imputing the data."
        )

    if duplicate_rows > 0:
        recommendations.append(
            f"The dataset contains {duplicate_rows} duplicate rows. "
            f"Consider removing duplicates."
        )

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        if df[col].dropna().empty:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = df[
            (df[col] < lower_bound) |
            (df[col] > upper_bound)
        ]

        if len(outliers) > 0:
            recommendations.append(
                f"Column '{col}' may contain outliers "
                f"({len(outliers)} detected values)."
            )

    left_col, right_col = st.columns([1.25, 1])

    # =========================
    # LEFT SIDE - DATA ANALYSIS
    # =========================
    with left_col:
        overview_tab, visual_tab, stats_tab = st.tabs([
            "Overview",
            "Visualizations",
            "Statistics"
        ])

        with overview_tab:
            st.subheader("Dataset Overview")

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric("Rows", df.shape[0])
            metric2.metric("Columns", df.shape[1])
            metric3.metric("Duplicates", duplicate_rows)
            metric4.metric("Quality Score", f"{quality_score}/100")

            if quality_score >= 80:
                st.success("Good data quality.")
            elif quality_score >= 50:
                st.warning("Medium data quality. Some issues need attention.")
            else:
                st.error("Poor data quality. Dataset needs cleaning.")

            st.progress(int(quality_score))

            st.subheader("Dataset Preview")
            st.dataframe(
                safe_dataframe(df.head()),
                use_container_width=True
            )

            st.subheader("Column Data Types")
            st.dataframe(
                safe_dataframe(data_types),
                use_container_width=True
            )

            st.subheader("Missing Values")
            st.dataframe(
                safe_dataframe(missing_df),
                use_container_width=True
            )

        with visual_tab:
            st.subheader("Data Quality Visualizations")

            st.write("### Missing Values by Column")

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.bar(
                missing_df["Column"],
                missing_df["Missing Values"]
            )

            ax.set_xlabel("Columns")
            ax.set_ylabel("Missing Values")
            ax.set_title("Missing Values per Column")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            st.write("### Data Types Distribution")

            dtype_counts = df.dtypes.astype(str).value_counts()

            fig2, ax2 = plt.subplots(figsize=(6, 6))

            ax2.pie(
                dtype_counts.values,
                labels=dtype_counts.index,
                autopct="%1.1f%%"
            )

            ax2.set_title("Column Data Types")

            st.pyplot(fig2)

        with stats_tab:
            st.subheader("Basic Statistics")
            st.dataframe(
                safe_dataframe(df.describe(include="all")),
                use_container_width=True
            )

    # =========================
    # RIGHT SIDE - AI AGENTS
    # =========================
    with right_col:
        st.subheader("AI Agents")

        agent_section, dataset_agent_section = st.tabs([
            "Data Quality Agent",
            "Dataset Chat Agent"
        ])

        # =========================
        # DATA QUALITY AGENT
        # =========================
        with agent_section:
            st.markdown("""
            ### Data Quality Agent

            Use this agent to analyze data quality issues such as missing values,
            duplicates, outliers, cleaning priorities, ML readiness, and preprocessing.
            """)

            quality_question = st.text_input(
                "Submit",
                placeholder="Example: What should I clean first?",
                key="quality_agent_question"
            )

            ask_quality_agent = st.button(
                "Ask Data Quality Agent",
                key="ask_quality_agent"
            )

            if ask_quality_agent and quality_question:
                context = {
                    "df": df,
                    "missing_df": missing_df,
                    "duplicate_rows": duplicate_rows,
                    "missing_cells": missing_cells,
                    "quality_score": quality_score,
                    "recommendations": recommendations,
                    "context_history": st.session_state.chat_history
                }

                result = run_data_quality_agent(
                    quality_question,
                    context
                )

                st.session_state.chat_history.append({
                    "question": quality_question,
                    "resolved_question": result.get(
                        "resolved_question",
                        quality_question
                    ),
                    "answer": result["answer"],
                    "tool": result["tool_used"]
                })

                st.success("Data Quality Agent Response")
                st.write(result["answer"])
                st.caption(f"Tool used: {result['tool_used']}")

        # =========================
        # DATASET CHAT AGENT
        # =========================
        with dataset_agent_section:
            st.markdown("""
            ### Dataset Chat Agent

            Use this agent to ask analytical questions directly about the dataset,
            such as averages, totals, top values, counts, and group-based insights.
            """)

            dataset_question = st.text_input(
                "Ask the Dataset Chat Agent",
                placeholder="Example: Which country spends the most?",
                key="dataset_chat_question"
            )

            ask_dataset_agent = st.button(
                "Ask Dataset Chat Agent",
                key="ask_dataset_agent"
            )

            if ask_dataset_agent and dataset_question:
                dataset_answer = answer_dataset_question(
                    dataset_question,
                    df
                )

                st.success("Dataset Chat Agent Response")

                if isinstance(dataset_answer, pd.DataFrame):
                    st.dataframe(
                        safe_dataframe(dataset_answer),
                        use_container_width=True
                    )
                else:
                    st.write(dataset_answer)

        # =========================
        # RECOMMENDATIONS
        # =========================
        with st.expander("Recommendations", expanded=False):
            if recommendations:
                for rec in recommendations:
                    st.warning(rec)
            else:
                st.success("No major data quality issues detected.")

        # =========================
        # AUTO DATA CLEANING
        # =========================
        with st.expander("Auto Data Cleaning", expanded=False):
            st.write("Automatically clean the uploaded dataset.")

            cleaned_df = df.copy()

            if st.button("Clean Dataset", key="clean_dataset_button"):
                cleaned_df = cleaned_df.drop_duplicates()

                numeric_cols_clean = cleaned_df.select_dtypes(
                    include=["int64", "float64"]
                ).columns

                for col in numeric_cols_clean:
                    cleaned_df[col] = cleaned_df[col].fillna(
                        cleaned_df[col].median()
                    )

                text_cols = cleaned_df.select_dtypes(include=["object"]).columns

                for col in text_cols:
                    cleaned_df[col] = cleaned_df[col].fillna("Unknown")

                st.success("Dataset cleaned successfully!")

                st.write("Cleaned Dataset Preview")
                st.dataframe(
                    safe_dataframe(cleaned_df.head()),
                    use_container_width=True
                )

                csv = cleaned_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download Cleaned CSV",
                    data=csv,
                    file_name="cleaned_dataset.csv",
                    mime="text/csv"
                )

        # =========================
        # CONVERSATION HISTORY
        # =========================
        with st.expander("Conversation History", expanded=False):
            if st.session_state.chat_history:
                for idx, item in enumerate(
                    reversed(st.session_state.chat_history),
                    start=1
                ):
                    st.write(f"### Question {idx}")
                    st.write("**Question:**")
                    st.write(item["question"])

                    if "resolved_question" in item:
                        st.write("**Resolved Question:**")
                        st.write(item["resolved_question"])

                    st.write("**Answer:**")
                    st.write(item["answer"])

                    st.write("**Tool Used:**")
                    st.code(item["tool"])

                    st.divider()

                if st.button("Clear History", key="clear_history_button"):
                    st.session_state.chat_history = []
                    st.rerun()
            else:
                st.info("No conversation history yet.")

else:
    st.info("Please upload a CSV file to start.")