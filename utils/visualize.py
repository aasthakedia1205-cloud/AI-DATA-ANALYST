import streamlit as st
import plotly.express as px

def create_visualizations(df):

    st.header("📊 Data Visualizations")

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

    # ---------------- Histogram ----------------
    if numeric_columns:
        st.subheader("📈 Histogram")

        selected_num = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=selected_num,
            nbins=30,
            title=f"Distribution of {selected_num}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Bar Chart ----------------
    if categorical_columns:
        st.subheader("📊 Bar Chart")

        selected_cat = st.selectbox(
            "Select Categorical Column",
            categorical_columns
        )

        bar_data = df[selected_cat].value_counts().head(10)

        fig = px.bar(
            x=bar_data.index,
            y=bar_data.values,
            labels={
                "x": selected_cat,
                "y": "Count"
            },
            title=f"Top 10 {selected_cat}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Correlation ----------------
    if len(numeric_columns) >= 2:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_columns].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Correlation Matrix"
        )

        st.plotly_chart(fig, use_container_width=True)

def dynamic_dashboard(df):

    st.header("🎨 Build Your Own Chart")

    columns = df.columns.tolist()

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Pie Chart",
            "Box Plot",
            "Histogram"
        ]
    )

    x_axis = st.selectbox(
        "Select X-axis",
        columns
    )

    y_axis = None

    if chart_type != "Pie Chart":
        y_axis = st.selectbox(
            "Select Y-axis",
            numeric_columns
        )

    color = st.selectbox(
        "Color (Optional)",
        ["None"] + columns
    )

    color = None if color == "None" else color

    if st.button("Generate Chart"):

        fig = None

        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color)

        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, color=color)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color)

        elif chart_type == "Pie Chart":
            pie = df[x_axis].value_counts()

            fig = px.pie(
                values=pie.values,
                names=pie.index
            )

        elif chart_type == "Box Plot":
            fig = px.box(df, x=x_axis, y=y_axis, color=color)

        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis)

        st.plotly_chart(fig, use_container_width=True)