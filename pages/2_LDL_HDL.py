import streamlit as st

st.set_page_config(page_title="LDL/HDL Ratio", layout="centered")

st.title("LDL/HDL Ratio")

st.write("""
The LDL/HDL ratio compares LDL-C, often called “bad cholesterol,” with HDL-C, often called “good cholesterol.”

A lower ratio is generally better because it means LDL is lower relative to HDL.
""")

st.subheader("General interpretation")

st.write("""
- **Lower ratio:** generally more favorable
- **Higher ratio:** may suggest higher cardiovascular risk
- This should be interpreted alongside ApoB, non-HDL cholesterol, triglycerides, blood pressure, inflammation, smoking status, diabetes risk, and family history.
""")

st.subheader("Formula")

st.code("LDL/HDL Ratio = LDL-C / HDL-C")

if st.button("Back to Calculator"):
    st.switch_page("app.py")
