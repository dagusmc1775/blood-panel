import streamlit as st


def show_info_page(page_key):
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

    if st.button("Back to Calculator"):
        st.session_state.info_page = None
        st.rerun()


def show_tyg_page():
    tyg = st.session_state.get("tyg", None)
    triglycerides = st.session_state.get("triglycerides", None)
    glucose = st.session_state.get("glucose", None)

    st.header("TyG Index")

    if tyg is None:
        st.warning("No TyG result is available yet. Return to the calculator and run your blood panel first.")
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
    
    st.write(f"**Category:** {category}")
    st.write(meaning)

    st.subheader("Your inputs")
    st.write(f"**Triglycerides:** {triglycerides} mg/dL")
    st.write(f"**Fasting Glucose:** {glucose} mg/dL")

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
- Track metabolic recovery alongside VO₂ max, fitness, and body composition
- Flag hidden risk even when standard labs look “normal”
""")

    st.subheader("Bottom line")
    st.write("""
The TyG Index is inexpensive, accessible, predictive, and actionable.

If your goal is long-term performance, cardiovascular health, and metabolic resilience, TyG can provide insight that A1C alone may miss.
""")

    st.caption("TyG is a screening and trend marker, not a standalone diagnosis. Interpretation depends on the full clinical picture.")


def show_ldl_hdl_page():
    st.header("LDL/HDL Ratio")
    st.write("LDL/HDL content here.")


def show_chol_hdl_page():
    st.header("Total Cholesterol/HDL Ratio")
    st.write("Total Cholesterol/HDL content here.")


def show_tg_hdl_page():
    st.header("Triglycerides/HDL Ratio")
    st.write("Triglycerides/HDL content here.")
