# ============================================================
# GENESIS AI - DECISION IMPACT ENGINE
# ============================================================


def calculate_decision_impact(decision):

    decision_type = str(
        decision.get(
            "decision_type",
            ""
        )
    ).lower()

    priority_score = float(
        decision.get(
            "priority_score",
            0
        ) or 0
    )

    title = str(
        decision.get(
            "title",
            ""
        )
    ).lower()

    reason = str(
        decision.get(
            "reason",
            ""
        )
    ).lower()


    # --------------------------------------------------------
    # BUSINESS IMPACT SCORE
    # --------------------------------------------------------

    impact_score = priority_score

    high_impact_keywords = [

        "negative profit",
        "loss",
        "high expense",
        "revenue",
        "profitability"

    ]

    for keyword in high_impact_keywords:

        if keyword in title or keyword in reason:

            impact_score += 15

            break


    # --------------------------------------------------------
    # DECISION TYPE IMPACT
    # --------------------------------------------------------

    if decision_type == "root_cause":

        impact_score += 10

    elif decision_type == "recommendation":

        impact_score += 5


    # --------------------------------------------------------
    # FINAL IMPACT SCORE
    # --------------------------------------------------------

    impact_score = min(
        round(impact_score),
        100
    )


    # --------------------------------------------------------
    # IMPACT LEVEL
    # --------------------------------------------------------

    if impact_score >= 90:

        impact_level = "Critical"

    elif impact_score >= 70:

        impact_level = "High"

    elif impact_score >= 40:

        impact_level = "Medium"

    else:

        impact_level = "Low"


    # --------------------------------------------------------
    # URGENCY LEVEL
    # --------------------------------------------------------

    if impact_score >= 90:

        urgency = "Immediate"

    elif impact_score >= 70:

        urgency = "High"

    elif impact_score >= 40:

        urgency = "Medium"

    else:

        urgency = "Low"


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "impact_score": impact_score,

        "impact_level": impact_level,

        "urgency": urgency

    }