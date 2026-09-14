# ============================================================
# GENESIS AI - DECISION ACTION PLAN ENGINE
# ============================================================


def generate_decision_action_plan(decision):

    impact_level = str(
        decision.get(
            "impact_level",
            "Low"
        )
    ).lower()

    urgency = str(
        decision.get(
            "urgency",
            "Low"
        )
    ).lower()

    decision_type = str(
        decision.get(
            "decision_type",
            ""
        )
    ).lower()


    # --------------------------------------------------------
    # ACTION TIMELINE
    # --------------------------------------------------------

    if urgency == "immediate":

        timeline = "Immediate"

    elif urgency in [
        "high",
        "urgent"
    ]:

        timeline = "Short-term"

    else:

        timeline = "Long-term"


    # --------------------------------------------------------
    # ACTION OWNER
    # --------------------------------------------------------

    title = str(
        decision.get(
            "title",
            ""
        )
    ).lower()


    if any(

        keyword in title

        for keyword in [

            "profit",

            "expense",

            "revenue"

        ]

    ):

        owner = "Finance Team"


    elif any(

        keyword in title

        for keyword in [

            "performance",

            "employee",

            "training",

            "leaves"

        ]

    ):

        owner = "HR / Operations Team"


    else:

        owner = "Management Team"


    # --------------------------------------------------------
    # ACTION STEPS
    # --------------------------------------------------------

    action_steps = []


    if decision_type == "root_cause":

        action_steps = [

            "Investigate the underlying cause.",

            "Identify the affected records or business areas.",

            "Analyze contributing factors.",

            "Create a corrective action plan."

        ]


    elif decision_type == "recommendation":

        action_steps = [

            "Review the recommended action.",

            "Assign responsible stakeholders.",

            "Implement the improvement plan.",

            "Monitor results and measure performance."

        ]


    else:

        action_steps = [

            "Review the identified issue.",

            "Assign responsible stakeholders.",

            "Implement corrective actions.",

            "Monitor business results."

        ]


    # --------------------------------------------------------
    # EXPECTED BUSINESS IMPACT
    # --------------------------------------------------------

    if impact_level == "critical":

        expected_impact = (

            "High potential business improvement and risk reduction."

        )

    elif impact_level == "high":

        expected_impact = (

            "Significant improvement in business performance."

        )

    elif impact_level == "medium":

        expected_impact = (

            "Moderate improvement in operational performance."

        )

    else:

        expected_impact = (

            "Limited but measurable business improvement."

        )


    # --------------------------------------------------------
    # SUCCESS METRIC
    # --------------------------------------------------------

    if any(

        keyword in title

        for keyword in [

            "profit",

            "loss"

        ]

    ):

        success_metric = (

            "Reduction in negative profit records."

        )


    elif "expense" in title:

        success_metric = (

            "Reduction in expense-to-revenue ratio."

        )


    elif any(

        keyword in title

        for keyword in [

            "performance",

            "employee"

        ]

    ):

        success_metric = (

            "Improvement in employee performance ratings."

        )


    else:

        success_metric = (

            "Measured improvement in the affected business metric."

        )


    # --------------------------------------------------------
    # FINAL ACTION PLAN
    # --------------------------------------------------------

    return {

        "timeline": timeline,

        "owner": owner,

        "action_steps": action_steps,

        "expected_impact": expected_impact,

        "success_metric": success_metric

    }