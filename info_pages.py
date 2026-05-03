import streamlit as st


INFO_PAGES = [
    ("TyG Index", "tyg"),
    ("LDL/HDL", "ldl_hdl"),
    ("Cholesterol/HDL", "chol_hdl"),
    ("Triglycerides/HDL", "tg_hdl"),
]


def render_info_nav_buttons(key_prefix: str = "info_nav") -> None:
    columns = st.columns(4)
    for column, (label, page_key) in zip(columns, INFO_PAGES):
        with column:
            if st.button(label, key=f"{key_prefix}_{page_key}", use_container_width=True):
                st.session_state.info_page = page_key
                st.rerun()


def render_back_button(key: str = "back_to_calculator_button") -> None:
    if st.button("Back to Calculator", key=key):
        st.session_state.info_page = None
        st.rerun()


def show_info_page(page_key: str) -> None:
    if page_key == "tyg":
        show_tyg_page()
    elif page_key == "ldl_hdl":
        show_ldl_hdl_page()
    elif page_key == "chol_hdl":
        show_chol_hdl_page()
    elif page_key == "tg_hdl":
        show_tg_hdl_page()
    else:
        st.error("Unknown information page.")

    st.divider()
    render_back_button(key=f"back_to_calculator_{page_key}")
    st.subheader("Learn More")
    render_info_nav_buttons(key_prefix=f"info_page_nav_{page_key}")


def show_tyg_page() -> None:
    tyg = st.session_state.get("tyg", None)
    triglycerides = st.session_state.get("calc_triglycerides", None)
    glucose = st.session_state.get("calc_glucose", None)

    st.header("TyG Index")

    if tyg is None:
        st.warning("No TyG result is available yet. Return to the calculator and run your blood panel first.")
        return

    if triglycerides is None or glucose is None:
        st.warning("Triglycerides and fasting glucose are missing. Return to the calculator and run the blood panel again.")
        return

    st.subheader(f"Your TyG Index: {tyg:.2f}")

    if tyg < 8.0:
        category = "Favorable / insulin sensitive"
        meaning = "Your TyG Index is in a favorable range and generally suggests good insulin sensitivity."
        action = "Maintain current habits. Continue trending over time, especially with changes in diet, training, or weight."
    elif tyg < 8.5:
        category = "Borderline"
        meaning = "Your TyG Index is approaching levels where insulin resistance risk may begin to increase."
        action = "Monitor over time. Small improvements in triglycerides, fasting glucose, sleep, and diet quality can move this lower."
    elif tyg < 9.0:
        category = "Likely insulin resistance"
        meaning = "Your TyG Index is in a range commonly associated with insulin resistance."
        action = "Focus on improving metabolic health: reduce processed carbs, improve triglycerides, monitor glucose trends, and maintain consistent aerobic training."
    elif tyg < 9.5:
        category = "High risk"
        meaning = "Your TyG Index is elevated and suggests increased risk of insulin resistance and metabolic dysfunction."
        action = "Consider a more structured approach: diet adjustments, weight management, increased activity, and possibly additional labs such as fasting insulin or A1C."
    else:
        category = "Very high risk"
        meaning = "Your TyG Index is significantly elevated and strongly associated with insulin resistance and higher cardiometabolic risk."
        action = "This warrants attention. Consider working with a clinician and reviewing full metabolic markers including A1C, fasting insulin, triglycerides, liver markers, and body composition."

    if triglycerides < 100:
        tg_context = "Your triglycerides are favorable. They are probably not the main reason for a higher TyG score."
    elif triglycerides < 150:
        tg_context = "Your triglycerides are acceptable but not ideal. They may be contributing modestly to your TyG score."
    elif triglycerides < 200:
        tg_context = "Your triglycerides are borderline high and are likely contributing meaningfully to your TyG score."
    else:
        tg_context = "Your triglycerides are high and are likely a major driver of your TyG score."

    if glucose < 100:
        glucose_context = "Your fasting glucose is in the normal range."
    elif glucose < 126:
        glucose_context = "Your fasting glucose is in the prediabetes range and is likely contributing to your TyG score."
    else:
        glucose_context = "Your fasting glucose is in the diabetes-range threshold and should be reviewed with a clinician."

    if triglycerides >= 150 and glucose >= 100:
        driver = "Both triglycerides and fasting glucose are pushing your TyG higher."
    elif triglycerides >= 150:
        driver = "Your TyG score appears primarily triglyceride-driven."
    elif glucose >= 100:
        driver = "Your TyG score appears primarily glucose-driven."
    else:
        driver = "Neither triglycerides nor fasting glucose is individually high, so the combined TyG score should mainly be used as a trend marker."

    st.write(f"**Category:** {category}")
    st.write(meaning)

    st.subheader("Your inputs")
    st.write(f"**Triglycerides:** {triglycerides} mg/dL")
    st.write(f"**Fasting Glucose:** {glucose} mg/dL")

    st.subheader("What is driving your TyG score?")
    st.write(driver)
    st.write(tg_context)
    st.write(glucose_context)

    st.subheader("What this number indicates")
    st.write(action)

    st.subheader("Who benefits most from knowing TyG?")
    st.write("""
TyG is especially useful if you:

- Are physically active but struggle with diet
- Have normal A1C but elevated triglycerides
- Are doing low-carb, keto, or intermittent fasting
- Want to reduce long-term heart disease risk
- Are monitoring metabolic health, not just weight
""")

    st.subheader("What it is not")
    st.write("""
- It is not a diagnosis
- It does not replace an oral glucose tolerance test, fasting insulin, HOMA-IR, or clamp studies
- It is best used as a trend marker over time
""")

    st.subheader("Practical use")
    st.write("""
People use TyG to:

- See whether diet changes are improving insulin sensitivity
- Decide how aggressive carbohydrate reduction or carb cycling should be
- Track metabolic recovery alongside VO2 max, fitness, and body composition
- Flag hidden risk even when standard labs look normal
""")

    st.subheader("Bottom line")
    st.write("""
The TyG Index is inexpensive, accessible, predictive, and actionable.

If your goal is long-term performance, cardiovascular health, and metabolic resilience, TyG can provide insight that A1C alone may miss.
""")

    st.caption("TyG is a screening and trend marker, not a standalone diagnosis. Interpretation depends on the full clinical picture.")


def show_ldl_hdl_page() -> None:
    st.header("LDL/HDL Ratio")
    st.write("LDL/HDL content here.")


def show_chol_hdl_page() -> None:
    st.header("Total Cholesterol/HDL Ratio")
    st.write("Total Cholesterol/HDL content here.")


def show_tg_hdl_page() -> None:
    st.header("Triglycerides/HDL Ratio")
    st.write("Triglycerides/HDL content here.")
