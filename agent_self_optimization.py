# ============================================================
# GENESIS AI - AGENT SELF OPTIMIZATION
# ============================================================


def calculate_agent_optimization_score(
    performance_data,
    reliability_data
):

    if not performance_data:
        return 0

    if not reliability_data:
        return 0

    average_time = performance_data.get(
        "average_execution_time_seconds",
        0
    )

    success_rate = reliability_data.get(
        "success_rate_percent",
        0
    )

    # Performance score
    if average_time <= 0.001:
        speed_score = 100

    elif average_time <= 0.005:
        speed_score = 90

    elif average_time <= 0.01:
        speed_score = 75

    elif average_time <= 0.05:
        speed_score = 60

    else:
        speed_score = 40

    # Reliability score
    reliability_score = success_rate

    # Combined optimization score
    optimization_score = (
        speed_score * 0.4
        +
        reliability_score * 0.6
    )

    return round(
        optimization_score,
        2
    )


def build_agent_optimization_profile(
    performance_summary,
    reliability_summary
):

    if not performance_summary:
        return []

    if not reliability_summary:
        return []

    reliability_map = {
        item.get("agent"): item
        for item in reliability_summary
    }

    optimization_profiles = []

    for performance in performance_summary:

        agent_name = performance.get(
            "agent"
        )

        reliability = reliability_map.get(
            agent_name,
            {}
        )

        optimization_score = (
            calculate_agent_optimization_score(
                performance,
                reliability
            )
        )

        optimization_profiles.append({

            "agent":
                agent_name,

            "optimization_score":
                optimization_score,

            "average_execution_time_seconds":
                performance.get(
                    "average_execution_time_seconds",
                    0
                ),

            "success_rate_percent":
                reliability.get(
                    "success_rate_percent",
                    0
                ),

            "failure_rate_percent":
                reliability.get(
                    "failure_rate_percent",
                    0
                ),

            "skip_rate_percent":
                reliability.get(
                    "skip_rate_percent",
                    0
                )
        })

    optimization_profiles.sort(
        key=lambda item:
            item["optimization_score"],
        reverse=True
    )

    return optimization_profiles


def select_best_agent(
    optimization_profiles
):

    if not optimization_profiles:
        return None

    return optimization_profiles[0]
def get_preferred_agent(
    optimization_profiles,
    requested_agents=None
):

    if not optimization_profiles:
        return None

    if requested_agents:
        filtered_profiles = [
            profile
            for profile in optimization_profiles
            if profile.get("agent") in requested_agents
        ]

        if filtered_profiles:
            return max(
                filtered_profiles,
                key=lambda item:
                    item.get(
                        "optimization_score",
                        0
                    )
            )
        

    return select_best_agent(
        optimization_profiles
    )
def generate_optimization_recommendation(
    optimization_profile
):

    if not optimization_profile:
        return {
            "agent": None,
            "recommendation": "No optimization data available."
        }

    agent_name = optimization_profile.get(
        "agent"
    )

    optimization_score = optimization_profile.get(
        "optimization_score",
        0
    )

    success_rate = optimization_profile.get(
        "success_rate_percent",
        0
    )

    average_time = optimization_profile.get(
        "average_execution_time_seconds",
        0
    )

    if success_rate < 70:

        recommendation = (
            "Reliability optimization required."
        )

    elif average_time > 0.01:

        recommendation = (
            "Performance optimization recommended."
        )

    elif optimization_score >= 95:

        recommendation = (
            "No optimization required. "
            "Agent performance is excellent."
        )

    elif optimization_score >= 85:

        recommendation = (
            "Minor optimization recommended."
        )

    else:

        recommendation = (
            "Agent requires optimization."
        )

    return {
        "agent": agent_name,
        "optimization_score": optimization_score,
        "recommendation": recommendation
    }
def get_agent_optimization_action(
    optimization_profile
):

    if not optimization_profile:
        return {
            "agent": None,
            "action": "unknown",
            "reason": "No optimization profile available."
        }

    agent_name = optimization_profile.get(
        "agent"
    )

    optimization_score = optimization_profile.get(
        "optimization_score",
        0
    )

    success_rate = optimization_profile.get(
        "success_rate_percent",
        0
    )

    average_time = optimization_profile.get(
        "average_execution_time_seconds",
        0
    )

    if success_rate < 70:

        action = "avoid"
        reason = (
            "Agent reliability is too low."
        )

    elif average_time > 0.01:

        action = "optimize"
        reason = (
            "Agent execution performance is slow."
        )

    elif optimization_score >= 95:

        action = "prefer"
        reason = (
            "Agent has excellent performance "
            "and reliability."
        )

    elif optimization_score >= 85:

        action = "use"

        reason = (
            "Agent performance is acceptable "
            "with minor optimization potential."
        )

    else:

        action = "optimize"

        reason = (
            "Agent optimization is required."
        )

    return {
        "agent": agent_name,
        "optimization_score": optimization_score,
        "action": action,
        "reason": reason
    }
def add_optimization_history(
    history,
    optimization_profile
):

    if history is None:
        history = []

    if not optimization_profile:
        return history

    history.append({
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
            )
    })

    return history


