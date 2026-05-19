from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("exception_prediction_model.pkl")

# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(
    title="United Utilities AI Operations API",
    description="AI-Powered SLA & Exception Risk Prediction API",
    version="1.0"
)

# =====================================================
# INPUT SCHEMA
# =====================================================

class JobInput(BaseModel):

    postcode: str

    phone_available: bool
    email_available: bool

    preferred_contact: str

    past_no_contact_count: int
    past_no_access_count: int

    total_contact_attempts: int
    field_visit_attempts: int

    cancellation_before_visit: bool

    appointment_slot: str

    days_between_booking_and_visit: int

    reschedule_count: int

    property_type: str

    shared_access: bool

    meter_location_current: str
    meter_location_target: str

# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")

def home():

    return {
        "message": "United Utilities AI Operations API Running"
    }

# =====================================================
# PREDICTION ENDPOINT
# =====================================================

@app.post("/predict")

def predict(job: JobInput):

    # ================================================
    # CONVERT INPUT TO DATAFRAME
    # ================================================

    input_data = pd.DataFrame([{
        "postcode": job.postcode,

        "phone_available": job.phone_available,
        "email_available": job.email_available,

        "preferred_contact": job.preferred_contact,

        "past_no_contact_count": job.past_no_contact_count,
        "past_no_access_count": job.past_no_access_count,

        "total_contact_attempts": job.total_contact_attempts,
        "field_visit_attempts": job.field_visit_attempts,

        "cancellation_before_visit": job.cancellation_before_visit,

        "appointment_slot": job.appointment_slot,

        "days_between_booking_and_visit":
            job.days_between_booking_and_visit,

        "reschedule_count": job.reschedule_count,

        "property_type": job.property_type,

        "shared_access": job.shared_access,

        "meter_location_current":
            job.meter_location_current,

        "meter_location_target":
            job.meter_location_target
    }])

    # ================================================
    # MODEL PREDICTION
    # ================================================

    probabilities = model.predict_proba(input_data)

    no_contact_prob = round(
        probabilities[0][:, 1][0] * 100,
        2
    )

    no_access_prob = round(
        probabilities[1][:, 1][0] * 100,
        2
    )

    dig_prob = round(
        probabilities[2][:, 1][0] * 100,
        2
    )

    survey_prob = round(
        probabilities[3][:, 1][0] * 100,
        2
    )

    # ================================================
    # SLA CALCULATION
    # ================================================

    BASE_SLA = 5

    expected_delay = (
        (no_contact_prob / 100) * 1.5 +
        (no_access_prob / 100) * 2.5 +
        (dig_prob / 100) * 6 +
        (survey_prob / 100) * 3
    )

    expected_sla = round(
        BASE_SLA + expected_delay,
        2
    )

    # ================================================
    # RISK CATEGORY
    # ================================================

    if expected_sla <= 7:
        risk_category = "Low Risk"

    elif expected_sla <= 10:
        risk_category = "Medium Risk"

    else:
        risk_category = "High Risk"

    # ================================================
    # RECOMMENDATIONS
    # ================================================

    recommendations = []

    if no_contact_prob > 20:

        recommendations.append(
            "Proactively contact customer before dispatch."
        )

    if no_access_prob > 20:

        recommendations.append(
            "Verify site/building access before visit."
        )

    if dig_prob > 15:

        recommendations.append(
            "Allocate specialist crew for possible dig work."
        )

    if survey_prob > 15:

        recommendations.append(
            "Consider pre-visit technical survey."
        )

    if expected_sla > 10:

        recommendations.append(
            "Add scheduling buffer due to elevated risk."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Standard dispatch recommended."
        )

    # ================================================
    # RETURN RESPONSE
    # ================================================

    return {
        "no_contact_risk": no_contact_prob,
        "no_access_risk": no_access_prob,
        "dig_risk": dig_prob,
        "survey_risk": survey_prob,
        "expected_sla_days": expected_sla,
        "risk_category": risk_category,
        "recommendations": recommendations
    }
