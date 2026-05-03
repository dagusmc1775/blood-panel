import math
import streamlit as st
from info_pages import show_info_page

st.set_page_config(page_title="Blood Panel Calculator", layout="centered")

st.title("Blood Panel Calculator")

if "info_page" not in st.session_state:
    st.session_state.info_page = None


if st.session_state.info_page is not None:
    show_info_page(st.session_state.info_page)

else:
    total_cholesterol = st.number_input("Total Cholesterol", min_value=0, step=1, key="total_cholesterol")
    ldl = st.number_input("LDL-C", min_value=0, step=1, key="ldl")
    hdl = st.number_input("HDL-C", min_value=0, step=1, key="hdl")
    triglycerides = st.number_input("Triglycerides", min_value=0, step=1, key="triglycerides")
    glucose = st.number_input("Fasting Glucose", min_value=0, step=1, key="glucose")

    if st.button("Calculate"):
        if hdl <= 0 or triglycerides <= 0 or glucose <= 0:
            st.error("HDL-C, triglycerides, and fasting glucose must be greater than zero.")
        else:
            tyg = math.log((triglycerides * glucose) / 2)
                st.session_state.tyg = tyg
                st.session_state.triglycerides = triglycerides
                st.session_state.glucose = glucose
            ldl_hdl = ldl / hdl
            total_hdl = total_cholesterol / hdl
            tg_hdl = triglycerides / hdl

            st.subheader("Results")
            st.write(f"**TyG Index:** {tyg:.2f}")
            st.write(f"**LDL/HDL Ratio:** {ldl_hdl:.2f}")
            st.write(f"**Total Cholesterol/HDL Ratio:** {total_hdl:.2f}")
            st.write(f"**Triglycerides/HDL Ratio:** {tg_hdl:.2f}")

            st.subheader("Learn More")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("TyG Index"):
                    st.session_state.info_page = "tyg"
                    st.rerun()

                if st.button("Cholesterol/HDL"):
                    st.session_state.info_page = "chol_hdl"
                    st.rerun()

            with col2:
                if st.button("LDL/HDL"):
                    st.session_state.info_page = "ldl_hdl"
                    st.rerun()

                if st.button("Triglycerides/HDL"):
                    st.session_state.info_page = "tg_hdl"
                    st.rerun()
