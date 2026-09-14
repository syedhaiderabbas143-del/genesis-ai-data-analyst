# ==========================================
# Genesis AI Multi-Agent Orchestrator
# ==========================================

from datetime import datetime


def run_orchestrator_agent(
    df,
    run_analyst_agent,
    run_quality_agent,
    run_engineer_agent,
    run_forecast_agent,
    run_insights_agent,
    run_recommendation_agent,
    run_root_cause_agent,
    run_decision_agent,
    run_reporting_agent
):

    try:

        # ==========================================
        # Basic Dataset Validation
        # ==========================================

        if df is None or df.empty:

            return {
                "success": False,
                "message": "No dataset available for orchestration."
            }


        # ==========================================
        # Run All AI Agents
        # ==========================================

        agent_results = {}


        # 1. Analyst Agent
        try:
            agent_results["analyst_agent"] = run_analyst_agent(df)
        except Exception as e:
            agent_results["analyst_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 2. Quality Agent
        try:
            agent_results["quality_agent"] = run_quality_agent(df)
        except Exception as e:
            agent_results["quality_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 3. Engineer Agent
        try:
            agent_results["engineer_agent"] = run_engineer_agent(df)
        except Exception as e:
            agent_results["engineer_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 4. Forecast Agent
        try:
            agent_results["forecast_agent"] = run_forecast_agent(df)
        except Exception as e:
            agent_results["forecast_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 5. Insights Agent
        try:
            agent_results["insights_agent"] = run_insights_agent(df)
        except Exception as e:
            agent_results["insights_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 6. Recommendation Agent
        try:
            agent_results["recommendation_agent"] = run_recommendation_agent(df)
        except Exception as e:
            agent_results["recommendation_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 7. Root Cause Agent
        try:
            agent_results["root_cause_agent"] = run_root_cause_agent(df)
        except Exception as e:
            agent_results["root_cause_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 8. Decision Agent
        try:
            agent_results["decision_agent"] = run_decision_agent(df)
        except Exception as e:
            agent_results["decision_agent"] = {
                "success": False,
                "error": str(e)
            }


        # 9. Reporting Agent
        try:
            agent_results["reporting_agent"] = run_reporting_agent(df)
        except Exception as e:
            agent_results["reporting_agent"] = {
                "success": False,
                "error": str(e)
            }


        # ==========================================
        # Agent Execution Summary
        # ==========================================

        successful_agents = []

        failed_agents = []


        for agent_name, result in agent_results.items():

            if result.get("success") is True:

                successful_agents.append(agent_name)

            else:

                failed_agents.append(agent_name)


        # ==========================================
        # Final Orchestration Response
        # ==========================================

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Multi-Agent Orchestration",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "orchestrator_status":
                "Completed",

            "dataset_overview": {

                "total_rows":
                    int(df.shape[0]),

                "total_columns":
                    int(df.shape[1])

            },

            "agent_execution_summary": {

                "total_agents":
                    len(agent_results),

                "successful_agents":
                    len(successful_agents),

                "failed_agents":
                    len(failed_agents),

                "successful_agent_names":
                    successful_agents,

                "failed_agent_names":
                    failed_agents

            },

            "agent_results":
                agent_results,

            "final_message":
                (
                    "Genesis AI successfully completed "
                    "multi-agent dataset analysis."
                )

        }


    except Exception as e:

        return {

            "success": False,

            "message":
                "Multi-Agent Orchestration failed.",

            "error":
                str(e)

        }