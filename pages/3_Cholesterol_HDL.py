import streamlit as st

st.set_page_config(page_title="Total Cholesterol/HDL Ratio", layout="centered")

st.title("Total Cholesterol/HDL Ratio")

st.write("""
The Total Cholesterol/HDL ratio compares total cholesterol against HDL-C.

It is a broad cardiovascular risk marker. Lower is generally better.
""")

st.subheader("General interpretation")

st.write("""
- **Lower ratio:** generally more favorable
- **Higher ratio:** may indicate higher cardiovascular risk
- This ratio can be useful, but it is less specific than looking at LDL-C, non-HDL-C, ApoB, triglycerides, and metabolic health together.
""")

st.subheader("Formula")

st.code("Total Cholesterol/HDL Ratio = Total Cholesterol / HDL-C")

if st.button("Back to Calculator"):
    st.switch_page("app.py")
