import math
import streamlit as st

st.set_page_config(page_title="Blood Panel Calculator", layout="centered")

st.title("Blood Panel Calculator")

total_cholesterol = st.number_input("Total Cholesterol", min_value=0, step=1)
ldl = st.number_input("LDL-C", min_value=0, step=1)
hdl = st.number_input("HDL-C", min_value=0, step=1)
triglycerides = st.number_input("Triglycerides", min_value=0, step=1)
glucose = st.number_input("Fasting Glucose", min_value=0, step=1)

if st.button("Calculate"):
    if hdl <= 0 or triglycerides <= 0 or glucose <= 0:
        st.error("HDL, triglycerides, and glucose must be greater than zero.")
    else:
        tyg = math.log((triglycerides * glucose) / 2)
        ldl_hdl = ldl / hdl
        total_hdl = total_cholesterol / hdl
        tg_hdl = triglycerides / hdl

        st.subheader("Results")
        st.write(f"**TyG Index:** {tyg:.2f}")
        st.write(f"**LDL/HDL Ratio:** {ldl_hdl:.2f}")
        st.write(f"**Total Cholesterol/HDL Ratio:** {total_hdl:.2f}")
        st.write(f"**Triglycerides/HDL Ratio:** {tg_hdl:.2f}")