def get_agent_optimization_history(
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
from agent_performance_intelligence import (
    analyze_agent_performance
)

from agent_reliability_intelligence import (
    analyze_agent_reliability
)

# ============================================================
# H3-F STEP 8E
# HISTORICAL PERFORMANCE BASED AGENT PREFERENCE
# ============================================================

def calculate_combined_agent_score(
    current_optimization_score,
    historical_agent_score
):
    """
    Combine current and historical agent performance.

    Current performance = 60%
    Historical performance = 40%
    """

    if current_optimization_score is None:
        current_optimization_score = 0

    if historical_agent_score is None:
        historical_agent_score = 0

    combined_score = (
        current_optimization_score * 0.60
        +
        historical_agent_score * 0.40
    )

    return round(
        combined_score,
        2
    )

# ============================================================
# H3-F STEP 8E
# PART 5A - HISTORICAL-AWARE AGENT SELECTION
# ============================================================

def select_best_agent_by_combined_score(
    optimization_profiles
):
    """
    Select the agent with the highest query-aware score.

    Priority:
    1. query_aware_score
    2. combined_score
    3. optimization_score
    """

    if not optimization_profiles:
        return None

    valid_profiles = [
        profile
        for profile in optimization_profiles
        if profile.get("agent")
    ]

    if not valid_profiles:
        return None

    best_profile = max(
        valid_profiles,
        key=lambda profile: profile.get(
            "query_aware_score",
            profile.get(
                "combined_score",
                profile.get(
                    "optimization_score",
                    0
                )
            )
        )
    )

    return best_profile

# ============================================================
# H3-F STEP 8E
# PART 6A - QUERY-AWARE COMBINED AGENT SCORE
# ============================================================

def calculate_query_aware_agent_score(
    combined_score,
    query_priority_score,
    relevance_weight=0.40
):
    """
    Combine agent performance with query relevance.

    combined_score:
        Current + historical performance score.

    query_priority_score:
        Query-specific priority/relevance score.

    relevance_weight:
        Weight given to query relevance.

    Remaining weight is given to combined performance.
    """

    if combined_score is None:
        combined_score = 0

    if query_priority_score is None:
        query_priority_score = 0

    if relevance_weight < 0:
        relevance_weight = 0

    if relevance_weight > 1:
        relevance_weight = 1

    performance_weight = 1 - relevance_weight

    final_score = (
        combined_score * performance_weight
        +
        query_priority_score * relevance_weight
    )

    return round(
        final_score,
        2
    )
# ============================================================
# H3-F STEP 8E
# PART 7A - AGENT SELECTION CONFIDENCE
# ============================================================

def calculate_agent_selection_confidence(
    optimization_profiles
):
    """
    Calculate confidence in the selected agent.

    Confidence is based on the gap between the
    highest and second-highest query-aware scores.

    Larger gap = higher confidence.
    """

    if not optimization_profiles:
        return {
            "confidence_score": 0,
            "confidence_level": "low",
            "selected_agent": None,
            "score_gap": 0
        }

    valid_profiles = [
        profile
        for profile in optimization_profiles
        if profile.get("agent")
    ]

    if not valid_profiles:
        return {
            "confidence_score": 0,
            "confidence_level": "low",
            "selected_agent": None,
            "score_gap": 0
        }

    sorted_profiles = sorted(
        valid_profiles,
        key=lambda profile: profile.get(
            "query_aware_score",
            profile.get(
                "combined_score",
                profile.get(
                    "optimization_score",
                    0
                )
            )
        ),
        reverse=True
    )

    best_profile = sorted_profiles[0]

    best_score = best_profile.get(
        "query_aware_score",
        best_profile.get(
            "combined_score",
            best_profile.get(
                "optimization_score",
                0
            )
        )
    )

    if len(sorted_profiles) > 1:

        second_best_profile = sorted_profiles[1]

        second_best_score = second_best_profile.get(
            "query_aware_score",
            second_best_profile.get(
                "combined_score",
                second_best_profile.get(
                    "optimization_score",
                    0
                )
            )
        )

    else:

        second_best_score = 0

    score_gap = best_score - second_best_score

    confidence_score = min(
        max(score_gap * 4, 0),
        100
    )

    if confidence_score >= 75:

        confidence_level = "high"

    elif confidence_score >= 40:

        confidence_level = "medium"

    else:

        confidence_level = "low"

    return {
        "confidence_score": round(
            confidence_score,
            2
        ),
        "confidence_level": confidence_level,
        "selected_agent": best_profile.get(
            "agent"
        ),
        "score_gap": round(
            score_gap,
            2
        )
    }

# ============================================================
# H3-F STEP 8E
# PART 7D - CONFIDENCE BASED DECISION POLICY
# ============================================================

def get_confidence_based_decision_policy(
    confidence_result
):
    """
    Determine the recommended action based on
    agent selection confidence.
    """

    if not confidence_result:
        return {
            "confidence_level": "low",
            "decision_mode": "validation_required",
            "action": "Run additional validation before proceeding."
        }

    confidence_level = confidence_result.get(
        "confidence_level",
        "low"
    )

    if confidence_level == "high":

        return {
            "confidence_level": "high",
            "decision_mode": "automatic",
            "action": "Proceed with the selected agent."
        }

    elif confidence_level == "medium":

        return {
            "confidence_level": "medium",
            "decision_mode": "cautious",
            "action": (
                "Proceed with the selected agent "
                "and perform secondary validation."
            )
        }

    else:

        return {
            "confidence_level": "low",
            "decision_mode": "validation_required",
            "action": (
                "Do not rely on automatic selection alone. "
                "Run additional validation or compare "
                "the next-best agent."
            )
        }

    # ============================================================
# H3-F STEP 8E
# PART 8A - LOW CONFIDENCE VALIDATION AGENT
# ============================================================

def get_validation_agents(
    optimization_profiles,
    selected_agent
):
    """
    Identify the selected agent and the best alternative
    agent for additional validation.
    """

    if not optimization_profiles:
        return {
            "selected_agent": selected_agent,
            "validation_agent": None,
            "validation_required": False
        }

    valid_profiles = [
        profile
        for profile in optimization_profiles
        if profile.get("agent")
    ]

    if not valid_profiles:
        return {
            "selected_agent": selected_agent,
            "validation_agent": None,
            "validation_required": False
        }

    sorted_profiles = sorted(
        valid_profiles,
        key=lambda profile: profile.get(
            "query_aware_score",
            profile.get(
                "combined_score",
                profile.get(
                    "optimization_score",
                    0
                )
            )
        ),
        reverse=True
    )

    validation_agent = None

    for profile in sorted_profiles:

        agent_name = profile.get(
            "agent"
        )

        if agent_name != selected_agent:

            validation_agent = agent_name
            break

    validation_required = (
        validation_agent is not None
    )

    return {
        "selected_agent": selected_agent,
        "validation_agent": validation_agent,
        "validation_required": validation_required
    }

# ============================================================
# H3-F STEP 8E
# PART 8C - VALIDATION RESULT COMPARISON
# ============================================================

def compare_agent_validation_results(
    primary_result,
    validation_result
):
    """
    Compare primary and validation agent results.

    The function checks whether both agents succeeded
    and whether their outputs are available for comparison.
    """

    if not primary_result:
        return {
            "validation_status": "failed",
            "agreement": False,
            "reason": "Primary agent result is unavailable."
        }

    if not validation_result:
        return {
            "validation_status": "failed",
            "agreement": False,
            "reason": "Validation agent result is unavailable."
        }

    primary_success = primary_result.get(
        "success",
        False
    )

    validation_success = validation_result.get(
        "success",
        False
    )

    if not primary_success:
        return {
            "validation_status": "failed",
            "agreement": False,
            "reason": "Primary agent execution failed."
        }

    if not validation_success:
        return {
            "validation_status": "failed",
            "agreement": False,
            "reason": "Validation agent execution failed."
        }

    return {
        "validation_status": "passed",
        "agreement": True,
        "reason": (
            "Primary and validation agents "
            "executed successfully."
        )
    }
# ============================================================
# H3-F STEP 8E — PART 9F
# SEMANTIC RESULT AGREEMENT
# ============================================================

def assess_semantic_result_agreement(
    primary_result,
    validation_result
):
    """
    Compare the analytical content of primary and
    validation agent results.

    This first version performs a structured-content
    comparison without using an external LLM.
    """

    if not primary_result:
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "reason": "Primary result is unavailable."
        }

    if not validation_result:
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "reason": "Validation result is unavailable."
        }

    if not isinstance(primary_result, dict):
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "reason": "Primary result is not structured."
        }

    if not isinstance(validation_result, dict):
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "reason": "Validation result is not structured."
        }

    # --------------------------------------------------------
    # UNWRAP AGENT RESULTS
    # --------------------------------------------------------

    primary_data = primary_result.get(
        "agent_result",
        primary_result
    )

    validation_data = validation_result.get(
        "agent_result",
        validation_result
    )

    if not isinstance(primary_data, dict):
        primary_data = primary_result

    if not isinstance(validation_data, dict):
        validation_data = validation_result

    # --------------------------------------------------------
    # EXTRACT COMMON ANALYTICAL SIGNALS
    # --------------------------------------------------------

    primary_analysis_type = (
        primary_data.get("analysis_type")
    )

    validation_analysis_type = (
        validation_data.get("analysis_type")
    )

    primary_recommendations = (
        primary_data.get(
            "analytics_recommendations",
            []
        )
    )

    validation_recommendations = (
        validation_data.get(
            "analytics_recommendations",
            []
        )
    )

    if not isinstance(primary_recommendations, list):
        primary_recommendations = []

    if not isinstance(validation_recommendations, list):
        validation_recommendations = []

    # --------------------------------------------------------
    # BASIC STRUCTURAL AGREEMENT
    # --------------------------------------------------------

    score = 0

    if primary_analysis_type:
        score += 20

    if validation_analysis_type:
        score += 20

    if primary_recommendations:
        score += 20

    if validation_recommendations:
        score += 20

    # --------------------------------------------------------
    # RECOMMENDATION OVERLAP
    # --------------------------------------------------------

    primary_text = " ".join(
        str(item).lower()
        for item in primary_recommendations
    )

    validation_text = " ".join(
        str(item).lower()
        for item in validation_recommendations
    )

    common_terms = [
        "correlation",
        "outlier",
        "group analysis",
        "forecast",
        "time-series",
        "dashboard",
        "performance",
        "sales",
        "revenue",
        "target"
    ]

    overlapping_terms = [
        term
        for term in common_terms
        if term in primary_text
        and term in validation_text
    ]

    if overlapping_terms:
        score += min(
            len(overlapping_terms) * 5,
            20
        )

    score = min(score, 100)

    # --------------------------------------------------------
    # AGREEMENT LEVEL
    # --------------------------------------------------------

    if score >= 75:
        agreement_level = "high"
        agreement = True

    elif score >= 50:
        agreement_level = "medium"
        agreement = True

    else:
        agreement_level = "low"
        agreement = False

    return {
        "agreement_score": score,
        "agreement_level": agreement_level,
        "agreement": agreement,
        "overlapping_terms": overlapping_terms,
        "reason": (
            "Primary and validation results contain "
            "compatible analytical signals."
            if agreement
            else
            "Primary and validation results do not "
            "contain sufficient compatible analytical signals."
        )
    }
