
import streamlit as st

st.set_page_config(page_title="EduInsight", layout="wide")

st.title("🎓 EduInsight")
st.subheader("Educational Visit Learning Analytics Platform")

st.markdown("""
Welcome to **EduInsight**, a learning analytics dashboard for educational visit surveys.

Use the sidebar to navigate through the analytics pages.
""")

st.info("""
Expected survey columns:

Q1,Q2,...,Q24

Likert questions should contain values 1–5.

Open-ended:
- Q4
- Q22
- Q23
- Q24
""")
