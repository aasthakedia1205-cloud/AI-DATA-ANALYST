# IMPORTS

import streamlit as st
import pandas as pd

from utils.visualize import create_visualizations, dynamic_dashboard
from utils.llm import (
    generate_business_insights,
    ask_ai,
    explain_model_results
)
from utils.clean_data import clean_dataset
from utils.health_score import calculate_health_score
from utils.report_generator import generate_pdf_report
from utils.auto_dashboard import generate_dashboard_recommendations
from utils.ml_model import (
    train_regression_model,
    train_classification_model,
    detect_problem_type,
    get_valid_target_columns
)
from utils.model_compare import compare_models

def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

def metric_card(icon, title, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# PAGE CONFIG

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# SESSION STATE

if "insights" not in st.session_state:
    st.session_state.insights = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "cleaning_report" not in st.session_state:
    st.session_state.cleaning_report = []

if "dashboard_ai" not in st.session_state:
    st.session_state.dashboard_ai = ""

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = ""

if "ml_results" not in st.session_state:
    st.session_state.ml_results = None

if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = None

if "model_review" not in st.session_state:
    st.session_state.model_review = ""

# SIDEBAR

st.sidebar.title("🤖 AI Data Analyst")

st.sidebar.success("Project Modules")

st.sidebar.write("📊 Dashboard")
st.sidebar.write("🩺 Dataset Health")
st.sidebar.write("🧹 Data Cleaning")
st.sidebar.write("🤖 AI Insights")
st.sidebar.write("💬 Chat")


# MAIN PAGE

st.title("📊 AI Data Analyst")
st.write("Upload your CSV or Excel dataset and let AI analyze it.")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name != st.session_state.last_uploaded_file:

        st.session_state.last_uploaded_file = uploaded_file.name

        st.session_state.dashboard_ai = ""

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset Uploaded Successfully!")

    # Sidebar Dataset Info
    st.sidebar.divider()
    st.sidebar.subheader("Dataset")

    st.sidebar.write(f"Rows : {df.shape[0]}")
    st.sidebar.write(f"Columns : {df.shape[1]}")

    # TABS
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Dashboard",
        "AI Dashboard",
        "Health",
        "Cleaning",
        "AI",
        "Chat",
        "Report",
        "Machine Learning"
    ])

    # =====================================================
    # DASHBOARD
    # =====================================================

    with tab1:

        st.header("📋 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("📄","Rows",df.shape[0])

        with c2:
            metric_card("📊","Columns",df.shape[1])

        with c3:
            metric_card("⚠️","Missing",df.isnull().sum().sum())

        with c4:
            metric_card("🔄","Duplicates",df.duplicated().sum())

        with st.expander("📑 Dataset Preview"):
            st.dataframe(df)

        with st.expander("📌 Column Information"):

            info_df = pd.DataFrame({
                "Column Name": df.columns,
                "Data Type": df.dtypes.astype(str),
                "Missing Values": df.isnull().sum().values,
                "Unique Values": df.nunique().values
            })

            st.dataframe(info_df)

        with st.expander("📊 Statistical Summary"):
            st.dataframe(df.describe())

        st.divider()

        create_visualizations(df)

        st.divider()

        dynamic_dashboard(df)

    # =====================================================
    # AI DASHBOARD
    # =====================================================

    with tab2:

        st.header("🤖 AI Dashboard Assistant")

        st.write(
            "AI is automatically understanding your dataset..."
        )

        if st.session_state.dashboard_ai == "":

            with st.spinner("🤖 AI is analyzing your dataset..."):

                st.session_state.dashboard_ai = (
                    generate_dashboard_recommendations(df)
                )

        st.markdown(st.session_state.dashboard_ai)

    # =====================================================
    # HEALTH
    # =====================================================

    with tab3:

        st.header("🩺 Dataset Health Score")

        score, report = calculate_health_score(df)

        st.metric("Health Score", f"{score}/100")

        st.progress(score / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Missing Values:** {report['Missing Values']}")
            st.write(f"**Duplicate Rows:** {report['Duplicate Rows']}")
            st.write(f"**Outliers:** {report['Outliers']}")

        with col2:
            st.write(f"**Missing %:** {report['Missing %']}%")
            st.write(f"**Empty Columns:** {report['Empty Columns']}")
            st.write(f"**Memory Usage:** {report['Memory Usage']} MB")

    # =====================================================
    # CLEANING
    # =====================================================

    with tab4:

        st.header("🧹 Data Cleaning Assistant")

        if st.button("Apply Data Cleaning"):

            st.session_state.cleaned_df, st.session_state.cleaning_report = clean_dataset(df)

        if st.session_state.cleaned_df is not None:

            st.success("Cleaning Completed!")

            st.subheader("Cleaning Report")

            for item in st.session_state.cleaning_report:
                st.write(item)

            st.subheader("Cleaned Dataset")

            st.dataframe(st.session_state.cleaned_df)

            csv = st.session_state.cleaned_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download Cleaned Dataset",
                csv,
                "cleaned_dataset.csv",
                "text/csv"
            )

    # =====================================================
    # AI INSIGHTS
    # =====================================================

    with tab5:

        st.header("🤖 AI Business Insights")

        if st.button("Generate AI Insights"):

            with st.spinner("Analyzing Dataset..."):
                st.session_state.insights = generate_business_insights(df)

        if st.session_state.insights:
            st.markdown(st.session_state.insights)

    # =====================================================
    # CHAT
    # =====================================================

    with tab6:

        st.header("💬 Chat with Your Data")

        question = st.text_input("Ask anything about your dataset")

        if st.button("Ask AI"):

            if question.strip():

                with st.spinner("Thinking..."):

                    answer = ask_ai(df, question)

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

            else:
                st.warning("Please enter a question.")

        if st.session_state.chat_history:

            st.subheader("Conversation")

            for chat in st.session_state.chat_history:

                st.markdown(f"**🧑 You:** {chat['question']}")
                st.markdown(f"**🤖 AI:** {chat['answer']}")

                st.divider()
    
    # =====================================================
    # AI REPORT GENERATOR
    # =====================================================

    with tab7:

        st.header("📄 AI Report Generator")

        st.write(
            "Generate a professional PDF report of your dataset."
        )

        if st.button("Generate PDF Report"):

            score, report = calculate_health_score(df)

            generate_pdf_report(
                filename="AI_Report.pdf",
                df=df,
                health_score=score,
                health_report=report,
                ai_insights=st.session_state.insights,
                cleaning_report=st.session_state.cleaning_report
            )

            with open("AI_Report.pdf", "rb") as pdf:

                st.download_button(
                    label="Download Report",
                    data=pdf,
                    file_name="AI_Report.pdf",
                    mime="application/pdf"
                )
                
    # =====================================================
    # MACHINE LEARNING
    # =====================================================

    with tab8:

        st.header("📈 Machine Learning")

        st.write("Train a Random Forest Regression model on your dataset.")

        valid_targets = get_valid_target_columns(df)

        target = st.selectbox(
            "Select Target Column",
            valid_targets
        )

        problem = detect_problem_type(df, target)

        st.info(f"Detected Problem Type: **{problem}**")

        if st.button("Train Model"):

            if problem == "Regression":

                with st.spinner("Training Regression Model..."):

                    st.session_state.ml_results = train_regression_model(df, target)

            elif problem == "Classification":

                with st.spinner("Training Classification Model..."):

                    st.session_state.ml_results = train_classification_model(df, target)

            else:

                st.error("This column cannot be used as a target.")

        if st.session_state.ml_results is not None:

            results = st.session_state.ml_results

            if problem == "Regression":

                col1, col2, col3 = st.columns(3)

                col1.metric("R²", results["R2"])
                col2.metric("MAE", results["MAE"])
                col3.metric("RMSE", results["RMSE"])

            else:

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Accuracy", results["Accuracy"])
                col2.metric("Precision", results["Precision"])
                col3.metric("Recall", results["Recall"])
                col4.metric("F1 Score", results["F1"])

            st.subheader("Feature Importance")

            importance = results["Importance"]

            st.bar_chart(
                importance.set_index("Feature")
            )
            st.subheader("Actual vs Predicted")

            prediction_df = pd.DataFrame({
                "Actual": results["Actual"].values,
                "Predicted": results["Predicted"]
            })

            st.dataframe(prediction_df)

            st.subheader("Actual vs Predicted Plot")

            st.pyplot(results["Plot"])

        st.divider()

        st.subheader("🏆 Model Comparison")

        if problem == "Regression":

            if st.button("Compare Regression Models"):

                with st.spinner("Comparing Models..."):

                    st.session_state.comparison_results = compare_models(
                        df,
                        target
                    )

            if st.session_state.comparison_results is not None:

                comparison = st.session_state.comparison_results

                st.dataframe(comparison)

                st.bar_chart(
                    comparison.set_index("Model")
                )

                best = comparison.iloc[0]

                st.success(
                    f"🏆 Best Model: {best['Model']} "
                    f"(R² = {best['R² Score']})"
                )  

        st.divider()

        st.subheader("🤖 AI Model Reviewer")

        if st.button("Explain Model Performance"):

            with st.spinner("AI is reviewing the models..."):

                st.session_state.model_review = explain_model_results(
                    comparison
                )

        if st.session_state.model_review:

            st.markdown(st.session_state.model_review)