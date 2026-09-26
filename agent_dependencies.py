# ============================================================
# GENESIS AI - AGENT DEPENDENCY ENGINE
# ============================================================


# ============================================================
# AGENT DEPENDENCY RULES
# ============================================================

AGENT_DEPENDENCIES = {

    "analyst_agent": [],

    "quality_agent": [],

    "engineer_agent": [
        "quality_agent"
    ],

    "root_cause_agent": [
        "quality_agent"
    ],

    "forecast_agent": [
        "analyst_agent"
    ],

    "insights_agent": [
        "analyst_agent"
    ],

    "recommendation_agent": [
        "root_cause_agent",
        "insights_agent"
    ],

    "decision_agent": [
        "root_cause_agent",
        "insights_agent",
        "recommendation_agent"
    ],

    "reporting_agent": [
        "insights_agent",
        "recommendation_agent",
        "decision_agent"
    ]
}


# ============================================================
# GET AGENT DEPENDENCIES
# ============================================================

def get_agent_dependencies(agent_name):

    return AGENT_DEPENDENCIES.get(
        agent_name,
        []
    )


# ============================================================
# RESOLVE AGENT EXECUTION ORDER
# ============================================================

def resolve_agent_execution_order(agents_to_run):

    resolved_agents = []

    visiting_agents = set()


    def resolve_agent(agent_name):

        # ----------------------------------------------------
        # ALREADY RESOLVED
        # ----------------------------------------------------

        if agent_name in resolved_agents:

            return


        # ----------------------------------------------------
        # CIRCULAR DEPENDENCY PROTECTION
        # ----------------------------------------------------

        if agent_name in visiting_agents:

            return


        visiting_agents.add(agent_name)


        # ----------------------------------------------------
        # RESOLVE DEPENDENCIES FIRST
        # ----------------------------------------------------

        dependencies = get_agent_dependencies(
            agent_name
        )


        for dependency in dependencies:

         resolve_agent(
        dependency
    )


        # ----------------------------------------------------
        # ADD CURRENT AGENT
        # ----------------------------------------------------

        visiting_agents.remove(
            agent_name
        )

        if agent_name not in resolved_agents:

            resolved_agents.append(
                agent_name
            )


    # ========================================================
    # RESOLVE ALL REQUESTED AGENTS
    # ========================================================

    for agent in agents_to_run:

        resolve_agent(agent)


    return resolved_agents

# ============================================================
# AUTOMATIC DEPENDENCY INJECTION
# ============================================================

def inject_agent_dependencies(agents_to_run):

    expanded_agents = list(agents_to_run)


    def add_dependencies(agent_name):

        dependencies = get_agent_dependencies(
            agent_name
        )


        for dependency in dependencies:

            # --------------------------------------------
            # ADD MISSING DEPENDENCY
            # --------------------------------------------

            if dependency not in expanded_agents:

                expanded_agents.append(
                    dependency
                )


            # --------------------------------------------
            # RECURSIVE DEPENDENCY CHECK
            # --------------------------------------------

            add_dependencies(
                dependency
            )


    # ========================================================
    # CHECK ALL REQUESTED AGENTS
    # ========================================================

    for agent_name in list(expanded_agents):

        add_dependencies(
            agent_name
        )


    # ========================================================
    # RETURN CORRECT EXECUTION ORDER
    # ========================================================

    return resolve_agent_execution_order(
        expanded_agents
    )

# ============================================================
# CHECK FAILED AGENT DEPENDENCIES
# ============================================================

def get_failed_dependencies(
    agent_name,
    previous_agent_results
):

    failed_dependencies = []

    dependencies = get_agent_dependencies(
        agent_name
    )

    for dependency in dependencies:

        dependency_result = previous_agent_results.get(
            dependency
        )

        # Dependency has not executed
        if dependency_result is None:

            failed_dependencies.append(
                dependency
            )

            continue

        # Dependency execution failed
        if not dependency_result.get(
            "success",
            False
        ):

            failed_dependencies.append(
                dependency
            )

    return failed_dependencies