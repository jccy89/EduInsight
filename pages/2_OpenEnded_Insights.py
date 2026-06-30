
import streamlit as st
from collections import Counter
import re

st.title("💡 Open-ended Insights")

if "df" not in st.session_state:
    st.warning("Upload data on Dashboard page first.")
    st.stop()

df=st.session_state["df"]

stop={"the","and","to","of","a","is","it","in","for","on","my","i","was","very","with","that"}

for col in ["Q22","Q23","Q24"]:

    if col not in df.columns:
        continue

    st.header(col)

    text=" ".join(df[col].dropna().astype(str))

    words=re.findall(r"[A-Za-z]+",text.lower())

    words=[w for w in words if w not in stop and len(w)>3]

    freq=Counter(words).most_common(20)

    st.write("Top keywords")

    st.table(freq)

    st.write("Sample responses")

    st.dataframe(df[[col]].dropna().head(10),use_container_width=True)
