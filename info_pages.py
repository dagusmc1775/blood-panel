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


def write_section(title: str, body: str | list[str]) -> None:
    st.subheader(title)
    if isinstance(body, list):
        for item in body:
            st.write(item)
    else:
        st.write(body)


def write_standard_page(
    header: str,
    result_line: str,
    input_lines: list[str],
    category: str,
    meaning: str,
    driver_lines: list[str],
    indicates: str,
    does_not_tell: str,
    practical_lines: list[str],
    bottom_line: str,
) -> None:
    st.header(header)
    write_section("Your Result", [result_line, *input_lines])
    write_section("Category", f"**{category}**")
    write_section("What it means", meaning)
    write_section("What is driving it", driver_lines)
    write_section("What this indicates", indicates)
    write_section("What this does NOT tell you", does_not_tell)
    write_section("Practical use / next steps", practical_lines)
    write_section("Bottom line", bottom_line)


def show_tyg_page() -> None:
    tyg = st.session_state.get("tyg", None)
    triglycerides = st.session_state.get("calc_triglycerides", None)
    glucose = st.session_state.get("calc_glucose", None)

    if tyg is None or triglycerides is None or glucose is None:
        st.header("TyG Index")
        st.warning("No TyG result is available yet. Return to the calculator and run your blood panel first.")
        return

    if tyg < 8.0:
        category = "Favorable / insulin sensitive"
        meaning = "This is a favorable TyG pattern and generally suggests good insulin sensitivity."
        action = "Maintain the habits supporting this result and use TyG as a trend marker during diet or training changes."
    elif tyg < 8.5:
        category = "Borderline"
        meaning = "This is an early watch zone. Insulin resistance risk may begin to rise even if single labs still look acceptable."
        action = "Look for small improvements in triglycerides, fasting glucose, sleep, and carbohydrate quality."
    elif tyg < 9.0:
        category = "Likely insulin resistance"
        meaning = "This range is commonly associated with insulin resistance and less favorable metabolic health."
        action = "Prioritize triglyceride reduction, glucose control, weight or waist improvement if relevant, and consistent aerobic training."
    elif tyg < 9.5:
        category = "High risk"
        meaning = "This is a strong metabolic warning signal and suggests elevated insulin resistance risk."
        action = "Consider a structured metabolic review, including A1C, fasting insulin, liver markers, waist trend, and diet pattern."
    else:
        category = "Very high risk"
        meaning = "This is a very strong signal for metabolic dysfunction risk and should not be treated as a minor fluctuation."
        action = "Review this with a clinician and consider additional testing such as A1C, fasting insulin, liver markers, and full cardiometabolic review."

    if triglycerides < 100:
        tg_context = "Triglycerides are favorable on their own."
    elif triglycerides < 150:
        tg_context = "Triglycerides are acceptable but not ideal."
    elif triglycerides < 200:
        tg_context = "Triglycerides are borderline high and likely contribute to TyG."
    else:
        tg_context = "Triglycerides are high and are a major TyG driver."

    if glucose < 100:
        glucose_context = "Fasting glucose is in the normal range."
    elif glucose < 126:
        glucose_context = "Fasting glucose is in the prediabetes range and likely contributes to TyG."
    else:
        glucose_context = "Fasting glucose is at a diabetes-range threshold and should be reviewed with a clinician."

    if triglycerides >= 150 and glucose >= 100:
        driver = "Both triglycerides and fasting glucose are pushing TyG higher."
    elif triglycerides >= 150:
        driver = "The TyG result appears primarily triglyceride-driven."
    elif glucose >= 100:
        driver = "The TyG result appears primarily glucose-driven."
    elif tyg >= 8.5:
        driver = "TyG is elevated even though triglycerides and glucose are not individually high. Their combined product is still elevated relative to ideal and should be trended."
    else:
        driver = "Neither triglycerides nor glucose is concerning by itself, which fits the favorable TyG category."

    indicates = (
        "Signal strength: TyG is a strong directional indicator of metabolic health because it combines fasting triglycerides and glucose. "
        "It is most useful when tracked over time alongside A1C, waist, fitness, and diet changes."
    )
    does_not_tell = (
        "TyG is not a diagnosis and does not replace fasting insulin, HOMA-IR, oral glucose tolerance testing, A1C, or clinician review. "
        "It also does not identify whether triglycerides, liver fat, sleep, medication, or diet is the root cause."
    )
    practical = [
        action,
        "Trend guidance: most useful when tracked over time alongside triglycerides and glucose.",
        "Common scenario: a low-carb or keto profile may show excellent glucose but still needs triglycerides monitored because TyG uses both numbers.",
    ]
    bottom = "TyG is inexpensive, accessible, predictive, and actionable, but it works best as a trend marker within the full metabolic picture."

    write_standard_page(
        "TyG Index",
        f"**Your TyG Index:** {tyg:.2f}",
        [
            f"**Triglycerides:** {triglycerides} mg/dL",
            f"**Fasting Glucose:** {glucose} mg/dL",
        ],
        category,
        meaning,
        [driver, tg_context, glucose_context],
        indicates,
        does_not_tell,
        practical,
        bottom,
    )


