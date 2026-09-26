# ============================================================
# GENESIS AI - EXECUTIVE SUMMARY ENGINE
# ============================================================


def generate_executive_summary(
    decisions,
    target_column=None
):

    # --------------------------------------------------------
    # NO DECISIONS
    # --------------------------------------------------------

    if not decisions:

        return {

            "executive_summary": {

                "top_priority": None,

                "decision_score": 0,

                "priority_level": "None",

                "quick_wins": [],

                "management_attention_required": False,

                "recommended_focus": (

                    "No significant decision patterns "
                    "were detected."

                )

            },

            "summary": (

                "Genesis AI could not generate an executive "
                "decision summary because no significant "
                "decisions were available."

            )

        }


    # --------------------------------------------------------
    # SORT DECISIONS
    # --------------------------------------------------------

    sorted_decisions = sorted(

        decisions,

        key=lambda x: x.get(

            "decision_score",

            0

        ),

        reverse=True

    )


    # --------------------------------------------------------
    # TOP PRIORITY
    # --------------------------------------------------------

    top_decision = sorted_decisions[0]


    top_factor = top_decision.get(

        "factor",

        "Unknown Factor"

    )


    top_score = top_decision.get(

        "decision_score",

        0

    )


    top_priority = top_decision.get(

        "priority",

        "Unknown"

    )


    # --------------------------------------------------------
    # QUICK WINS
    # --------------------------------------------------------

    quick_wins = []


    for decision in sorted_decisions:

        if decision.get(

            "quick_win",

            False

        ):

            quick_wins.append(

                decision.get(

                    "factor",

                    "Unknown Factor"

                )

            )


    # --------------------------------------------------------
    # MANAGEMENT ATTENTION
    # --------------------------------------------------------

    management_attention_required = (

        top_priority

        in [

            "Critical",

            "High"

        ]

    )


    # --------------------------------------------------------
    # RECOMMENDED FOCUS
    # --------------------------------------------------------

    recommended_action = top_decision.get(

        "recommended_action",

        "Further investigation is recommended."

    )


    recommended_focus = (

        f"Immediately focus on {top_factor}. "

        f"{recommended_action}"

    )


    # --------------------------------------------------------
    # CREATE EXECUTIVE SUMMARY
    # --------------------------------------------------------

    executive_summary = {

        "target_column": target_column,

        "top_priority": top_factor,

        "decision_score": top_score,

        "priority_level": top_priority,

        "quick_wins": quick_wins,

        "management_attention_required":

            management_attention_required,

        "recommended_focus":

            recommended_focus

    }


    # --------------------------------------------------------
    # TEXT SUMMARY
    # --------------------------------------------------------

    summary = (

        f"Genesis AI identified {top_factor} "

        f"as the highest business priority "

        f"with a Decision Score of "

        f"{top_score}/100 "

        f"({top_priority})."

    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "executive_summary":

            executive_summary,

        "summary":

            summary

    }