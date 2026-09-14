# ============================================================
# GENESIS AI - DECISION GROUPING & CONSISTENCY ENGINE
# ============================================================


def group_decisions(decisions):

    groups = {}

    # --------------------------------------------------------
    # PROCESS ALL DECISIONS
    # --------------------------------------------------------

    for decision in decisions:

        title = str(
            decision.get(
                "title",
                ""
            )
        )

        # Remove "Action:" so recommendation and root cause
        # can belong to the same issue group.

        clean_title = title.replace(
            "Action:",
            ""
        ).strip()


        # ----------------------------------------------------
        # CREATE GROUP IF NOT EXISTS
        # ----------------------------------------------------

        if clean_title not in groups:

            groups[clean_title] = {

                "issue": clean_title,

                "root_cause": None,

                "recommendation": None,

                "priority": decision.get(
                    "priority",
                    "Medium"
                ),

                "priority_score": decision.get(
                    "priority_score",
                    0
                ),

                "impact_score": decision.get(
                    "impact_score",
                    0
                ),

                "impact_level": decision.get(
                    "impact_level",
                    "Low"
                ),

                "urgency": decision.get(
                    "urgency",
                    "Low"
                ),

                "action_plan": decision.get(
                    "action_plan",
                    {}
                )

            }


        # ----------------------------------------------------
        # ROOT CAUSE
        # ----------------------------------------------------

        if decision.get(
            "decision_type"
        ) == "root_cause":

            groups[clean_title][
                "root_cause"
            ] = {

                "reason": decision.get(
                    "reason",
                    ""
                ),

                "recommended_action": decision.get(
                    "recommended_action",
                    ""
                )

            }


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        elif decision.get(
            "decision_type"
        ) == "recommendation":

            groups[clean_title][
                "recommendation"
            ] = {

                "reason": decision.get(
                    "reason",
                    ""
                ),

                "recommended_action": decision.get(
                    "recommended_action",
                    ""
                )

            }


        # ----------------------------------------------------
        # UPDATE GROUP WITH HIGHEST IMPACT
        # ----------------------------------------------------

        current_impact = groups[
            clean_title
        ].get(
            "impact_score",
            0
        )

        decision_impact = decision.get(
            "impact_score",
            0
        )


        if decision_impact > current_impact:

            groups[clean_title][
                "priority"
            ] = decision.get(
                "priority",
                "Medium"
            )

            groups[clean_title][
                "priority_score"
            ] = decision.get(
                "priority_score",
                0
            )

            groups[clean_title][
                "impact_score"
            ] = decision_impact

            groups[clean_title][
                "impact_level"
            ] = decision.get(
                "impact_level",
                "Low"
            )

            groups[clean_title][
                "urgency"
            ] = decision.get(
                "urgency",
                "Low"
            )

            groups[clean_title][
                "action_plan"
            ] = decision.get(
                "action_plan",
                {}
            )


    # --------------------------------------------------------
    # CONVERT TO LIST
    # --------------------------------------------------------

    grouped_decisions = list(
        groups.values()
    )


    # --------------------------------------------------------
    # SORT BY IMPACT
    # --------------------------------------------------------

    grouped_decisions = sorted(

        grouped_decisions,

        key=lambda x: x.get(
            "impact_score",
            0
        ),

        reverse=True

    )


    # --------------------------------------------------------
    # ADD GROUP RANK
    # --------------------------------------------------------

    for index, group in enumerate(
        grouped_decisions
    ):

        group["rank"] = index + 1


    # --------------------------------------------------------
    # CONSISTENCY STATISTICS
    # --------------------------------------------------------

    complete_groups = 0

    for group in grouped_decisions:

        if (

            group.get("root_cause")

            and

            group.get("recommendation")

        ):

            complete_groups += 1


    return {

        "groups": grouped_decisions,

        "total_groups": len(
            grouped_decisions
        ),

        "complete_groups": complete_groups,

        "incomplete_groups": (

            len(grouped_decisions)

            - complete_groups

        )

    }