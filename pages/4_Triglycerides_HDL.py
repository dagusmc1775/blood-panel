import streamlit as st

st.set_page_config(page_title="Triglycerides/HDL Ratio", layout="centered")

st.title("Triglycerides/HDL Ratio")

st.write("""
The Triglycerides/HDL ratio is often used as a simple marker of insulin resistance and metabolic health.

A lower value is generally better.
""")

st.subheader("General interpretation")

st.write("""
- **Lower ratio:** generally suggests better insulin sensitivity
- **Higher ratio:** may suggest insulin resistance, higher cardiometabolic risk, or poorer triglyceride handling
- This is especially useful when interpreted with fasting glucose, A1C, waist size, blood pressure, and triglyceride level.
""")

st.subheader("Formula")

st.code("Triglycerides/HDL Ratio = Triglycerides / HDL-C")

if st.button("Back to Calculator"):
    st.switch_page("app.py")
