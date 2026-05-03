import math

import streamlit as st


st.set_page_config(page_title="Blood Panel Calculator", layout="centered")


SAVED_INPUT_KEYS = {
    "total_cholesterol": "saved_total_cholesterol",
    "ldl": "saved_ldl",
    "hdl": "saved_hdl",
    "triglycerides": "saved_triglycerides",
    "glucose": "saved_glucose",
    "apob": "saved_apob",
    "hba1c": "saved_hba1c",
}


CORE_INPUT_KEYS = {"total_cholesterol", "ldl", "hdl", "triglycerides", "glucose"}


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
        "calc_apob": None,
        "calc_hba1c": None,
        "saved_total_cholesterol": 0,
        "saved_ldl": 0,
        "saved_hdl": 0,
        "saved_triglycerides": 0,
        "saved_glucose": 0,
        "saved_apob": 0.0,
        "saved_hba1c": 0.0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_input_value(widget_key: str, saved_key: str) -> None:
    st.session_state[saved_key] = st.session_state[widget_key]


def render_number_input(label: str, widget_key: str, help_text: str | None = None) -> int | float:
    saved_key = SAVED_INPUT_KEYS[widget_key]
    if widget_key not in st.session_state:
        st.session_state[widget_key] = st.session_state.get(saved_key, 0)

    if widget_key in CORE_INPUT_KEYS:
        return st.number_input(
            label,
            min_value=0,
            step=1,
            key=widget_key,
            help=help_text,
            on_change=sync_input_value,
            args=(widget_key, saved_key),
        )

    return st.number_input(
        label,
        min_value=0.0,
        step=0.1,
        format="%.1f",
        key=widget_key,
        help=help_text,
        on_change=sync_input_value,
        args=(widget_key, saved_key),
    )


def normalize_optional_value(value: int | float) -> float | None:
    numeric = float(value or 0.0)
    if numeric <= 0.0:
        return None
    return numeric


