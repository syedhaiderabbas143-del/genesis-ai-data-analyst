# ============================================================
# GENESIS AI - DECISION CONFIDENCE & RISK ENGINE
# ============================================================


def calculate_decision_confidence_and_risk(decision):

    # --------------------------------------------------------
    # GET DECISION VALUES
    # --------------------------------------------------------

    priority_score = decision.get(
        "priority_score",
        0
    )

    impact_score = decision.get(
        "impact_score",
        0
    )

    decision_type = str(
        decision.get(
            "decision_type",
            ""
        )
    ).lower()


    # --------------------------------------------------------
    # CONFIDENCE SCORE
    # --------------------------------------------------------

    confidence_score = 50


    # Priority contributes to confidence

    if priority_score >= 90:

        confidence_score += 25

    elif priority_score >= 70:

        confidence_score += 20

    elif priority_score >= 40:

        confidence_score += 10


    # Impact contributes to confidence

    if impact_score >= 90:

        confidence_score += 20

    elif impact_score >= 70:

        confidence_score += 15

    elif impact_score >= 40:

        confidence_score += 5


    # Recommendation decisions have clearer actions

    if decision_type == "recommendation":

        confidence_score += 5


    confidence_score = min(
        confidence_score,
        100
    )


    # --------------------------------------------------------
    # CONFIDENCE LEVEL
    # --------------------------------------------------------

    if confidence_score >= 85:

        confidence_level = "Very High"

    elif confidence_score >= 70:

        confidence_level = "High"

    elif confidence_score >= 50:

        confidence_level = "Medium"

    else:

        confidence_level = "Low"


    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    risk_score = 0


    # Higher impact = Higher risk

    if impact_score >= 90:

        risk_score += 50

    elif impact_score >= 70:

        risk_score += 35

    elif impact_score >= 40:

        risk_score += 20


    # Higher priority = Higher business risk

    if priority_score >= 90:

        risk_score += 40

    elif priority_score >= 70:

        risk_score += 30

    elif priority_score >= 40:

        risk_score += 15


    risk_score = min(
        risk_score,
        100
    )


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if risk_score >= 80:

        risk_level = "Critical"

    elif risk_score >= 60:

        risk_level = "High"

    elif risk_score >= 30:

        risk_level = "Medium"

    else:

        risk_level = "Low"


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "confidence_score": confidence_score,

        "confidence_level": confidence_level,

        "risk_score": risk_score,

        "risk_level": risk_level

    }