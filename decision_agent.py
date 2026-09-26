import pandas as pd
import numpy as np
from datetime import datetime
from context_intelligence import extract_decision_intelligence


def run_decision_agent(
    df: pd.DataFrame,
    context=None
):
    # -----------------------------------
    # Workflow Context
    # -----------------------------------

    context = context or {}

    previous_agent_results = context.get(
        "previous_agent_results",
        {}
    )

    shared_context = context.get(
        "shared_context",
        {}
    )

    context_information = {

        "context_available": bool(context),

        "previous_agents_count":
            len(previous_agent_results),

        "previous_agents":
            list(previous_agent_results.keys()),

        "shared_context_keys":
            list(shared_context.keys())
    }

    context_based_decisions = []

    # -----------------------------------
    # Check Root Cause Agent Result
    # -----------------------------------

    root_cause_result = previous_agent_results.get(
        "root_cause_agent"
    )

    if root_cause_result:

        context_based_decisions.append({

            "source_agent": "root_cause_agent",

            "decision":
                "Root Cause Analysis was considered "
                "before generating final decisions."
        })

    # -----------------------------------
    # Check Recommendation Agent Result
    # -----------------------------------

    recommendation_result = previous_agent_results.get(
        "recommendation_agent"
    )

    if recommendation_result:

        context_based_decisions.append({

            "source_agent": "recommendation_agent",

            "decision":
                "Recommendation Agent results were considered "
                "for decision making."
        })

    # -----------------------------------
    # Check Insights Agent Result
    # -----------------------------------

    insights_result = previous_agent_results.get(
        "insights_agent"
    )

    if insights_result:

        context_based_decisions.append({

            "source_agent": "insights_agent",

            "decision":
                "Insights Agent findings were considered "
                "for decision making."
        })
    if df is None or df.empty:
        return {
            "success": False,
            "message": "No dataset available for decision analysis."
        }
        # ====================================================
    # WORKFLOW CONTEXT
    # ====================================================

    context = context or {}

    previous_agent_results = context.get(
        "previous_agent_results",
        {}
    )

    shared_context = context.get(
        "shared_context",
        {}
    )

    # ====================================================
    # ACTUAL DECISION CONTEXT INTELLIGENCE
    # ====================================================

    decision_context_intelligence = (
        extract_decision_intelligence(
            previous_agent_results
        )
    )

    total_rows = len(df)
    total_columns = len(df.columns)

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    decisions = []
    # ====================================================
    # CONTEXT-BASED DECISIONS
    # ====================================================

    if decision_context_intelligence.get(
        "context_available"
    ):

        # ------------------------------------------------
        # ROOT CAUSE BASED DECISIONS
        # ------------------------------------------------

        root_causes = decision_context_intelligence.get(
            "root_cause_summary",
            []
        )

        for root_cause in root_causes:

            # Safety check:
            # Root cause must be a dictionary

            if not isinstance(root_cause, dict):
                continue

            severity = root_cause.get(
                "severity",
                "Medium"
            )

            issue_type = root_cause.get(
                "issue_type",
                "Unknown Issue"
            )

            column = root_cause.get(
                "column",
                "Dataset"
            )

            decisions.append({

                "decision_area":
                    "Root Cause Response",

                "priority":
                    severity,

                "decision":
                    (
                        f"Address {issue_type} detected "
                        f"in {column}."
                    ),

                "reason":
                    (
                        "This decision is based on Root Cause "
                        "Agent analysis."
                    ),

                "source_agent":
                    "root_cause_agent"
            })

            issue_type = root_cause.get(
                "issue_type",
                "Unknown Issue"
            )

            column = root_cause.get(
                "column",
                "Dataset"
            )

            decisions.append({

                "decision_area":
                    "Root Cause Response",

                "priority":
                    severity,

                "decision":
                    (
                        f"Address {issue_type} detected "
                        f"in {column}."
                    ),

                "reason":
                    (
                        "This decision is based on Root Cause "
                        "Agent analysis."
                    ),

                "source_agent":
                    "root_cause_agent"
            })


        # ------------------------------------------------
        # RECOMMENDATION BASED DECISIONS
        # ------------------------------------------------

        recommendations = (
            decision_context_intelligence.get(
                "recommendation_summary",
                []
            )
        )

        
        for recommendation in recommendations:

            if isinstance(recommendation, dict):

                recommendation_text = recommendation.get(
                    "recommendation",
                    str(recommendation)
                )

            else:

                recommendation_text = str(
                    recommendation
                )


            decisions.append({

                "decision_area":
                    "Recommendation Implementation",

                "priority":
                    "Medium",

                "decision":
                    recommendation_text,

                "reason":
                    (
                        "This decision is based on actionable "
                        "recommendations from Recommendation Agent."
                    ),

                "source_agent":
                    "recommendation_agent"
            })


        # ------------------------------------------------
        # INSIGHTS BASED DECISIONS
        # ------------------------------------------------

        insights = decision_context_intelligence.get(
            "insights_summary",
            []
        )

        for insight in insights:

            if isinstance(insight, dict):

                insight_text = insight.get(
                    "insight",
                    str(insight)
                )

            else:

                insight_text = str(insight)


            decisions.append({

                "decision_area":
                    "Insight-Based Strategy",

                "priority":
                    "Medium",

                "decision":
                    (
                        "Review and act on the identified "
                        "business insight."
                    ),

                "reason":
                    insight_text,

                "source_agent":
                    "insights_agent"
            })
            decisions.append({

                "decision_area":
                    "Insight-Based Strategy",

                "priority":
                    "Medium",

                "decision":
                    (
                        "Review and act on the identified "
                        "business insight."
                    ),

                "reason":
                    insight,

                "source_agent":
                    "insights_agent"
            })
    # -----------------------------------
    # Data Quality Decision
    # -----------------------------------

    if missing_values > 0:

        decisions.append({
            "decision_area": "Data Quality",
            "priority": "High",
            "decision": "Improve data collection and handle missing values.",
            "reason": f"{missing_values} missing values detected."
        })

    else:

        decisions.append({
            "decision_area": "Data Quality",
            "priority": "Low",
            "decision": "Maintain current data quality standards.",
            "reason": "No missing values detected."
        })

    # -----------------------------------
    # Duplicate Data Decision
    # -----------------------------------

    if duplicate_rows > 0:

        decisions.append({
            "decision_area": "Data Management",
            "priority": "Medium",
            "decision": "Remove duplicate records before further analysis.",
            "reason": f"{duplicate_rows} duplicate records detected."
        })

    # -----------------------------------
    # Numeric Variability Decisions
    # -----------------------------------

    high_variability_columns = []

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) == 0:
            continue

        mean_value = series.mean()
        std_value = series.std()

        if mean_value != 0:

            coefficient_variation = abs(
                (std_value / mean_value) * 100
            )

            if coefficient_variation > 100:

                high_variability_columns.append({
                    "column": column,
                    "coefficient_variation": round(
                        float(coefficient_variation),
                        2
                    )
                })

    if high_variability_columns:

        decisions.append({
            "decision_area": "Business Performance",
            "priority": "High",
            "decision": (
                "Investigate high variability metrics and "
                "segment the dataset for deeper analysis."
            ),
            "reason": (
                f"{len(high_variability_columns)} numeric "
                "columns show high variability."
            )
        })

    # -----------------------------------
    # Dataset Size Decision
    # -----------------------------------

    if total_rows >= 1000:

        decisions.append({
            "decision_area": "Analytics Readiness",
            "priority": "Medium",
            "decision": (
                "Proceed with advanced analytics, forecasting "
                "and machine learning workflows."
            ),
            "reason": (
                f"Dataset contains {total_rows} records, "
                "which is sufficient for deeper analysis."
            )
        })

    else:

        decisions.append({
            "decision_area": "Analytics Readiness",
            "priority": "High",
            "decision": (
                "Collect additional data before advanced "
                "forecasting and machine learning."
            ),
            "reason": (
                f"Dataset contains only {total_rows} records."
            )
        })

    # -----------------------------------
    # Decision Priority Summary
    # -----------------------------------

    high_priority = len([
        decision
        for decision in decisions
        if decision["priority"] == "High"
    ])

    medium_priority = len([
        decision
        for decision in decisions
        if decision["priority"] == "Medium"
    ])

    low_priority = len([
        decision
        for decision in decisions
        if decision["priority"] == "Low"
    ])

    if high_priority > 0:
        overall_decision_status = "Action Required"
    else:
        overall_decision_status = "Ready for Advanced Analytics"

    # -----------------------------------
    # Final Response
    # -----------------------------------

    return {
        "success": True,

        "analysis_type": "Genesis AI Decision Agent",

        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "dataset_overview": {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "numeric_columns": len(numeric_columns),
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows
        },

        "decision_summary": {
            "overall_status": overall_decision_status,
            "total_decisions": len(decisions),
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority
        },
        "workflow_context": {

    "context_available":
        decision_context_intelligence.get(
            "context_available",
            False
        ),

    "previous_agents":
        list(
            previous_agent_results.keys()
        ),

    "shared_context_keys":
        list(
            shared_context.keys()
        )
},

"actual_context_intelligence":
    decision_context_intelligence,

                "high_variability_columns":
            high_variability_columns,

        "recommended_decisions":
            decisions,

        "context_information":
            context_information,

        "context_based_decisions":
            context_based_decisions
    }