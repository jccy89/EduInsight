from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(
        visit,
        organiser,
        date,
        students,
        responses,
        completion,
        overall,
        dimension_df
    ):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "Educational Visit Analytics Report",
        styles["Title"]
    )

    story.append(title)

    story.append(
        Paragraph(
            f"<b>Educational Visit:</b> {visit}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Organiser:</b> {organiser}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Visit Date:</b> {date}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Students Attended:</b> {students}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Responses Received:</b> {responses}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Completion Rate:</b> {completion:.1f}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Mean Score:</b> {overall:.2f}/5",
            styles["Normal"]
        )
    )
    
    story.append(
        Paragraph(
            "<b>Learning Dimension Scores</b>",
            styles["Heading2"]
        )
    )
    
    table_data = [

        ["Learning Dimension", "Mean", "Performance"]

    ]

    for _, row in dimension_df.iterrows():

        table_data.append(

            [

                row["Dimension"],

                f"{row['Mean']:.2f}",

                row["Performance"]

            ]

        )

    table = Table(
        table_data,
        colWidths=[260, 70, 120]
    )

    table.setStyle(

        TableStyle([

            # Header background
            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            # Header font colour
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            # Header font
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            # Header padding
            ("BOTTOMPADDING", (0,0), (-1,0), 10),

            # Body background
            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            # Grid lines
            ("GRID", (0,0), (-1,-1), 1, colors.black),

            # Alignment
            ("ALIGN", (1,1), (-1,-1), "CENTER"),

            # Body font
            ("FONTNAME", (0,1), (-1,-1), "Helvetica"),

            # Font size
            ("FONTSIZE", (0,0), (-1,-1), 10),

            # Padding
            ("BOTTOMPADDING", (0,1), (-1,-1), 8),

            ("TOPPADDING", (0,1), (-1,-1), 8),

        ])

    )
    story.append(table)  

    doc.build(story)

    buffer.seek(0)

    return buffer