def show_ldl_hdl_page() -> None:
    ldl_hdl = st.session_state.get("ldl_hdl", None)
    ldl = st.session_state.get("calc_ldl", None)
    hdl = st.session_state.get("calc_hdl", None)

    if ldl_hdl is None or ldl is None or hdl is None:
        st.header("LDL/HDL Ratio")
        st.warning("No LDL/HDL result is available yet. Return to the calculator and run your blood panel first.")
        return

    if ldl_hdl < 2.0:
        category = "Favorable"
        meaning = "This ratio suggests a favorable balance between LDL burden and HDL support."
        action = "Maintain the pattern and keep checking whether ApoB, triglycerides, blood pressure, and family history agree."
    elif ldl_hdl < 2.5:
        category = "Good / near ideal"
        meaning = "This is near ideal, but risk can still differ depending on LDL particle burden and overall context."
        action = "Continue monitoring trends and focus on keeping LDL appropriate for your personal risk profile."
    elif ldl_hdl < 3.5:
        category = "Borderline / watchful"
        meaning = "This ratio is drifting into a watch zone where LDL burden may be outpacing HDL support."
        action = "Identify whether LDL is rising, HDL is weak, or both are moving in the wrong direction."
    elif ldl_hdl < 5.0:
        category = "Elevated risk"
        meaning = "This ratio points to a less favorable lipid balance and may reflect higher atherogenic exposure."
        action = "Consider a more complete cardiovascular review, especially ApoB or LDL-P, inflammation markers, and blood pressure."
    else:
        category = "High risk"
        meaning = "This ratio is high and may indicate a substantially unfavorable LDL to HDL balance."
        action = "Review this with a clinician, particularly if LDL is high, HDL is low, or family history is concerning."

    if ldl < 100:
        ldl_context = "LDL-C is favorable."
    elif ldl < 130:
        ldl_context = "LDL-C is near optimal or mildly elevated depending on risk profile."
    elif ldl < 160:
        ldl_context = "LDL-C is borderline high."
    elif ldl < 190:
        ldl_context = "LDL-C is high."
    else:
        ldl_context = "LDL-C is very high; possible familial or genetic risk should be reviewed with a clinician."

    if hdl < 40:
        hdl_context = "HDL-C is low for men and can amplify risk."
    elif hdl < 60:
        hdl_context = "HDL-C is acceptable but not strongly protective."
    else:
        hdl_context = "HDL-C is generally protective."

    if ldl >= 130 and hdl < 40:
        driver = "Both high LDL-C and low HDL-C are worsening the ratio, so the signal is more concerning."
    elif ldl >= 130 and hdl >= 60:
        driver = "LDL-C is elevated, but high HDL-C is partially offsetting the ratio. That does not erase LDL-related risk."
    elif ldl >= 130:
        driver = "The ratio appears primarily LDL-driven."
    elif ldl < 100 and hdl < 60:
        driver = "LDL-C is favorable, but HDL-C is not strongly protective, which keeps the ratio from looking even better."
    elif hdl < 40:
        driver = "The ratio appears primarily HDL-driven because low HDL-C is weakening the denominator."
    elif ldl_hdl >= 3.5:
        driver = "The ratio is unfavorable even without a single extreme value, so the overall lipid balance deserves attention."
    else:
        driver = "The ratio is supported by a reasonable LDL-C and HDL-C balance."

    indicates = (
        "Signal strength: LDL/HDL is a directional cardiovascular signal, but it is weaker than ApoB or LDL particle measures for particle burden. "
        "LDL carries cholesterol to tissues, including artery walls, while HDL helps move cholesterol back to the liver."
    )
    does_not_tell = (
        "LDL/HDL does not show ApoB, LDL-P, particle size, oxidation status, CAC score, or inflammatory risk. "
        "LDL is necessary; the goal is not zero LDL, but LDL that is appropriate for risk profile."
    )
    practical = [
        action,
        "Trend guidance: useful as a snapshot, but better when tracked with LDL-C, HDL-C, triglycerides, and ApoB if available.",
        "Common scenario: an endurance athlete may have high HDL that improves the ratio, but ApoB or LDL-P can still matter if LDL-C is elevated.",
    ]
    bottom = "LDL/HDL helps separate atherogenic burden from protective capacity, but it should not replace ApoB, LDL-P, CAC score, or inflammatory markers."

    write_standard_page(
        "LDL/HDL Ratio",
        f"**Your LDL/HDL Ratio:** {ldl_hdl:.2f}",
        [f"**LDL-C:** {ldl} mg/dL", f"**HDL-C:** {hdl} mg/dL"],
        category,
        meaning,
        [driver, ldl_context, hdl_context],
        indicates,
        does_not_tell,
        practical,
        bottom,
    )