def calculate_results(
    total_cholesterol: int,
    ldl: int,
    hdl: int,
    triglycerides: int,
    glucose: int,
    apob: float | None,
    hba1c: float | None,
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
    st.session_state.calc_apob = apob
    st.session_state.calc_hba1c = hba1c
    st.session_state.tyg = math.log((triglycerides * glucose) / 2)
    st.session_state.ldl_hdl = ldl / hdl
    st.session_state.total_hdl = total_cholesterol / hdl
    st.session_state.tg_hdl = triglycerides / hdl
    st.session_state.has_results = True


def get_optional_marker_context() -> list[str]:
    context = []
    apob = st.session_state.get("calc_apob", None)
    hba1c = st.session_state.get("calc_hba1c", None)

    if apob is None:
        context.append("ApoB not provided; atherogenic particle burden cannot be directly assessed from this app run.")
    elif apob < 80:
        context.append(f"ApoB: {apob:.1f} mg/dL, which supports a lower atherogenic particle burden context.")
    elif apob < 100:
        context.append(f"ApoB: {apob:.1f} mg/dL, an intermediate particle-burden context that should be interpreted with personal risk.")
    else:
        context.append(f"ApoB: {apob:.1f} mg/dL, which adds concern for higher atherogenic particle burden even if ratios look acceptable.")

    if hba1c is None:
        context.append("HbA1c not provided; longer-term glucose exposure cannot be assessed from this app run.")
    elif hba1c < 5.7:
        context.append(f"HbA1c: {hba1c:.1f}%, which supports a normal longer-term glucose context.")
    elif hba1c < 6.5:
        context.append(f"HbA1c: {hba1c:.1f}%, which adds prediabetes-range context to the metabolic interpretation.")
    else:
        context.append(f"HbA1c: {hba1c:.1f}%, which adds diabetes-range context and warrants clinician review.")

    return context


def render_calculator() -> None:
    st.title("Blood Panel Calculator")

    total_cholesterol = render_number_input("Total Cholesterol", "total_cholesterol")
    ldl = render_number_input("LDL-C", "ldl")
    hdl = render_number_input("HDL-C", "hdl")
    triglycerides = render_number_input("Triglycerides", "triglycerides")
    glucose = render_number_input("Fasting Glucose", "glucose")

    st.subheader("Optional context markers")
    apob = render_number_input(
        "ApoB (optional)",
        "apob",
        help_text="ApoB estimates atherogenic particle number. Leave at 0 if it was not tested.",
    )
    hba1c = render_number_input(
        "HbA1c (optional)",
        "hba1c",
        help_text="HbA1c reflects longer-term glucose exposure. Leave at 0 if it was not tested.",
    )

    if st.button("Calculate", key="calculate_button"):
        calculate_results(
            total_cholesterol,
            ldl,
            hdl,
            triglycerides,
            glucose,
            normalize_optional_value(apob),
            normalize_optional_value(hba1c),
        )

    if st.session_state.has_results:
        st.subheader("Results")
        st.write(f"**TyG Index:** {st.session_state.tyg:.2f}")
        st.write(f"**LDL/HDL Ratio:** {st.session_state.ldl_hdl:.2f}")
        st.write(f"**Total Cholesterol/HDL Ratio:** {st.session_state.total_hdl:.2f}")
        st.write(f"**Triglycerides/HDL Ratio:** {st.session_state.tg_hdl:.2f}")

        st.subheader("Learn More")
        render_info_nav_buttons(key_prefix="main_info_nav")


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


def write_lines(lines: list[str]) -> None:
    for line in lines:
        st.write(line)


def render_definition_expanders() -> None:
    st.subheader("Expanders / definitions")
    with st.expander("What is atherogenic burden?"):
        st.write(
            "Atherogenic burden is the amount of cholesterol-carrying particle exposure that can contribute to plaque formation. "
            "LDL-C is one clue, but ApoB and LDL-P can better estimate particle burden."
        )
    with st.expander("What is metabolic stress?"):
        st.write(
            "Metabolic stress means the lipid and glucose pattern may reflect insulin resistance, excess energy storage, liver fat, "
            "poor sleep, alcohol effect, high refined carbohydrate intake, or low activity."
        )
    with st.expander("What does this ratio miss?"):
        st.write(
            "Ratios do not diagnose disease and do not directly measure insulin, ApoB, LDL-P, inflammation, oxidation, plaque, "
            "HDL function, or medication effects. Use them as decision-support signals, not final answers."
        )
    with st.expander("Advanced markers to consider"):
        st.write(
            "ApoB estimates the number of atherogenic particles. LDL-P/NMR estimates LDL particle number and size. "
            "CAC score images calcified coronary plaque. Non-HDL cholesterol captures cholesterol carried by all non-HDL particles. "
            "hs-CRP can add inflammatory context."
        )


def render_metric_report(
    header: str,
    result_lines: list[str],
    category: str,
    meaning: str,
    driver_lines: list[str],
    agreement: str,
    indicates: str,
    does_not_tell: str,
    practical_lines: list[str],
    bottom_line: str,
) -> None:
    st.header(header)
    st.caption("Key terms such as atherogenic burden, metabolic stress, insulin resistance, ApoB, LDL-P, CAC score, and non-HDL cholesterol are defined in the expanders below.")
    st.subheader("Your Result")
    write_lines(result_lines)
    st.subheader("Category")
    st.write(f"**{category}**")
    st.subheader("What it means")
    st.write(meaning)
    st.subheader("What is driving it")
    write_lines([agreement, *driver_lines])
    st.subheader("What this indicates")
    st.write(indicates)
    st.subheader("What this does NOT tell you")
    st.write(does_not_tell)
    st.subheader("Practical use / next steps")
    write_lines(practical_lines)
    st.subheader("Bottom line")
    st.write(bottom_line)
    marker_context = get_optional_marker_context()
    if marker_context:
        st.subheader("Optional marker context")
        write_lines(marker_context)
    render_definition_expanders()


def classify_tg(triglycerides: float) -> str:
    if triglycerides < 100:
        return "favorable"
    if triglycerides < 150:
        return "acceptable"
    if triglycerides < 200:
        return "borderline high"
    return "high"


def classify_glucose(glucose: float) -> str:
    if glucose < 100:
        return "normal"
    if glucose < 126:
        return "prediabetes-range"
    return "diabetes-range threshold"


def classify_hdl(hdl: float) -> str:
    if hdl < 40:
        return "low"
    if hdl < 60:
        return "acceptable"
    return "protective"


def classify_ldl(ldl: float) -> str:
    if ldl < 100:
        return "favorable"
    if ldl < 130:
        return "near optimal or mildly elevated"
    if ldl < 160:
        return "borderline high"
    if ldl < 190:
        return "high"
    return "very high"


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
        meaning = "This is a favorable TyG pattern and generally fits lower insulin resistance risk."
        action = "Maintain the habits supporting this result; use it as a trend marker during diet or training changes."
    elif tyg < 8.5:
        category = "Borderline"
        meaning = "This is an early watch zone. The combined triglyceride-glucose product is starting to rise."
        action = "Look for small improvements in triglycerides, fasting glucose, sleep, alcohol intake, and carbohydrate quality."
    elif tyg < 9.0:
        category = "Likely insulin resistance"
        meaning = "This range commonly aligns with insulin resistance or metabolic stress."
        action = "Prioritize triglyceride reduction, glucose control, waist trend, and consistent aerobic training."
    elif tyg < 9.5:
        category = "High risk"
        meaning = "This is a strong metabolic warning signal. It should not be brushed off as noise."
        action = "Consider a structured metabolic review with A1C, fasting insulin, liver markers, and waist trend."
    else:
        category = "Very high risk"
        meaning = "This is a very strong signal for metabolic dysfunction risk."
        action = "Review this with a clinician and consider deeper cardiometabolic testing."

    tg_status = classify_tg(triglycerides)
    glucose_status = classify_glucose(glucose)
    if triglycerides >= 150 and glucose >= 100:
        agreement = "The ratio looks poor and the underlying numbers confirm concern."
        driver = "Both triglycerides and fasting glucose are pushing TyG higher."
    elif triglycerides >= 150:
        agreement = "The ratio agrees with the triglyceride signal."
        driver = "TyG appears primarily triglyceride-driven."
    elif glucose >= 100:
        agreement = "The ratio agrees with the fasting glucose signal."
        driver = "TyG appears primarily glucose-driven."
    elif tyg >= 8.5:
        agreement = "The result is mixed and should be interpreted with additional markers."
        driver = "TyG is elevated even though neither triglycerides nor glucose crosses an individual threshold; their combined product is still elevated relative to ideal."
    elif tyg >= 8.0:
        agreement = "The ratio is watchful even though the individual inputs are not frankly high."
        driver = "Small glucose differences such as 85 vs 88 usually do not materially change interpretation unless triglycerides are also elevated. Here, trend matters more than one point."
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "Triglycerides and glucose both support the favorable TyG category."

    render_metric_report(
        "TyG Index",
        [
            f"**TyG Index:** {tyg:.2f}",
            f"**Triglycerides:** {triglycerides} mg/dL ({tg_status})",
            f"**Fasting Glucose:** {glucose} mg/dL ({glucose_status})",
        ],
        category,
        meaning,
        [driver, "TyG is driven by the combination of triglycerides and glucose, not either number alone."],
        agreement,
        "Signal strength: TyG is a strong directional indicator of metabolic health and insulin resistance risk.",
        "TyG does not diagnose diabetes, measure insulin directly, or identify whether sleep, liver fat, diet, medication, or alcohol is the root cause.",
        [
            action,
            "Trend guidance: most useful when tracked over time alongside triglycerides, fasting glucose, A1C, waist, and fitness changes.",
            "Common scenario: a low-carb or keto profile may have good glucose but still needs triglycerides watched because TyG uses both values.",
        ],
        "TyG is inexpensive and actionable, but it is best used as a trend marker within the full metabolic picture.",
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
        meaning = "This ratio suggests a favorable balance between LDL-C burden and HDL-C support."
        action = "Maintain the pattern, but still compare it with ApoB, blood pressure, family history, and triglycerides."
    elif ldl_hdl < 2.5:
        category = "Good / near ideal"
        meaning = "This is near ideal, but risk can still differ depending on particle burden and overall context."
        action = "Keep trending LDL-C and HDL-C; consider ApoB if LDL-C is rising or family history is strong."
    elif ldl_hdl < 3.5:
        category = "Borderline / watchful"
        meaning = "The balance is drifting into a watch zone where LDL-C burden may be outpacing HDL-C support."
        action = "Identify whether LDL-C is rising, HDL-C is weak, or both are moving in the wrong direction."
    elif ldl_hdl < 5.0:
        category = "Elevated risk"
        meaning = "This points to a less favorable lipid balance and possible higher atherogenic burden."
        action = "Consider a fuller cardiovascular review, especially ApoB or LDL-P, inflammation markers, and blood pressure."
    else:
        category = "High risk"
        meaning = "This ratio is high and may reflect a substantially unfavorable LDL-C to HDL-C pattern."
        action = "Review this with a clinician, particularly if LDL-C is high, HDL-C is low, or family history is concerning."

    ldl_status = classify_ldl(ldl)
    hdl_status = classify_hdl(hdl)
    if ldl >= 130 and hdl < 40:
        agreement = "The ratio looks poor and the underlying drivers confirm concern."
        driver = "Both high LDL-C and low HDL-C are worsening the ratio."
    elif ldl >= 130 and hdl >= 60:
        agreement = "The result is mixed and should be interpreted with additional markers."
        driver = "High HDL-C is partially offsetting elevated LDL-C, but it does not erase LDL-related particle risk."
    elif ldl >= 130:
        agreement = "The ratio agrees with the LDL-C concern."
        driver = "The result appears primarily LDL-driven."
    elif ldl < 100 and hdl < 60:
        agreement = "The ratio looks decent, but one underlying driver is not ideal."
        driver = "LDL-C is favorable, but HDL-C is not strongly protective."
    elif hdl < 40:
        agreement = "The ratio is being pulled in the wrong direction by low HDL-C."
        driver = "Low HDL-C is the main driver."
    elif ldl_hdl >= 3.5:
        agreement = "The ratio looks poor even without one extreme value."
        driver = "The combined LDL-C and HDL-C balance is unfavorable and deserves more context."
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "LDL-C and HDL-C both support the current category."

    render_metric_report(
        "LDL/HDL Ratio",
        [
            f"**LDL/HDL Ratio:** {ldl_hdl:.2f}",
            f"**LDL-C:** {ldl} mg/dL ({ldl_status})",
            f"**HDL-C:** {hdl} mg/dL ({hdl_status})",
        ],
        category,
        meaning,
        [driver],
        agreement,
        "Signal strength: LDL/HDL is a directional cardiovascular signal, but ApoB and LDL-P are stronger for particle burden.",
        "LDL/HDL does not show ApoB, LDL-P, particle size, oxidation, CAC score, HDL function, or inflammatory risk.",
        [
            action,
            "Trend guidance: better as a trend with LDL-C, HDL-C, triglycerides, non-HDL cholesterol, and ApoB if available.",
            "Common scenario: an endurance athlete may have high HDL-C that improves the ratio while ApoB or LDL-P still matters if LDL-C is elevated.",
        ],
        "LDL/HDL is useful, but it does not replace ApoB, LDL-P, CAC score, or inflammatory markers.",
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
        meaning = "Total cholesterol is well balanced against HDL-C."
        action = "Maintain the pattern while checking whether LDL-C and triglycerides also agree."
    elif total_hdl < 5.0:
        category = "Moderate / watchful"
        meaning = "The ratio is moderate, so the entered LDL-C and triglycerides determine whether this is reassuring or mixed."
        action = "Use the full lipid panel, not total cholesterol alone, to decide how much attention this needs."
    elif total_hdl < 6.0:
        category = "Elevated risk"
        meaning = "The cholesterol balance is less favorable and may indicate increased cardiovascular risk."
        action = "Look for the driver: high total cholesterol, low HDL-C, elevated LDL-C, or elevated triglycerides."
    else:
        category = "High risk"
        meaning = "Total cholesterol is unfavorable relative to HDL-C."
        action = "Review this pattern with a clinician, especially if LDL-C, triglycerides, or blood pressure are also elevated."

    ldl_concerning = ldl is not None and ldl >= 130
    tg_concerning = triglycerides is not None and triglycerides >= 150
    if total_cholesterol >= 240 and hdl < 40:
        agreement = "The ratio looks poor and the underlying drivers confirm concern."
        driver = "High total cholesterol and low HDL-C are both worsening the ratio."
    elif total_cholesterol >= 240 and hdl >= 60:
        agreement = "The result is mixed and should be interpreted with additional markers."
        driver = "Favorable HDL-C is offsetting higher total cholesterol; LDL-C, triglycerides, ApoB, and non-HDL cholesterol decide whether that is reassuring."
    elif total_hdl < 5.0 and (ldl_concerning or tg_concerning):
        agreement = "The ratio looks acceptable, but underlying drivers are concerning."
        drivers = []
        if ldl_concerning:
            drivers.append("LDL-C is elevated")
        if tg_concerning:
            drivers.append("triglycerides are elevated")
        driver = f"This ratio is acceptable, but {' and '.join(drivers)}, which adds risk context despite the ratio."
    elif total_hdl >= 5.0 and (ldl_concerning or tg_concerning or hdl < 40):
        agreement = "The ratio looks poor and the underlying numbers support concern."
        driver = "The entered LDL-C, triglycerides, or HDL-C pattern reinforces the elevated ratio."
    elif hdl >= 60 and total_cholesterol >= 200:
        agreement = "The result is mixed and should be interpreted with additional markers."
        driver = "High HDL-C is helping offset higher total cholesterol. Total cholesterol alone can be misleading here."
    elif total_hdl >= 5.0:
        agreement = "The ratio looks poor even without a single obvious driver."
        driver = "The balance between total cholesterol and HDL-C is unfavorable enough to warrant full-panel review."
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "Total cholesterol and HDL-C are reasonably aligned with the category."

    contribution = []
    if ldl_concerning:
        contribution.append("LDL-C appears to contribute to atherogenic burden.")
    if tg_concerning:
        contribution.append("Triglycerides suggest possible metabolic stress or triglyceride-rich particle burden.")
    if not contribution:
        contribution.append("LDL-C and triglycerides do not stand out as obvious drivers in the entered values.")

    render_metric_report(
        "Total Cholesterol/HDL Ratio",
        [
            f"**Total Cholesterol/HDL Ratio:** {total_hdl:.2f}",
            f"**Total Cholesterol:** {total_cholesterol} mg/dL",
            f"**HDL-C:** {hdl} mg/dL ({classify_hdl(hdl)})",
        ],
        category,
        meaning,
        [driver, *contribution],
        agreement,
        "Signal strength: this is a broad directional signal. Total cholesterol alone can be misleading because it combines protective and atherogenic fractions.",
        "This ratio does not show ApoB, LDL-P, LDL particle size, inflammation, CAC score, or whether high total cholesterol is mostly HDL-C versus atherogenic particles.",
        [
            action,
            "Trend guidance: best tracked with LDL-C, HDL-C, triglycerides, non-HDL cholesterol, and ApoB when available.",
            "Common scenario: a low-carb or endurance profile may raise total cholesterol while HDL-C is strong; ApoB and triglycerides help separate benign from concerning patterns.",
        ],
        "Total Cholesterol/HDL adds context, but the full lipid pattern matters more than total cholesterol alone.",
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
        action = "Watch triglyceride trend, carbohydrate quality, alcohol intake, sleep, and waist changes."
    elif tg_hdl < 4.0:
        category = "Moderate metabolic risk"
        meaning = "This ratio suggests a more concerning metabolic pattern often linked with insulin resistance."
        action = "Prioritize triglyceride reduction, glucose control, and regular aerobic activity."
    else:
        category = "High metabolic risk"
        meaning = "This ratio is high and can be a strong warning sign for insulin resistance or metabolic syndrome risk."
        action = "Consider a focused metabolic review, especially if fasting glucose, A1C, waist, or blood pressure are also elevated."

    if triglycerides >= 150 and hdl < 40:
        agreement = "The ratio looks poor and the underlying drivers confirm concern."
        driver = "High triglycerides and low HDL-C are both worsening the ratio."
    elif triglycerides >= 150 and hdl >= 40:
        agreement = "The ratio agrees with the triglyceride concern."
        driver = "High triglycerides are driving the ratio despite acceptable HDL-C."
    elif triglycerides < 100 and hdl < 40:
        agreement = "The ratio may look mixed because one driver is favorable and one is weak."
        driver = "Triglycerides are favorable, but low HDL-C is weakening the ratio."
    elif hdl < 40:
        agreement = "The ratio is being pulled in the wrong direction by low HDL-C."
        driver = "Low HDL-C is the main driver."
    elif tg_hdl >= 3.0:
        agreement = "The ratio looks poor even without one extreme value."
        driver = "The combined triglyceride-HDL pattern is metabolically unfavorable and should be interpreted with glucose and waist trend."
    elif triglycerides >= 100 and hdl >= 60:
        agreement = "The result is mixed but partly offset."
        driver = "Higher HDL-C is helping offset triglycerides that are not fully ideal."
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "Low triglycerides and adequate HDL-C support the favorable category."

    if glucose is not None and glucose >= 100:
        glucose_note = "Fasting glucose is also elevated, which strengthens the insulin resistance signal."
    else:
        glucose_note = "Fasting glucose does not add an obvious warning signal, but this ratio can still reveal early metabolic stress."

    render_metric_report(
        "Triglycerides/HDL Ratio",
        [
            f"**Triglycerides/HDL Ratio:** {tg_hdl:.2f}",
            f"**Triglycerides:** {triglycerides} mg/dL ({classify_tg(triglycerides)})",
            f"**HDL-C:** {hdl} mg/dL ({classify_hdl(hdl)})",
        ],
        category,
        meaning,
        [driver, glucose_note],
        agreement,
        "Signal strength: triglycerides/HDL is a strong practical marker for insulin resistance risk and metabolic syndrome patterns.",
        "This ratio does not diagnose diabetes, measure insulin directly, show liver fat, or replace A1C, fasting insulin, waist, blood pressure, or clinical assessment.",
        [
            action,
            "Trend guidance: best tracked over time with triglycerides, HDL-C, fasting glucose, A1C, waist, and blood pressure.",
            "Common scenario: a high triglyceride metabolic profile often improves when refined carbohydrates, alcohol, excess calories, and inactivity are addressed.",
        ],
        "Triglycerides/HDL is one of the most useful simple ratios for metabolic health, but it should be read with glucose and the full lipid panel.",
    )


def main() -> None:
    initialize_session_state()

    if st.session_state.info_page is not None:
        show_info_page(st.session_state.info_page)
    else:
        render_calculator()


if __name__ == "__main__":
    main()


