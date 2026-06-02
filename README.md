# AI Data Quality & Dataset Analysis Agent

## Overview

AI Data Quality & Dataset Analysis Agent is an intelligent Streamlit application designed to help users analyze, clean, and interact with datasets using AI-powered agents.

The project combines:

* Data Quality Analysis
* Automated Data Cleaning
* Dataset Chat
* Machine Learning Readiness Assessment
* OpenAI-Powered Intent Detection
* Context-Aware AI Agent Memory

The application allows users to upload any CSV dataset and receive insights about data quality, preprocessing requirements, and business-related questions through natural language.

---

## Features

### Data Quality Analysis

The application automatically analyzes uploaded datasets and provides:

* Missing Values Detection
* Duplicate Detection
* Outlier Detection
* Data Type Analysis
* Data Quality Score (0–100)

### AI Data Quality Agent

The Data Quality Agent can answer questions such as:

* What should I clean first?
* Why is the quality score low?
* What preprocessing steps do you recommend?
* Is this dataset suitable for machine learning?
* Which columns are most problematic?
* Explain the missing values issue.
* What should I do after cleaning?

### Dataset Chat Agent

The Dataset Chat Agent allows users to ask questions directly about the uploaded data.

Examples:

* What is the average age?
* What is the maximum income?
* Which columns are numeric?
* How many rows are there?
* Which country spends the most?
* Which country has the highest average spending?
* Show top 5 customers by total_spent.
* Who are the biggest spenders?
* Which category appears most frequently?

### Auto Data Cleaning

The application can automatically:

* Remove duplicate rows
* Fill missing numeric values using median
* Fill missing text values using "Unknown"
* Export a cleaned CSV file

### Conversation Memory

The AI agent remembers previous questions and supports context-aware follow-up questions such as:

* Why?
* Explain more.
* What about duplicates?
* And after that?

---

## Architecture

### Data Quality Agent

User Question
↓
OpenAI Intent Router
↓
Tool Selection
↓
Data Analysis Tools
↓
Response

### Dataset Chat Agent

User Question
↓
OpenAI Dataset Router
↓
Pandas Analysis
↓
Response

---

## Technologies Used

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib

### AI

* OpenAI API (GPT-4o-mini)
* Intent Routing
* Context-Aware Agent Memory

### Environment Management

* Python Dotenv

---

## Project Structure

```text
ai-data-quality-assistant/
│
├── app.py
│
├── agent/
│   ├── data_quality_agent.py
│   ├── dataset_chat.py
│   ├── dataset_chat_router.py
│   └── llm_router.py
│
├── tools/
│   ├── data_quality_tools.py
│   └── __init__.py
│
├── .env
├── requirements.txt
└── README.md
```

---

Live Demo
https://aidataqualityassistant-fjsaf9op9jhbgtyzexdtdg.streamlit.app/

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd ai-data-quality-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

---

## Sample Dataset Included

The project includes a generated dataset:

```text
Sample_customer_data.csv

```

Dataset characteristics:

* 50,800 rows
* 15 columns
* 800 duplicate rows
* Missing values
* Outliers
* Invalid records
* Customer spending information
* Country and city information
* Subscription data
* Churn risk information

The dataset was intentionally designed to test Data Quality and AI Agent capabilities.

---

## Example Questions for the Included Dataset

### Data Quality Agent

* What should I clean first?
* Why?
* Explain the missing values issue.
* What preprocessing steps do you suggest?
* Is this dataset suitable for machine learning?
* Which columns are most problematic?
* What should I do after cleaning?
* Why does the quality score decrease?
* Generate a cleaning strategy.

### Dataset Chat Agent

* What is the average age?
* What is the average income?
* What is the maximum total_spent?
* Which country spends the most?
* Which country has the highest average spending?
* Show top 5 customers by total_spent.
* Who are the biggest spenders?
* Which subscription type is most common?
* How many customers are from Kosovo?
* Which product category appears most frequently?
* Which city has the highest total spending?
* Which country generates the most revenue?
* What are the top 10 customers by spending?

---

## Machine Learning Use Cases

The application can be used before building machine learning models to:

* Assess data quality
* Identify missing values
* Detect duplicates
* Detect outliers
* Evaluate ML readiness
* Generate preprocessing recommendations

---

## Future Improvements

Potential future enhancements include:

* PDF Report Generation
* Automated Insight Generation
* Interactive Visualizations
* Natural Language SQL Queries
* Predictive Modeling Assistant
* Multi-file Analysis
* Dashboard Export
* Advanced Data Profiling

---

## Author

Created as a voluntary AI  Engineering project to demonstrate:

* Data Analysis
* Data Quality Assessment
* AI Agent Design
* OpenAI Integration
* Streamlit Development
* Machine Learning Preparation Workflows