# ============================================================
# H3-F STEP 8E
# PART 8E - FINAL VALIDATION DECISION ENGINE
# ============================================================

def build_final_validation_decision(
    validation_comparison,
    confidence_decision_policy
):
    """
    Convert validation and confidence information
    into a final validation decision.
    """

    if not validation_comparison:
        return {
            "final_decision": "escalate",
            "decision_reason": (
                "Validation comparison is unavailable."
            ),
            "validated": False
        }

    validation_status = validation_comparison.get(
        "validation_status",
        "failed"
    )

    agreement = validation_comparison.get(
        "agreement",
        False
    )

    confidence_level = "low"

    if confidence_decision_policy:
        confidence_level = confidence_decision_policy.get(
            "confidence_level",
            "low"
        )

    if (
        validation_status == "passed"
        and agreement is True
    ):

        if confidence_level == "high":

            return {
                "final_decision": "validated",
                "decision_reason": (
                    "Validation passed and confidence "
                    "is high."
                ),
                "validated": True
            }

        elif confidence_level == "medium":

            return {
                "final_decision": "validated_with_caution",
                "decision_reason": (
                    "Validation passed, but confidence "
                    "is medium."
                ),
                "validated": True
            }

        else:

            return {
                "final_decision": "validated_with_low_confidence",
                "decision_reason": (
                    "Validation passed, but selection "
                    "confidence is low."
                ),
                "validated": True
            }

    return {
        "final_decision": "requires_review",
        "decision_reason": (
            "Validation did not sufficiently support "
            "the selected agent."
        ),
        "validated": False
    }
