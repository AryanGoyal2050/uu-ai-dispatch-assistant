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

def render_risk_card(
    title,
    probability,
    sla_impact,
    risk_level,
    risk_color,
    reasons,
    actions
):
    details_section = ""

    if risk_level in ["HIGH", "MEDIUM"]:

        details_section = f"""

        <p style="
        color:#A855F7;
        font-size:22px;
        font-weight:700;
        margin-top:10px;
        margin-bottom:14px;
        ">
        Possible Reasons
        </p>

        <ul style="
        color:#D1D5DB;
        font-size:18px;
        line-height:1.8;
        padding-left:22px;
        margin-bottom:28px;
        ">
        {''.join([f"<li>{r}</li>" for r in reasons])}
        </ul>

        <p style="
        color:#A855F7;
        font-size:22px;
        font-weight:700;
        margin-bottom:14px;
        ">
        Recommended Actions
        </p>

        <ul style="
        color:#D1D5DB;
        font-size:18px;
        line-height:1.8;
        padding-left:22px;
        ">
        {''.join([f"<li>{a}</li>" for a in actions])}
        </ul>

        """

    st.markdown(f"""
    <div class="metric-box">

    <p style="
    text-align:center;
    color:#A855F7;
    font-size:32px;
    font-weight:700;
    margin-bottom:20px;
    ">
    {title}
    </p>

    <p style="
    text-align:center;
    font-size:58px;
    font-weight:800;
    color:white;
    margin-bottom:8px;
    ">
    {probability}%
    </p>

    <p style="
    text-align:center;
    color:#D1D5DB;
    font-size:20px;
    margin-bottom:28px;
    ">
    +{sla_impact} SLA Days
    </p>

    <p style="
    background:{risk_color};
    color:white;
    padding:10px 18px;
    border-radius:999px;
    display:inline-block;
    font-weight:700;
    font-size:16px;
    margin-bottom:28px;
    ">
    {risk_level} RISK
    </p>
    
    </div>
    """, unsafe_allow_html=True)

    if risk_level in ["HIGH", "MEDIUM"]:
        st.markdown(details_section, unsafe_allow_html=True)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- REMOVE STREAMLIT DEFAULTS ---------- */

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [aria-selected="true"] {
    border-bottom: none !important;
}

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* ---------- GLOBAL ---------- */