def show_chol_hdl_page() -> None:
    total_hdl = st.session_state.get("total_hdl", None)
    total_cholesterol = st.session_state.get("calc_total_cholesterol", None)
    hdl = st.session_state.get("calc_hdl", None)
    ldl = st.session_state.get("calc_ldl", None)
    triglycerides = st.session_state.get("calc_triglycerides", None)

    if total_hdl is None or total_cholesterol is None or hdl is None:
        st.header("Total Cholesterol/HDL Ratio")
        st.warning("No Total Cholesterol/HDL result is available yet. Return to the calculator and run your blood panel first.")
        return

    if total_hdl < 3.5:
        category = "Favorable"
        meaning = "This ratio suggests total cholesterol is well balanced against HDL-C."
        action = "Maintain the pattern, but still review LDL-C, triglycerides, and personal risk factors."
    elif total_hdl < 5.0:
        category = "Moderate / watchful"
        meaning = "This ratio is acceptable for many people but worth watching if LDL-C or triglycerides are elevated."
        action = "Look at the full lipid panel to see whether total cholesterol is being driven by LDL-C, HDL-C, or triglyceride-rich particles."
    elif total_hdl < 6.0:
        category = "Elevated risk"
        meaning = "This ratio suggests a less favorable cholesterol balance and may indicate increased cardiovascular risk."
        action = "Consider lifestyle changes and a more complete risk review, especially if LDL-C or triglycerides are also high."
    else:
        category = "High risk"
        meaning = "This ratio is high and suggests total cholesterol is unfavorable relative to HDL-C."
        action = "Review this pattern with a clinician, especially if HDL-C is low or LDL-C and triglycerides are elevated."

    if total_cholesterol >= 240 and hdl < 40:
        driver = "High total cholesterol and low HDL-C are both worsening the ratio."
    elif total_cholesterol >= 240 and hdl >= 60:
        driver = "Total cholesterol is high, but favorable HDL-C is partially offsetting the ratio. LDL-C and triglycerides still decide whether that is reassuring."
    elif total_cholesterol >= 240:
        driver = "High total cholesterol appears to be the main driver."
    elif hdl < 40:
        driver = "Low HDL-C is worsening the ratio even if total cholesterol is not extremely high."
    elif hdl >= 60 and total_cholesterol >= 200:
        driver = "Favorable HDL-C is helping offset higher total cholesterol. This can be benign or concerning depending on LDL-C and triglycerides."
    elif total_hdl >= 5.0:
        driver = "The ratio is elevated, so the balance is unfavorable even if no single value looks extreme."
    else:
        driver = "The ratio is supported by a reasonable total cholesterol and HDL-C balance."

    contribution_notes = []
    if ldl is not None and ldl >= 130:
        contribution_notes.append("LDL-C appears to be contributing to the total cholesterol burden.")
    if triglycerides is not None and triglycerides >= 150:
        contribution_notes.append("Triglycerides may indicate more triglyceride-rich particles contributing to risk.")
    if not contribution_notes:
        contribution_notes.append("LDL-C and triglycerides do not stand out as obvious drivers, so the ratio should be interpreted in the full panel context.")

    indicates = (
        "Signal strength: this is a broad directional signal. Total cholesterol alone can be misleading because it combines LDL-C, HDL-C, and other cholesterol fractions."
    )
    does_not_tell = (
        "This ratio does not show ApoB, LDL particle number, LDL particle size, inflammation, CAC score, or whether high total cholesterol is mostly protective HDL-C versus atherogenic particles."
    )
    practical = [
        action,
        "Trend guidance: useful as a snapshot, but better tracked over time with LDL-C, HDL-C, triglycerides, and non-HDL cholesterol.",
        "Common scenario: a low-carb or endurance profile may raise total cholesterol while HDL-C is strong, so LDL-C, ApoB, and triglycerides become important context."
    ]
    bottom = "Total Cholesterol/HDL is useful for quick context, but total cholesterol alone can be misleading. The full lipid pattern matters more."

    write_standard_page(
        "Total Cholesterol/HDL Ratio",
        f"**Your Total Cholesterol/HDL Ratio:** {total_hdl:.2f}",
        [
            f"**Total Cholesterol:** {total_cholesterol} mg/dL",
            f"**HDL-C:** {hdl} mg/dL",
        ],
        category,
        meaning,
        [driver, *contribution_notes],
        indicates,
        does_not_tell,
        practical,
        bottom,
    )