# ============================================================
# H3-F STEP 8E — PART 9F STEP 8
# SEMANTIC DECISION POLICY
# ============================================================

def build_semantic_decision_policy(
    semantic_agreement
):
    """
    Convert semantic agreement results into a
    decision policy for the final result.
    """

    if not semantic_agreement:
        return {
            "decision_mode": "escalate",
            "semantic_status": "unavailable",
            "action": (
                "Semantic agreement is unavailable. "
                "Additional review is required."
            )
        }

    agreement_score = semantic_agreement.get(
        "agreement_score",
        0
    )

    agreement_level = semantic_agreement.get(
        "agreement_level",
        "low"
    )

    agreement = semantic_agreement.get(
        "agreement",
        False
    )

    # --------------------------------------------------------
    # HIGH AGREEMENT
    # --------------------------------------------------------

    if (
        agreement is True
        and agreement_level == "high"
        and agreement_score >= 75
    ):
        return {
            "decision_mode": "automatic",
            "semantic_status": "high_agreement",
            "action": (
                "Primary and validation results show strong "
                "semantic agreement. Proceed automatically."
            )
        }

    # --------------------------------------------------------
    # MEDIUM AGREEMENT
    # --------------------------------------------------------

    if (
        agreement is True
        and agreement_level == "medium"
        and agreement_score >= 50
    ):
        return {
            "decision_mode": "cautious",
            "semantic_status": "medium_agreement",
            "action": (
                "Results are compatible but semantic agreement "
                "is not strong enough for fully automatic "
                "acceptance. Proceed with caution."
            )
        }

    # --------------------------------------------------------
    # LOW / CONFLICT
    # --------------------------------------------------------

    return {
        "decision_mode": "escalate",
        "semantic_status": "low_or_conflicting",
        "action": (
            "Primary and validation results do not show "
            "sufficient semantic agreement. Escalate for "
            "additional analysis or review."
        )
    }
# ============================================================
# H3-F STEP 8E — PART 9F STEP 9
# COMBINED FINAL INTELLIGENCE DECISION
# ============================================================

def build_combined_intelligence_decision(
    confidence_decision_policy,
    final_result_quality,
    semantic_decision_policy
):
    """
    Combine confidence, final-result quality and semantic
    agreement into one final intelligence decision.
    """

    if not confidence_decision_policy:
        return {
            "final_decision_mode": "escalate",
            "decision_status": "insufficient_confidence_data",
            "action": (
                "Confidence information is unavailable. "
                "Escalate for additional validation."
            )
        }

    if not final_result_quality:
        return {
            "final_decision_mode": "escalate",
            "decision_status": "insufficient_quality_data",
            "action": (
                "Final result quality information is unavailable. "
                "Escalate for additional validation."
            )
        }

    if not semantic_decision_policy:
        return {
            "final_decision_mode": "escalate",
            "decision_status": "insufficient_semantic_data",
            "action": (
                "Semantic agreement information is unavailable. "
                "Escalate for additional analysis."
            )
        }

    confidence_level = confidence_decision_policy.get(
        "confidence_level",
        "low"
    )

    quality_level = final_result_quality.get(
        "quality_level",
        "low"
    )

    quality_usable = final_result_quality.get(
        "usable",
        False
    )

    semantic_status = semantic_decision_policy.get(
        "semantic_status",
        "low_or_conflicting"
    )

    semantic_mode = semantic_decision_policy.get(
        "decision_mode",
        "escalate"
    )

    # --------------------------------------------------------
    # HIGH-CONFIDENCE + HIGH-QUALITY + HIGH-AGREEMENT
    # --------------------------------------------------------

    if (
        confidence_level == "high"
        and quality_level == "high"
        and quality_usable is True
        and semantic_status == "high_agreement"
        and semantic_mode == "automatic"
    ):
        return {
            "final_decision_mode": "automatic",
            "decision_status": "fully_validated",
            "action": (
                "Confidence, result quality and semantic "
                "agreement are all strong. Accept the final "
                "result automatically."
            )
        }

    # --------------------------------------------------------
    # GOOD RESULT BUT CAUTION REQUIRED
    # --------------------------------------------------------

    if (
        quality_usable is True
        and semantic_status == "medium_agreement"
    ):
        return {
            "final_decision_mode": "cautious",
            "decision_status": "validated_with_caution",
            "action": (
                "Final result quality is sufficient and the "
                "agents are reasonably compatible, but semantic "
                "agreement is not strong enough for automatic "
                "acceptance."
            )
        }

    # --------------------------------------------------------
    # LOW CONFIDENCE
    # --------------------------------------------------------

    if confidence_level == "low":
        return {
            "final_decision_mode": "validation_required",
            "decision_status": "low_confidence",
            "action": (
                "Agent selection confidence is low. Keep the "
                "validated result but require additional "
                "validation before fully automatic acceptance."
            )
        }

    # --------------------------------------------------------
    # LOW QUALITY
    # --------------------------------------------------------

    if quality_usable is not True:
        return {
            "final_decision_mode": "escalate",
            "decision_status": "low_result_quality",
            "action": (
                "The final result does not meet the required "
                "quality threshold. Escalate for additional "
                "analysis."
            )
        }

    # --------------------------------------------------------
    # LOW / CONFLICTING SEMANTIC AGREEMENT
    # --------------------------------------------------------

    if semantic_mode == "escalate":
        return {
            "final_decision_mode": "escalate",
            "decision_status": "semantic_conflict",
            "action": (
                "Primary and validation results do not provide "
                "sufficient semantic agreement. Escalate for "
                "additional analysis."
            )
        }

    # --------------------------------------------------------
    # DEFAULT SAFE DECISION
    # --------------------------------------------------------

    return {
        "final_decision_mode": "cautious",
        "decision_status": "validated_with_caution",
        "action": (
            "The result passed basic validation but does not "
            "meet the strongest criteria for automatic "
            "acceptance. Proceed cautiously."
        )
    }
