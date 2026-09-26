# ============================================================
# GENESIS AI - DECISION EXPLANATION ENGINE
# ============================================================


def generate_decision_explanation(decision):

    title = decision.get(
        "title",
        "Business Decision"
    )

    reason = decision.get(
        "reason",
        ""
    )

    recommended_action = decision.get(
        "recommended_action",
        ""
    )

    priority = decision.get(
        "priority",
        "Medium"
    )

    impact_level = decision.get(
        "impact_level",
        "Low"
    )

    urgency = decision.get(
        "urgency",
        "Low"
    )

    confidence_level = decision.get(
        "confidence_level",
        "Medium"
    )

    risk_level = decision.get(
        "risk_level",
        "Medium"
    )


    # --------------------------------------------------------
    # BUILD EXPLANATION
    # --------------------------------------------------------

    why_points = []


    # Original Business Reason

    if reason:

        why_points.append(
            reason
        )


    # Impact Explanation

    if impact_level in [

        "Critical",

        "High"

    ]:

        why_points.append(

            f"This issue has a {impact_level.lower()} business impact."

        )


    # Confidence Explanation

    if confidence_level:

        why_points.append(

            f"The AI confidence level for this decision is {confidence_level.lower()}."

        )


    # Risk Explanation

    if risk_level in [

        "Critical",

        "High"

    ]:

        why_points.append(

            f"Delaying action may increase the {risk_level.lower()} business risk."

        )


    # Urgency Explanation

    if urgency == "Immediate":

        urgency_message = (

            "Immediate management attention is recommended."

        )

    elif urgency == "High":

        urgency_message = (

            "This issue should be addressed as a high-priority business action."

        )

    else:

        urgency_message = (

            "The issue should be monitored and addressed according to business priorities."

        )


    # --------------------------------------------------------
    # FINAL EXPLANATION
    # --------------------------------------------------------

    explanation = {

        "decision": title,

        "priority": priority,

        "why_this_decision": why_points,

        "urgency_explanation": urgency_message,

        "recommended_action": recommended_action

    }


    return explanation