def show_tg_hdl_page() -> None:
    tg_hdl = st.session_state.get("tg_hdl", None)
    triglycerides = st.session_state.get("calc_triglycerides", None)
    hdl = st.session_state.get("calc_hdl", None)
    glucose = st.session_state.get("calc_glucose", None)

    if tg_hdl is None or triglycerides is None or hdl is None:
        st.header("Triglycerides/HDL Ratio")
        st.warning("No Triglycerides/HDL result is available yet. Return to the calculator and run your blood panel first.")
        return

    if tg_hdl < 2.0:
        category = "Favorable / insulin sensitive"
        meaning = "This pattern is generally favorable and often aligns with better insulin sensitivity."
        action = "Maintain the habits supporting low triglycerides and adequate HDL-C."
    elif tg_hdl < 3.0:
        category = "Mildly watchful"
        meaning = "This is a mild watch zone where metabolic risk may be starting to rise."
        action = "Watch triglyceride trends, carbohydrate quality, alcohol intake, sleep, and waist changes."
    elif tg_hdl < 4.0:
        category = "Moderate metabolic risk"
        meaning = "This ratio suggests a more concerning metabolic pattern often linked with insulin resistance."
        action = "Prioritize triglyceride reduction, improved glucose control, and regular aerobic activity."
    else:
        category = "High metabolic risk"
        meaning = "This ratio is high and can be a strong warning sign for insulin resistance or metabolic syndrome risk."
        action = "Consider a focused metabolic review, especially if fasting glucose, A1C, waist, or blood pressure are also elevated."

    if triglycerides >= 150 and hdl < 40:
        driver = "Both high triglycerides and low HDL-C are worsening the ratio, which strengthens the metabolic risk signal."
    elif triglycerides >= 150 and hdl >= 40:
        driver = "High triglycerides are driving the ratio despite acceptable HDL-C."
    elif triglycerides < 100 and hdl < 40:
        driver = "Triglycerides are favorable, but low HDL-C is weakening the ratio."
    elif hdl < 40:
        driver = "Low HDL-C is the main driver."
    elif triglycerides >= 150:
        driver = "High triglycerides are the main driver."
    elif tg_hdl >= 3.0:
        driver = "The ratio is metabolically unfavorable even without an extreme single value, so the combined pattern matters."
    else:
        driver = "Low triglycerides and adequate HDL-C are supporting the favorable ratio."

    if glucose is not None and glucose >= 100:
        glucose_note = "Fasting glucose is also elevated, which makes the insulin-resistance signal more important."
    else:
        glucose_note = "Fasting glucose does not add an obvious warning signal, but triglyceride/HDL can still reveal early metabolic strain."

    indicates = (
        "Signal strength: triglycerides/HDL is a strong practical marker for insulin resistance risk and metabolic syndrome patterns, especially when triglycerides are high."
    )
    does_not_tell = (
        "This ratio does not diagnose diabetes, measure insulin directly, show liver fat, or replace A1C, fasting insulin, blood pressure, waist, or clinical assessment."
    )
    practical = [
        action,
        "Trend guidance: best tracked over time alongside triglycerides, HDL-C, fasting glucose, A1C, and waist trend.",
        "Common scenario: a high triglyceride metabolic profile often improves when refined carbohydrates, alcohol, excess calories, and inactivity are addressed.",
    ]
    bottom = "Triglycerides/HDL is one of the most useful simple ratios for metabolic health, but it should be interpreted with glucose, waist, blood pressure, and the full lipid panel."

    write_standard_page(
        "Triglycerides/HDL Ratio",
        f"**Your Triglycerides/HDL Ratio:** {tg_hdl:.2f}",
        [
            f"**Triglycerides:** {triglycerides} mg/dL",
            f"**HDL-C:** {hdl} mg/dL",
        ],
        category,
        meaning,
        [driver, glucose_note],
        indicates,
        does_not_tell,
        practical,
        bottom,
    )
