# ============================================================
# GENESIS AI - CONTEXT INTELLIGENCE ENGINE
# ============================================================


def get_agent_result(previous_agent_results, agent_name):
    """
    Safely retrieves the actual result of a previous agent.
    """

    result = previous_agent_results.get(agent_name)

    if not result:
        return None

    # Agent Executor wraps results inside "agent_result"
    if isinstance(result, dict):

        if "agent_result" in result:
            return result.get("agent_result")

    return result


# ============================================================
# ROOT CAUSE INTELLIGENCE
# ============================================================

def extract_root_cause_intelligence(previous_agent_results):

    result = get_agent_result(
        previous_agent_results,
        "root_cause_agent"
    )

    if not result:
        return []

    findings = []

    root_causes = result.get(
        "identified_root_causes",
        []
    )

    for item in root_causes[:10]:

        findings.append({

            "issue_type":
                item.get("issue_type"),

            "column":
                item.get("column"),

            "severity":
                item.get("severity"),

            "possible_root_cause":
                item.get("possible_root_cause")
        })

    outliers = result.get(
        "outlier_root_causes",
        {}
    )

    for column, details in list(
        outliers.items()
    )[:10]:

        findings.append({

            "issue_type": "Outlier",

            "column": column,

            "severity": "Review",

            "possible_root_cause":
                details.get("possible_root_cause")
        })

    return findings


# ============================================================
# RECOMMENDATION INTELLIGENCE
# ============================================================

def extract_recommendation_intelligence(previous_agent_results):

    result = get_agent_result(
        previous_agent_results,
        "recommendation_agent"
    )

    if not result:
        return []

    recommendations = []

    data_quality = result.get(
        "data_quality_recommendations",
        []
    )

    for item in data_quality[:10]:

        recommendations.append({

            "priority":
                item.get("priority"),

            "recommendation":
                item.get("recommendation"),

            "source":
                "data_quality_recommendations"
        })

    analytics = result.get(
        "analytics_recommendations",
        []
    )

    for item in analytics[:10]:

        recommendations.append({

            "priority": "Medium",

            "recommendation": item,

            "source":
                "analytics_recommendations"
        })

    advanced = result.get(
        "advanced_analysis_recommendations",
        []
    )

    for item in advanced[:10]:

        recommendations.append({

            "priority": "Medium",

            "recommendation": item,

            "source":
                "advanced_analysis_recommendations"
        })

    return recommendations


# ============================================================
# INSIGHTS INTELLIGENCE
# ============================================================

def extract_insights_intelligence(previous_agent_results):

    result = get_agent_result(
        previous_agent_results,
        "insights_agent"
    )

    if not result:
        return []

    findings = []

    key_findings = result.get(
        "key_findings",
        []
    )

    for item in key_findings[:10]:

        findings.append(item)

    recommendations = result.get(
        "recommendations",
        []
    )

    return {

        "key_findings": findings,

        "recommendations":
            recommendations[:10]
    }


# ============================================================
# DECISION INTELLIGENCE
# ============================================================

def extract_decision_intelligence(previous_agent_results):
    result = get_agent_result(
        previous_agent_results,
        "decision_agent"
    )

    if not result:
        return []

    decisions = result.get(
        "recommended_decisions",
        []
    )

    return decisions[:10]


# ============================================================
# COMBINED CONTEXT INTELLIGENCE
# ============================================================

def build_context_intelligence(previous_agent_results):
    """
    Builds structured intelligence from all
    previously executed Genesis AI agents.
    """

    return {

        "root_cause_intelligence":
            extract_root_cause_intelligence(
                previous_agent_results
            ),

        "recommendation_intelligence":
            extract_recommendation_intelligence(
                previous_agent_results
            ),

        "insights_intelligence":
            extract_insights_intelligence(
                previous_agent_results
            ),

        "decision_intelligence":
            extract_decision_intelligence(
                previous_agent_results
            )
    }

# ============================================================
# INSIGHTS AGENT CONTEXT INTELLIGENCE
# ============================================================