# ============================================================
# H3-F STEP 8E — PART 9F STEP 10
# SEMANTIC AGREEMENT V2
# ============================================================

    # --------------------------------------------------------
    # 1. ANALYSIS TYPE
    # --------------------------------------------------------
    #
    # Different specialist agents are expected to have
    # different analysis types.
    #
    # Therefore, analysis type is used only as contextual
    # information and NOT as a strict agreement requirement.
    # --------------------------------------------------------

    primary_analysis_type = str(
        primary_data.get(
            "analysis_type",
            ""
        )
    ).strip().lower()

    validation_analysis_type = str(
        validation_data.get(
            "analysis_type",
            ""
        )
    ).strip().lower()

    analysis_type_match = (
        bool(primary_analysis_type)
        and bool(validation_analysis_type)
        and (
            primary_analysis_type
            == validation_analysis_type
        )
    )
    print("DEBUG PRIMARY ANALYSIS TYPE:", repr(primary_analysis_type))
    print("DEBUG VALIDATION ANALYSIS TYPE:", repr(validation_analysis_type))
    # --------------------------------------------------------
    # 2. ANALYTICAL RECOMMENDATIONS
    # --------------------------------------------------------

    primary_analytics = primary_data.get(
        "analytics_recommendations",
        []
    )

    validation_analytics = validation_data.get(
        "analytics_recommendations",
        []
    )

    if not isinstance(primary_analytics, list):
        primary_analytics = []

    if not isinstance(validation_analytics, list):
        validation_analytics = []

    # --------------------------------------------------------
    # 3. FORECASTING RECOMMENDATIONS
    # --------------------------------------------------------

    primary_forecasting = primary_data.get(
        "forecasting_recommendations",
        []
    )

    validation_forecasting = validation_data.get(
        "forecasting_recommendations",
        []
    )

    if not isinstance(primary_forecasting, list):
        primary_forecasting = []

    if not isinstance(validation_forecasting, list):
        validation_forecasting = []

    # --------------------------------------------------------
    # 4. ADVANCED ANALYSIS RECOMMENDATIONS
    # --------------------------------------------------------

    primary_advanced = primary_data.get(
        "advanced_analysis_recommendations",
        []
    )

    validation_advanced = validation_data.get(
        "advanced_analysis_recommendations",
        []
    )

    if not isinstance(primary_advanced, list):
        primary_advanced = []

    if not isinstance(validation_advanced, list):
        validation_advanced = []

    # --------------------------------------------------------
    # 5. CONTEXT-BASED RECOMMENDATIONS
    # --------------------------------------------------------

    primary_context = primary_data.get(
        "context_based_recommendations",
        []
    )

    validation_context = validation_data.get(
        "context_based_recommendations",
        []
    )

    if not isinstance(primary_context, list):
        primary_context = []

    if not isinstance(validation_context, list):
        validation_context = []

    # --------------------------------------------------------
    # 6. RECOMMENDATION TEXT NORMALIZATION
    # --------------------------------------------------------

    def normalize_recommendation_items(items):
        normalized = []

        for item in items:

            if isinstance(item, dict):
                text = " ".join(
                    str(value)
                    for value in item.values()
                )
            else:
                text = str(item)

            text = (
                text
                .lower()
                .strip()
            )

            if text:
                normalized.append(text)

        return normalized

    primary_texts = (
        normalize_recommendation_items(
            primary_analytics
            + primary_forecasting
            + primary_advanced
            + primary_context
        )
    )

    validation_texts = (
        normalize_recommendation_items(
            validation_analytics
            + validation_forecasting
            + validation_advanced
            + validation_context
        )
    )

    # --------------------------------------------------------
    # 7. MEANINGFUL TERM COMPARISON
    # --------------------------------------------------------

    
    

    primary_combined_text = " ".join(
        primary_texts
    )

    validation_combined_text = " ".join(
        validation_texts
    )
    semantic_term_weights = {
        "sales": 5,
        "revenue": 5,
        "profit": 5,
        "expense": 5,
        "target": 5,
        "performance": 5,
        "correlation": 4,
        "outlier": 4,
        "group analysis": 4,
        "forecast": 4,
        "forecasting": 4,
        "time-series": 4,
        "trend": 4,
        "statistical": 3,
        "predictive": 3,
        "pattern": 3,
        "improvement": 3,
        "kpi": 3,
        "dashboard": 2,
        "data quality": 2,
        "anomaly": 4
    }
    semantic_concept_groups = {
    "sales_performance": [
        "sales",
        "monthly sales",
        "sales performance",
        "business sales",
        "sales decline",
        "sales decrease"
    ],
    "revenue_performance": [
        "revenue",
        "income",
        "business revenue",
        "revenue performance",
        "revenue decline",
        "revenue decrease"
    ],
    "profitability": [
        "profit",
        "profitability",
        "profit margin",
        "margin",
        "net profit"
    ],
    "cost_management": [
        "expense",
        "expenses",
        "cost",
        "costs",
        "spending"
    ],
    "target_performance": [
        "target",
        "achievement",
        "target achievement",
        "goal",
        "goal achievement"
    ],
    "employee_performance": [
        "performance",
        "employee performance",
        "productivity",
        "efficiency"
    ],
    "trend_analysis": [
        "trend",
        "time-series",
        "time series",
        "historical trend",
        "growth trend",
        "declining trend"
    ],
    "forecasting": [
        "forecast",
        "forecasting",
        "prediction",
        "predictive",
        "future estimate"
    ],
    "anomaly_detection": [
        "outlier",
        "outliers",
        "anomaly",
        "anomalies",
        "unusual pattern"
    ],
    "relationship_analysis": [
        "correlation",
        "relationship",
        "association",
        "dependency"
    ],
    "group_comparison": [
        "group analysis",
        "group comparison",
        "department comparison",
        "city comparison",
        "branch comparison",
        "segment comparison"
    ],
    "data_quality": [
        "data quality",
        "missing values",
        "duplicates",
        "duplicate records",
        "data cleaning"
    ]
}
    overlapping_terms = []

    for concept_name, concept_terms in semantic_concept_groups.items():
        primary_has_concept = any(
            term in primary_text
            for term in concept_terms
        )

        validation_has_concept = any(
            term in validation_text
            for term in concept_terms
        )

        if primary_has_concept and validation_has_concept:
            overlapping_terms.append(concept_name)

    semantic_term_score = 0

    for concept_name in overlapping_terms:
        concept_weight = 3

        if concept_name in [
            "sales_performance",
            "revenue_performance",
            "profitability",
            "target_performance",
            "employee_performance"
        ]:
            concept_weight = 5

        elif concept_name in [
            "trend_analysis",
            "forecasting",
            "anomaly_detection",
            "relationship_analysis",
            "group_comparison"
        ]:
            concept_weight = 4

        semantic_term_score += concept_weight

    semantic_term_score = min(
        semantic_term_score,
        40
    )

    score += semantic_term_score

    # --------------------------------------------------------
    # 8. RECOMMENDATION CATEGORY AGREEMENT
    # --------------------------------------------------------

    category_matches = 0

    if primary_analytics and validation_analytics:
        category_matches += 1

    if primary_forecasting and validation_forecasting:
        category_matches += 1

    if primary_advanced and validation_advanced:
        category_matches += 1

    if primary_context and validation_context:
        category_matches += 1

    # Maximum category contribution = 20
    score += min(
        category_matches * 5,
        20
    )

    # --------------------------------------------------------
    # 9. WORKFLOW AGREEMENT
    # --------------------------------------------------------

    primary_workflow = primary_data.get(
        "recommended_workflow",
        []
    )

    validation_workflow = validation_data.get(
        "recommended_workflow",
        []
    )

    if not isinstance(primary_workflow, list):
        primary_workflow = []

    if not isinstance(validation_workflow, list):
        validation_workflow = []

    if primary_workflow and validation_workflow:
        score += 15

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = min(
        score,
        100
    )

    if score >= 75:
        agreement_level = "high"
        agreement = True

    elif score >= 50:
        agreement_level = "medium"
        agreement = True

    else:
        agreement_level = "low"
        agreement = False

    if agreement_level == "high":
        comparison_status = "strong_semantic_agreement"

    elif agreement_level == "medium":
        comparison_status = "moderate_semantic_agreement"

    else:
        comparison_status = "weak_semantic_agreement"

    return {
        "agreement_score": score,
        "agreement_level": agreement_level,
        "agreement": agreement,
        "comparison_status": comparison_status,
        "analysis_type_match": analysis_type_match,
        "category_matches": category_matches,
        "overlapping_terms": overlapping_terms,
        "semantic_term_score": semantic_term_score,
        "reason": (
            "Primary and validation results contain "
            "multiple compatible analytical signals."
            if agreement
            else
            "Primary and validation results do not "
            "contain sufficient compatible analytical signals."
        )
    }
