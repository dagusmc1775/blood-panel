import math

import streamlit as st

from info_pages import show_info_page


st.set_page_config(page_title="Blood Panel Calculator", layout="centered")


def initialize_session_state() -> None:
    defaults = {
        "info_page": None,
        "has_results": False,
        "tyg": None,
        "ldl_hdl": None,
        "total_hdl": None,
        "tg_hdl": None,
        "calc_triglycerides": None,
        "calc_glucose": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def calculate_results(
    total_cholesterol: int,
    ldl: int,
    hdl: int,
    triglycerides: int,
    glucose: int,
) -> None:
    if hdl <= 0 or triglycerides <= 0 or glucose <= 0:
        st.error("HDL-C, triglycerides, and fasting glucose must be greater than zero.")
        st.session_state.has_results = False
        return

    st.session_state.tyg = math.log((triglycerides * glucose) / 2)
    st.session_state.ldl_hdl = ldl / hdl
    st.session_state.total_hdl = total_cholesterol / hdl
    st.session_state.tg_hdl = triglycerides / hdl
    st.session_state.calc_triglycerides = triglycerides
    st.session_state.calc_glucose = glucose
    st.session_state.has_results = True


def render_calculator() -> None:
    st.title("Blood Panel Calculator")

    total_cholesterol = st.number_input("Total Cholesterol", min_value=0, step=1, key="total_cholesterol")
    ldl = st.number_input("LDL-C", min_value=0, step=1, key="ldl")
    hdl = st.number_input("HDL-C", min_value=0, step=1, key="hdl")
    triglycerides = st.number_input("Triglycerides", min_value=0, step=1, key="triglycerides")
    glucose = st.number_input("Fasting Glucose", min_value=0, step=1, key="glucose")

    if st.button("Calculate", key="calculate_button"):
        calculate_results(total_cholesterol, ldl, hdl, triglycerides, glucose)

    if st.session_state.has_results:
        st.subheader("Results")
        st.write(f"**TyG Index:** {st.session_state.tyg:.2f}")
        st.write(f"**LDL/HDL Ratio:** {st.session_state.ldl_hdl:.2f}")
        st.write(f"**Total Cholesterol/HDL Ratio:** {st.session_state.total_hdl:.2f}")
        st.write(f"**Triglycerides/HDL Ratio:** {st.session_state.tg_hdl:.2f}")

        st.subheader("Learn More")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("TyG Index", key="info_tyg_button"):
                st.session_state.info_page = "tyg"
                st.rerun()

            if st.button("Cholesterol/HDL", key="info_chol_hdl_button"):
                st.session_state.info_page = "chol_hdl"
                st.rerun()

        with col2:
            if st.button("LDL/HDL", key="info_ldl_hdl_button"):
                st.session_state.info_page = "ldl_hdl"
                st.rerun()

            if st.button("Triglycerides/HDL", key="info_tg_hdl_button"):
                st.session_state.info_page = "tg_hdl"
                st.rerun()


def main() -> None:
    initialize_session_state()

    if st.session_state.info_page is not None:
        show_info_page(st.session_state.info_page)
    else:
        render_calculator()


if __name__ == "__main__":
    main()
