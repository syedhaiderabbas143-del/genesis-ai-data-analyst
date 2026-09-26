# ============================================================
# GENESIS AI - AGENT EXECUTION METRICS
# ============================================================

import time


# ============================================================
# START AGENT TIMER
# ============================================================

def start_agent_timer():

    return time.perf_counter()


# ============================================================
# STOP AGENT TIMER
# ============================================================

def stop_agent_timer(start_time):

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return round(
        execution_time,
        4
    )


# ============================================================
# CREATE AGENT METRIC
# ============================================================

def create_agent_metric(
    agent_name,
    execution_time,
    status
):

    return {

        "agent": agent_name,

        "execution_time_seconds": execution_time,

        "status": status
    }


# ============================================================
# CALCULATE WORKFLOW METRICS
# ============================================================

def calculate_workflow_metrics(
    agent_metrics,
    workflow_execution_time
):

    if not agent_metrics:

        return {

            "total_agents": 0,

            "successful_agents": 0,

            "failed_agents": 0,

            "skipped_agents": 0,

            "total_execution_time_seconds":
                workflow_execution_time,

            "fastest_agent": None,

            "slowest_agent": None
        }


    successful_agents = [

        metric

        for metric in agent_metrics

        if metric.get("status") == "success"
    ]


    failed_agents = [

        metric

        for metric in agent_metrics

        if metric.get("status") == "failed"
    ]


    skipped_agents = [

        metric

        for metric in agent_metrics

        if metric.get("status") == "skipped"
    ]


    # ========================================================
    # FASTEST / SLOWEST AGENT
    # ========================================================

    executed_agents = [

        metric

        for metric in agent_metrics

        if metric.get("status") == "success"
    ]


    fastest_agent = None

    slowest_agent = None


    if executed_agents:

        fastest_agent = min(

            executed_agents,

            key=lambda metric:
                metric.get(
                    "execution_time_seconds",
                    0
                )
        )


        slowest_agent = max(

            executed_agents,

            key=lambda metric:
                metric.get(
                    "execution_time_seconds",
                    0
                )
        )


    # ========================================================
    # RETURN METRICS
    # ========================================================

    return {

        "total_agents": len(agent_metrics),

        "successful_agents": len(
            successful_agents
        ),

        "failed_agents": len(
            failed_agents
        ),

        "skipped_agents": len(
            skipped_agents
        ),

        "total_execution_time_seconds":

            round(
                workflow_execution_time,
                4
            ),

        "fastest_agent":

            fastest_agent,

        "slowest_agent":

            slowest_agent
    }