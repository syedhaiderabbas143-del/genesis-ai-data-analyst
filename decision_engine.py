# ============================================================
# GENESIS AI - DECISION PRIORITY ENGINE
# ============================================================


def calculate_decision_priority(
    root_causes,
    recommendations
):

    decisions = []

    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------

    if not root_causes:

        return {

            "decisions": [],

            "summary": (
                "No significant factors were available "
                "for decision prioritization."
            )

        }


    # --------------------------------------------------------
    # FIND HIGHEST ROOT CAUSE SCORE
    # --------------------------------------------------------

    scores = []

    for cause in root_causes:

        try:

            score = float(
                cause.get(
                    "score",
                    0
                )
            )

            scores.append(score)

        except Exception:

            pass


    max_score = max(scores) if scores else 0


    # --------------------------------------------------------
    # CREATE ROOT CAUSE LOOKUP
    # --------------------------------------------------------

    cause_lookup = {}

    for cause in root_causes:

        factor = cause.get("factor")

        try:

            score = float(
                cause.get(
                    "score",
                    0
                )
            )

        except Exception:

            score = 0


        impact = cause.get(

            "impact_strength",

            "Unknown"

        )


        if factor:

            cause_lookup[factor] = {

                "score": score,

                "impact": impact

            }


    # --------------------------------------------------------
    # PRIORITIZE RECOMMENDATIONS
    # --------------------------------------------------------

    for recommendation in recommendations:

        factor = recommendation.get(

            "factor",

            "Unknown Factor"

        )


        cause_data = cause_lookup.get(

            factor,

            {}

        )


        raw_score = cause_data.get(

            "score",

            0

        )


        # ----------------------------------------------------
        # NORMALIZE SCORE TO 0 - 100
        # ----------------------------------------------------

        if max_score > 0:

            decision_score = (

                raw_score / max_score

            ) * 100

        else:

            decision_score = 0


        decision_score = round(

            decision_score,

            2

        )


        # ----------------------------------------------------
        # DETERMINE PRIORITY
        # ----------------------------------------------------

        if decision_score >= 80:

            priority_level = "Critical"

        elif decision_score >= 60:

            priority_level = "High"

        elif decision_score >= 30:

            priority_level = "Medium"

        else:

            priority_level = "Low"


        # ----------------------------------------------------
        # QUICK WIN DETECTION
        # ----------------------------------------------------

        quick_win = (

            priority_level in [

                "Critical",

                "High"

            ]

        )


        # ----------------------------------------------------
        # DECISION OBJECT
        # ----------------------------------------------------

        decisions.append({

            "factor": factor,

            "priority": priority_level,

            "score": round(

                raw_score,

                2

            ),

            "decision_score": decision_score,

            "quick_win": quick_win,

            "recommended_action":

                recommendation.get(

                    "recommendation",

                    "Further investigation required."

                ),

            "expected_impact":

                recommendation.get(

                    "expected_impact",

                    "Unknown"

                )

        })


    # --------------------------------------------------------
    # SORT BY DECISION SCORE
    # --------------------------------------------------------

    decisions = sorted(

        decisions,

        key=lambda x:

            x["decision_score"],

        reverse=True

    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    if decisions:

        highest = decisions[0]


        summary = (

            f"Genesis AI prioritized "

            f"{len(decisions)} business decisions. "

            f"Highest priority factor: "

            f"{highest['factor']} "

            f"with a Decision Score of "

            f"{highest['decision_score']}/100 "

            f"({highest['priority']})."

        )

    else:

        summary = (

            "No business decisions could be generated."

        )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "decisions": decisions,

        "summary": summary

    }