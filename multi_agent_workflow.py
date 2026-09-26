# ============================================================
# GENESIS AI - MULTI AGENT WORKFLOW ENGINE
# ============================================================

import uuid

from agent_router import route_agent

from agent_execution_metrics import (
    start_agent_timer,
    stop_agent_timer,
    create_agent_metric,
    calculate_workflow_metrics
)
from agent_priority import (
    get_query_based_priority
)

from agent_optimization_memory import (
    save_optimization_memory,
    get_agent_optimization_memory,
    calculate_historical_agent_score
)

from agent_self_optimization import (
    add_optimization_history,
    build_agent_optimization_profile,
    select_best_agent,
    get_preferred_agent,
    generate_optimization_recommendation,
    get_agent_optimization_action,
    calculate_combined_agent_score,
    select_best_agent_by_combined_score,
    calculate_query_aware_agent_score,
    calculate_agent_selection_confidence,
    get_confidence_based_decision_policy,
    get_validation_agents,
        compare_agent_validation_results,
    select_final_result_source,
    build_final_validation_decision, 
    assess_final_result_quality,
    assess_semantic_result_agreement,
    assess_semantic_result_agreement_v2,
    build_semantic_decision_policy,
    build_combined_intelligence_decision
    
)

from agent_reliability_intelligence import (
    analyze_agent_reliability
)

from agent_performance_intelligence import (
    analyze_agent_performance
)

from agent_execution_history import (
    add_execution_history
)

from agent_executor import execute_agent

from context_intelligence import (
    build_context_intelligence
)

from workflow_status import (
    build_workflow_status
)

from agent_execution_planner import (
    create_agent_execution_plan
)

from agent_dependencies import (
    resolve_agent_execution_order,
    get_failed_dependencies
)


# ============================================================
# H3-F STEP 8D
# PERSISTENT OPTIMIZATION MEMORY
# ============================================================

# In-memory optimization history shared across workflow runs
# while the Python process is running.
OPTIMIZATION_MEMORY = []


# ============================================================
# MAIN MULTI AGENT WORKFLOW
# ============================================================

