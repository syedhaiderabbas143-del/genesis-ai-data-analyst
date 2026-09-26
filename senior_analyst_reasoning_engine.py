# ============================================================
# GENESIS AI - SENIOR ANALYST REASONING ENGINE
# ============================================================


def generate_senior_analyst_reasoning(
    decisions
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not decisions:

        return {

            "success": True,

            "primary_business_concern": None,

            "reasoning": "No major business concerns were detected.",

            "supporting_evidence": [],

            "recommended_management_decision": None,

            "next_priority": None

        }


    # --------------------------------------------------------
    # SORT DECISIONS
    # --------------------------------------------------------

    sorted_decisions = sorted(

        decisions,

        key=lambda x: (

            x.get(
                "impact_score",
                0
            ),

            x.get(
                "risk_score",
                0
            ),

            x.get(
                "priority_score",
                0
            )

        ),

        reverse=True

    )


    # --------------------------------------------------------
    # SELECT PRIMARY DECISION
    # --------------------------------------------------------

    primary_decision = sorted_decisions[0]


    title = primary_decision.get(

        "title",

        "Business Issue"

    )


    reason = primary_decision.get(

        "reason",

        "No detailed reason available."

    )


    impact_level = primary_decision.get(

        "impact_level",

        "Low"

    )


    risk_level = primary_decision.get(

        "risk_level",

        "Low"

    )


    confidence_level = primary_decision.get(

        "confidence_level",

        "Medium"

    )


    urgency = primary_decision.get(

        "urgency",

        "Low"

    )


    recommended_action = primary_decision.get(

        "recommended_action",

        "Further investigation is recommended."

    )


    # --------------------------------------------------------
    # GENERATE SENIOR ANALYST REASONING
    # --------------------------------------------------------

    reasoning = (

        f"{title} has been identified as the primary "

        f"business concern because it has the highest "

        f"combination of business impact, risk, and priority "

        f"among the detected issues."

    )


    # --------------------------------------------------------
    # SUPPORTING EVIDENCE
    # --------------------------------------------------------

    supporting_evidence = [

        reason,

        f"Business impact level: {impact_level}.",

        f"Business risk level: {risk_level}.",

        f"AI confidence level: {confidence_level}.",

        f"Required urgency: {urgency}."

    ]


    # --------------------------------------------------------
    # DETERMINE MANAGEMENT DECISION
    # --------------------------------------------------------

    if urgency == "Immediate":

        management_decision = (

            "Immediate management intervention is recommended. "

            "The responsible team should investigate the issue "

            "and begin corrective action without delay."

        )

    elif urgency == "High":

        management_decision = (

            "This issue should be treated as a high-priority "

            "management action and addressed in the short term."

        )

    else:

        management_decision = (

            "The issue should be monitored and included in "

            "the business improvement plan."

        )


    # --------------------------------------------------------
    # NEXT PRIORITY
    # --------------------------------------------------------

    next_priority = None


    if len(sorted_decisions) > 1:

        next_decision = sorted_decisions[1]

        next_priority = {

            "title": next_decision.get(

                "title",

                "Business Issue"

            ),

            "priority": next_decision.get(

                "priority",

                "Medium"

            ),

            "impact_level": next_decision.get(

                "impact_level",

                "Low"

            ),

            "recommended_action": next_decision.get(

                "recommended_action",

                ""

            )

        }


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "primary_business_concern": {

            "title": title,

            "priority": primary_decision.get(

                "priority",

                "Medium"

            ),

            "impact_level": impact_level,

            "risk_level": risk_level,

            "confidence_level": confidence_level,

            "urgency": urgency

        },

        "reasoning": reasoning,

        "supporting_evidence": supporting_evidence,

        "recommended_management_decision": {

            "decision": management_decision,

            "recommended_action": recommended_action

        },

        "next_priority": next_priority

    }