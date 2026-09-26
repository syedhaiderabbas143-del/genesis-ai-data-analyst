# ============================================================
# GENESIS AI - PLANNER AGENT
# ============================================================

from datetime import datetime


def run_planner_agent(query):
    """
    Genesis AI Planner Agent

    Analyzes the user's query and creates an intelligent
    execution plan by selecting the required agents.
    """

    query_lower = query.lower()

    execution_plan = []

    # ========================================================
    # ROOT CAUSE ANALYSIS
    # ========================================================

    root_cause_keywords = [
        "why",
        "decreasing",
        "decrease",
        "problem",
        "issue",
        "reason",
        "cause",
        "drop",
        "loss"
    ]

    if any(keyword in query_lower for keyword in root_cause_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "root_cause_agent",
                "purpose": "Identify the possible root causes of the problem."
            }
        )

    # ========================================================
    # FORECAST ANALYSIS
    # ========================================================

    forecast_keywords = [
        "forecast",
        "predict",
        "prediction",
        "future",
        "next year",
        "next month"
    ]

    if any(keyword in query_lower for keyword in forecast_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "forecast_agent",
                "purpose": "Generate future predictions and forecasts."
            }
        )

    # ========================================================
    # DATA QUALITY ANALYSIS
    # ========================================================

    quality_keywords = [
        "quality",
        "missing",
        "duplicate",
        "clean",
        "error"
    ]

    if any(keyword in query_lower for keyword in quality_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "quality_agent",
                "purpose": "Analyze dataset quality and identify data issues."
            }
        )

    # ========================================================
    # INSIGHTS ANALYSIS
    # ========================================================

    insights_keywords = [
        "insight",
        "analyze",
        "analysis",
        "trend",
        "performance"
    ]

    if any(keyword in query_lower for keyword in insights_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "insights_agent",
                "purpose": "Generate meaningful insights from the dataset."
            }
        )

    # ========================================================
    # RECOMMENDATION ANALYSIS
    # ========================================================

    recommendation_keywords = [
        "recommend",
        "recommendation",
        "what should",
        "improve",
        "solution",
        "do"
    ]

    if any(keyword in query_lower for keyword in recommendation_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "recommendation_agent",
                "purpose": "Generate actionable recommendations."
            }
        )

    # ========================================================
    # DECISION ANALYSIS
    # ========================================================

    decision_keywords = [
        "decision",
        "choose",
        "best option",
        "strategy"
    ]

    if any(keyword in query_lower for keyword in decision_keywords):

        execution_plan.append(
            {
                "step": len(execution_plan) + 1,
                "agent": "decision_agent",
                "purpose": "Support decision-making using data analysis."
            }
        )

    # ========================================================
    # DEFAULT PLAN
    # ========================================================

    if not execution_plan:

        execution_plan = [

            {
                "step": 1,
                "agent": "analyst_agent",
                "purpose": "Perform general dataset analysis."
            },

            {
                "step": 2,
                "agent": "insights_agent",
                "purpose": "Generate important insights."
            }

        ]

    # ========================================================
    # RETURN EXECUTION PLAN
    # ========================================================

    return {

        "success": True,

        "planner": "Genesis AI Planner Agent",

        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "user_query": query,

        "total_steps": len(execution_plan),

        "execution_plan": execution_plan

    }