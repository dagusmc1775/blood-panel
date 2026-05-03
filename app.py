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


REFERENCE_RANGES = {
    "tyg": "Reference: <8.0 favorable; 8.0-<8.5 watch zone; 8.5+ increasing insulin resistance risk.",
    "ldl_hdl": "Reference: <2.0 favorable; 2.0-<2.5 good; 2.5-<3.5 watchful; 3.5+ elevated.",
    "total_hdl": "Reference: <3.5 favorable; 3.5-<5.0 watchful; 5.0+ elevated.",
    "tg_hdl": "Reference: <2.0 favorable; 2.0-<3.0 watchful; 3.0+ elevated metabolic risk.",
    "hdl": "Reference: >39 mg/dL for men is generally better; >=60 is generally favorable/protective.",
    "ldl": "Reference: <100 mg/dL generally favorable; 100-129 near optimal/watchful; >=130 elevated; >=190 very high.",
    "triglycerides": "Reference: <150 mg/dL generally normal/favorable; >=150 elevated.",
    "glucose": "Reference: <100 mg/dL normal; 100-125 prediabetes range; >=126 diabetes-range threshold.",
    "apob": "Reference: <80 mg/dL favorable; 80-<100 watchful; 100-<130 elevated; >=130 high.",
    "hba1c": "Reference: <5.7% normal; 5.7-<6.5 prediabetes range; >=6.5 diabetes-range threshold.",
}


def severity_from_label(label: str) -> str:
    normalized = label.lower()
    if any(term in normalized for term in ("very high", "high risk", "high metabolic", "elevated risk", "elevated", "diabetes-range", "likely insulin resistance")):
        return "red"
    if any(term in normalized for term in ("watch", "borderline", "moderate", "near optimal", "mildly", "context")):
        return "yellow"
    return "green"


def write_status_line(message: str, severity: str) -> None:
    if severity == "red":
        st.error(message)
    elif severity == "yellow":
        st.warning(message)
    else:
        st.success(message)


def render_result_status(label: str, value: str, status: str, reference: str) -> None:
    write_status_line(f"{label}: {value} - {status}", severity_from_label(status))
    st.caption(reference)


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


def classify_tyg_value(tyg: float) -> str:
    if tyg < 8.0:
        return "Favorable / good insulin sensitivity"
    if tyg < 8.5:
        return "Watch zone"
    return "Elevated insulin resistance risk"


def classify_ldl_hdl_value(ldl_hdl: float) -> str:
    if ldl_hdl < 2.0:
        return "Favorable"
    if ldl_hdl < 2.5:
        return "Good"
    if ldl_hdl < 3.5:
        return "Watchful"
    return "Elevated risk"


def classify_total_hdl_value(total_hdl: float) -> str:
    if total_hdl < 3.5:
        return "Favorable"
    if total_hdl < 5.0:
        return "Watchful"
    return "Elevated risk"


def classify_tg_hdl_value(tg_hdl: float) -> str:
    if tg_hdl < 2.0:
        return "Favorable / good insulin sensitivity"
    if tg_hdl < 3.0:
        return "Watchful"
    return "Elevated metabolic risk"


