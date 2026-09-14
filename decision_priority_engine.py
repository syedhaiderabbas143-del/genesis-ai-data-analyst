def calculate_priority_score(
    insight_type,
    score=0,
    title=""
):

    insight_type = str(insight_type or "").lower()
    title = str(title or "").lower()

    try:
        score = float(score or 0)
    except Exception:
        score = 0

    priority_score = 40

    critical_keywords = [
        "negative profit",
        "profit risk",
        "loss",
        "critical",
        "high expense ratio"
    ]

    if any(keyword in title for keyword in critical_keywords):
        priority_score = 90

    elif insight_type in [
        "high_expense_ratio",
        "negative_profit",
        "low_performance"
    ]:
        priority_score = 80

    elif insight_type == "high_variation":

        if score >= 100:
            priority_score = 85
        elif score >= 70:
            priority_score = 75
        elif score >= 50:
            priority_score = 65
        else:
            priority_score = 55

    elif insight_type == "correlation":

        if abs(score) >= 0.8:
            priority_score = 70
        elif abs(score) >= 0.6:
            priority_score = 60
        else:
            priority_score = 45

    elif insight_type == "data_quality":
        priority_score = 30

    if score >= 80:
        priority_score += 5
    elif score >= 50:
        priority_score += 3

    priority_score = min(priority_score, 100)

    if priority_score >= 90:
        priority = "Critical"
    elif priority_score >= 70:
        priority = "High"
    elif priority_score >= 40:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "priority_score": priority_score
    }
# ============================================================
# GENESIS AI - DECISION PRIORITY ENGINE
# ============================================================

# ============================================================
# DYNAMIC PRIORITY SCORING
# ============================================================


def calculate_decision_priority(
    root_causes,
    recommendations
):

    decisions = []


    # --------------------------------------------------------
    # PRIORITY RULES
    # --------------------------------------------------------

    


    # --------------------------------------------------------
    # PROCESS ROOT CAUSES
    # --------------------------------------------------------

    for item in root_causes:

            priority_result = calculate_priority_score(

        insight_type=item.get(
            "type",
            ""
        ),

        score=item.get(
            "score",
            0
        ),

        title=item.get(
            "title",
            ""
        )

    )


    priority = priority_result[
        "priority"
    ]

    score = priority_result[
        "priority_score"
    ]


    decisions.append({

            "decision_type": "root_cause",

            "priority": priority,

            "priority_score": score,

            "title": item.get(
                "title",
                "Business Issue"
            ),

            "reason": item.get(
                "message",
                ""
            ),

            "recommended_action": (

                "Investigate and address the identified root cause."

            )

        })


    # --------------------------------------------------------
    # PROCESS RECOMMENDATIONS
    # --------------------------------------------------------

    for item in recommendations:

            priority_result = calculate_priority_score(

        insight_type=item.get(
            "type",
            ""
        ),

        score=item.get(
            "score",
            0
        ),

        title=item.get(
            "title",
            ""
        )

    )


    priority = priority_result[
        "priority"
    ]

    score = priority_result[
        "priority_score"
    ]


    decisions.append({

            "decision_type": "recommendation",

            "priority": priority,

            "priority_score": score,

            "title": item.get(
                "title",
                "Recommended Action"
            ),

            "reason": item.get(
                "message",
                ""
            ),

            "recommended_action": item.get(
                "recommendation",
                item.get(
                    "message",
                    ""
                )
            )

        })


    # --------------------------------------------------------
    # SORT DECISIONS
    # --------------------------------------------------------

    decisions = sorted(

        decisions,

        key=lambda x: x.get(
            "priority_score",
            0
        ),

        reverse=True

    )


    # --------------------------------------------------------
    # ADD DECISION RANK
    # --------------------------------------------------------

    for index, decision in enumerate(decisions):

        decision["rank"] = index + 1


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "decisions": decisions,

        "total_decisions": len(
            decisions
        )

    }