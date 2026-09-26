import pandas as pd
import numpy as np
from datetime import datetime
from context_intelligence import (
    extract_insights_context_intelligence
)

class InsightsAgent:
    """
    Genesis AI Insights Agent

    Automatically discovers important insights,
    trends, extremes, anomalies and recommendations
    from the uploaded dataset.
    """

    def analyze(self, df: pd.DataFrame, context=None):
                # -----------------------------------
        # Workflow Context
        # -----------------------------------

        context = context or {}

        previous_agent_results = context.get(
            "previous_agent_results",
            {}
        )
        # ====================================================
        # ACTUAL INSIGHTS CONTEXT INTELLIGENCE
        # ====================================================

        actual_context_intelligence = (
            extract_insights_context_intelligence(
                previous_agent_results
            )
        )
        shared_context = context.get(
            "shared_context",
            {}
        )

        previous_agents = list(
            previous_agent_results.keys()
        )

        context_information = {

            "context_available": bool(context),

            "previous_agents_count":
                len(previous_agent_results),

            "previous_agents":
                previous_agents,

            "shared_context_keys":
                list(shared_context.keys())
        }

        context_based_findings = []

        # Check Root Cause Agent Result
        root_cause_result = previous_agent_results.get(
            "root_cause_agent"
        )

        if root_cause_result:

            context_based_findings.append(
                {
                    "source_agent": "root_cause_agent",
                    "finding":
                        "Root Cause Analysis results were "
                        "received and considered."
                }
            )

        # Check Recommendation Agent Result
        recommendation_result = previous_agent_results.get(
            "recommendation_agent"
        )

        if recommendation_result:

            context_based_findings.append(
                {
                    "source_agent": "recommendation_agent",
                    "finding":
                        "Recommendation Agent results were "
                        "received and considered."
                }
            )
        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        # -----------------------------------
        # Dataset Overview
        # -----------------------------------

        overview = {
            
            "total_rows": total_rows,
            "total_columns": total_columns,
            "numeric_columns": len(numeric_columns),
            "categorical_columns": len(categorical_columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum())
        }

        # -----------------------------------
        # Numeric Insights
        # -----------------------------------

        numeric_insights = {}

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            numeric_insights[column] = {
                "minimum": round(float(series.min()), 2),
                "maximum": round(float(series.max()), 2),
                "average": round(float(series.mean()), 2),
                "median": round(float(series.median()), 2),
                "standard_deviation": round(
                    float(series.std()), 2
                ) if len(series) > 1 else 0
            }

        # -----------------------------------
        # Categorical Insights
        # -----------------------------------

        categorical_insights = {}

        for column in categorical_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            value_counts = series.value_counts()

            top_value = None
            top_count = 0

            if len(value_counts) > 0:

                top_value = str(value_counts.index[0])
                top_count = int(value_counts.iloc[0])

            categorical_insights[column] = {
                "unique_values": int(series.nunique()),
                "most_common_value": top_value,
                "most_common_count": top_count
            }

        # -----------------------------------
        # Automatic Key Findings
        # -----------------------------------

        key_findings = []

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            key_findings.append(
                {
                    "column": column,
                    "insight": (
                        f"{column} ranges from "
                        f"{round(float(series.min()), 2)} to "
                        f"{round(float(series.max()), 2)} "
                        f"with an average of "
                        f"{round(float(series.mean()), 2)}."
                    )
                }
            )

        # -----------------------------------
        # Top Dataset Metrics
        # -----------------------------------

        top_metrics = []

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            top_metrics.append(
                {
                    "column": column,
                    "maximum_value": round(
                        float(series.max()), 2
                    ),
                    "minimum_value": round(
                        float(series.min()), 2
                    ),
                    "average_value": round(
                        float(series.mean()), 2
                    )
                }
            )

        # -----------------------------------
        # Potential Anomaly Detection
        # -----------------------------------

        anomaly_summary = {}

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) < 4:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            anomalies = series[
                (series < lower_bound) |
                (series > upper_bound)
            ]

            anomaly_summary[column] = {
                "potential_anomalies": int(
                    len(anomalies)
                ),
                "lower_bound": round(
                    float(lower_bound), 2
                ),
                "upper_bound": round(
                    float(upper_bound), 2
                )
            }

        # -----------------------------------
        # Recommendations
        # -----------------------------------

        recommendations = []

        missing_values = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        if missing_values > 0:

            recommendations.append(
                "Review and clean missing values "
                "before advanced analysis."
            )

        if duplicate_rows > 0:

            recommendations.append(
                "Remove duplicate records to improve "
                "dataset reliability."
            )

        anomaly_columns = []

        for column, result in anomaly_summary.items():

            if result["potential_anomalies"] > 0:
                anomaly_columns.append(column)

        if anomaly_columns:

            recommendations.append(
                "Review potential outliers detected in: "
                + ", ".join(anomaly_columns[:5])
            )

        if not recommendations:

            recommendations.append(
                "Dataset quality appears strong. "
                "Proceed with advanced analytics, "
                "forecasting and business intelligence."
            )

        # -----------------------------------
        # Agent Summary
        # -----------------------------------

        if missing_values == 0 and duplicate_rows == 0:

            agent_summary = (
                "Dataset is clean and ready for "
                "advanced analysis."
            )

        else:

            agent_summary = (
                "Dataset contains quality issues that "
                "should be reviewed before advanced analysis."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Insights Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "agent_summary":
                agent_summary,

            "dataset_overview":
                overview,

            "numeric_insights":
                numeric_insights,

            "categorical_insights":
                categorical_insights,

            "key_findings":
                key_findings,

            "top_metrics":
                top_metrics,

                        "anomaly_summary":
                anomaly_summary,

            "recommendations":
                recommendations,

            "context_information":
                context_information,
"actual_context_intelligence":
    actual_context_intelligence,
            "context_based_findings":
                context_based_findings

        }

        


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_insights_agent(df, context=None):

    agent = InsightsAgent()

    return agent.analyze(
        df,
        context=context
    )
