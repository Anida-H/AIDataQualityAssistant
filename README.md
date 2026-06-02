# AI Data Quality & Dataset Analysis Agent

## Overview

AI Data Quality & Dataset Analysis Agent is an AI-powered application built with Streamlit, Pandas, and OpenAI.

The project helps users analyze, clean, and interact with datasets through two specialized AI agents:

* **Data Quality Agent** – focuses on data quality assessment, cleaning recommendations, and machine learning readiness.
* **Dataset Chat Agent** – allows users to ask natural language questions directly about the dataset and receive analytical insights.

The application combines traditional data analysis techniques with OpenAI-powered intent routing and context-aware conversations.

---

## Live Demo

Streamlit Deployment:

https://aidataqualityassistant-fjsaf9op9jhbgtyzexdtdg.streamlit.app/

---

## Features

### Data Quality Analysis

The application automatically performs:

* Missing Values Detection
* Duplicate Detection
* Outlier Detection
* Data Type Analysis
* Data Quality Score Calculation
* Dataset Overview

---

### AI Data Quality Agent

The Data Quality Agent helps users understand the quality of their dataset.

Capabilities:

* Detect missing values
* Detect duplicates
* Detect outliers
* Explain quality issues
* Recommend cleaning actions
* Assess ML readiness
* Suggest preprocessing steps
* Explain quality score
* Maintain conversation context
* Handle follow-up questions

Example questions:

```text
What should I clean first?
Why?
Explain in more detail.
What should I do after that?
Which columns are problematic?
How can I improve the quality score?
Is this dataset ready for machine learning?
What preprocessing steps do you recommend?
```

---

### Dataset Chat Agent

The Dataset Chat Agent allows users to interact directly with the uploaded dataset using natural language.

Capabilities:

* Count records
* List columns
* Identify numeric columns
* Calculate averages
* Calculate minimum and maximum values
* Count categorical values
* Find top records
* Perform group-based analysis
* Answer business-oriented questions

Example questions:

```text
How many rows are in the dataset?
List all columns.
Which columns are numeric?
What is the average age?
What is the average income?
What is the maximum total_spent?
How many customers are from Kosovo?
Who are the biggest spenders?
Show top 10 customers by spending.
Which country spends the most?
Which country has the highest average spending?
Which product category appears most frequently?
Which subscription type is most common?
Which country generates the most revenue?
```

---

### Auto Data Cleaning

The application can automatically:

* Remove duplicate rows
* Fill missing numeric values using median
* Fill missing text values using "Unknown"
* Generate a cleaned dataset
* Download the cleaned CSV file

---

### Conversation Memory

The Data Quality Agent supports context-aware follow-up questions.

Examples:

```text
What should I clean first?
Why?
Explain more.
What should I do after that?
```

The agent remembers previous interactions and provides contextual answers.

---

## AI Agent Architecture

### Data Quality Agent

```text
User Question
      ↓
OpenAI Intent Router
      ↓
Tool Selection
      ↓
Data Quality Tools
      ↓
Response
```

### Dataset Chat Agent

```text
User Question
      ↓
OpenAI Dataset Router
      ↓
Pandas Analysis Engine
      ↓
Response
```

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

* OpenAI GPT-4o-mini
* Intent Routing
* Context-Aware Agent Memory

### Environment Management

* Python Dotenv

---

## Project Structure

```text
AIDataQualityAssistant/
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
│
├── data/
│   ├── sample_data.csv
│   ├── sample_data_2.csv
│   └── dirty_customer_data_50k.csv
│
├── screenshots/
│   ├── screenshot1.png
│   ├── screenshot2.png
│   └── screenshot3.png
|   |__ screenshot4.png
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Anida-H/AIDataQualityAssistant.git
cd AIDataQualityAssistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

---

## Sample Dataset Included

The repository contains a generated dataset:

```text
Sample_customer_data.csv
```

Dataset characteristics:

* 50,800 rows
* 15 columns
* Missing values
* Duplicate rows
* Outliers
* Invalid records
* Customer spending information
* Country and city information
* Subscription information
* Churn risk information

The dataset was intentionally designed to test AI-powered data quality workflows.

---

## Machine Learning Use Cases

The application can be used before building machine learning models to:

* Assess data quality
* Detect missing values
* Detect duplicates
* Detect outliers
* Evaluate ML readiness
* Generate preprocessing recommendations
* Prepare datasets for modeling

---

## Future Improvements

Potential future enhancements:

* PDF Report Generation
* Advanced Data Profiling
* Interactive AI Visualizations
* Automatic Insight Generation
* Predictive Modeling Assistant
* Multi-file Analysis
* SQL Query Generation
* Dashboard Export

---

## Author

Created as a personal AI  Engineering project to demonstrate:

* Data Quality Assessment
* AI Agent Design
* OpenAI Integration
* Streamlit Development
* Dataset Analytics
* Machine Learning Preparation Workflows
