# ============================================================
# GENESIS AI - WORKFLOW MEMORY
# ============================================================

from datetime import datetime


class WorkflowMemory:
    """
    Shared memory system for Genesis AI multi-agent workflows.

    Stores:
    - User query
    - Workflow plan
    - Agent results
    - Shared context
    - Workflow history
    """

    def __init__(self, user_query=None):

        self.workflow_id = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.created_at = datetime.now().isoformat()

        self.user_query = user_query

        self.plan = []

        self.agent_results = {}

        self.shared_context = {}

        self.history = []


    # ========================================================
    # SET WORKFLOW PLAN
    # ========================================================

    def set_plan(self, plan):

        self.plan = plan

        self._add_history(
            action="workflow_plan_created",
            details={
                "total_steps": len(plan)
            }
        )


    # ========================================================
    # SAVE AGENT RESULT
    # ========================================================

    def save_agent_result(self, agent_name, result):

        self.agent_results[agent_name] = result

        self._add_history(
            action="agent_result_saved",
            details={
                "agent": agent_name
            }
        )


    # ========================================================
    # GET AGENT RESULT
    # ========================================================

    def get_agent_result(self, agent_name):

        return self.agent_results.get(agent_name)


    # ========================================================
    # SAVE SHARED CONTEXT
    # ========================================================

    def set_context(self, key, value):

        self.shared_context[key] = value


    # ========================================================
    # GET SHARED CONTEXT
    # ========================================================

    def get_context(self, key, default=None):

        return self.shared_context.get(key, default)


    # ========================================================
    # GET ALL PREVIOUS RESULTS
    # ========================================================

    def get_all_results(self):

        return self.agent_results


    # ========================================================
    # ADD HISTORY
    # ========================================================

    def _add_history(self, action, details=None):

        history_entry = {

            "timestamp": datetime.now().isoformat(),

            "action": action,

            "details": details or {}
        }

        self.history.append(history_entry)


    # ========================================================
    # GET COMPLETE MEMORY
    # ========================================================

    def get_memory(self):

        return {

            "workflow_id": self.workflow_id,

            "created_at": self.created_at,

            "user_query": self.user_query,

            "plan": self.plan,

            "agent_results": self.agent_results,

            "shared_context": self.shared_context,

            "history": self.history
        }


    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear_memory(self):

        self.plan = []

        self.agent_results = {}

        self.shared_context = {}

        self.history = []

        return {
            "success": True,
            "message": "Workflow memory cleared successfully."
        }