def render_calculator() -> None:
    st.title("Blood Panel Calculator")

    total_cholesterol = render_number_input("Total Cholesterol", "total_cholesterol")
    ldl = render_number_input("LDL-C", "ldl")
    hdl = render_number_input("HDL-C", "hdl")
    triglycerides = render_number_input("Triglycerides", "triglycerides")
    glucose = render_number_input("Fasting Glucose", "glucose")

    st.subheader("Optional Lab Inputs")
    st.caption("Leave these at 0 if ApoB or HbA1c were not included on your lab report.")
    apob = render_number_input(
        "ApoB (mg/dL, optional)",
        "apob",
        help_text="ApoB estimates atherogenic particle number. Leave at 0 if it was not tested.",
    )
    hba1c = render_number_input(
        "HbA1c (%, optional)",
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
        render_result_status(
            "TyG Index",
            f"{st.session_state.tyg:.2f}",
            classify_tyg_value(st.session_state.tyg),
            REFERENCE_RANGES["tyg"],
        )
        render_result_status(
            "LDL/HDL Ratio",
            f"{st.session_state.ldl_hdl:.2f}",
            classify_ldl_hdl_value(st.session_state.ldl_hdl),
            REFERENCE_RANGES["ldl_hdl"],
        )
        render_result_status(
            "Total Cholesterol/HDL Ratio",
            f"{st.session_state.total_hdl:.2f}",
            classify_total_hdl_value(st.session_state.total_hdl),
            REFERENCE_RANGES["total_hdl"],
        )
        render_result_status(
            "Triglycerides/HDL Ratio",
            f"{st.session_state.tg_hdl:.2f}",
            classify_tg_hdl_value(st.session_state.tg_hdl),
            REFERENCE_RANGES["tg_hdl"],
        )

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


def write_lines(lines: list[str | dict[str, str]]) -> None:
    for line in lines:
        if isinstance(line, dict):
            render_result_status(line["label"], line["value"], line["status"], line["reference"])
            continue
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
    optional_marker_lines: list[str] | None = None,
) -> None:
    st.header(header)
    st.caption("Key terms such as atherogenic burden, metabolic stress, insulin resistance, ApoB, LDL-P, CAC score, and non-HDL cholesterol are defined in the expanders below.")
    st.subheader("Your Result")
    write_lines(result_lines)
    st.subheader("Category")
    write_status_line(category, severity_from_label(category))
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
    if optional_marker_lines:
        st.subheader("Additional context from ApoB and HbA1c")
        write_lines(optional_marker_lines)
    st.caption("This tool is for education and trend awareness. It does not diagnose disease or replace medical advice.")
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


def classify_apob(apob: float) -> str:
    if apob < 80:
        return "favorable"
    if apob < 100:
        return "moderate / watchful"
    if apob < 130:
        return "elevated"
    return "high"


def classify_hba1c(hba1c: float) -> str:
    if hba1c < 5.7:
        return "normal range"
    if hba1c < 6.5:
        return "prediabetes range"
    return "diabetes-range threshold"


def get_apob_context(ldl: float | None) -> list[str]:
    apob = st.session_state.get("calc_apob", None)
    if apob is None:
        return ["ApoB was not provided. ApoB or LDL-P/NMR can better estimate atherogenic particle burden; LDL-C and non-HDL cholesterol are indirect markers."]

    lines = [f"ApoB: {apob:.1f} mg/dL ({classify_apob(apob)}). {REFERENCE_RANGES['apob']}"]
    if ldl is not None and ldl < 130 and apob >= 100:
        lines.append(
            "Your LDL-C does not look severely elevated, but ApoB suggests the number of atherogenic particles may be higher than LDL-C alone implies. "
            "In plain terms, LDL-C estimates how much cholesterol is being carried, while ApoB better estimates how many cholesterol-carrying particles are present."
        )
    elif ldl is not None and ldl >= 130 and apob < 80:
        lines.append(
            "If LDL-C is high but ApoB is favorable, LDL-C may overstate particle burden compared with ApoB. "
            "That does not make LDL-C irrelevant, but it makes the risk picture more nuanced."
        )
    elif ldl is not None and ldl >= 130 and apob >= 100:
        lines.append("Both LDL-C and ApoB are elevated, so atherogenic burden is more strongly supported.")
    else:
        lines.append("ApoB refines the lipid interpretation but does not override the ratio category.")
    lines.append("For ApoB, generally lower is better; clinician review is especially useful when ApoB and LDL-C disagree.")
    return lines


