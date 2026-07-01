import streamlit as st
import pandas as pd
from utils.pdf_report import create_pdf

# =====================================================
# Performance Rating
# =====================================================

def get_rating(score):

    if score >= 4.50:
        return "🟢 Excellent"

    elif score >= 4.00:
        return "🔵 Very Good"

    elif score >= 3.50:
        return "🟡 Good"

    elif score >= 3.00:
        return "🟠 Fair"

    else:
        return "🔴 Needs Improvement"

st.title("📄 Educational Visit Analytics Report")

if "df" not in st.session_state:

    st.warning("Please upload the survey file from the Dashboard page first.")

    st.stop()

df = st.session_state["df"]

# =====================================================
# Visit Information
# =====================================================

st.header("📋 Visit Information")

col1, col2 = st.columns(2)

with col1:

    visit_name = st.text_input(
        "Educational Visit",
        value="TEGAS Digital Village Visit"
    )

    organiser = st.text_input(
        "Organiser",
        value="School of Foundation Studies"
    )

with col2:

    total_students = st.number_input(
        "Students Attended",
        min_value=1,
        value=200,
        step=1
    )

    visit_date = st.date_input(
        "Visit Date"
    )

# =====================================================
# Detect Likert Questions
# =====================================================

likert = []

for col in df.columns:

    c = col.lower().strip()

    if c.startswith("q"):

        try:

            number = int(c[1:])

            if number not in [4,22,23,24]:

                likert.append(col)

        except:
            pass

likert = sorted(
    likert,
    key=lambda x: int(x.lower()[1:])
)

for col in likert:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# =====================================================
# Calculate Statistics
# =====================================================

responses = len(df)

completion = responses / total_students * 100

overall = df[likert].mean().mean()

# =====================================================
# Learning Dimensions
# =====================================================

themes = {

    "Student Engagement":["q1"],

    "Entrepreneurial Awareness":[
        "q2","q3"
    ],

    "Authentic Learning":[
        "q5","q6","q7","q8","q9","q10","q11"
    ],

    "Entrepreneur Inspiration":[
        "q12","q13","q14","q15"
    ],

    "Career Development":[
        "q16","q17","q18","q19","q20","q21"
    ]

}

scores = {}

for theme, questions in themes.items():

    cols = []

    for q in questions:

        for c in df.columns:

            if c.lower() == q.lower():

                cols.append(c)

    scores[theme] = round(
        df[cols].mean().mean(),
        2
    )

# =====================================================
# Executive Report
# =====================================================

st.divider()

st.header("📊 Educational Visit Analytics Report")

st.markdown(f"**Visit:** {visit_name}")

st.markdown(f"**Organiser:** {organiser}")

st.markdown(f"**Students Attended:** {total_students}")

st.markdown(f"**Responses:** {responses}")

st.markdown(f"**Completion Rate:** {completion:.1f}%")

st.markdown(f"**Overall Mean Score:** {overall:.2f}/5")

st.divider()

st.subheader("📚 Learning Dimension Scores")

dimension_df = pd.DataFrame({

    "Dimension": list(scores.keys()),

    "Mean": list(scores.values())

})

dimension_df["Performance"] = dimension_df["Mean"].apply(get_rating)

st.dataframe(
    dimension_df,
    use_container_width=True,
    hide_index=True
)

pdf_buffer = create_pdf(

    visit=visit_name,

    organiser=organiser,

    date=str(visit_date),

    students=total_students,

    responses=responses,

    completion=completion,

    overall=overall,

    dimension_df=dimension_df

)

st.download_button(

    label="📥 Download Summary Report (PDF)",

    data=pdf_buffer.getvalue(),

    file_name="Educational_Visit_Analytics_Report.pdf",

    mime="application/pdf"

)

st.divider()

st.success(
    "This report summarises students' perceptions of the educational visit based on the survey responses."
)