# ============================================================
# H3-F STEP 8E
# PART 9A - FINAL RESULT SOURCE SELECTION
# ============================================================

def select_final_result_source(
    final_validation_decision,
    selected_agent,
    validation_agent
):
    """
    Decide which result source should be treated as final.

    Possible sources:
    - primary
    - validation
    - escalate
    """

    if not final_validation_decision:
        return {
            "final_result_source": "escalate",
            "selected_agent": selected_agent,
            "validation_agent": validation_agent,
            "reason": (
                "Final validation decision is unavailable."
            )
        }

    final_decision = final_validation_decision.get(
        "final_decision",
        "requires_review"
    )

    if final_decision == "validated":

        return {
            "final_result_source": "primary",
            "selected_agent": selected_agent,
            "validation_agent": validation_agent,
            "reason": (
                "Primary result passed validation "
                "with high confidence."
            )
        }

    elif final_decision == "validated_with_caution":

        return {
            "final_result_source": "primary",
            "selected_agent": selected_agent,
            "validation_agent": validation_agent,
            "reason": (
                "Primary result passed validation "
                "with medium confidence."
            )
        }

    elif final_decision == "validated_with_low_confidence":

        return {
            "final_result_source": "validation",
            "selected_agent": selected_agent,
            "validation_agent": validation_agent,
            "reason": (
                "Validation passed, but primary selection "
                "confidence is low. Use validation result "
                "as the safer final source."
            )
        }

    else:

        return {
            "final_result_source": "escalate",
            "selected_agent": selected_agent,
            "validation_agent": validation_agent,
            "reason": (
                "Validation did not sufficiently support "
                "the primary result."
            )
        }

    # ============================================================
# H3-F STEP 8E — PART 9E
# FINAL RESULT QUALITY ASSESSMENT
# ============================================================

