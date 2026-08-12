import streamlit as st
import plotly.express as px
from utils.chart_theme import style_chart

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
            title=f"Distribution of {selected_num}",
            color_discrete_sequence=[
                "#D47E30",
                "#6F4E37",
                "#F39A46",
                "#A05A2C",
                "#8C6239"
            ]
        )
        
        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )
        fig.update_layout(
            height=480
        )

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
            title=f"Top 10 {selected_cat}",
            color_discrete_sequence=[
                "#D47E30",
                "#6F4E37",
                "#F39A46",
                "#A05A2C",
                "#8C6239"
            ]
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )
        fig.update_layout(
            height=480
        )

    # ---------------- Correlation ----------------
    if len(numeric_columns) >= 2:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_columns].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Matrix",
            color_continuous_scale=[
                "#111111",
                "#6F4E37",
                "#D47E30"
            ]
        )

        fig = style_chart(fig)

        st.plotly_chart(
            fig,    
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )
        fig.update_layout(
            height=480
        )

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
    MOCHA_COLORS = [
        "#D47E30",
        "#6F4E37",
        "#F39A46",
        "#A05A2C",
        "#8C6239"
    ]

    color = st.selectbox(
        "Color (Optional)",
        ["None"] + columns
    )

    color = None if color == "None" else color

    if st.button("Generate Chart"):

        fig = None

        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color,color_discrete_sequence=MOCHA_COLORS)

        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, color=color,color_discrete_sequence=MOCHA_COLORS)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color,color_discrete_sequence=MOCHA_COLORS)

        elif chart_type == "Pie Chart":

            pie = df[x_axis].value_counts()

            # Keep top 7 categories
            pie = pie.head(7)

            fig = px.pie(
                values=pie.values,
                names=pie.index,
                hole=0.45,
                title=f"Top {len(pie)} {x_axis}",
                color_discrete_sequence=[
                    "#D47E30",
                    "#F39A46",
                    "#FFD166",
                    "#8C6239",
                    "#6F4E37",
                    "#C68642",
                    "#E76F51"
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(
                    line=dict(color="#151515", width=2)
                )
            )

            fig.update_layout(
                showlegend=False,
                paper_bgcolor="#151515",
                plot_bgcolor="#151515",
                font=dict(color="white")
            )

        elif chart_type == "Box Plot":
            fig = px.box(df, x=x_axis, y=y_axis, color=color,color_discrete_sequence=MOCHA_COLORS)

        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis,color_discrete_sequence=MOCHA_COLORS)

        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )
        fig.update_layout(
            height=480
        )