# ============================================================
# GENESIS AI - AGENT EXECUTION HISTORY
# ============================================================

from datetime import datetime


# ============================================================
# CREATE EXECUTION HISTORY RECORD
# ============================================================

def create_execution_history_record(
    workflow_id,
    agent_name,
    execution_time_seconds,
    status
):

    return {

        "workflow_id": workflow_id,

        "agent": agent_name,

        "execution_time_seconds":
            execution_time_seconds,

        "status": status,

        "timestamp":
            datetime.now().isoformat()
    }


# ============================================================
# ADD RECORD TO HISTORY
# ============================================================

def add_execution_history(
    history,
    workflow_id,
    agent_name,
    execution_time_seconds,
    status
):

    if history is None:

        history = []


    record = create_execution_history_record(

        workflow_id,

        agent_name,

        execution_time_seconds,

        status
    )


    history.append(record)


    return history


# ============================================================
# GET AGENT HISTORY
# ============================================================

def get_agent_execution_history(
    history,
    agent_name
):

    if not history:

        return []


    return [

        record

        for record in history

        if record.get("agent") == agent_name
    ]


# ============================================================
# GET WORKFLOW HISTORY
# ============================================================

def get_workflow_execution_history(
    history,
    workflow_id
):

    if not history:

        return []


    return [

        record

        for record in history

        if record.get("workflow_id") == workflow_id
    ]