import streamlit as st


def show_info_page(page_key):
    if page_key == "tyg":
        st.header("TyG Index")
        st.write("""
        The TyG Index is a calculated marker often used as a proxy for insulin resistance.

        It uses fasting triglycerides and fasting glucose.

        Higher values may suggest poorer metabolic health.

        Formula: TyG = ln((Triglycerides × Fasting Glucose) / 2)
        """)

    elif page_key == "ldl_hdl":
        st.header("LDL/HDL Ratio")
        st.write("""
        The LDL/HDL ratio compares LDL-C with HDL-C.

        A lower ratio is generally more favorable. A higher ratio may suggest higher cardiovascular risk.

        Formula: LDL/HDL Ratio = LDL-C / HDL-C
        """)

    elif page_key == "chol_hdl":
        st.header("Total Cholesterol/HDL Ratio")
        st.write("""
        This ratio compares total cholesterol against HDL-C.

        Lower is generally better. Higher values may indicate higher cardiovascular risk.

        Formula: Total Cholesterol/HDL Ratio = Total Cholesterol / HDL-C
        """)

    elif page_key == "tg_hdl":
        st.header("Triglycerides/HDL Ratio")
        st.write("""
        The Triglycerides/HDL ratio is often used as a simple marker of insulin resistance and metabolic health.

        Lower is generally better. Higher values may suggest insulin resistance or poorer triglyceride handling.

        Formula: Triglycerides/HDL Ratio = Triglycerides / HDL-C
        """)

    if st.button("Back to Calculator"):
        st.session_state.info_page = None
        st.rerun()