def get_hba1c_context(ratio_elevated: bool, glucose: float | None) -> list[str]:
    hba1c = st.session_state.get("calc_hba1c", None)
    if hba1c is None:
        return ["HbA1c was not provided; HbA1c can provide longer-term glucose context. Fasting glucose, triglycerides, TyG, and TG/HDL are being used as proxy markers."]

    lines = [f"HbA1c: {hba1c:.1f}% ({classify_hba1c(hba1c)}). {REFERENCE_RANGES['hba1c']}"]
    hba1c_elevated = hba1c >= 5.7
    if ratio_elevated and not hba1c_elevated:
        lines.append("The ratio is elevated while HbA1c is normal. This may indicate early metabolic risk that has not yet shown up in longer-term glucose control.")
    elif ratio_elevated and hba1c_elevated:
        lines.append("Both the short-term/proxy ratio and longer-term HbA1c point toward metabolic dysfunction.")
    elif glucose is not None and glucose < 100 and hba1c_elevated:
        lines.append("Fasting glucose is normal, but HbA1c is elevated. Glucose control may be worse over time than the fasting snapshot suggests.")
    else:
        lines.append("HbA1c refines the metabolic interpretation but does not override the ratio category.")
    lines.append("For HbA1c, generally lower is better unless it is already very low or a clinician says a lower target is inappropriate.")
    return lines


def get_apob_marker_display() -> list[str]:
    apob = st.session_state.get("calc_apob", None)
    if apob is None:
        return []
    return [f"ApoB: {apob:.1f} mg/dL. {REFERENCE_RANGES['apob']}"]


def get_hba1c_marker_display() -> list[str]:
    hba1c = st.session_state.get("calc_hba1c", None)
    if hba1c is None:
        return []
    return [f"HbA1c: {hba1c:.1f}%. {REFERENCE_RANGES['hba1c']}"]


