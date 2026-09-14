def save_optimization_memory(
    memory,
    optimization_profile
):
    if memory is None:
        memory = []

    if not optimization_profile:
        return memory

    memory.append({
        "agent":
            optimization_profile.get(
                "agent"
            ),

        "optimization_score":
            optimization_profile.get(
                "optimization_score",
                0
            ),

        "average_execution_time_seconds":
            optimization_profile.get(
                "average_execution_time_seconds",
                0
            ),

        "success_rate_percent":
            optimization_profile.get(
                "success_rate_percent",
                0
            ),

        "failure_rate_percent":
            optimization_profile.get(
                "failure_rate_percent",
                0
            ),

        "skip_rate_percent":
            optimization_profile.get(
                "skip_rate_percent",
                0
            )
    })

    return memory


def get_agent_optimization_memory(
    memory,
    agent_name
):
    if not memory:
        return []

    return [
        record
        for record in memory
        if record.get("agent") == agent_name
    ]


def calculate_historical_agent_score(
    memory,
    agent_name
):
    agent_memory = get_agent_optimization_memory(
        memory,
        agent_name
    )

    if not agent_memory:
        return 0

    scores = [
        record.get(
            "optimization_score",
            0
        )
        for record in agent_memory
        if record.get(
            "optimization_score"
        ) is not None
    ]

    if not scores:
        return 0

    average_score = sum(scores) / len(scores)

    return round(
        average_score,
        2
    )
