import streamlit as st
import requests
import plotly.graph_objects as go
import numpy as np
import datetime

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwQwu4I2VyAVYLWCkowgghNGN1HEqA4-qzK1d19MzelOH5TRxWlFSYlVdeGhrb3futT/exec"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Student Dropout Risk System",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Dropout Risk Assessment System")
st.caption(
    "Rule-based early warning decision support system derived from machine learning factor analysis"
)

st.markdown("---")

# --------------------------------------------------
# BASIC INFORMATION
# --------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Female", "Male"])
with col2:
    level = st.selectbox("Level of Study", ["Undergraduate", "Graduate"])

st.markdown("### Please rate the following factors (1 = Low, 5 = High)")

# --------------------------------------------------
# FACTOR INPUTS
# --------------------------------------------------
financial = st.slider("💰 Financial Stress", 1, 5, 3)
psychological = st.slider("🧠 Psychological Stress", 1, 5, 3)
social = st.slider("👥 Social Challenges", 1, 5, 3)
institutional = st.slider("🏫 Institutional Issues", 1, 5, 3)

st.markdown("---")

# --------------------------------------------------
# SUBMIT BUTTON
# --------------------------------------------------
if st.button("🔍 Assess Dropout Risk"):

    # ---------------- Risk Calculation ----------------
    risk_score = (
        0.40 * financial +
        0.30 * psychological +
        0.20 * social +
        0.10 * institutional
    )

    risk_score_normalized = risk_score / 5

    if risk_score_normalized < 0.40:
        risk_label = "Low Risk"
        color = "green"
    elif risk_score_normalized < 0.70:
        risk_label = "Medium Risk"
        color = "orange"
    else:
        risk_label = "High Risk"
        color = "red"

    # ---------------- Display Result ----------------
    st.subheader("📊 Risk Assessment Result")
    st.markdown(
        f"**Risk Level:** <span style='color:{color}; font-weight:bold'>{risk_label}</span>",
        unsafe_allow_html=True
    )
    st.write(f"**Risk Score:** {risk_score_normalized:.2f}")

    # ---------------- Gauge ----------------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score_normalized * 100,
        title={'text': "Dropout Risk (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': 'lightgreen'},
                {'range': [40, 70], 'color': 'gold'},
                {'range': [70, 100], 'color': 'salmon'}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Dominant Factors ----------------
    st.subheader("🔎 Dominant Contributing Factors")
    factors = {
        "Financial": financial,
        "Psychological": psychological,
        "Social": social,
        "Institutional": institutional
    }
    sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)

    for factor, score in sorted_factors:
        st.write(f"- **{factor} Factor** (Score: {score})")

    # ---------------- Recommendations ----------------
    st.subheader("✅ Recommended Support Actions")
    top_factor = sorted_factors[0][0]

    if top_factor == "Financial":
        st.write("- Fee installment plans")
        st.write("- Emergency financial aid or scholarships")
        st.write("- Part-time work opportunities")
    elif top_factor == "Psychological":
        st.write("- Academic and mental health counseling")
        st.write("- Stress management workshops")
        st.write("- Faculty mentoring")
    elif top_factor == "Social":
        st.write("- Peer mentoring programs")
        st.write("- Family engagement initiatives")
        st.write("- Student support groups")
    else:
        st.write("- Institutional advising services")
        st.write("- Academic policy flexibility")
        st.write("- Administrative support")

    st.info(
        "Note: This system provides early-warning risk assessment based on dominant factors. "
        "It does not claim deterministic prediction."
    )

    # --------------------------------------------------
    # SAVE DATA TO GOOGLE SHEET (IMPORTANT PART)
    # --------------------------------------------------
    payload = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gender": gender,
        "level": level,
        "financial": financial,
        "psychological": psychological,
        "social": social,
        "institutional": institutional,
        "risk_score": round(risk_score_normalized, 2),
        "risk_label": risk_label
    }

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
        if response.status_code == 200:
            st.success("✅ Data saved successfully to Google Sheet")
        else:
            st.error("❌ Failed to save data to Google Sheet")
    except Exception as e:
        st.error(f"Error: {e}")
