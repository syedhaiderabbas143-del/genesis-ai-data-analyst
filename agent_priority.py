# ============================================================
# GENESIS AI - AGENT PRIORITY ENGINE
# ============================================================


# ============================================================
# DEFAULT AGENT PRIORITIES
# ============================================================

AGENT_PRIORITIES = {

    "quality_agent": 90,

    "root_cause_agent": 85,

    "analyst_agent": 80,

    "insights_agent": 75,

    "recommendation_agent": 70,

    "forecast_agent": 65,

    "decision_agent": 60,

    "engineer_agent": 55,

    "reporting_agent": 50
}


# ============================================================
# GET AGENT PRIORITY
# ============================================================

def get_agent_priority(agent_name):

    return AGENT_PRIORITIES.get(
        agent_name,
        0
    )


# ============================================================
# SORT AGENTS BY PRIORITY
# ============================================================

def sort_agents_by_priority(agents):

    return sorted(

        agents,

        key=lambda agent: get_agent_priority(agent),

        reverse=True
    )


# ============================================================
# GET PRIORITY LEVEL
# ============================================================

def get_priority_level(priority):

    if priority >= 80:

        return "critical"

    elif priority >= 60:

        return "high"

    elif priority >= 40:

        return "medium"

    else:

        return "low"


# ============================================================
# GET AGENT PRIORITY DETAILS
# ============================================================

def get_agent_priority_details(agent_name):

    priority = get_agent_priority(agent_name)

    return {

        "agent": agent_name,

        "priority": priority,

        "priority_level": get_priority_level(
            priority
        )
    }
# ============================================================
# QUERY-BASED PRIORITY BOOST RULES
# ============================================================

QUERY_PRIORITY_RULES = {

    "root_cause": {

        "keywords": [

            "why",

            "problem",

            "issue",

            "decreasing",

            "decrease",

            "drop",

            "decline"
        ],

        "agents": {

            "root_cause_agent": 30,

            "insights_agent": 20
        }
    },


    "recommendation": {

        "keywords": [

            "recommend",

            "suggest",

            "improve",

            "improvement",

            "what should",

            "how can"
        ],

        "agents": {

            "recommendation_agent": 30,

            "decision_agent": 20
        }
    },


    "forecast": {

        "keywords": [

            "predict",

            "forecast",

            "future",

            "next month",

            "next year"
        ],

        "agents": {

            "forecast_agent": 40,

            "analyst_agent": 15
        }
    },


    "data_quality": {

        "keywords": [

            "missing",

            "duplicate",

            "clean",

            "quality",

            "error"
        ],

        "agents": {

            "quality_agent": 30,

            "engineer_agent": 20
        }
    }
}


# ============================================================
# GET QUERY-BASED AGENT PRIORITY
# ============================================================

def get_query_based_priority(agent_name, query):

    # Get default priority
    priority = get_agent_priority(
        agent_name
    )


    # Safety check
    if not query:

        return priority


    query_lower = query.lower()


    # ========================================================
    # CHECK QUERY RULES
    # ========================================================

    for rule in QUERY_PRIORITY_RULES.values():

        keywords = rule.get(
            "keywords",
            []
        )

        agent_boosts = rule.get(
            "agents",
            {}
        )


        # Check keyword match
        keyword_found = any(

            keyword in query_lower

            for keyword in keywords
        )


        if keyword_found:

            priority_boost = agent_boosts.get(
                agent_name,
                0
            )

            priority += priority_boost


    return priority


# ============================================================
# SORT AGENTS BY QUERY PRIORITY
# ============================================================

def sort_agents_by_query_priority(agents, query):

    return sorted(

        agents,

        key=lambda agent: get_query_based_priority(
            agent,
            query
        ),

        reverse=True
    )


# ============================================================
# GET QUERY PRIORITY DETAILS
# ============================================================

def get_query_priority_details(agent_name, query):

    base_priority = get_agent_priority(
        agent_name
    )


    final_priority = get_query_based_priority(
        agent_name,
        query
    )


    return {

        "agent": agent_name,

        "base_priority": base_priority,

        "final_priority": final_priority,

        "priority_boost": (

            final_priority - base_priority

        ),

        "priority_level": get_priority_level(
            final_priority
        )
    }