# ============================================================
# GENESIS AI - AGENT EXECUTOR
# ============================================================

from analyst_agent import run_analyst_agent
from quality_agent import run_quality_agent
from engineer_agent import run_engineer_agent
from forecast_agent import run_forecast_agent
from insights_agent import run_insights_agent
from recommendation_agent import run_recommendation_agent
from root_cause_agent import run_root_cause_analysis
from decision_agent import run_decision_agent
from reporting_agent import run_reporting_agent


def execute_agent(agent_name, df, context=None):
    """
    Executes the selected Genesis AI agent.
    """

    if df is None:
        return {
            "success": False,
            "message": "No dataset available. Please upload a dataset first."
        }

    try:

        # ========================================================
        # ANALYST AGENT
        # ========================================================

        if agent_name == "analyst_agent":

            result = run_analyst_agent(df)

        # ========================================================
        # QUALITY AGENT
        # ========================================================

        elif agent_name == "quality_agent":

            result = run_quality_agent(df)

        # ========================================================
        # ENGINEER AGENT
        # ========================================================

        elif agent_name == "engineer_agent":

            result = run_engineer_agent(df)

        # ========================================================
        # FORECAST AGENT
        # ========================================================

        elif agent_name == "forecast_agent":

            result = run_forecast_agent(df)

        # ========================================================
        # INSIGHTS AGENT
        # ========================================================

        elif agent_name == "insights_agent":

            result = run_insights_agent(
                df,
                context=context
            )

        # ========================================================
        # RECOMMENDATION AGENT
        # ========================================================

        elif agent_name == "recommendation_agent":

            result = run_recommendation_agent(
                df,
                context=context
            )

        # ========================================================
        # ROOT CAUSE AGENT
        # ========================================================

        elif agent_name == "root_cause_agent":

            result = run_root_cause_analysis(
                df,
                context=context
            )

        # ========================================================
        # DECISION AGENT
        # ========================================================

        elif agent_name == "decision_agent":

            result = run_decision_agent(
                df,
                context=context
            )

        # ========================================================
        # REPORTING AGENT
        # ========================================================

        elif agent_name == "reporting_agent":

            result = run_reporting_agent(
                df,
                context=context
            )

        # ========================================================
        # UNKNOWN AGENT
        # ========================================================

        else:

            return {
                "success": False,
                "message": f"Unknown agent: {agent_name}"
            }

        return {
    "success": True,
    "executed_agent": agent_name,
    "agent_result": result,

    "context_available": context is not None,

    "context_summary": {
        "workflow_id": context.get("workflow_id") if context else None,
        "user_query": context.get("user_query") if context else None,
        "previous_results_count": len(
            context.get("previous_agent_results", {})
        ) if context else 0
    }
}

    except Exception as e:

        return {
            "success": False,
            "executed_agent": agent_name,
            "error": str(e)
        }