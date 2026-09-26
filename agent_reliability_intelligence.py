# ============================================================
# GENESIS AI - AGENT RELIABILITY INTELLIGENCE
# ============================================================


def analyze_agent_reliability(history):

    if not history:
        return {
            "total_records": 0,
            "agents_analyzed": 0,
            "reliability_summary": []
        }

    agent_groups = {}

    for record in history:

        agent_name = record.get("agent")

        if not agent_name:
            continue

        if agent_name not in agent_groups:
            agent_groups[agent_name] = []

        agent_groups[agent_name].append(
            record
        )

    reliability_summary = []

    for agent_name, records in agent_groups.items():

        total_executions = len(records)

        successful_executions = sum(
            1
            for record in records
            if record.get("status") == "success"
        )

        failed_executions = sum(
            1
            for record in records
            if record.get("status") == "failed"
        )

        skipped_executions = sum(
            1
            for record in records
            if record.get("status") == "skipped"
        )

        success_rate = (
            successful_executions /
            total_executions
        ) * 100

        failure_rate = (
            failed_executions /
            total_executions
        ) * 100

        skip_rate = (
            skipped_executions /
            total_executions
        ) * 100

        if success_rate >= 95:

            reliability = "excellent"

        elif success_rate >= 85:

            reliability = "good"

        elif success_rate >= 70:

            reliability = "medium"

        else:

            reliability = "poor"

        reliability_summary.append({

            "agent":
                agent_name,

            "total_executions":
                total_executions,

            "successful_executions":
                successful_executions,

            "failed_executions":
                failed_executions,

            "skipped_executions":
                skipped_executions,

            "success_rate_percent":
                round(success_rate, 2),

            "failure_rate_percent":
                round(failure_rate, 2),

            "skip_rate_percent":
                round(skip_rate, 2),

            "reliability":
                reliability
        })

    return {

        "total_records":
            len(history),

        "agents_analyzed":
            len(reliability_summary),

        "reliability_summary":
            reliability_summary
    }