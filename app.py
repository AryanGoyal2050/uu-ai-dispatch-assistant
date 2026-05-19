import streamlit as st
import pandas as pd
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="United Utilities AI Dispatch Assistant",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# MINIMAL ACCENTURE STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #050816;
    }

    /* Top bar */
    header {
        background-color: #0B1023 !important;
    }

    [data-testid="stToolbar"] {
        background-color: #0B1023 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161A2D;
        border-right: 1px solid #2B2F45;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Purple headings */
    h1, h2, h3 {
        color: #A855F7 !important;
    }

    /* Divider */
    hr {
        border-color: #7C3AED !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #680BD3, #8B5CF6);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #7C3AED, #A855F7);
        color: white !important;
    }

    /* Selectboxes */
    div[data-baseweb="select"] > div {
        background-color: #0B1023 !important;
        border: 1px solid #2E344D !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    div[data-baseweb="select"] svg {
        fill: #A855F7 !important;
    }

    /* Dropdown options */
    ul {
        background-color: #111827 !important;
    }

    li {
        background-color: #111827 !important;
        color: white !important;
    }

    li:hover {
        background-color: #312E81 !important;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #0B1023;
        border: 1px solid #272C45;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 0 12px rgba(104,11,211,0.12);
    }

    /* Metric labels */
    div[data-testid="metric-container"] label {
        color: #B8C1EC !important;
    }

    /* Metric values */
    div[data-testid="metric-container"] div {
        color: white !important;
    }

    /* Sliders */
    .stSlider * {
        color: white !important;
    }

    /* Success box */
    .stSuccess {
        background-color: rgba(34,197,94,0.15) !important;
        color: #86EFAC !important;
        border-radius: 12px;
    }

    .stSuccess * {
        color: #86EFAC !important;
    }

    /* Warning box */
    .stWarning {
        background-color: rgba(250,204,21,0.15) !important;
        color: #FDE68A !important;
        border-radius: 12px;
    }

    .stWarning * {
        color: #FDE68A !important;
    }

    /* Error box */
    .stError {
        background-color: rgba(239,68,68,0.15) !important;
        color: #FCA5A5 !important;
        border-radius: 12px;
    }

    .stError * {
        color: #FCA5A5 !important;
    }

    /* Recommendations text */
    p, li {
        color: #E5E7EB;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load("exception_prediction_model.pkl")

# =========================================================
# TITLE
# =========================================================

st.title("⚡ United Utilities AI Dispatch Assistant")

st.markdown(
    "AI-Powered SLA & Exception Risk Prediction System"
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Job Input Details")

# =========================================================
# INPUTS
# =========================================================

postcode = st.sidebar.selectbox(
    "Postcode",
    [
        "PC01", "PC02", "PC03", "PC04", "PC05",
        "PC06", "PC07", "PC08", "PC09", "PC10",
        "PC11", "PC12", "PC13", "PC14", "PC15"
    ]
)

phone_available = st.sidebar.selectbox(
    "Phone Available",
    [True, False]
)

email_available = st.sidebar.selectbox(
    "Email Available",
    [True, False]
)

preferred_contact = st.sidebar.selectbox(
    "Preferred Contact",
    ["Call", "SMS", "Email", "Mail"]
)

past_no_contact_count = st.sidebar.slider(
    "Past No Contact Count",
    0,
    5,
    0
)

past_no_access_count = st.sidebar.slider(
    "Past No Access Count",
    0,
    5,
    0
)

total_contact_attempts = st.sidebar.slider(
    "Total Contact Attempts",
    1,
    10,
    2
)

field_visit_attempts = st.sidebar.slider(
    "Field Visit Attempts",
    0,
    5,
    0
)

cancellation_before_visit = st.sidebar.selectbox(
    "Cancellation Before Visit",
    [True, False]
)

appointment_slot = st.sidebar.selectbox(
    "Appointment Slot",
    ["Morning", "Afternoon", "Evening"]
)

days_between_booking_and_visit = st.sidebar.slider(
    "Days Between Booking & Visit",
    1,
    30,
    5
)

reschedule_count = st.sidebar.slider(
    "Reschedule Count",
    0,
    5,
    0
)

property_type = st.sidebar.selectbox(
    "Property Type",
    ["House", "Apartment", "Commercial"]
)

shared_access = st.sidebar.selectbox(
    "Shared Access",
    [True, False]
)

meter_location_current = st.sidebar.selectbox(
    "Current Meter Location",
    ["Internal", "External"]
)

meter_location_target = st.sidebar.selectbox(
    "Target Meter Location",
    ["Internal", "External"]
)

# =========================================================
# ANALYZE BUTTON IN SIDEBAR
# =========================================================

st.sidebar.markdown("---")

analyze_button = st.sidebar.button(
    "⚡ Analyze Job",
    use_container_width=True
)

# =========================================================
# CREATE INPUT DATAFRAME
# =========================================================

input_data = pd.DataFrame({
    "postcode": [postcode],
    "phone_available": [phone_available],
    "email_available": [email_available],
    "preferred_contact": [preferred_contact],
    "past_no_contact_count": [past_no_contact_count],
    "past_no_access_count": [past_no_access_count],
    "total_contact_attempts": [total_contact_attempts],
    "field_visit_attempts": [field_visit_attempts],
    "cancellation_before_visit": [cancellation_before_visit],
    "appointment_slot": [appointment_slot],
    "days_between_booking_and_visit": [days_between_booking_and_visit],
    "reschedule_count": [reschedule_count],
    "property_type": [property_type],
    "shared_access": [shared_access],
    "meter_location_current": [meter_location_current],
    "meter_location_target": [meter_location_target]
})

# =========================================================
# PREDICTIONS
# =========================================================

if analyze_button:

    probabilities = model.predict_proba(input_data)

    no_contact_prob = round(probabilities[0][:, 1][0] * 100, 2)
    no_access_prob = round(probabilities[1][:, 1][0] * 100, 2)
    dig_prob = round(probabilities[2][:, 1][0] * 100, 2)
    survey_prob = round(probabilities[3][:, 1][0] * 100, 2)

    # =====================================================
    # SLA CALCULATION
    # =====================================================

    BASE_SLA = 5

    expected_delay = (
        (no_contact_prob / 100) * 1.5 +
        (no_access_prob / 100) * 2.5 +
        (dig_prob / 100) * 6 +
        (survey_prob / 100) * 3
    )

    expected_sla = round(BASE_SLA + expected_delay, 2)

    overall_risk = round(
        (
            no_contact_prob +
            no_access_prob +
            dig_prob +
            survey_prob
        ) / 4,
        2
    )

    # =====================================================
    # RISK CATEGORY
    # =====================================================

    if expected_sla <= 7:
        risk_category = "Low Risk"

    elif expected_sla <= 10:
        risk_category = "Medium Risk"

    else:
        risk_category = "High Risk"

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    st.header("AI Prediction Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "No Contact Risk",
        f"{no_contact_prob}%"
    )

    col2.metric(
        "No Access Risk",
        f"{no_access_prob}%"
    )

    col3.metric(
        "Dig Risk",
        f"{dig_prob}%"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Survey Risk",
        f"{survey_prob}%"
    )

    col5.metric(
        "Expected SLA",
        f"{expected_sla} days"
    )

    col6.metric(
        "Overall Risk",
        f"{overall_risk}%"
    )

    # =====================================================
    # RISK CLASSIFICATION
    # =====================================================

    st.subheader("Risk Classification")

    if risk_category == "Low Risk":
        st.success(risk_category)

    elif risk_category == "Medium Risk":
        st.warning(risk_category)

    else:
        st.error(risk_category)

    # =====================================================
    # OPERATIONAL RECOMMENDATIONS
    # =====================================================

    st.subheader("Operational Recommendations")

    recommendations = []

    if no_contact_prob > 20:
        recommendations.append(
            "📞 Proactively contact customer before dispatch."
        )

    if no_access_prob > 20:
        recommendations.append(
            "🔑 Verify site/building access before visit."
        )

    if dig_prob > 15:
        recommendations.append(
            "🚧 Allocate specialist crew for possible dig work."
        )

    if survey_prob > 15:
        recommendations.append(
            "📋 Consider pre-visit technical survey."
        )

    if expected_sla > 10:
        recommendations.append(
            "⚠️ Add scheduling buffer due to elevated operational risk."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "✅ Standard dispatch recommended."
        )

    for rec in recommendations:
        st.write(rec)

