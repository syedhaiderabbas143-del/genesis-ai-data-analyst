# ============================================================
# GENESIS AI - PLANNED WORKFLOW
# ============================================================

from planner_agent import run_planner_agent
from agent_executor import execute_agent
from workflow_memory import WorkflowMemory


def run_planned_workflow(query, df):
    """
    Creates an execution plan using Planner Agent,
    executes agents step-by-step,
    and passes previous agent results as context.
    """

    # ========================================================
    # CHECK DATASET
    # ========================================================

    if df is None:
        return {
            "success": False,
            "message": "No dataset available. Please upload a dataset first."
        }

    try:

        # ====================================================
        # STEP 0: CREATE WORKFLOW MEMORY
        # ====================================================

        memory = WorkflowMemory(
            user_query=query
        )

        # ====================================================
        # STEP 1: GENERATE EXECUTION PLAN
        # ====================================================

        planner_result = run_planner_agent(query)

        if not planner_result.get("success"):

            memory.set_context(
                "planner_error",
                planner_result
            )

            return {
                "success": False,
                "message": "Planner Agent failed to create an execution plan.",
                "planner_result": planner_result,
                "workflow_memory": memory.get_memory()
            }

        execution_plan = planner_result.get(
            "execution_plan",
            []
        )

        # ====================================================
        # STEP 2: SAVE PLAN IN MEMORY
        # ====================================================

        memory.set_plan(
            execution_plan
        )

        memory.set_context(
            "planner_result",
            planner_result
        )

        # ====================================================
        # STEP 3: EXECUTE PLANNED AGENTS
        # ====================================================

        workflow_results = {}

        successful_agents = []

        failed_agents = []

        for plan_step in execution_plan:

            agent_name = plan_step.get(
                "agent"
            )

            # ================================================
            # BUILD AGENT CONTEXT
            # ================================================

            agent_context = {

                "workflow_id":
                    memory.workflow_id,

                "user_query":
                    query,

                "previous_agent_results":
                    memory.get_all_results(),

                "shared_context":
                    memory.shared_context
            }

            # ================================================
            # EXECUTE AGENT WITH CONTEXT
            # ================================================

            execution_result = execute_agent(
                agent_name,
                df,
                context=agent_context
            )

            # ================================================
            # SAVE RESULT IN WORKFLOW MEMORY
            # ================================================

            memory.save_agent_result(
                agent_name,
                execution_result
            )

            # ================================================
            # STORE WORKFLOW RESULT
            # ================================================

            workflow_results[agent_name] = {

                "step":
                    plan_step.get("step"),

                "purpose":
                    plan_step.get("purpose"),

                "execution_result":
                    execution_result
            }

            # ================================================
            # TRACK SUCCESS / FAILURE
            # ================================================

            if execution_result.get("success"):

                successful_agents.append(
                    agent_name
                )

            else:

                failed_agents.append(
                    agent_name
                )

        # ====================================================
        # STEP 4: SAVE WORKFLOW SUMMARY IN MEMORY
        # ====================================================

        memory.set_context(
            "successful_agents",
            successful_agents
        )

        memory.set_context(
            "failed_agents",
            failed_agents
        )

        memory.set_context(
            "total_agents_executed",
            len(execution_plan)
        )

        # ====================================================
        # STEP 5: RETURN COMPLETE WORKFLOW
        # ====================================================

        return {

            "success": True,

            "workflow_type":
                "Genesis AI Planned Workflow with Context Intelligence",

            "workflow_id":
                memory.workflow_id,

            "user_query":
                query,

            "planner_result":
                planner_result,

            "total_planned_agents":
                len(execution_plan),

            "successful_agents":
                successful_agents,

            "failed_agents":
                failed_agents,

            "workflow_results":
                workflow_results,

            "workflow_memory":
                memory.get_memory()
        }

    except Exception as e:

        return {

            "success": False,

            "error":
                str(e)
        }