html, body, [class*="css"] {
    background-color: #020617;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- TABS ---------- */

.stTabs [data-baseweb="tab-list"] {
    gap: 18px;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"] {
    height: 65px;
    padding-left: 32px;
    padding-right: 32px;
    background: #0F172A;
    border-radius: 18px;
    color: white;
    font-size: 18px;
    font-weight: 600;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(
        90deg,
        #6D28D9,
        #8B5CF6
    ) !important;
    color: white !important;
}

button[kind="tab"]::after {
    display: none !important;
}

/* ---------- INPUTS ---------- */

.stSelectbox > div > div {
    background-color: #1E293B !important;
    color: white !important;
    border-radius: 12px !important;
}

.stSlider > div[data-baseweb="slider"] {
    color: #A855F7 !important;
}

/* ---------- BUTTON ---------- */

.stButton > button {
    background: linear-gradient(
        90deg,
        #6D28D9,
        #8B5CF6
    );
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: 600;
}

/* ---------- DATAFRAME ---------- */

[data-testid="stDataFrame"] {
    background-color: #111827;
    border-radius: 16px;
    padding: 10px;
}

.metric-box {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(168,85,247,0.2);
}

.metric-title {
    color: #A855F7;
    font-size: 18px;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 42px;
    font-weight: 700;
}

.analysis-box {
    background: #111827;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 25px;
    border-left: 6px solid #8B5CF6;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODELS
# =========================================================

no_access_model = joblib.load("no_access_model.pkl")
dig_model = joblib.load("dig_model.pkl")
survey_model = joblib.load("survey_model.pkl")

# =========================================================
# FEATURE LISTS
# =========================================================

NO_ACCESS_FEATURES = [
    "postcode",
    "phone_available",
    "email_available",
    "preferred_contact",
    "past_no_contact_count",
    "past_no_access_count",
    "total_contact_attempts",
    "field_visit_attempts",
    "cancellation_before_visit",
    "appointment_slot",
    "days_between_booking_and_visit",
    "reschedule_count",
    "property_type",
    "shared_access",
    "meter_location_current",
    "meter_location_target"
]

DIG_FEATURES = [
    "postcode",
    "property_type",
    "shared_access",
    "field_visit_attempts",
    "days_between_booking_and_visit",
    "meter_location_current",
    "meter_location_target"
]

SURVEY_FEATURES = [
    "postcode",
    "property_type",
    "shared_access",
    "field_visit_attempts",
    "past_no_access_count",
    "days_between_booking_and_visit",
    "reschedule_count",
    "meter_location_current",
    "meter_location_target"
]

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<h1 style="
    font-size:56px;
    font-weight:800;
    color:#A855F7;
">
⚡ United Utilities AI Dispatch Assistant
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    color:#E5E7EB;
    font-size:20px;
">
AI-Powered SLA & Exception Risk Prediction System
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs([
    "Single Work Order Analysis",
    "Bulk Work Order Analysis"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown("""
    <h2 style="color:#A855F7;">
    Job Input Details
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        postcode = st.selectbox(
            "Postcode",
            [f"PC{str(i).zfill(2)}" for i in range(1,16)]
        )

        phone_available = st.selectbox(
            "Phone Available",
            [True, False]
        )

        email_available = st.selectbox(
            "Email Available",
            [True, False]
        )

        preferred_contact = st.selectbox(
            "Preferred Contact",
            ["Call", "SMS", "Email", "Mail"]
        )

    with col2:

        past_no_contact_count = st.slider(
            "Past No Contact Count",
            0, 5, 0
        )

        past_no_access_count = st.slider(
            "Past No Access Count",
            0, 5, 0
        )

        total_contact_attempts = st.slider(
            "Total Contact Attempts",
            1, 10, 2
        )

        field_visit_attempts = st.slider(
            "Field Visit Attempts",
            0, 5, 0
        )

    with col3:

        cancellation_before_visit = st.selectbox(
            "Cancellation Before Visit",
            [True, False]
        )

        appointment_slot = st.selectbox(
            "Appointment Slot",
            ["Morning", "Afternoon", "Evening"]
        )

        days_between_booking_and_visit = st.slider(
            "Days Between Booking & Visit",
            1, 30, 5
        )

        reschedule_count = st.slider(
            "Reschedule Count",
            0, 5, 0
        )

    with col4:

        property_type = st.selectbox(
            "Property Type",
            ["House", "Apartment", "Commercial"]
        )

        shared_access = st.selectbox(
            "Shared Access",
            [True, False]
        )

        meter_location_current = st.selectbox(
            "Current Meter Location",
            ["Internal", "External"]
        )

        meter_location_target = st.selectbox(
            "Target Meter Location",
            ["Internal", "External"]
        )

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_button = st.button("⚡ Analyze Job")

    # =====================================================
    # INPUT DATA
    # =====================================================

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

    # =====================================================
    # RESULTS
    # =====================================================

    if analyze_button:

        no_access_prob = round(
            no_access_model.predict_proba(
                input_data[NO_ACCESS_FEATURES]
            )[0][1] * 100,
            2
        )

        dig_prob = round(
            dig_model.predict_proba(
                input_data[DIG_FEATURES]
            )[0][1] * 100,
            2
        )

        survey_prob = round(
            survey_model.predict_proba(
                input_data[SURVEY_FEATURES]
            )[0][1] * 100,
            2
        )

        no_access_sla = round(
            (no_access_prob / 100) * 2.5,
            2
        )

        dig_sla = round(
            (dig_prob / 100) * 6,
            2
        )

        survey_sla = round(
            (survey_prob / 100) * 3,
            2
        )

        expected_sla = round(
            5 +
            no_access_sla +
            dig_sla +
            survey_sla,
            2
        )

        overall_risk = round(
            (
                no_access_prob +
                dig_prob +
                survey_prob
            ) / 3,
            2
        )


        # =====================================================
        # EXCEPTION ANALYSIS INSIDE CARDS
        # =====================================================

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <h2 style="color:#A855F7;">
        Exception Risk Breakdown
        </h2>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)

        # =====================================================
        # NO ACCESS CARD
        # =====================================================

        with m1:

            if no_access_prob < 20:
                no_access_level = "LOW"
                no_access_color = "#10B981"

            elif no_access_prob < 45:
                no_access_level = "MEDIUM"
                no_access_color = "#F59E0B"

            else:
                no_access_level = "HIGH"
                no_access_color = "#EF4444"

            no_access_reasons = []
            no_access_actions = []

            if shared_access:
                no_access_reasons.append(
                    "Shared-access property may delay technician entry."
                )

            if past_no_access_count >= 1:
                no_access_reasons.append(
                    "Previous no-access history identified."
                )

            if total_contact_attempts <= 2:
                no_access_reasons.append(
                    "Low customer engagement detected."
                )

            no_access_actions.append(
                "Verify building/security access before dispatch."
            )

            no_access_actions.append(
                "Trigger customer access confirmation."
            )

            reasons_html = "".join(
                [f"<li>{r}</li>" for r in no_access_reasons]
            )

            actions_html = "".join(
                [f"<li>{a}</li>" for a in no_access_actions]
            )

            render_risk_card(
                title="No Access Risk",
                probability=no_access_prob,
                sla_impact=no_access_sla,
                risk_level=no_access_level,
                risk_color=no_access_color,
                reasons=no_access_reasons,
                actions=no_access_actions
            )

        # =====================================================
        # DIG CARD
        # =====================================================

        with m2:

            if dig_prob < 20:
                dig_level = "LOW"
                dig_color = "#10B981"

            elif dig_prob < 45:
                dig_level = "MEDIUM"
                dig_color = "#F59E0B"

            else:
                dig_level = "HIGH"
                dig_color = "#EF4444"

            dig_reasons = []
            dig_actions = []

            if meter_location_target == "External":
                dig_reasons.append(
                    "External meter installation may require excavation."
                )

            if property_type == "Commercial":
                dig_reasons.append(
                    "Commercial infrastructure may require chamber work."
                )

            if postcode in ["PC11", "PC12", "PC13"]:
                dig_reasons.append(
                    "Historical dig activity detected in postcode region."
                )

            dig_actions.append(
                "Allocate specialist dig crew."
            )

            dig_actions.append(
                "Initiate contractor planning early."
            )

            dig_reasons_html = "".join(
                [f"<li>{r}</li>" for r in dig_reasons]
            )

            dig_actions_html = "".join(
                [f"<li>{a}</li>" for a in dig_actions]
            )

            render_risk_card(
                title="Dig Risk",
                probability=dig_prob,
                sla_impact=dig_sla,
                risk_level=dig_level,
                risk_color=dig_color,
                reasons=dig_reasons,
                actions=dig_actions
            )

        # =====================================================
        # SURVEY CARD
        # =====================================================

        with m3:

            if survey_prob < 20:
                survey_level = "LOW"
                survey_color = "#10B981"

            elif survey_prob < 45:
                survey_level = "MEDIUM"
                survey_color = "#F59E0B"

            else:
                survey_level = "HIGH"
                survey_color = "#EF4444"

            survey_reasons = []
            survey_actions = []

            if shared_access:
                survey_reasons.append(
                    "Shared property layout may require technical assessment."
                )

            if property_type == "Commercial":
                survey_reasons.append(
                    "Commercial property complexity detected."
                )

            if field_visit_attempts >= 2:
                survey_reasons.append(
                    "Multiple previous visits indicate site uncertainty."
                )

            survey_actions.append(
                "Schedule pre-visit technical survey."
            )

            survey_actions.append(
                "Assign experienced technician."
            )

            survey_reasons_html = "".join(
                [f"<li>{r}</li>" for r in survey_reasons]
            )

            survey_actions_html = "".join(
                [f"<li>{a}</li>" for a in survey_actions]
            )

            render_risk_card(
                title="Survey Risk",
                probability=survey_prob,
                sla_impact=survey_sla,
                risk_level=survey_level,
                risk_color=survey_color,
                reasons=survey_reasons,
                actions=survey_actions
            )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown("""
    <h2 style="color:#A855F7;">
    Bulk Work Order Analysis
    </h2>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        output_rows = []

        for _, row in df.iterrows():

            row_df = pd.DataFrame([row])

            no_access = round(
                no_access_model.predict_proba(
                    row_df[NO_ACCESS_FEATURES]
                )[0][1] * 100,
                2
            )

            dig = round(
                dig_model.predict_proba(
                    row_df[DIG_FEATURES]
                )[0][1] * 100,
                2
            )

            survey = round(
                survey_model.predict_proba(
                    row_df[SURVEY_FEATURES]
                )[0][1] * 100,
                2
            )

            expected_sla = round(
                5 +
                (no_access / 100) * 2.5 +
                (dig / 100) * 6 +
                (survey / 100) * 3,
                2
            )

            overall = round(
                (
                    no_access +
                    dig +
                    survey
                ) / 3,
                2
            )

            output_rows.append({

                "Work Order ID":
                row.get("work_order_id", "N/A"),

                "No Access Risk":
                f"{no_access}%",

                "Dig Risk":
                f"{dig}%",

                "Survey Risk":
                f"{survey}%",

                "Expected SLA":
                f"{expected_sla} Days",

                "Overall Risk":
                f"{overall}%"
            })

        output_df = pd.DataFrame(output_rows)

        st.dataframe(
            output_df,
            use_container_width=True
        )

        csv = output_df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Results CSV",
            data=csv,
            file_name="bulk_work_order_results.csv",
            mime="text/csv"
        )