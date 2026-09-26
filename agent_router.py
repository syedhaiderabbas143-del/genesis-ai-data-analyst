# ============================================================
# GENESIS AI - AGENT ROUTER
# ============================================================

def route_agent(user_query: str):
    """
    Routes the user query to the most appropriate Genesis AI agent.
    """

    if not user_query:
        return {
            "success": False,
            "message": "Please provide a question for analysis."
        }

    query = user_query.lower()

    # ============================================================
    # FORECAST AGENT
    # ============================================================

    forecast_keywords = [
        "forecast",
        "predict",
        "prediction",
        "future",
        "next month",
        "next year",
        "trend forecast",
        "estimate future"
    ]

    if any(keyword in query for keyword in forecast_keywords):
        return {
            "success": True,
            "selected_agent": "forecast_agent",
            "reason": "Forecasting or prediction request detected"
        }

    # ============================================================
    # QUALITY AGENT
    # ============================================================

    quality_keywords = [
        "quality",
        "missing values",
        "missing data",
        "duplicate",
        "duplicates",
        "null values",
        "clean data",
        "data quality"
    ]

    if any(keyword in query for keyword in quality_keywords):
        return {
            "success": True,
            "selected_agent": "quality_agent",
            "reason": "Data quality request detected"
        }

    # ============================================================
    # ROOT CAUSE AGENT
    # ============================================================

    root_cause_keywords = [
        "root cause",
        "why",
        "problem",
        "issue",
        "reason",
        "cause",
        "what caused",
        "why happened"
    ]

    if any(keyword in query for keyword in root_cause_keywords):
        return {
            "success": True,
            "selected_agent": "root_cause_agent",
            "reason": "Root cause analysis request detected"
        }

    # ============================================================
    # RECOMMENDATION AGENT
    # ============================================================

    recommendation_keywords = [
        "recommend",
        "recommendation",
        "suggest",
        "suggestion",
        "improve",
        "improvement",
        "what should i do",
        "best action"
    ]

    if any(keyword in query for keyword in recommendation_keywords):
        return {
            "success": True,
            "selected_agent": "recommendation_agent",
            "reason": "Recommendation request detected"
        }

    # ============================================================
    # DECISION AGENT
    # ============================================================

    decision_keywords = [
        "decision",
        "decide",
        "choose",
        "which option",
        "best option",
        "compare options",
        "should we"
    ]

    if any(keyword in query for keyword in decision_keywords):
        return {
            "success": True,
            "selected_agent": "decision_agent",
            "reason": "Decision-making request detected"
        }

    # ============================================================
    # REPORTING AGENT
    # ============================================================

    reporting_keywords = [
        "report",
        "summary",
        "executive summary",
        "business report",
        "analysis report"
    ]

    if any(keyword in query for keyword in reporting_keywords):
        return {
            "success": True,
            "selected_agent": "reporting_agent",
            "reason": "Reporting request detected"
        }

    # ============================================================
    # INSIGHTS AGENT
    # ============================================================

    insights_keywords = [
        "insight",
        "insights",
        "important findings",
        "key findings",
        "discover",
        "patterns"
    ]

    if any(keyword in query for keyword in insights_keywords):
        return {
            "success": True,
            "selected_agent": "insights_agent",
            "reason": "Insights request detected"
        }

    # ============================================================
    # ENGINEER AGENT
    # ============================================================

    engineer_keywords = [
        "engineer",
        "feature",
        "transformation",
        "feature engineering",
        "derived column"
    ]

    if any(keyword in query for keyword in engineer_keywords):
        return {
            "success": True,
            "selected_agent": "engineer_agent",
            "reason": "Data engineering request detected"
        }

    # ============================================================
    # ANALYST AGENT (DEFAULT)
    # ============================================================

    return {
        "success": True,
        "selected_agent": "analyst_agent",
        "reason": "General data analysis request detected"
    }