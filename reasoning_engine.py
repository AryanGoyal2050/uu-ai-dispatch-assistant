# reasoning_engine.py

def generate_no_access_insights(input_data, probability):

    reasons = []
    actions = []

    if input_data["shared_access"]:
        reasons.append(
            "Shared-access property may delay technician entry."
        )

        actions.append(
            "Verify building/security access before dispatch."
        )

    if input_data["field_visit_attempts"] >= 2:
        reasons.append(
            "Previous failed visits indicate accessibility issues."
        )

        actions.append(
            "Trigger pre-visit customer confirmation."
        )

    if input_data["appointment_slot"] == "Evening":
        reasons.append(
            "Evening appointment slots historically show lower access success."
        )

        actions.append(
            "Consider rescheduling to a morning slot."
        )

    if input_data["property_type"] == "Apartment":
        reasons.append(
            "Apartment properties often require coordinated access."
        )

        actions.append(
            "Notify customer to arrange access beforehand."
        )

    if probability >= 30:
        actions.append(
            "Assign experienced technician for access-sensitive visit."
        )

    return {
        "reasons": list(set(reasons)),
        "actions": list(set(actions))
    }


# ======================================================

def generate_dig_insights(input_data, probability):

    reasons = []
    actions = []

    if input_data["meter_location_current"] == "Internal" and \
       input_data["meter_location_target"] == "External":

        reasons.append(
            "Meter relocation from internal to external may require excavation."
        )

        actions.append(
            "Initiate dig approval planning early."
        )

    if input_data["postcode"] in ["PC11", "PC12", "PC13"]:
        reasons.append(
            "This postcode historically shows higher excavation requirements."
        )

        actions.append(
            "Allocate external contractor availability buffer."
        )

    if input_data["property_type"] == "Commercial":
        reasons.append(
            "Commercial sites often involve more complex infrastructure."
        )

        actions.append(
            "Assign technician familiar with commercial utility layouts."
        )

    if probability >= 20:
        actions.append(
            "Inform customer about possible excavation-related delay."
        )

    return {
        "reasons": list(set(reasons)),
        "actions": list(set(actions))
    }


# ======================================================

def generate_survey_insights(input_data, probability):

    reasons = []
    actions = []

    if input_data["shared_access"]:
        reasons.append(
            "Shared-access properties may require additional inspection."
        )

        actions.append(
            "Create survey work order before main visit."
        )

    if input_data["property_type"] == "Commercial":
        reasons.append(
            "Commercial properties often require engineering assessment."
        )

        actions.append(
            "Assign experienced assessor for technical validation."
        )

    if input_data["reschedule_count"] >= 2:
        reasons.append(
            "Multiple reschedules indicate potential unresolved site constraints."
        )

        actions.append(
            "Perform site assessment before dispatch."
        )

    if input_data["days_between_booking_and_visit"] > 14:
        reasons.append(
            "Long lead times may indicate planning uncertainty."
        )

        actions.append(
            "Validate site readiness before technician allocation."
        )

    if probability >= 20:
        actions.append(
            "Route case through survey-first workflow."
        )

    return {
        "reasons": list(set(reasons)),
        "actions": list(set(actions))
    }