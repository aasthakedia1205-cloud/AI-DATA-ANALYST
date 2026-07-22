from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


def generate_pdf_report(
    filename,
    df,
    health_score,
    health_report,
    ai_insights,
    cleaning_report
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # -----------------------
    # Title
    # -----------------------

    story.append(
        Paragraph("<b>AI DATA ANALYST REPORT</b>", styles["Title"])
    )

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------
    # Dataset Overview
    # -----------------------

    story.append(
        Paragraph("<b>Dataset Overview</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"Rows : {df.shape[0]}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Columns : {df.shape[1]}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"Missing Values : {df.isnull().sum().sum()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Duplicate Rows : {df.duplicated().sum()}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------
    # Health Score
    # -----------------------

    story.append(
        Paragraph("<b>Dataset Health</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Health Score : {health_score}/100",
            styles["Normal"]
        )
    )

    for key, value in health_report.items():

        story.append(
            Paragraph(f"{key}: {value}", styles["Normal"])
        )

    story.append(Spacer(1, 20))

    # -----------------------
    # AI Insights
    # -----------------------

    story.append(
        Paragraph("<b>AI Business Insights</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(ai_insights.replace("\n", "<br/>"), styles["Normal"])
    )

    story.append(Spacer(1, 20))

    # -----------------------
    # Cleaning Report
    # -----------------------

    story.append(
        Paragraph("<b>Cleaning Report</b>", styles["Heading2"])
    )

    if cleaning_report:

        for item in cleaning_report:

            story.append(
                Paragraph(f"• {item}", styles["Normal"])
            )

    else:

        story.append(
            Paragraph(
                "No cleaning performed.",
                styles["Normal"]
            )
        )

    doc.build(story)