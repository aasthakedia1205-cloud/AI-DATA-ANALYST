AI Data Analyst

An end-to-end AI-powered data analysis platform built with Python and Streamlit that allows users to upload datasets, automatically analyze and clean data, generate visualizations, obtain AI-powered business insights, train machine learning models, and generate reports — all through an interactive dashboard.

🔗 Live Demo: https://ai-data-analyst-ntpqim6vmr3rruk3ej2ni5.streamlit.app/

Dashboard Preview
<img width="959" height="440" alt="dashboard_ai" src="https://github.com/user-attachments/assets/6441a9fb-f62b-432b-90f0-085f1e9f7d51" />

Overview

Traditional data analysis often requires multiple tools for data cleaning, visualization, statistical analysis, machine learning and reporting.

AI Data Analyst brings these tasks together in a single interactive application.

Users can upload a CSV or Excel dataset and use the platform to:

Explore the dataset
Identify missing values and duplicates
Clean and preprocess data
Generate visualizations dynamically
Get AI-powered business insights
Ask questions about their dataset using natural language
Calculate dataset health
Train machine learning models
Compare model performance
Generate predictions
Generate downloadable reports

The goal is to make data analysis more accessible while combining traditional data science techniques with Generative AI.

✨ Key Features
📁 Dataset Upload

Upload datasets directly through the Streamlit interface.

Supported formats:

CSV
Excel (.xlsx)

The application automatically reads the dataset and displays basic information such as:

Number of rows
Number of columns
Missing values
Duplicate rows
📊 Dataset Analysis

The dashboard provides an overview of the uploaded dataset, including:

Dataset preview
Column information
Data types
Statistical summary
Missing-value analysis
Duplicate detection

This helps users understand the structure and quality of their data before performing further analysis.

🧹 Automated Data Cleaning

The application provides data-cleaning functionality to help identify and handle common data-quality problems.

It can assist with issues such as:

Missing values
Duplicate records
Incorrect or inconsistent data
Data preprocessing

A cleaned dataset can then be used for visualization and machine learning.

📈 Dynamic Data Visualization

Users can generate visualizations based on the columns in their dataset.

The dashboard supports different visualization types, including:

Histograms
Bar charts
Line charts
Scatter plots
Pie charts
Other dynamically generated charts

The visualization system automatically works with the columns selected by the user.

🤖 AI-Powered Business Insights

The application integrates Google Gemini to analyze uploaded datasets and generate meaningful insights.

The AI can provide:

Dataset summary
Important business insights
Data-quality observations
Recommendations
Patterns and trends within the dataset

Instead of manually inspecting large datasets, users can receive an AI-generated analysis.

💬 AI Data Assistant

Users can ask questions about their dataset using natural language.

For example:

"Which region generated the highest sales?"

or

"What are the main trends in this dataset?"

The AI Assistant analyzes the uploaded dataset and returns an understandable response.

This makes the application useful even for users without advanced programming or data-analysis knowledge.

❤️ Dataset Health Score

The application calculates an overall dataset health score based on data-quality characteristics.

This provides users with a quick indication of whether their dataset is:

Healthy
Needs attention
Requires cleaning

The health score helps users understand data quality before using the dataset for machine learning.

🤖 Machine Learning

The application can automatically identify the type of machine-learning problem based on the selected target column.

It supports:

Regression
Classification

Users can select a target variable and train an appropriate model directly from the dashboard.

⚖️ Model Comparison

Multiple machine-learning models can be evaluated and compared based on their performance.

This allows users to understand which model performs better for their dataset instead of relying on a single algorithm.

📄 Automated Reports

The application can generate a downloadable PDF report containing important information and analysis from the dataset.

This makes it easier to share the results of the analysis.

🧠 AI Workflow
Upload Dataset
       ↓
Dataset Overview
       ↓
Data Quality Analysis
       ↓
Data Cleaning
       ↓
Visualization
       ↓
AI Business Insights
       ↓
AI Data Assistant
       ↓
Machine Learning
       ↓
Model Comparison
       ↓
Predictions & Reports
🛠️ Tech Stack

Programming Language

Python
Data Analysis
pandas
NumPy
Visualization
Plotly
Machine Learning
scikit-learn
Generative AI
Google Gemini
Web Application
Streamlit
Reporting
ReportLab
Frontend Styling
HTML
CSS

📂 Project Structure
AI_DATA_ANALYST/
│
├── assets/
│   └── style.css
│
├── utils/
│   ├── auto_dashboard.py
│   ├── clean_data.py
│   ├── health_score.py
│   ├── llm.py
│   ├── ml_model.py
│   ├── model_compare.py
│   ├── report_generator.py
│   ├── theme.py
│   └── visualize.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

🔍 Application Modules

| Module           | Purpose                                 |
| ---------------- | --------------------------------------- |
| Dataset Upload   | Upload CSV/Excel datasets               |
| Dashboard        | Dataset overview and analysis           |
| Data Cleaning    | Identify and clean data-quality issues  |
| Visualization    | Generate interactive charts             |
| AI Insights      | Generate business insights using Gemini |
| AI Assistant     | Ask questions about the dataset         |
| Health Score     | Evaluate dataset quality                |
| Machine Learning | Train prediction models                 |
| Model Comparison | Compare model performance               |
| Reports          | Generate downloadable reports           |

Author

Aastha Kedia Data Science Student