def run_multi_agent_workflow(query, df):

    if df is None:

        return {
            "success": False,
            "message": (
                "No dataset available. "
                "Please upload a dataset first."
            )
        }

    # ========================================================
    # START COMPLETE WORKFLOW TIMER
    # ========================================================

    workflow_start_time = start_agent_timer()

    try:

        # ====================================================
        # STEP 1: ROUTE PRIMARY AGENT
        # ====================================================

        routing_result = route_agent(query)

        if not routing_result.get("success"):

            return {
                "success": False,
                "message": "Agent routing failed.",
                "routing_result": routing_result
            }

        primary_agent = routing_result.get(
            "selected_agent"
        )

        # ====================================================
        # STEP 2: CREATE AGENT WORKFLOW
        # ====================================================

        agents_to_run = []

        # Add primary agent first
        if primary_agent:
            agents_to_run.append(
                primary_agent
            )

        query_lower = query.lower()

        # ====================================================
        # ROOT CAUSE WORKFLOW
        # ====================================================

        if (
            "why" in query_lower
            or "decreasing" in query_lower
            or "decrease" in query_lower
            or "problem" in query_lower
            or "issue" in query_lower
        ):

            for agent in [
                "root_cause_agent",
                "insights_agent"
            ]:

                if agent not in agents_to_run:
                    agents_to_run.append(agent)

        # ====================================================
        # RECOMMENDATION WORKFLOW
        # ====================================================

        if (
            "recommend" in query_lower
            or "suggest" in query_lower
            or "what should" in query_lower
            or "improve" in query_lower
            or "increase" in query_lower
        ):

            for agent in [
                "recommendation_agent",
                "decision_agent"
            ]:

                if agent not in agents_to_run:
                    agents_to_run.append(agent)

        # ====================================================
        # FORECAST WORKFLOW
        # ====================================================

        if (
            "predict" in query_lower
            or "forecast" in query_lower
            or "future" in query_lower
            or "next year" in query_lower
            or "next month" in query_lower
        ):

            for agent in [
                "forecast_agent",
                "insights_agent"
            ]:

                if agent not in agents_to_run:
                    agents_to_run.append(agent)

        # ====================================================
        # DATA QUALITY WORKFLOW
        # ====================================================

        if (
            "quality" in query_lower
            or "missing" in query_lower
            or "clean" in query_lower
            or "duplicate" in query_lower
        ):

            for agent in [
                "quality_agent",
                "engineer_agent"
            ]:

                if agent not in agents_to_run:
                    agents_to_run.append(agent)

        # ====================================================
        # STEP 2I: RESOLVE AGENT DEPENDENCY ORDER
        # ====================================================

        agents_to_run = resolve_agent_execution_order(
            agents_to_run
        )

        # ====================================================
        # STEP 2I-G: CREATE AGENT EXECUTION PLAN
        # ====================================================

        execution_plan = create_agent_execution_plan(
            agents_to_run,
            query
        )

        # ====================================================
        # GET SAFE FINAL EXECUTION ORDER
        # ====================================================

        agents_to_run = execution_plan.get(
            "final_execution_order",
            agents_to_run
        )

        # ====================================================
        # STEP 3: EXECUTE ALL AGENTS WITH SEQUENTIAL CONTEXT
        # ====================================================

        workflow_results = {}

        agent_metrics = []

        # Unique ID for this workflow
        workflow_id = str(
            uuid.uuid4()
        )

        # Results from agents that already executed
        previous_agent_results = {}

        # Current workflow execution history
        execution_history = []

        # Current workflow optimization history
        optimization_history = []

        # ====================================================
        # EXECUTE AGENTS
        # ====================================================

        for agent_name in agents_to_run:

            agent_start_time = start_agent_timer()

            # ================================================
            # STEP 2I-E: CHECK FAILED DEPENDENCIES
            # ================================================

            failed_dependencies = get_failed_dependencies(
                agent_name,
                previous_agent_results
            )

            if failed_dependencies:

                skipped_result = {
                    "success": False,
                    "executed_agent": agent_name,
                    "status": "skipped",
                    "message": (
                        "Agent skipped because required "
                        "dependencies failed or were unavailable."
                    ),
                    "failed_dependencies": (
                        failed_dependencies
                    )
                }

                workflow_results[
                    agent_name
                ] = skipped_result

                previous_agent_results[
                    agent_name
                ] = skipped_result

                # ============================================
                # RECORD SKIPPED AGENT METRIC
                # ============================================

                agent_execution_time = stop_agent_timer(
                    agent_start_time
                )

                agent_metric = create_agent_metric(
                    agent_name,
                    agent_execution_time,
                    "skipped"
                )

                agent_metrics.append(
                    agent_metric
                )

                execution_history = add_execution_history(
                    execution_history,
                    workflow_id,
                    agent_name,
                    agent_execution_time,
                    "skipped"
                )

                continue

            # ================================================
            # BUILD CONTEXT FROM PREVIOUS AGENTS
            # ================================================

            if previous_agent_results:

                context_intelligence = (
                    build_context_intelligence(
                        previous_agent_results
                    )
                )

            else:

                context_intelligence = {}

            # ================================================
            # BUILD AGENT CONTEXT
            # ================================================

            agent_context = {
                "workflow_id": workflow_id,
                "user_query": query,
                "current_agent": agent_name,

                "previous_agent_results":
                    previous_agent_results,

                "context_intelligence":
                    context_intelligence
            }

            # ================================================
            # EXECUTE AGENT
            # ================================================

            agent_result = execute_agent(
                agent_name,
                df,
                context=agent_context
            )

            # ================================================
            # SAVE RESULT FOR NEXT AGENTS
            # ================================================

            workflow_results[
                agent_name
            ] = agent_result

            previous_agent_results[
                agent_name
            ] = agent_result

            # ================================================
            # RECORD AGENT EXECUTION METRIC
            # ================================================

            agent_execution_time = stop_agent_timer(
                agent_start_time
            )

            if agent_result.get("success"):

                agent_status = "success"

            else:

                agent_status = "failed"

            agent_metric = create_agent_metric(
                agent_name,
                agent_execution_time,
                agent_status
            )

            agent_metrics.append(
                agent_metric
            )

            # IMPORTANT:
            # Record the actual status, not "skipped".
            execution_history = add_execution_history(
                execution_history,
                workflow_id,
                agent_name,
                agent_execution_time,
                agent_status
            )

        # ====================================================
        # STEP 2I-H2-E: CALCULATE WORKFLOW EXECUTION METRICS
        # ====================================================

        workflow_execution_time = stop_agent_timer(
            workflow_start_time
        )

        workflow_metrics = calculate_workflow_metrics(
            agent_metrics,
            workflow_execution_time
        )

        # ====================================================
        # H3-F STEP 8C:
        # PERFORMANCE & RELIABILITY INTELLIGENCE
        # ====================================================

        performance_intelligence = (
            analyze_agent_performance(
                execution_history
            )
        )

        reliability_intelligence = (
            analyze_agent_reliability(
                execution_history
            )
        )
        
                # ====================================================
        # H3-F STEP 8E:
        # HISTORICAL + COMBINED AGENT INTELLIGENCE
        # ====================================================

        historical_agent_scores = {}
        combined_agent_scores = {}

        optimization_profiles = (
            build_agent_optimization_profile(
                performance_intelligence.get(
                    "performance_summary",
                    []
                ),
                reliability_intelligence.get(
                    "reliability_summary",
                    []
                )
            )
        )

        # ====================================================
        # CURRENT BEST AGENT
        # ====================================================

                # CURRENT BEST AGENT

        # Safety guard:
        # Optimization profile generation may return None.
        optimization_profiles = optimization_profiles or []

        best_agent = select_best_agent(
            optimization_profiles
        )

                # ====================================================
        # CALCULATE HISTORICAL + COMBINED + QUERY-AWARE SCORES
        # ====================================================

        for optimization_profile in (optimization_profiles or []):
            agent_name = optimization_profile.get(
                "agent"
            )

            # ------------------------------------------------
            # HISTORICAL SCORE
            # ------------------------------------------------

            historical_score = (
                calculate_historical_agent_score(
                    OPTIMIZATION_MEMORY,
                    agent_name
                )
            )

            historical_agent_scores[
                agent_name
            ] = historical_score

            # ------------------------------------------------
            # CURRENT OPTIMIZATION SCORE
            # ------------------------------------------------

            current_score = optimization_profile.get(
                "optimization_score",
                0
            )

            # ------------------------------------------------
            # COMBINED SCORE
            # ------------------------------------------------

            combined_score = (
                calculate_combined_agent_score(
                    current_score,
                    historical_score
                )
            )

            combined_agent_scores[
                agent_name
            ] = combined_score

            # ------------------------------------------------
            # QUERY PRIORITY
            # ------------------------------------------------

            query_priority_result = get_query_based_priority(
                agent_name,
                query
            )

            if isinstance(
                query_priority_result,
                dict
            ):

                query_priority_score = (
                    query_priority_result.get(
                        "final_priority",
                        query_priority_result.get(
                            "priority",
                            0
                        )
                    )
                )

            else:

                query_priority_score = (
                    query_priority_result
                )

            # ------------------------------------------------
            # QUERY-AWARE SCORE
            # ------------------------------------------------

            query_aware_score = (
                calculate_query_aware_agent_score(
                    combined_score,
                    query_priority_score
                )
            )

            # ------------------------------------------------
            # SAVE SCORES INTO PROFILE
            # ------------------------------------------------

            optimization_profile[
                "historical_score"
            ] = historical_score

            optimization_profile[
                "combined_score"
            ] = combined_score

            optimization_profile[
                "query_priority_score"
            ] = query_priority_score

            optimization_profile[
                "query_aware_score"
            ] = query_aware_score


               # ====================================================
        # H3-F STEP 8E:
        # HISTORICAL + QUERY-AWARE AGENT SELECTION
        # ====================================================

        combined_preferred_agent = (
            select_best_agent_by_combined_score(
                optimization_profiles
            )
        )

        if combined_preferred_agent:

            preferred_agent = combined_preferred_agent

        else:

            preferred_agent = get_preferred_agent(
                optimization_profiles,
                agents_to_run
            )


        # ====================================================
        # H3-F STEP 8E:
        # CALCULATE AGENT SELECTION CONFIDENCE
        # ====================================================

        agent_selection_confidence = (
            calculate_agent_selection_confidence(
                optimization_profiles
            )
        )


        # ====================================================
        # H3-F STEP 8E:
        # CONFIDENCE-BASED DECISION POLICY
        # ====================================================

        confidence_decision_policy = (
            get_confidence_based_decision_policy(
                agent_selection_confidence
            )
        )


        # ====================================================
        # H3-F STEP 8E:
        # PREPARE VALIDATION AGENT
        # ====================================================

        selected_agent_name = (
            preferred_agent.get("agent")
            if isinstance(
                preferred_agent,
                dict
            )
            else preferred_agent
        )

        validation_info = get_validation_agents(
            optimization_profiles,
            selected_agent_name
        )


        # ====================================================
        # H3-F STEP 8E:
        # VALIDATION INITIALIZATION
        # ====================================================

        validation_result = None
        validation_comparison = None
        final_validation_decision = None
        final_result_source = None


        # ====================================================
        # H3-F STEP 8E:
        # EXECUTE VALIDATION AGENT
        # ====================================================

        if (
            confidence_decision_policy.get(
                "decision_mode"
            ) == "validation_required"
            and
            validation_info.get(
                "validation_required"
            )
        ):

            validation_agent = validation_info.get(
                "validation_agent"
            )

            if validation_agent:

                validation_context = {
                    "workflow_id": workflow_id,
                    "user_query": query,
                    "current_agent": validation_agent,
                    "validation_for": selected_agent_name,
                    "previous_agent_results":
                        previous_agent_results,
                    "context_intelligence":
                        context_intelligence
                }

                validation_result = execute_agent(
                    validation_agent,
                    df,
                    context=validation_context
                )
                print()
                print("===== SEMANTIC V2 INPUT DIAGNOSTIC =====")

                primary_debug = workflow_results.get(
                    selected_agent_name
                )

                print(
                    "PRIMARY TYPE:",
                    type(primary_debug).__name__
                )

                print(
                    "VALIDATION TYPE:",
                    type(validation_result).__name__
                )

                if isinstance(primary_debug, dict):
                    print(
                        "PRIMARY KEYS:",
                        list(primary_debug.keys())
                    )

                if isinstance(validation_result, dict):
                    print(
                        "VALIDATION KEYS:",
                        list(validation_result.keys())
                    )

                print("========================================")
                print()
                print("===== SEMANTIC V2 INPUT DIAGNOSTIC =====")

                print(
                    "PRIMARY TYPE:",
                    type(
                        workflow_results.get(
                            selected_agent_name
                        )
                    ).__name__
                )

                print(
                    "VALIDATION TYPE:",
                    type(
                        validation_result
                    ).__name__
                )

                print(
                    "PRIMARY KEYS:",
                    list(
                        workflow_results.get(
                            selected_agent_name
                        ).keys()
                    )
                    if isinstance(
                        workflow_results.get(
                            selected_agent_name
                        ),
                        dict
                    )
                    else "NOT A DICT"
                )

                print(
                    "VALIDATION KEYS:",
                    list(
                        validation_result.keys()
                    )
                    if isinstance(
                        validation_result,
                        dict
                    )
                    else "NOT A DICT"
                )

                print("========================================")


                # ====================================================
                # COMPARE PRIMARY + VALIDATION RESULTS
                # ====================================================

                primary_result = workflow_results.get(
                    selected_agent_name
                )

                validation_comparison = (
                    compare_agent_validation_results(
                        primary_result,
                        validation_result
                    )
                )
                


        # ====================================================
        # H3-F STEP 8E:
        # BUILD FINAL VALIDATION DECISION
        # ====================================================

        final_validation_decision = (
            build_final_validation_decision(
                validation_comparison,
                confidence_decision_policy
            )
        )
        # ====================================================
        # H3-F STEP 8E — PART 9F STEP 3
        # SEMANTIC RESULT AGREEMENT
        # ====================================================

        semantic_result_agreement = (
            assess_semantic_result_agreement(
                workflow_results.get(
                    selected_agent_name
                ),
                validation_result
            )
        )
                # ============================================================
        # H3-F STEP 8E — PART 9F STEP 10
        # SEMANTIC AGREEMENT V2
        # ============================================================

        semantic_result_agreement_v2 = (
            assess_semantic_result_agreement_v2(
                workflow_results.get(
                    selected_agent_name
                ),
                validation_result
            )
        )
        
        # ====================================================
        # H3-F STEP 8E — PART 9F STEP 8 — STEP 3
        # SEMANTIC DECISION POLICY
        # ====================================================

        semantic_decision_policy = (
            build_semantic_decision_policy(
                semantic_result_agreement
            )
        )
        
        # ====================================================
        # H3-F STEP 8E:
        # SELECT FINAL RESULT SOURCE
        # ====================================================

        validation_agent_name = (
            validation_info.get(
                "validation_agent"
            )
        )

        final_result_source = (
            select_final_result_source(
                final_validation_decision,
                selected_agent_name,
                validation_agent_name
            )
        )
        # ====================================================
        # H3-F STEP 8E — PART 9D
        # BUILD ACTUAL FINAL RESULT PAYLOAD
        # ====================================================

        final_result = None

        if final_result_source:

            result_source = (
                final_result_source.get(
                    "final_result_source"
                )
            )

            # ------------------------------------------------
            # PRIMARY RESULT
            # ------------------------------------------------

            if result_source == "primary":

                final_result = workflow_results.get(
                    selected_agent_name
                )

            # ------------------------------------------------
            # VALIDATION RESULT
            # ------------------------------------------------

            elif result_source == "validation":

                final_result = validation_result

            # ------------------------------------------------
            # ESCALATION
            # ------------------------------------------------

            elif result_source == "escalate":

                final_result = {
                    "success": False,
                    "status": "escalation_required",
                    "message": (
                        "No sufficiently validated final "
                        "result is available."
                    )
                }

        # ----------------------------------------------------
        # FINAL RESULT INTELLIGENCE PAYLOAD
        # ----------------------------------------------------

        final_result_payload = {
            "final_result": final_result,

            "final_result_source": (
                final_result_source.get(
                    "final_result_source"
                )
                if final_result_source
                else "escalate"
            ),

            "primary_agent": selected_agent_name,

            "validation_agent": validation_agent_name,

            "final_decision": (
                final_validation_decision.get(
                    "final_decision"
                )
                if final_validation_decision
                else "escalate"
            ),

            "validated": (
                final_validation_decision.get(
                    "validated",
                    False
                )
                if final_validation_decision
                else False
            ),

            "confidence": (
                agent_selection_confidence.get(
                    "confidence_score",
                    0
                )
                if agent_selection_confidence
                else 0
            ),

            "confidence_level": (
                agent_selection_confidence.get(
                    "confidence_level",
                    "low"
                )
                if agent_selection_confidence
                else "low"
            )
        }

        # ====================================================
        # GENERATE RECOMMENDATION + ACTION
        # ====================================================
        # ====================================================
        # H3-F STEP 8E — PART 9E STEP 3
        # FINAL RESULT QUALITY ASSESSMENT
        # ====================================================

        final_result_quality = (
            assess_final_result_quality(
                final_result
            )
        )
            # ============================================================
    # H3-F STEP 8E — PART 9F STEP 9
    # COMBINED INTELLIGENCE DECISION
    # ============================================================

        combined_intelligence_decision = (
        build_combined_intelligence_decision(
            confidence_decision_policy,
            final_result_quality,
            semantic_decision_policy
        )
    )
        optimization_recommendation = (
            generate_optimization_recommendation(
                preferred_agent
            )
        )

        optimization_action = (
            get_agent_optimization_action(
                preferred_agent
            )
        )


        # ====================================================
        # H3-F STEP 8C:
        # SAVE CURRENT OPTIMIZATION HISTORY
        # ====================================================

        for optimization_profile in (optimization_profiles or []):
            optimization_history = (
                add_optimization_history(
                    optimization_history,
                    optimization_profile
                )
            )


        # ====================================================
        # H3-F STEP 8D:
        # SAVE CURRENT OPTIMIZATION MEMORY
        # AFTER HISTORICAL SCORES ARE CALCULATED
        # ====================================================

        for optimization_profile in (optimization_profiles or []):
            # Keep the same memory object across workflow runs.
            OPTIMIZATION_MEMORY[:] = (
                save_optimization_memory(
                    OPTIMIZATION_MEMORY,
                    optimization_profile
                )
            )


        # ====================================================
        # STEP 3A: BUILD WORKFLOW STATUS
        # ====================================================
        # ====================================================
        # STEP 3A: BUILD WORKFLOW STATUS
        # ====================================================

        workflow_status = build_workflow_status(
            workflow_results
        )

        # ====================================================
        # FINAL CONTEXT INTELLIGENCE
        # ====================================================

        final_context_intelligence = (
            build_context_intelligence(
                previous_agent_results
                
            )
        )

        # ====================================================
        # STEP 4: RETURN COMPLETE WORKFLOW
        # ====================================================

        return {

            "success": True,

            "workflow_type":
                "Genesis AI Multi-Agent Workflow",

            "user_query":
                query,

            "primary_agent":
                primary_agent,

            "agents_executed":
                agents_to_run,

            "total_agents_executed":
                len(agents_to_run),

            "workflow_results":
                workflow_results,

            "workflow_id":
                workflow_id,

            "execution_plan":
                execution_plan,

            "workflow_status":
                workflow_status,

            "workflow_metrics":
                workflow_metrics,

            "execution_history":
                execution_history,

            "performance_intelligence":
                performance_intelligence,

            "reliability_intelligence":
                reliability_intelligence,

            "optimization_profiles":
                optimization_profiles,

            "best_agent":
                best_agent,

            "preferred_agent":
    preferred_agent,

"combined_preferred_agent":
    combined_preferred_agent,

"agent_selection_confidence":
    agent_selection_confidence,
    "confidence_decision_policy":
    confidence_decision_policy,
    "validation_info":
    validation_info,

"validation_result":
    validation_result,

"validation_comparison":
    validation_comparison,
    "final_validation_decision":
    final_validation_decision,
    "final_result_source":
    final_result_source,
    
            "final_result_payload":
                final_result_payload,
                            "final_result_quality":
                final_result_quality,
                            "semantic_result_agreement":
                semantic_result_agreement,
                "semantic_result_agreement_v2":
    semantic_result_agreement_v2,

                            "semantic_decision_policy":
                semantic_decision_policy,
                "combined_intelligence_decision":
    combined_intelligence_decision,
"optimization_recommendation":
    optimization_recommendation,

            "optimization_action":
                optimization_action,

            "optimization_history":
                optimization_history,

            "optimization_memory":
                OPTIMIZATION_MEMORY,

            "historical_agent_scores":
                historical_agent_scores,
                "combined_agent_scores":
    combined_agent_scores,

            "final_context_intelligence":
                final_context_intelligence
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "success": False,
            "error": repr(e)
        }