def extract_insights_context_intelligence(
    previous_agent_results
):

    intelligence = {

        "root_cause_findings": [],

        "recommendation_findings": [],

        "combined_context_findings": []
    }


    # --------------------------------------------------------
    # ROOT CAUSE AGENT INTELLIGENCE
    # --------------------------------------------------------

    root_cause_result = get_agent_result(
        previous_agent_results,
        "root_cause_agent"
    ) or {}


    if root_cause_result:

        root_cause_summary = root_cause_result.get(
            "root_cause_summary",
            {}
        )

        identified_root_causes = root_cause_result.get(
            "identified_root_causes",
            []
        )

        outlier_root_causes = root_cause_result.get(
            "outlier_root_causes",
            {}
        )


        intelligence[
            "root_cause_findings"
        ].append({

            "root_cause_status":
                root_cause_summary.get(
                    "status"
                ),

            "total_detected_issues":
                root_cause_summary.get(
                    "total_detected_issues",
                    0
                ),

            "identified_root_causes":
                len(identified_root_causes),

            "outlier_columns":
                list(outlier_root_causes.keys())
        })


    # --------------------------------------------------------
    # RECOMMENDATION AGENT INTELLIGENCE
    # --------------------------------------------------------

    recommendation_result = get_agent_result(
        previous_agent_results,
        "recommendation_agent"
    ) or {}


    if recommendation_result:

        dataset_readiness = recommendation_result.get(
            "dataset_readiness",
            {}
        )


        # ----------------------------------------------------
        # COLLECT RECOMMENDATIONS FROM ALL SOURCES
        # ----------------------------------------------------

        recommendations = []

        recommendation_sources = [

            "recommendations",

            "advanced_analysis_recommendations",

            "analytics_recommendations",

            "data_quality_recommendations"
        ]


        for source in recommendation_sources:

            source_recommendations = recommendation_result.get(
                source,
                []
            )


            if not source_recommendations:

                continue


            if isinstance(
                source_recommendations,
                list
            ):

                recommendations.extend(
                    source_recommendations
                )

            else:

                recommendations.append(
                    source_recommendations
                )


        # ----------------------------------------------------
        # RECOMMENDED WORKFLOW
        # ----------------------------------------------------

        workflow = recommendation_result.get(
            "recommended_workflow",
            []
        )


        # ----------------------------------------------------
        # STORE RECOMMENDATION INTELLIGENCE
        # ----------------------------------------------------

        intelligence[
            "recommendation_findings"
        ].append({

            "dataset_readiness":
                dataset_readiness.get(
                    "status"
                ),

            "recommendations_count":
                len(recommendations),

            "recommended_workflow_steps":
                len(workflow)
        })


    # --------------------------------------------------------
    # BUILD COMBINED INTELLIGENCE
    # --------------------------------------------------------

    if root_cause_result and recommendation_result:

        intelligence[
            "combined_context_findings"
        ].append(

            "Root Cause Analysis and Recommendation "
            "results were combined to generate deeper insights."
        )


    elif root_cause_result:

        intelligence[
            "combined_context_findings"
        ].append(

            "Insights Agent received Root Cause Analysis "
            "results for deeper dataset interpretation."
        )


    elif recommendation_result:

        intelligence[
            "combined_context_findings"
        ].append(

            "Insights Agent received Recommendation Agent "
            "results for intelligent analysis guidance."
        )


    else:

        intelligence[
            "combined_context_findings"
        ].append(

            "No previous agent intelligence was available."
        )


    return intelligence

# ============================================================
# DECISION AGENT CONTEXT INTELLIGENCE
# ============================================================

def extract_decision_intelligence(previous_agent_results):
    decision_intelligence = {

        "root_cause_summary": [],

        "recommendation_summary": [],

        "insights_summary": [],

        "context_available": False
    }


    # ========================================================
    # EMPTY CONTEXT CHECK
    # ========================================================

    if not previous_agent_results:

        return decision_intelligence


    decision_intelligence["context_available"] = True


    # ========================================================
    # ROOT CAUSE INTELLIGENCE
    # ========================================================

    root_cause_result = get_agent_result(
        previous_agent_results,
        "root_cause_agent"
    ) or {}


    if root_cause_result:

        root_causes = root_cause_result.get(
            "identified_root_causes",
            []
        )

        for cause in root_causes[:5]:

            if isinstance(cause, dict):

                decision_intelligence[
                    "root_cause_summary"
                ].append({

                    "issue_type": cause.get(
                        "issue_type"
                    ),

                    "severity": cause.get(
                        "severity"
                    ),

                    "column": cause.get(
                        "column"
                    )
                })


    # ========================================================
    # RECOMMENDATION INTELLIGENCE
    # ========================================================

    recommendation_result = get_agent_result(
        previous_agent_results,
        "recommendation_agent"
    ) or {}


    if recommendation_result:

        recommendations = []


        recommendation_sources = [

            "recommendations",

            "advanced_analysis_recommendations",

            "analytics_recommendations",

            "data_quality_recommendations"
        ]


        for source in recommendation_sources:

            source_recommendations = recommendation_result.get(
                source,
                []
            )


            if not source_recommendations:

                continue


            if isinstance(
                source_recommendations,
                list
            ):

                recommendations.extend(
                    source_recommendations
                )

            else:

                recommendations.append(
                    source_recommendations
                )


        for recommendation in recommendations[:5]:

            if isinstance(recommendation, dict):

                decision_intelligence[
                    "recommendation_summary"
                ].append(

                    recommendation.get(
                        "recommendation",
                        str(recommendation)
                    )
                )

            else:

                decision_intelligence[
                    "recommendation_summary"
                ].append(
                    str(recommendation)
                )


    # ========================================================
    # INSIGHTS INTELLIGENCE
    # ========================================================

    insights_result = get_agent_result(
        previous_agent_results,
        "insights_agent"
    ) or {}


    if insights_result:

        key_findings = insights_result.get(
            "key_findings",
            []
        )


        for finding in key_findings[:5]:

            if isinstance(finding, dict):

                insight = finding.get(
                    "insight"
                )

                if insight:

                    decision_intelligence[
                        "insights_summary"
                    ].append(
                        str(insight)
                    )

            else:

                decision_intelligence[
                    "insights_summary"
                ].append(
                    str(finding)
                )


    # ========================================================
    # RETURN FINAL DECISION CONTEXT
    # ========================================================

    return decision_intelligence
    # ========================================================
    # INSIGHTS INTELLIGENCE
    # ========================================================

    insights_result = get_agent_result(
        previous_agent_results,
        "insights_agent"
    ) or {}

    if insights_result:

        key_findings = insights_result.get(
            "key_findings",
            []
        )

        for finding in key_findings[:5]:

            if isinstance(finding, dict):

                insight = finding.get("insight")

                if insight:

                    decision_intelligence[
                        "insights_summary"
                    ].append(insight)

            else:

                decision_intelligence[
                    "insights_summary"
                ].append(
                    str(finding)
                )

    # ========================================================
    # FINAL RETURN
    # ========================================================

    return decision_intelligence

# ============================================================
# BACKWARD COMPATIBILITY ALIAS
# ============================================================

def extract_decision_context_intelligence(previous_agent_results):
    """
    Compatibility wrapper for older tests and workflow modules.
    """
    return extract_decision_intelligence(previous_agent_results)