def assess_final_result_quality(final_result):
    """
    Assess the structural quality and usability of the
    final agent result.

    Supports both direct results and wrapped results
    containing an agent_result payload.
    """

    if not final_result:
        return {
            "quality_score": 0,
            "quality_level": "low",
            "usable": False,
            "reason": "Final result is unavailable."
        }

    if not isinstance(final_result, dict):
        return {
            "quality_score": 0,
            "quality_level": "low",
            "usable": False,
            "reason": "Final result is not a structured dictionary."
        }

    # --------------------------------------------------------
    # STEP 1 — FIND ACTUAL AGENT RESULT
    # --------------------------------------------------------

    result_data = final_result

    nested_agent_result = final_result.get(
        "agent_result"
    )

    if isinstance(nested_agent_result, dict):
        result_data = nested_agent_result

    score = 0

    # --------------------------------------------------------
    # STEP 2 — SUCCESS CHECK
    # --------------------------------------------------------

    if (
        final_result.get("success") is True
        or result_data.get("success") is True
    ):
        score += 25

    # --------------------------------------------------------
    # STEP 3 — STRUCTURED RESULT CHECK
    # --------------------------------------------------------

    if isinstance(result_data, dict):
        score += 25

    # --------------------------------------------------------
    # STEP 4 — ANALYSIS TYPE CHECK
    # --------------------------------------------------------

    if result_data.get("analysis_type"):
        score += 15

    # --------------------------------------------------------
    # STEP 5 — ANALYTICAL CONTENT CHECK
    # --------------------------------------------------------

    content_fields = [
        "dataset_overview",
        "dataset_readiness",
        "analytics_recommendations",
        "forecasting_recommendations",
        "advanced_analysis_recommendations",
        "context_based_recommendations",
        "recommended_workflow",
        "context_intelligence"
    ]

    content_count = sum(
        1
        for field in content_fields
        if result_data.get(field) not in (
            None,
            "",
            [],
            {}
        )
    )

    if content_count >= 4:
        score += 25

    elif content_count >= 2:
        score += 15

    elif content_count >= 1:
        score += 10

    # --------------------------------------------------------
    # STEP 6 — GENERATED TIME CHECK
    # --------------------------------------------------------

    if result_data.get("generated_at"):
        score += 10

    # --------------------------------------------------------
    # STEP 7 — MAXIMUM SCORE
    # --------------------------------------------------------

    score = min(score, 100)

    # --------------------------------------------------------
    # STEP 8 — QUALITY LEVEL
    # --------------------------------------------------------

    if score >= 80:
        quality_level = "high"
        usable = True

    elif score >= 50:
        quality_level = "medium"
        usable = True

    else:
        quality_level = "low"
        usable = False

    # --------------------------------------------------------
    # STEP 9 — REASON
    # --------------------------------------------------------

    if usable:
        reason = (
            "Final result contains sufficient structured "
            "agent output and analytical content."
        )
    else:
        reason = (
            "Final result does not contain sufficient "
            "structured analytical content."
        )

    return {
        "quality_score": score,
        "quality_level": quality_level,
        "usable": usable,
        "reason": reason
    }

    score = 0

    # --------------------------------------------------------
    # SUCCESS SIGNAL
    # --------------------------------------------------------

    if final_result.get("success") is True:
        score += 30

    # --------------------------------------------------------
    # RESULT / DATA SIGNAL
    # --------------------------------------------------------

    result_fields = [
        "result",
        "data",
        "insights",
        "analysis",
        "answer",
        "message"
    ]

    has_result_content = any(
        final_result.get(field) not in (None, "", [], {})
        for field in result_fields
    )

    if has_result_content:
        score += 30

    # --------------------------------------------------------
    # STATUS SIGNAL
    # --------------------------------------------------------

    if final_result.get("status"):
        score += 20

    # --------------------------------------------------------
    # AGENT SIGNAL
    # --------------------------------------------------------

    if final_result.get("agent"):
        score += 20

    # --------------------------------------------------------
    # QUALITY LEVEL
    # --------------------------------------------------------

    if score >= 80:
        quality_level = "high"
        usable = True

    elif score >= 50:
        quality_level = "medium"
        usable = True

    else:
        quality_level = "low"
        usable = False

    return {
        "quality_score": score,
        "quality_level": quality_level,
        "usable": usable,
        "reason": (
            "Final result contains sufficient quality signals."
            if usable
            else
            "Final result does not contain sufficient quality signals."
        )
    }
# ============================================================
# H3-F STEP 8E — PART 9F STEP 10
# SEMANTIC AGREEMENT V2
# ============================================================

