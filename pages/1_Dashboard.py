import streamlit as st
import pandas as pd
import plotly.express as px

QUESTION_TEXT = {

    "q1":"I actively engaged with the sharing sessions and demonstrations during the visit.",

    "q2":"The visit helped me better understand what a startup is and how entrepreneurs begin their journey.",

    "q3":"This visit helped me understand how TEGAS can support me if I want to start my own business.",

    "q5":"The visit provided meaningful real-world exposure to engineering, science and digital technologies.",

    "q6":"The environment stimulated my curiosity about innovation and startups with the integration of digital technologies.",

    "q7":"The visit enhanced my understanding of how engineering, science, and digital solutions impact society and the environment.",

    "q8":"The visit encouraged me to think critically about real-world engineering, scientific, and digital innovation challenges and opportunities.",

    "q9":"The visit increased my awareness of the importance of creativity, teamwork, and adaptability in innovation.",

    "q10":"I can relate what I experienced during the visit to concepts learned in class.",

    "q11":"I developed a better understanding of how innovation is created and applied in real-world contexts.",

    "q12":"The entrepreneurs' stories helped me understand the challenges involved in starting a business.",

    "q13":"The tips and advice shared by the entrepreneurs were practical and easy to understand.",

    "q14":"I felt inspired by at least one of the entrepreneurs who shared their experience.",

    "q15":"After this visit, I feel more motivated to consider entrepreneurial activities in the future.",

    "q16":"The visit helped me see more options and possibilities for my future career path.",

    "q17":"I can imagine myself starting a business or startup at some point in my future.",

    "q18":"The entrepreneurs' sharing helped me recognise my strengths and how I can develop myself further.",

    "q19":"The stories shared made me think differently about how to face failures in my life.",

    "q20":"I could personally relate to at least one entrepreneur's life story or struggle.",

    "q21":"After this visit, I feel more confident in my ability to explore or engage in entrepreneurial activities."

}

st.title("📊 EduInsight Dashboard")

uploaded = st.file_uploader(
    "Upload Survey CSV",
    type="csv"
)

if uploaded:

    # ============================================
    # Read CSV
    # ============================================

    df = pd.read_csv(uploaded)

    st.session_state["df"] = df

    # ============================================
    # Visit Information
    # ============================================

    st.header("📋 Visit Information")

    col1, col2 = st.columns(2)

    with col1:

        visit_name = st.text_input(
            "Educational Visit",
            value="TEGAS Digital Village Visit"
        )

        visit_date = st.date_input(
            "Visit Date"
        )

    with col2:

        total_students = st.number_input(
            "Total Students Attended",
            min_value=1,
            value=len(df),
            step=1
        )

        organiser = st.text_input(
            "Organiser",
            value="School of Foundation Studies"
        )

    # ============================================
    # Detect Likert Questions Automatically
    # ============================================

    likert = []

    for col in df.columns:

        col_lower = col.lower().strip()

        if col_lower.startswith("q"):

            try:

                number = int(col_lower[1:])

                # Skip open-ended questions
                if number not in [4, 22, 23, 24]:

                    likert.append(col)

            except:
                pass

    # Sort correctly
    available = sorted(
        likert,
        key=lambda x: int(x.lower()[1:])
    )

    # Convert to numeric (just in case)
    for col in available:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ============================================
    # Dashboard Statistics
    # ============================================

    responses = len(df)

    completion = responses / total_students * 100

    overall = df[available].mean().mean()

    # ============================================
    # KPI Cards
    # ============================================

    st.header("📈 Dashboard Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Responses",
        responses
    )

    c2.metric(
        "Completion Rate",
        f"{completion:.1f}%"
    )

    c3.metric(
        "Overall Mean",
        f"{overall:.2f} / 5"
    )

    # ============================================
    # Learning Themes
    # ============================================

    themes = {

        "Student Engagement": ["q1"],

        "Entrepreneurial Awareness": [
            "q2",
            "q3"
        ],

        "Authentic Learning": [
            "q5",
            "q6",
            "q7",
            "q8",
            "q9",
            "q10",
            "q11"
        ],

        "Entrepreneur Inspiration": [
            "q12",
            "q13",
            "q14",
            "q15"
        ],

        "Career Development": [
            "q16",
            "q17",
            "q18",
            "q19",
            "q20",
            "q21"
        ]

    }

    st.header("📚 Learning Dimension Scores")

    scores = {}

    for theme, questions in themes.items():

        cols = []

        for question in questions:

            for column in df.columns:

                if column.lower() == question.lower():

                    cols.append(column)

        if len(cols) > 0:

            scores[theme] = df[cols].mean().mean()

    score_df = pd.DataFrame({

        "Learning Dimension": list(scores.keys()),

        "Average Score": list(scores.values())

    })

    fig = px.bar(

        score_df,

        x="Learning Dimension",

        y="Average Score",

        text="Average Score",

        range_y=[0, 5]

    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(size=18)
    )

    # Font sizes for axes
    fig.update_layout(
        xaxis_title="Learning Dimension",
        yaxis_title="Average Score",
        xaxis=dict(
            title_font=dict(size=18),   # X-axis title
            tickfont=dict(size=14)      # X-axis labels
        ),
        yaxis=dict(
            title_font=dict(size=18),   # Y-axis title
            tickfont=dict(size=14)      # Y-axis labels
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================
    # Question Explorer
    # ============================================

    question_options = {

        QUESTION_TEXT.get(q.lower(), q): q

        for q in available

    }

    selected_question = st.selectbox(

        "Choose Question",

        list(question_options.keys())

    )

    actual_column = question_options[selected_question]

    counts = (

        df[actual_column]

        .value_counts()

        .sort_index()

    )

    fig = px.bar(

        x=counts.index,

        y=counts.values,

        text=counts.values,

        labels={

            "x": "Likert Scale",

            "y": "Responses"

        }

    )

    # Font size for the counts above each bar
    fig.update_traces(
        textposition="inside",
        textfont=dict(size=18)      # Count font size
    )

    fig.update_layout(

        xaxis=dict(

            tickmode="linear",

            title_font=dict(size=18),

            tickfont=dict(size=16)

        ),

        yaxis=dict(
            title_font=dict(size=18),

            tickfont=dict(size=16)
        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

else:

    st.info("👆 Please upload a survey CSV file to begin.")
