# ============================================================
# GENESIS AI - WORKFLOW STATUS ENGINE
# ============================================================


def build_workflow_status(workflow_results):

    status_summary = {

        "total_agents": 0,

        "successful_agents": [],

        "failed_agents": [],

        "skipped_agents": [],

        "overall_status": "unknown"
    }


    # ========================================================
    # EMPTY WORKFLOW CHECK
    # ========================================================

    if not workflow_results:

        status_summary["overall_status"] = "empty"

        return status_summary


    # ========================================================
    # ANALYZE AGENT RESULTS
    # ========================================================

    status_summary["total_agents"] = len(
        workflow_results
    )


    for agent_name, result in workflow_results.items():

        # Safety check
        if not isinstance(result, dict):

            status_summary[
                "failed_agents"
            ].append(agent_name)

            continue


        agent_status = result.get(
            "status"
        )


        agent_success = result.get(
            "success",
            False
        )


        # ====================================================
        # SKIPPED AGENT
        # ====================================================

        if agent_status == "skipped":

            status_summary[
                "skipped_agents"
            ].append(agent_name)


        # ====================================================
        # SUCCESSFUL AGENT
        # ====================================================

        elif agent_success is True:

            status_summary[
                "successful_agents"
            ].append(agent_name)


        # ====================================================
        # FAILED AGENT
        # ====================================================

        else:

            status_summary[
                "failed_agents"
            ].append(agent_name)


    # ========================================================
    # DETERMINE OVERALL WORKFLOW STATUS
    # ========================================================

    successful_count = len(
        status_summary["successful_agents"]
    )

    failed_count = len(
        status_summary["failed_agents"]
    )

    skipped_count = len(
        status_summary["skipped_agents"]
    )


    if successful_count == status_summary["total_agents"]:

        status_summary[
            "overall_status"
        ] = "success"


    elif successful_count > 0:

        status_summary[
            "overall_status"
        ] = "partial_success"


    elif skipped_count == status_summary["total_agents"]:

        status_summary[
            "overall_status"
        ] = "skipped"


    else:

        status_summary[
            "overall_status"
        ] = "failed"


    # ========================================================
    # RETURN SUMMARY
    # ========================================================

    return status_summary