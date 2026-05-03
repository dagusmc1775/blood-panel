import streamlit as st
st.set_page_config(page_title="TyG Index", layout="centered")

st.title("TyG Index")

st.write("""
The TyG Index is a calculated marker often used as a proxy for insulin resistance.

It uses fasting triglycerides and fasting glucose.

Higher values may suggest poorer metabolic health, especially when paired with elevated triglycerides, elevated fasting glucose, abdominal fat, high blood pressure, or low HDL.
""")

st.subheader("General interpretation")

st.write("""
- **Lower:** generally better insulin sensitivity
- **Middle range:** possible early insulin resistance
- **Higher:** stronger concern for insulin resistance or metabolic syndrome risk
""")

st.subheader("Formula")

st.code("TyG Index = ln((Triglycerides × Fasting Glucose) / 2)")

if st.button("Back to Calculator"):
    st.switch_page("app.py")
