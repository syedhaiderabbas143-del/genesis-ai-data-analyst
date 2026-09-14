import pandas as pd
import numpy as np
from datetime import datetime


class RecommendationAgent:
    """
    Genesis AI Recommendation Agent

    Generates intelligent recommendations for:
    - Data quality
    - Analytics workflows
    - Forecasting opportunities
    - Further analysis
    - Business intelligence
    """

    def analyze(self, df: pd.DataFrame, context=None):

        total_rows = int(len(df))
        total_columns = int(len(df.columns))
                # ====================================================
        # ACTUAL CONTEXT INTELLIGENCE
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

        context_intelligence = {

            "context_available": bool(context),

            "previous_agents_count":
                len(previous_agent_results),

            "previous_agents":
                list(previous_agent_results.keys()),

            "shared_context_keys":
                list(shared_context.keys()),

            "intelligence_findings": []
        }

        # ====================================================
        # ROOT CAUSE AGENT INTELLIGENCE
        # ====================================================

        root_cause_execution = previous_agent_results.get(
            "root_cause_agent"
        )

        root_cause_data = {}

        if root_cause_execution:

            root_cause_data = root_cause_execution.get(
                "agent_result",
                {}
            )

            root_cause_summary = root_cause_data.get(
                "root_cause_summary",
                {}
            )

            root_cause_status = root_cause_summary.get(
                "status"
            )

            total_detected_issues = root_cause_summary.get(
                "total_detected_issues",
                0
            )

            if total_detected_issues == 0:

                context_intelligence[
                    "intelligence_findings"
                ].append({

                    "source_agent":
                        "root_cause_agent",

                    "finding":
                        "Root Cause Agent found no major "
                        "data quality or anomaly issues.",

                    "impact":
                        "Data cleaning should not be the "
                        "primary recommendation."
                })

            else:

                context_intelligence[
                    "intelligence_findings"
                ].append({

                    "source_agent":
                        "root_cause_agent",

                    "finding":
                        f"{total_detected_issues} potential "
                        "root cause issues were detected.",

                    "impact":
                        "Issue resolution should be prioritized "
                        "before advanced analysis."
                })
        # ====================================================
        # ACTUAL CONTEXT INTELLIGENCE
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

        context_intelligence = {

            "context_available": bool(context),

            "previous_agents_count":
                len(previous_agent_results),

            "previous_agents":
                list(previous_agent_results.keys()),

            "shared_context_keys":
                list(shared_context.keys()),

            "intelligence_findings": []
        }

        # ====================================================
        # ROOT CAUSE AGENT INTELLIGENCE
        # ====================================================

        root_cause_execution = previous_agent_results.get(
            "root_cause_agent"
        )

        root_cause_data = {}

        if root_cause_execution:

            root_cause_data = root_cause_execution.get(
                "agent_result",
                {}
            )

            root_cause_summary = root_cause_data.get(
                "root_cause_summary",
                {}
            )

            root_cause_status = root_cause_summary.get(
                "status"
            )

            total_detected_issues = root_cause_summary.get(
                "total_detected_issues",
                0
            )

            if total_detected_issues == 0:

                context_intelligence[
                    "intelligence_findings"
                ].append({

                    "source_agent":
                        "root_cause_agent",

                    "finding":
                        "Root Cause Agent found no major "
                        "data quality or anomaly issues.",

                    "impact":
                        "Data cleaning should not be the "
                        "primary recommendation."
                })

            else:

                context_intelligence[
                    "intelligence_findings"
                ].append({

                    "source_agent":
                        "root_cause_agent",

                    "finding":
                        f"{total_detected_issues} potential "
                        "root cause issues were detected.",

                    "impact":
                        "Issue resolution should be prioritized "
                        "before advanced analysis."
                })
        total_missing = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        datetime_columns = df.select_dtypes(
            include=["datetime64[ns]", "datetimetz"]
        ).columns.tolist()
        # -----------------------------------
        # Workflow Context
        # -----------------------------------

        context = context or {}

        previous_agent_results = context.get(
            "previous_agent_results",
            {}
        )

        root_cause_result = previous_agent_results.get(
            "root_cause_agent"
        )

        context_based_recommendations = []

        if root_cause_result:

            context_based_recommendations.append(
                {
                    "source_agent": "root_cause_agent",
                    "message":
                        "Root Cause Agent results were received and "
                        "considered for recommendations."
                }
            )
        # -----------------------------------
        # Data Quality Recommendations
        # -----------------------------------

        data_quality_recommendations = []

        if total_missing > 0:
            data_quality_recommendations.append({
                "priority": "High",
                "recommendation":
                    "Clean or impute missing values before advanced analysis."
            })
        else:
            data_quality_recommendations.append({
                "priority": "Low",
                "recommendation":
                    "No missing values detected. Dataset quality is strong."
            })
        # ====================================================
        # CONTEXT-BASED RECOMMENDATION ADJUSTMENTS
        # ====================================================

        context_based_recommendations = []

        if root_cause_execution:

            root_cause_summary = root_cause_data.get(
                "root_cause_summary",
                {}
            )

            total_detected_issues = root_cause_summary.get(
                "total_detected_issues",
                0
            )

            if total_detected_issues == 0:

                context_based_recommendations.append({

                    "priority": "Medium",

                    "recommendation":
                        "Root Cause Analysis found no major "
                        "dataset issues. Focus on business "
                        "performance analysis, correlation, "
                        "forecasting and hidden patterns.",

                    "reason":
                        "Previous Root Cause Agent detected "
                        "no major issues."
                })

            else:

                context_based_recommendations.append({

                    "priority": "High",

                    "recommendation":
                        "Resolve the issues identified by "
                        "Root Cause Analysis before relying "
                        "on advanced analytics results.",

                    "reason":
                        f"Root Cause Agent detected "
                        f"{total_detected_issues} potential issues."
                })
        if duplicate_rows > 0:
            data_quality_recommendations.append({
                "priority": "High",
                "recommendation":
                    "Remove duplicate records to improve dataset reliability."
            })
        else:
            data_quality_recommendations.append({
                "priority": "Low",
                "recommendation":
                    "No duplicate records detected."
            })

        # -----------------------------------
        # Analytics Recommendations
        # -----------------------------------

        analytics_recommendations = []

        if len(numeric_columns) >= 2:
            analytics_recommendations.append(
                "Run correlation analysis to identify relationships "
                "between numeric variables."
            )

        if len(numeric_columns) > 0:
            analytics_recommendations.append(
                "Run outlier detection on important numeric columns."
            )

        if len(categorical_columns) > 0:
            analytics_recommendations.append(
                "Perform group analysis and comparisons across "
                "categorical variables."
            )

        analytics_recommendations.append(
            "Generate Top/Bottom rankings to identify "
            "high and low performing records."
        )

        # -----------------------------------
        # Forecasting Recommendations
        # -----------------------------------

        forecasting_recommendations = []

        if len(datetime_columns) > 0 and len(numeric_columns) > 0:

            forecasting_recommendations.append(
                "Dataset contains datetime and numeric columns. "
                "Time-series forecasting is recommended."
            )

        elif len(datetime_columns) > 0:

            forecasting_recommendations.append(
                "Datetime columns detected. Add or identify a "
                "numeric metric for forecasting."
            )

        else:

            forecasting_recommendations.append(
                "No dedicated datetime column detected. "
                "Forecasting may require a time-based column."
            )

        # -----------------------------------
        # Advanced Analysis Recommendations
        # -----------------------------------

        advanced_recommendations = []

        if len(numeric_columns) >= 2:

            advanced_recommendations.append(
                "Use correlation matrix analysis for "
                "multi-variable relationships."
            )

        if total_rows >= 1000:

            advanced_recommendations.append(
                "Dataset size is suitable for advanced "
                "statistical and predictive analysis."
            )

        advanced_recommendations.append(
            "Run automated AI insights to identify "
            "hidden patterns and important findings."
        )

        advanced_recommendations.append(
            "Create an executive dashboard for monitoring "
            "key business metrics."
        )

        # -----------------------------------
        # Recommended Workflow
        # -----------------------------------

        recommended_workflow = []

        if total_missing > 0 or duplicate_rows > 0:

            recommended_workflow.append({
                "step": 1,
                "engine":
                    "Data Quality Agent",
                "action":
                    "Resolve missing values and duplicate records."
            })

        recommended_workflow.extend([

            {
                "step": len(recommended_workflow) + 1,
                "engine":
                    "Analyst Agent",
                "action":
                    "Generate statistical and dataset insights."
            },

            {
                "step": len(recommended_workflow) + 2,
                "engine":
                    "Correlation Analysis Engine",
                "action":
                    "Identify relationships between important metrics."
            },

            {
                "step": len(recommended_workflow) + 3,
                "engine":
                    "Insights Agent",
                "action":
                    "Discover key findings and hidden patterns."
            },

            {
                "step": len(recommended_workflow) + 4,
                "engine":
                    "Forecast Agent",
                "action":
                    "Evaluate forecasting opportunities."
            },

            {
                "step": len(recommended_workflow) + 5,
                "engine":
                    "Dashboard Engine",
                "action":
                    "Visualize important KPIs and insights."
            }

        ])

        # -----------------------------------
        # Overall Readiness
        # -----------------------------------

        if (
            total_missing == 0
            and duplicate_rows == 0
        ):
            readiness_status = "Excellent"

            readiness_message = (
                "Dataset is clean and ready for advanced "
                "analytics workflows."
            )

        elif total_missing > 0 or duplicate_rows > 0:

            readiness_status = "Needs Attention"

            readiness_message = (
                "Dataset should be cleaned before proceeding "
                "with advanced analysis."
            )

        else:

            readiness_status = "Ready"

            readiness_message = (
                "Dataset is ready for analysis."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Recommendation Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "dataset_overview": {

                "total_rows": total_rows,

                "total_columns": total_columns,

                "numeric_columns":
                    len(numeric_columns),

                "categorical_columns":
                    len(categorical_columns),

                "datetime_columns":
                    len(datetime_columns),

                "missing_values":
                    total_missing,

                "duplicate_rows":
                    duplicate_rows
            },

            "dataset_readiness": {

                "status":
                    readiness_status,

                "message":
                    readiness_message
            },

            "data_quality_recommendations":
                data_quality_recommendations,

            "analytics_recommendations":
                analytics_recommendations,

            "forecasting_recommendations":
                forecasting_recommendations,

            "advanced_analysis_recommendations":
                advanced_recommendations,
                
                "context_based_recommendations":
    context_based_recommendations,

            "recommended_workflow":
                recommended_workflow,            "context_intelligence":
                context_intelligence,

            "context_based_recommendations":
                context_based_recommendations

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_recommendation_agent(df, context=None):

    agent = RecommendationAgent()

    return agent.analyze(
        df,
        context=context
    )