# ============================================================
# GENESIS AI - AGENT EXECUTION PLANNER
# ============================================================

from agent_dependencies import (
    resolve_agent_execution_order
)

from agent_priority import (
    get_query_based_priority,
    get_agent_priority_details
)


# ============================================================
# CREATE AGENT EXECUTION PLAN
# ============================================================

def create_agent_execution_plan(
    agents_to_run,
    user_query=""
):

    # ========================================================
    # STEP 1: VALIDATE AGENTS
    # ========================================================

    if not agents_to_run:

        return {

            "requested_agents": [],

            "dependency_order": [],

            "priority_order": [],

            "final_execution_order": [],

            "priority_details": []
        }


    # ========================================================
    # STEP 2: RESOLVE DEPENDENCIES
    # ========================================================

    dependency_order = resolve_agent_execution_order(
        agents_to_run
    )


    # ========================================================
    # STEP 3: APPLY QUERY-BASED PRIORITY
    # ========================================================

    priority_scores = []


    for agent_name in dependency_order:

        # ----------------------------------------------------
        # QUERY-BASED PRIORITY
        # ----------------------------------------------------

        if user_query:

            priority_result = get_query_based_priority(
                agent_name,
                user_query
            )

        # ----------------------------------------------------
        # DEFAULT PRIORITY
        # ----------------------------------------------------

        else:

            priority_result = get_agent_priority_details(
                agent_name
            )


        # ====================================================
        # HANDLE PRIORITY RESULT
        # ====================================================

        if isinstance(priority_result, dict):

            priority_score = priority_result.get(

                "final_priority",

                priority_result.get(
                    "priority",
                    0
                )
            )

        else:

            priority_score = priority_result


        priority_scores.append({

            "agent": agent_name,

            "priority": priority_score

        })


    # ========================================================
    # STEP 4: SORT BY PRIORITY
    # ========================================================

    priority_scores.sort(

        key=lambda item: item["priority"],

        reverse=True

    )


    priority_order = [

        item["agent"]

        for item in priority_scores
    ]


    # ========================================================
    # STEP 5: PROTECT DEPENDENCY ORDER
    # ========================================================

    # Priority influences execution preference,
    # but dependencies must always execute first.

    final_execution_order = resolve_agent_execution_order(
        priority_order
    )


    # ========================================================
    # STEP 6: GET PRIORITY DETAILS
    # ========================================================

    priority_details = []


    for agent_name in final_execution_order:

        if user_query:

            priority_detail = get_query_based_priority(

                agent_name,

                user_query
            )

        else:

            priority_detail = get_agent_priority_details(

                agent_name
            )


        priority_details.append(

            priority_detail
        )


    # ========================================================
    # RETURN COMPLETE EXECUTION PLAN
    # ========================================================

    return {

        "requested_agents": agents_to_run,

        "dependency_order": dependency_order,

        "priority_order": priority_order,

        "final_execution_order": final_execution_order,

        "priority_details": priority_details
    }