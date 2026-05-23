from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

from reasoning_engine import *

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI()

# =====================================================
# LOAD MODELS
# =====================================================

no_access_model = joblib.load("no_access_model.pkl")
dig_model = joblib.load("dig_model.pkl")
survey_model = joblib.load("survey_model.pkl")

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
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "message":
        "United Utilities AI Dispatch Assistant API Running"
    }

# =====================================================
# PREDICT
# =====================================================

@app.post("/predict")

def predict(job: JobInput):

    input_data = pd.DataFrame([job.dict()])

    # =================================================
    # PREDICTIONS
    # =================================================

    no_access_prob = round(
        no_access_model.predict_proba(input_data)[0][1] * 100,
        2
    )

    dig_prob = round(
        dig_model.predict_proba(input_data)[0][1] * 100,
        2
    )

    survey_prob = round(
        survey_model.predict_proba(input_data)[0][1] * 100,
        2
    )

    # =================================================
    # SLA
    # =================================================

    BASE_SLA = 5

    expected_delay = (
        (no_access_prob / 100) * 2.5 +
        (dig_prob / 100) * 6 +
        (survey_prob / 100) * 3
    )

    expected_sla = round(
        BASE_SLA + expected_delay,
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

    # =================================================
    # REASONING
    # =================================================

    input_dict = input_data.iloc[0].to_dict()

    no_access_insights = generate_no_access_insights(
        input_dict,
        no_access_prob
    )

    dig_insights = generate_dig_insights(
        input_dict,
        dig_prob
    )

    survey_insights = generate_survey_insights(
        input_dict,
        survey_prob
    )

    # =================================================
    # RESPONSE
    # =================================================

    return {

        "no_access_risk": no_access_prob,

        "dig_risk": dig_prob,

        "survey_risk": survey_prob,

        "overall_risk": overall_risk,

        "expected_sla_days": expected_sla,

        "no_access_analysis": no_access_insights,

        "dig_analysis": dig_insights,

        "survey_analysis": survey_insights
    }