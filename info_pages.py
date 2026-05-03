import streamlit as st


def show_info_page(page_key):
    if page_key == "tyg":
    tyg = st.session_state.get("tyg", None)
    triglycerides = st.session_state.get("triglycerides", None)
    glucose = st.session_state.get("glucose", None)

    st.header("TyG Index")

    if tyg is None:
        st.warning("No TyG result is available yet. Return to the calculator and run your blood panel first.")
    else:
        st.subheader(f"Your TyG Index: {tyg:.2f}")

        if tyg < 8.0:
            category = "Excellent / metabolically favorable"
            meaning = """
            Your TyG Index is in a favorable range. This generally suggests better insulin sensitivity
            and lower triglyceride-glucose burden.
            """
            action = """
            Keep doing what is working. This is a good marker to trend over time, especially if you are
            changing diet, training volume, body weight, or carbohydrate intake.
            """

        elif tyg < 8.5:
            category = "Good / mildly watchful"
            meaning = """
            Your TyG Index is still relatively favorable, but it is getting closer to the range where
            insulin resistance risk becomes more relevant.
            """
            action = """
            This is a useful range to monitor. Improvements may come from lowering triglycerides,
            improving fasting glucose, reducing processed carbohydrates, improving sleep, and maintaining
            regular aerobic training.
            """

        elif tyg < 9.0:
            category = "Moderate insulin resistance risk"
            meaning = """
            Your TyG Index is in a range commonly associated with increased insulin resistance risk.
            This does not diagnose insulin resistance by itself, but it suggests your triglycerides and
            fasting glucose together deserve attention.
            """
            action = """
            This is where TyG becomes especially useful as a trend marker. Diet quality, carbohydrate
            tolerance, fasting glucose, triglycerides, waist size, blood pressure, A1C, and possibly fasting
            insulin are worth watching together.
            """

        else:
            category = "High insulin resistance risk"
            meaning = """
            Your TyG Index is elevated. Higher TyG values are commonly associated with insulin resistance,
            metabolic syndrome risk, fatty liver risk, and higher cardiometabolic risk.
            """
            action = """
            This is worth discussing with your clinician, especially if A1C, fasting glucose, triglycerides,
            blood pressure, waist size, or liver enzymes are also elevated.
            """

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

    If your goal is long-term performance, cardiovascular health, and metabolic resilience,
    TyG can provide insight that A1C alone may miss.
    """)

    st.caption(
        "TyG is a screening and trend marker, not a standalone diagnosis. Interpretation depends on the full clinical picture."
    )
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