def assess_semantic_result_agreement_v2(
    primary_result,
    validation_result
):
    """
    Semantic Agreement V2.

    Compares the actual analytical content of primary and
    validation agent results instead of requiring the same
    agent type.
    """

    if not primary_result:
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "comparison_status": "primary_unavailable",
            "reason": "Primary result is unavailable."
        }

    if not validation_result:
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "comparison_status": "validation_unavailable",
            "reason": "Validation result is unavailable."
        }

    if not isinstance(primary_result, dict):
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "comparison_status": "primary_invalid",
            "reason": "Primary result is not structured."
        }

    if not isinstance(validation_result, dict):
        return {
            "agreement_score": 0,
            "agreement_level": "low",
            "agreement": False,
            "comparison_status": "validation_invalid",
            "reason": "Validation result is not structured."
        }

    # --------------------------------------------------------
    # EXTRACT NESTED AGENT RESULTS
    # --------------------------------------------------------

    primary_data = primary_result.get(
        "agent_result",
        primary_result
    )

    validation_data = validation_result.get(
        "agent_result",
        validation_result
    )

    if not isinstance(primary_data, dict):
        primary_data = primary_result

    if not isinstance(validation_data, dict):
        validation_data = validation_result

    score = 0

    # --------------------------------------------------------
    # ANALYSIS TYPE
    # --------------------------------------------------------

    primary_analysis_type = str(
        primary_data.get(
            "analysis_type",
            ""
        )
    ).strip().lower()

    validation_analysis_type = str(
        validation_data.get(
            "analysis_type",
            ""
        )
    ).strip().lower()

    analysis_type_match = (
        bool(primary_analysis_type)
        and bool(validation_analysis_type)
        and (
            primary_analysis_type
            == validation_analysis_type
        )
    )

    # Same analysis type is a positive signal,
    # but different specialist agents are NOT a conflict.

    if analysis_type_match:
        score += 10

    # --------------------------------------------------------
    # COLLECT ALL ANALYTICAL TEXT
    # --------------------------------------------------------
    def collect_text(value):
        texts = []

        if isinstance(value, dict):
            for key, item in value.items():
                if key in [
                    "generated_at",
                    "workflow_id",
                    "user_query"
                ]:
                    continue

                texts.extend(collect_text(item) or [])

        elif isinstance(value, list):
            for item in value:
                texts.extend(collect_text(item) or [])

        elif isinstance(value, str):
            text = value.strip().lower()

            if text:
                texts.append(text)

        return texts
    

    

    primary_texts = collect_text(primary_data)
    if not primary_texts:
        primary_texts = [
            str(primary_data)
        ]

    validation_texts = collect_text(validation_data)
    if not validation_texts:
        validation_texts = [
            str(validation_data)
        ]

    primary_text = " ".join(primary_texts)
    validation_text = " ".join(validation_texts)
    print("DEBUG PRIMARY TEXT:", primary_text[:1000])
    print("DEBUG VALIDATION TEXT:", validation_text[:1000])
    print("DEBUG PRIMARY TEXT COUNT:", len(primary_texts))
    print("DEBUG VALIDATION TEXT COUNT:", len(validation_texts))

    overlapping_terms = []

    
    

    # --------------------------------------------------------
    # BUSINESS / ANALYTICAL SEMANTIC TERMS
    # --------------------------------------------------------

    semantic_term_weights = {
        "sales": 2,
        "revenue": 3,
        "profit": 3,
        "expense": 2,
        "target": 2,
        "performance": 3,
        "correlation": 3,
        "outlier": 3,
        "group analysis": 3,
        "forecast": 3,
        "forecasting": 3,
        "time-series": 3,
        "time series": 3,
        "trend": 3,
        "dashboard": 2,
        "statistical": 3,
        "predictive": 3,
        "pattern": 2,
        "improvement": 2,
        "kpi": 3,
        "sales analysis": 3,
        "revenue analysis": 3,
        "profit analysis": 3,
        "expense analysis": 3,
        "performance analysis": 3,
        "business analysis": 3,
        "financial analysis": 3,
        "trend analysis": 3,
        "time series analysis": 3,
        "data analysis": 3,
        "descriptive analysis": 3,
        "diagnostic analysis": 3,
        "predictive analysis": 3,
        "prescriptive analysis": 3,
        "comparison": 2,
        "distribution": 2,
        "average": 2,
        "mean": 2,
        "median": 2,
        "sum": 2,
        "count": 2,
        "growth": 2,
        "decline": 2,
        "increase": 2,
        "decrease": 2,
        "risk": 2,
        "anomaly": 3,
        "anomalies": 3,
        "relationship": 2,
        "dependency": 2,
        "insight": 2,
        "insights": 2,
        "recommendation": 2,
        "recommendations": 2,
    }

    overlapping_terms = [
        term
        for term in semantic_term_weights
        if term in primary_text
        and term in validation_text
    ]

    semantic_term_score = sum(
        semantic_term_weights.get(term, 0)
        for term in overlapping_terms
    )

    semantic_term_score = min(
        semantic_term_score,
        40
    )

    score += semantic_term_score

    # --------------------------------------------------------
    # RECOMMENDATION CATEGORY AGREEMENT
    # --------------------------------------------------------

    recommendation_fields = [
        "analytics_recommendations",
        "forecasting_recommendations",
        "advanced_analysis_recommendations",
        "context_based_recommendations"
    ]

    category_matches = 0

    for field in recommendation_fields:

        primary_items = primary_data.get(
            field,
            []
        )

        validation_items = validation_data.get(
            field,
            []
        )

        if (
            isinstance(primary_items, list)
            and isinstance(validation_items, list)
            and primary_items
            and validation_items
        ):
            category_matches += 1

    score += min(
        category_matches * 5,
        20
    )

    # --------------------------------------------------------
    # DATASET CONTEXT AGREEMENT
    # --------------------------------------------------------

    primary_overview = primary_data.get(
        "dataset_overview",
        {}
    )

    validation_overview = validation_data.get(
        "dataset_overview",
        {}
    )

    if (
        isinstance(primary_overview, dict)
        and isinstance(validation_overview, dict)
        and primary_overview
        and validation_overview
    ):

        comparable_keys = [
            "total_rows",
            "total_columns",
            "missing_values",
            "duplicate_rows"
        ]

        matching_context_fields = 0

        for key in comparable_keys:

            if (
                key in primary_overview
                and key in validation_overview
                and primary_overview.get(key)
                == validation_overview.get(key)
            ):
                matching_context_fields += 1

        score += min(
            matching_context_fields * 5,
            20
        )

    # --------------------------------------------------------
    # WORKFLOW AGREEMENT
    # --------------------------------------------------------

    primary_workflow = primary_data.get(
        "recommended_workflow",
        []
    )

    validation_workflow = validation_data.get(
        "recommended_workflow",
        []
    )

    if (
        isinstance(primary_workflow, list)
        and isinstance(validation_workflow, list)
        and primary_workflow
        and validation_workflow
    ):
        score += 10

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = min(
        score,
        100
    )

    if score >= 75:
        agreement_level = "high"
        agreement = True

    elif score >= 50:
        agreement_level = "medium"
        agreement = True

    else:
        agreement_level = "low"
        agreement = False

    if agreement_level == "high":
        comparison_status = (
            "strong_semantic_agreement"
        )

    elif agreement_level == "medium":
        comparison_status = (
            "moderate_semantic_agreement"
        )

    else:
        comparison_status = (
            "weak_semantic_agreement"
        )

    return {
        "agreement_score": score,
        "agreement_level": agreement_level,
        "agreement": agreement,
        "comparison_status": comparison_status,
        "analysis_type_match": analysis_type_match,
        "category_matches": category_matches,
        "overlapping_terms": overlapping_terms,
        "semantic_term_score": semantic_term_score,
        "reason": (
            "Primary and validation results contain "
            "compatible analytical signals."
            if agreement
            else
            "Primary and validation results do not "
            "contain sufficient compatible analytical signals."
        )
    }