def show_tyg_page() -> None:
    tyg = st.session_state.get("tyg", None)
    triglycerides = st.session_state.get("calc_triglycerides", None)
    glucose = st.session_state.get("calc_glucose", None)

    if tyg is None or triglycerides is None or glucose is None:
        st.header("TyG Index")
        st.warning("No TyG result is available yet. Return to the calculator and run your blood panel first.")
        return

    if tyg < 8.0:
        category = "Favorable / good insulin sensitivity"
        meaning = "This is a favorable TyG pattern and generally fits lower insulin resistance risk. Good insulin sensitivity is a positive metabolic sign."
        action = "Keep the favorable pieces in place with good diet quality, regular aerobic exercise, resistance training, sleep quality, and weight or waist management when relevant."
    elif tyg < 8.5:
        category = "Watch zone"
        meaning = "This is an early watch zone. The combined triglyceride-glucose product is starting to rise."
        action = "Look for small improvements in triglycerides, fasting glucose, sleep, alcohol intake, exercise consistency, and carbohydrate quality."
    elif tyg < 9.0:
        category = "Elevated insulin resistance risk"
        meaning = "This range commonly aligns with higher insulin resistance risk or metabolic stress."
        action = "Prioritize diet quality, reducing refined carbohydrates and added sugars when triglycerides or glucose are high, regular aerobic exercise, resistance training, sleep quality, and waist trend."
    elif tyg < 9.5:
        category = "High risk"
        meaning = "This is a stronger metabolic risk signal and is worth reviewing in context."
        action = "Consider clinician review and a fuller metabolic workup, especially HbA1c, fasting insulin, liver markers, blood pressure, and waist trend."
    else:
        category = "Very high risk"
        meaning = "This is a very strong signal for metabolic dysfunction risk and deserves follow-up."
        action = "Review this with a clinician and consider deeper cardiometabolic testing."

    tg_status = classify_tg(triglycerides)
    glucose_status = classify_glucose(glucose)
    if triglycerides >= 150 and glucose >= 100:
        agreement = "The ratio looks unfavorable and the underlying numbers confirm concern."
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
        agreement = "The ratio is mildly watchful because the combined pattern is not ideal, even though no single required input is severely abnormal."
        driver = (
            "Your individual triglyceride and glucose values are not high, but the combined TyG calculation is close enough to the watch zone that it is worth trending. "
            "This is not a diagnosis or a red flag by itself."
        )
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "Triglycerides and glucose both support the favorable TyG category."

    render_metric_report(
        "TyG Index",
        [
            {"label": "TyG Index", "value": f"{tyg:.2f}", "status": category, "reference": REFERENCE_RANGES["tyg"]},
            {"label": "Triglycerides", "value": f"{triglycerides} mg/dL", "status": tg_status, "reference": REFERENCE_RANGES["triglycerides"]},
            {"label": "Fasting Glucose", "value": f"{glucose} mg/dL", "status": glucose_status, "reference": REFERENCE_RANGES["glucose"]},
        ],
        category,
        meaning,
        [driver, "TyG is driven by the combination of triglycerides and glucose, not either number alone.", *get_hba1c_context(tyg >= 8.5, glucose)],
        agreement,
        "TyG is a strong directional indicator of metabolic health and insulin resistance risk, and generally lower is better.",
        "TyG does not diagnose diabetes, measure insulin directly, or identify the root cause. Missing information can be checked with HbA1c and/or CGM for glucose control over time, fasting insulin, HOMA-IR, OGTT, or clinician-directed testing for insulin resistance, and liver enzymes plus imaging such as ultrasound, FibroScan, MRI-PDFF, or clinician-directed evaluation when liver fat is a concern.",
        [
            action,
            "Tracking means comparing repeat lab panels over time, ideally using the same lab and similar fasting conditions. For TyG, generally lower is better.",
            "On low-carb or keto diets, fasting glucose may look good while triglycerides still determine much of the TyG result. That is why both values should be reviewed together.",
        ],
        "TyG uses standard bloodwork values, so it is easy to calculate from labs many people already have. It is useful because changes in triglycerides and fasting glucose can often be improved through diet, exercise, sleep, weight management, and metabolic health interventions.",
        get_hba1c_marker_display(),
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
        action = "Keep the favorable pieces in place, but watch whether ApoB, triglycerides, blood pressure, or glucose markers move in the wrong direction on future labs."
    elif ldl_hdl < 2.5:
        category = "Good / near ideal"
        meaning = "This is near ideal, but risk can still differ depending on particle burden and overall context."
        action = "Keep trending LDL-C and HDL-C; consider clinician review or ApoB if LDL-C is rising, family history is strong, or other risk markers are present."
    elif ldl_hdl < 3.5:
        category = "Borderline / watchful"
        meaning = "The balance is drifting into a watch zone where LDL-C burden may be outpacing HDL-C support."
        action = "Identify whether LDL-C is rising, HDL-C is weak, or both are moving in the wrong direction."
    elif ldl_hdl < 5.0:
        category = "Elevated risk"
        meaning = "This points to a less favorable lipid balance and possible higher atherogenic burden."
        action = "Consider clinician review and fuller cardiovascular context, especially ApoB or LDL-P, hs-CRP, blood pressure, glucose control, and personal risk factors."
    else:
        category = "High risk"
        meaning = "This ratio is high and may reflect a substantially unfavorable LDL-C to HDL-C pattern."
        action = "Review this with a clinician, particularly if LDL-C is high, HDL-C is low, or family history is concerning."

    ldl_status = classify_ldl(ldl)
    hdl_status = classify_hdl(hdl)
    if ldl >= 130 and hdl < 40:
        agreement = "The ratio looks unfavorable and the underlying drivers confirm concern."
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
        agreement = "The ratio looks unfavorable even without one extreme value."
        driver = "The combined LDL-C and HDL-C balance is unfavorable and deserves more context."
    else:
        agreement = "The ratio agrees with the underlying numbers."
        driver = "LDL-C and HDL-C both support the current category."

    render_metric_report(
        "LDL/HDL Ratio",
        [
            {"label": "LDL/HDL Ratio", "value": f"{ldl_hdl:.2f}", "status": category, "reference": REFERENCE_RANGES["ldl_hdl"]},
            {"label": "LDL-C", "value": f"{ldl} mg/dL", "status": ldl_status, "reference": REFERENCE_RANGES["ldl"]},
            {"label": "HDL-C", "value": f"{hdl} mg/dL", "status": hdl_status, "reference": REFERENCE_RANGES["hdl"]},
        ],
        category,
        meaning,
        [driver, *get_apob_context(ldl)],
        agreement,
        "LDL/HDL is a directional cardiovascular signal, and generally lower is better, but ApoB and LDL-P are stronger for particle burden.",
        "LDL/HDL does not show particle burden, artery plaque burden, HDL function, or inflammatory risk. Missing information can be checked with ApoB or LDL-P/NMR for particle burden, CAC score for calcified artery plaque burden, and hs-CRP for inflammation.",
        [
            action,
            "Tracking means comparing repeat lab panels over time, ideally using the same lab and similar fasting conditions. For LDL/HDL, generally lower is better.",
            "An endurance athlete may have high HDL-C that improves the ratio while ApoB or LDL-P still matters if LDL-C is elevated.",
        ],
        "Use this ratio as a quick screen, but make decisions from the full pattern: LDL-C, HDL-C, triglycerides, non-HDL cholesterol, ApoB if available, blood pressure, glucose control, and personal risk factors.",
        get_apob_marker_display(),
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
        action = "Keep the favorable pieces in place while checking whether LDL-C, triglycerides, ApoB, blood pressure, and glucose markers also agree."
    elif total_hdl < 5.0:
        category = "Moderate / watchful"
        meaning = "The ratio is moderate, so the entered LDL-C and triglycerides determine whether this is reassuring or mixed."
        action = "Use the full lipid panel, not total cholesterol alone, to decide how much attention this needs. Diet quality, exercise, sleep, waist trend, and alcohol moderation can matter when triglycerides or glucose are moving higher."
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
        agreement = "The ratio looks unfavorable and the underlying drivers confirm concern."
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
        agreement = "The ratio looks unfavorable and the underlying numbers support concern."
        driver = "The entered LDL-C, triglycerides, or HDL-C pattern reinforces the elevated ratio."
    elif hdl >= 60 and total_cholesterol >= 200:
        agreement = "The result is mixed and should be interpreted with additional markers."
        driver = "High HDL-C is helping offset higher total cholesterol. Total cholesterol alone can be misleading here."
    elif total_hdl >= 5.0:
        agreement = "The ratio looks unfavorable even without a single obvious driver."
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
            {"label": "Total Cholesterol/HDL Ratio", "value": f"{total_hdl:.2f}", "status": category, "reference": REFERENCE_RANGES["total_hdl"]},
            {"label": "Total Cholesterol", "value": f"{total_cholesterol} mg/dL", "status": "See full lipid pattern", "reference": "No single total cholesterol range is used here; interpret it with LDL-C, HDL-C, triglycerides, non-HDL cholesterol, and ApoB if available."},
            {"label": "HDL-C", "value": f"{hdl} mg/dL", "status": classify_hdl(hdl), "reference": REFERENCE_RANGES["hdl"]},
        ],
        category,
        meaning,
        [driver, *contribution, *get_apob_context(ldl)],
        agreement,
        "This ratio is useful for spotting patterns, but it should be interpreted alongside the underlying lab values and other risk markers. Total cholesterol alone can be misleading because it combines protective and atherogenic fractions.",
        "This ratio does not show particle burden, inflammation, artery plaque burden, or whether high total cholesterol is mostly HDL-C versus atherogenic particles. Missing information can be checked with ApoB or LDL-P/NMR for particle burden, hs-CRP for inflammation, CAC score for calcified artery plaque burden, and the full lipid panel including non-HDL cholesterol.",
        [
            action,
            "Tracking means comparing repeat lab panels over time, ideally using the same lab and similar fasting conditions. For Total Cholesterol/HDL, generally lower is better.",
            "A low-carb or endurance profile may raise total cholesterol while HDL-C is strong; ApoB and triglycerides help separate more reassuring from more concerning patterns.",
        ],
        "Use this ratio as a quick screen, but make decisions from the full pattern: LDL-C, HDL-C, triglycerides, non-HDL cholesterol, ApoB if available, blood pressure, glucose control, and personal risk factors.",
        get_apob_marker_display(),
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
        category = "Favorable / good insulin sensitivity"
        meaning = "This pattern is generally favorable and often aligns with better insulin sensitivity, which is a positive metabolic sign."
        action = "Keep the habits supporting low triglycerides and adequate HDL-C, including diet quality, regular aerobic exercise, resistance training, sleep quality, and weight or waist management when relevant."
    elif tg_hdl < 3.0:
        category = "Mildly watchful"
        meaning = "This is a mild watch zone where metabolic risk may be starting to rise."
        action = "Watch triglyceride trend, carbohydrate quality, added sugars, alcohol intake, sleep, exercise consistency, and waist changes."
    elif tg_hdl < 4.0:
        category = "Moderate metabolic risk"
        meaning = "This ratio suggests a more concerning metabolic pattern often linked with insulin resistance."
        action = "Prioritize diet quality, reducing refined carbohydrates and added sugars when triglycerides or glucose are high, alcohol moderation when triglycerides are elevated, regular aerobic activity, resistance training, sleep quality, and waist trend."
    else:
        category = "High metabolic risk"
        meaning = "This ratio is high and can be a strong warning sign for insulin resistance or metabolic syndrome risk."
        action = "Consider a focused metabolic review, especially if fasting glucose, HbA1c, waist, or blood pressure are also elevated."

    if triglycerides >= 150 and hdl < 40:
        agreement = "The ratio looks unfavorable and the underlying drivers confirm concern."
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
        agreement = "The ratio looks unfavorable even without one extreme value."
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
            {"label": "Triglycerides/HDL Ratio", "value": f"{tg_hdl:.2f}", "status": category, "reference": REFERENCE_RANGES["tg_hdl"]},
            {"label": "Triglycerides", "value": f"{triglycerides} mg/dL", "status": classify_tg(triglycerides), "reference": REFERENCE_RANGES["triglycerides"]},
            {"label": "HDL-C", "value": f"{hdl} mg/dL", "status": classify_hdl(hdl), "reference": REFERENCE_RANGES["hdl"]},
        ],
        category,
        meaning,
        [driver, glucose_note, *get_hba1c_context(tg_hdl >= 3.0, glucose)],
        agreement,
        "Triglycerides/HDL is a strong practical marker for insulin resistance risk and metabolic syndrome patterns, and generally lower is better.",
        "This ratio does not diagnose diabetes, measure insulin directly, show glucose control over time, or measure liver fat. Missing information can be checked with HbA1c and/or CGM for glucose control over time, fasting insulin, HOMA-IR, OGTT, or clinician-directed testing for insulin resistance, and liver enzymes plus imaging such as ultrasound, FibroScan, MRI-PDFF, or clinician-directed evaluation when liver fat or steatosis is a concern.",
        [
            action,
            "Tracking means comparing repeat lab panels over time, ideally using the same lab and similar fasting conditions. For Triglycerides/HDL, generally lower is better; HDL-C is generally better higher, within reason.",
            "A high triglyceride metabolic profile often improves when refined carbohydrates, added sugars, alcohol, excess calories, sleep issues, and inactivity are addressed.",
        ],
        "Triglycerides/HDL is one of the most useful simple ratios for metabolic health, but it should be read with glucose and the full lipid panel.",
        get_hba1c_marker_display(),
    )


def main() -> None:
    initialize_session_state()

    if st.session_state.info_page is not None:
        show_info_page(st.session_state.info_page)
    else:
        render_calculator()


if __name__ == "__main__":
    main()





