# ============================================================
# GENESIS AI - AGENT PERFORMANCE INTELLIGENCE
# ============================================================

def analyze_agent_performance(history):

    if not history:
        return {
            "total_records": 0,
            "agents_analyzed": 0,
            "performance_summary": [],
            "fastest_agent": None,
            "slowest_agent": None
        }

    agent_groups = {}

    for record in history:

        agent_name = record.get("agent")

        if not agent_name:
            continue

        if agent_name not in agent_groups:
            agent_groups[agent_name] = []

        agent_groups[agent_name].append(record)

    performance_summary = []

    for agent_name, records in agent_groups.items():

        execution_times = [
            record.get(
                "execution_time_seconds",
                0
            )
            for record in records
            if record.get(
                "execution_time_seconds"
            ) is not None
        ]

        if not execution_times:
            continue

        total_time = sum(
            execution_times
        )

        average_time = (
            total_time /
            len(execution_times)
        )

        success_count = sum(
            1
            for record in records
            if record.get("status") == "success"
        )

        failed_count = sum(
            1
            for record in records
            if record.get("status") == "failed"
        )

        skipped_count = sum(
            1
            for record in records
            if record.get("status") == "skipped"
        )

        performance_summary.append({
            "agent": agent_name,
            "execution_count": len(records),
            "average_execution_time_seconds":
                round(average_time, 4),
            "total_execution_time_seconds":
                round(total_time, 4),
            "successful_executions":
                success_count,
            "failed_executions":
                failed_count,
            "skipped_executions":
                skipped_count
        })

    fastest_agent = None
    slowest_agent = None

    if performance_summary:

        fastest_agent = min(
            performance_summary,
            key=lambda item:
                item[
                    "average_execution_time_seconds"
                ]
        )

        slowest_agent = max(
            performance_summary,
            key=lambda item:
                item[
                    "average_execution_time_seconds"
                ]
        )

    return {
        "total_records": len(history),
        "agents_analyzed":
            len(performance_summary),
        "performance_summary":
            performance_summary,
        "fastest_agent":
            fastest_agent,
        "slowest_agent":
            slowest_agent
    }
