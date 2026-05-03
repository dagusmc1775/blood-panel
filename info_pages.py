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
    ldl_hdl = st.session_state.get("ldl_hdl", None)
    ldl = st.session_state.get("calc_ldl", None)
    hdl = st.session_state.get("calc_hdl", None)

    st.header("LDL/HDL Ratio")

    if ldl_hdl is None or ldl is None or hdl is None:
        st.warning("No LDL/HDL result is available yet. Return to the calculator and run your blood panel first.")
        return

    st.subheader(f"Your LDL/HDL Ratio: {ldl_hdl:.2f}")

    if ldl_hdl < 2.0:
        category = "Favorable"
        meaning = "Your LDL/HDL ratio is in a favorable range and generally suggests a healthy balance between atherogenic burden and protective capacity."
        action = "Maintain the habits supporting this pattern and keep interpreting the ratio alongside the full lipid panel and overall risk profile."
    elif ldl_hdl < 2.5:
        category = "Good / near ideal"
        meaning = "Your LDL/HDL ratio is near an ideal range, though individual LDL-C, HDL-C, triglycerides, and risk factors still matter."
        action = "Continue monitoring trends and focus on sustainable diet, exercise, sleep, and body-composition habits."
    elif ldl_hdl < 3.5:
        category = "Borderline / watchful"
        meaning = "Your LDL/HDL ratio is in a watchful range where lipid balance may be drifting in a less favorable direction."
        action = "Look at what is driving the ratio. Improving LDL-C, HDL-C, triglycerides, insulin sensitivity, and inflammation markers may be useful."
    elif ldl_hdl < 5.0:
        category = "Elevated risk"
        meaning = "Your LDL/HDL ratio is elevated and may indicate a higher atherogenic burden relative to protective cholesterol transport."
        action = "Consider a more complete cardiovascular risk review, including family history, blood pressure, metabolic markers, and advanced lipid testing."
    else:
        category = "High risk"
        meaning = "Your LDL/HDL ratio is high and may reflect a lipid pattern associated with increased cardiovascular risk."
        action = "Review this with a clinician, especially if LDL-C is high, HDL-C is low, or you have other risk factors such as hypertension, diabetes, smoking history, or family history."

    if ldl < 100:
        ldl_context = "Your LDL-C is favorable."
    elif ldl < 130:
        ldl_context = "Your LDL-C is near optimal or mildly elevated, depending on your risk profile."
    elif ldl < 160:
        ldl_context = "Your LDL-C is borderline high."
    elif ldl < 190:
        ldl_context = "Your LDL-C is high."
    else:
        ldl_context = "Your LDL-C is very high, which can suggest possible familial or genetic risk; clinician review is warranted."

    if hdl < 40:
        hdl_context = "Your HDL-C is low for men and can act as a risk amplifier."
    elif hdl < 60:
        hdl_context = "Your HDL-C is acceptable but not strongly protective."
    else:
        hdl_context = "Your HDL-C is generally protective."

    if ldl >= 130 and hdl < 40:
        driver = "Your ratio is being worsened by both high LDL-C and low HDL-C."
    elif ldl >= 130:
        driver = "Your ratio appears primarily LDL-driven."
    elif hdl < 40:
        driver = "Your ratio appears primarily HDL-driven."
    else:
        driver = "Your ratio is not being driven by a clearly abnormal LDL or HDL value; interpret it in the full lipid context."

    st.write(f"**Category:** {category}")
    st.write(meaning)

    st.subheader("Your inputs")
    st.write(f"**LDL-C:** {ldl} mg/dL")
    st.write(f"**HDL-C:** {hdl} mg/dL")

    st.subheader("What is driving your LDL/HDL ratio?")
    st.write(driver)
    st.write(ldl_context)
    st.write(hdl_context)

    st.subheader("What this number indicates")
    st.write(action)

    st.subheader("What LDL tells you")
    st.write("LDL carries cholesterol to tissues, including artery walls. Higher LDL generally means more opportunity for plaque formation, especially when other risk factors are present. LDL is necessary; the goal is not zero LDL, but LDL that is appropriate for your risk profile.")

    st.subheader("What HDL tells you")
    st.write("HDL helps move cholesterol away from arteries and back to the liver. Higher HDL is generally favorable, but extremely high HDL does not always mean more protection. HDL function matters more than the number, and HDL function is not measured on standard labs.")

    st.subheader("The real value of the LDL/HDL ratio")
    st.write("Total cholesterol alone can be misleading. LDL and HDL help separate atherogenic burden from protective capacity, and the LDL/HDL ratio gives a quick view of that balance.")

    st.subheader("What LDL/HDL reveals about metabolic health")
    st.write("A higher LDL/HDL ratio can travel with insulin resistance, higher triglycerides, excess visceral fat, inflammation, and less favorable lifestyle patterns. It is most useful when interpreted alongside triglycerides, glucose, blood pressure, body composition, and family history.")

    st.subheader("What LDL/HDL does not tell you")
    st.write("The LDL/HDL ratio is useful, but it does not show LDL particle number, particle size, oxidation status, or inflammatory risk. It also does not replace a clinician's full cardiovascular risk assessment.")

    st.subheader("Advanced tests that may help")
    st.write("Advanced tests may include ApoB, LDL-P/NMR, hs-CRP, and CAC score. These can add context when standard cholesterol numbers do not fully explain risk.")

    st.subheader("Bottom line")
    st.write("LDL/HDL is a helpful summary marker, but it is not the whole cardiovascular story. Use it as a trend marker and risk-context clue, then interpret it alongside the full lipid panel, metabolic markers, and personal risk factors.")


def show_chol_hdl_page() -> None:
    st.header("Total Cholesterol/HDL Ratio")
    st.write("Total Cholesterol/HDL content here.")


def show_tg_hdl_page() -> None:
    st.header("Triglycerides/HDL Ratio")
    st.write("Triglycerides/HDL content here.")

