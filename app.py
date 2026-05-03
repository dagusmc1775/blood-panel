import math

import streamlit as st

from info_pages import render_info_nav_buttons, show_info_page


st.set_page_config(page_title="Blood Panel Calculator", layout="centered")


SAVED_INPUT_KEYS = {
    "total_cholesterol": "saved_total_cholesterol",
    "ldl": "saved_ldl",
    "hdl": "saved_hdl",
    "triglycerides": "saved_triglycerides",
    "glucose": "saved_glucose",
}


def initialize_session_state() -> None:
    defaults = {
        "info_page": None,
        "has_results": False,
        "tyg": None,
        "ldl_hdl": None,
        "total_hdl": None,
        "tg_hdl": None,
        "calc_total_cholesterol": None,
        "calc_ldl": None,
        "calc_hdl": None,
        "calc_triglycerides": None,
        "calc_glucose": None,
        "saved_total_cholesterol": 0,
        "saved_ldl": 0,
        "saved_hdl": 0,
        "saved_triglycerides": 0,
        "saved_glucose": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_input_value(widget_key: str, saved_key: str) -> None:
    st.session_state[saved_key] = st.session_state[widget_key]


def render_number_input(label: str, widget_key: str) -> int:
    saved_key = SAVED_INPUT_KEYS[widget_key]
    if widget_key not in st.session_state:
        st.session_state[widget_key] = int(st.session_state.get(saved_key, 0))

    return st.number_input(
        label,
        min_value=0,
        step=1,
        key=widget_key,
        on_change=sync_input_value,
        args=(widget_key, saved_key),
    )


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

    st.session_state.calc_total_cholesterol = total_cholesterol
    st.session_state.calc_ldl = ldl
    st.session_state.calc_hdl = hdl
    st.session_state.calc_triglycerides = triglycerides
    st.session_state.calc_glucose = glucose
    st.session_state.tyg = math.log((triglycerides * glucose) / 2)
    st.session_state.ldl_hdl = ldl / hdl
    st.session_state.total_hdl = total_cholesterol / hdl
    st.session_state.tg_hdl = triglycerides / hdl
    st.session_state.has_results = True


def render_calculator() -> None:
    st.title("Blood Panel Calculator")

    total_cholesterol = render_number_input("Total Cholesterol", "total_cholesterol")
    ldl = render_number_input("LDL-C", "ldl")
    hdl = render_number_input("HDL-C", "hdl")
    triglycerides = render_number_input("Triglycerides", "triglycerides")
    glucose = render_number_input("Fasting Glucose", "glucose")

    if st.button("Calculate", key="calculate_button"):
        calculate_results(total_cholesterol, ldl, hdl, triglycerides, glucose)

    if st.session_state.has_results:
        st.subheader("Results")
        st.write(f"**TyG Index:** {st.session_state.tyg:.2f}")
        st.write(f"**LDL/HDL Ratio:** {st.session_state.ldl_hdl:.2f}")
        st.write(f"**Total Cholesterol/HDL Ratio:** {st.session_state.total_hdl:.2f}")
        st.write(f"**Triglycerides/HDL Ratio:** {st.session_state.tg_hdl:.2f}")

        st.subheader("Learn More")
        render_info_nav_buttons(key_prefix="main_info_nav")


def main() -> None:
    initialize_session_state()

    if st.session_state.info_page is not None:
        show_info_page(st.session_state.info_page)
    else:
        render_calculator()


if __name__ == "__main__":
    main()
