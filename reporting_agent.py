import pandas as pd
import numpy as np
from datetime import datetime
from context_intelligence import build_context_intelligence


class ReportingAgent:
    """
    Genesis AI Reporting Agent

    Generates a structured analytics report containing:
    - Executive summary
    - Dataset overview
    - Data quality summary
    - Numeric insights
    - Key findings
    - Recommended next actions
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

        context_based_report_sources = []

        # -----------------------------------
        # Check Previous Agent Results
        # -----------------------------------

        for agent_name in previous_agent_results.keys():

            context_based_report_sources.append(
                {
                    "source_agent": agent_name,
                    "status":
                        "Previous agent result received "
                        "for report generation."
                }
            )
                        # -----------------------------------
            # Build Actual Context Intelligence
            # -----------------------------------

            context_intelligence = build_context_intelligence(
                previous_agent_results
            )

            root_cause_intelligence = (
                context_intelligence.get(
                    "root_cause_intelligence",
                    []
                )
            )

            recommendation_intelligence = (
                context_intelligence.get(
                    "recommendation_intelligence",
                    []
                )
            )

            insights_intelligence = (
                context_intelligence.get(
                    "insights_intelligence",
                    {}
                )
            )

            decision_intelligence = (
                context_intelligence.get(
                    "decision_intelligence",
                    []
                )
            )
        if df is None or df.empty:
            return {
                "success": False,
                "message": "No dataset available for reporting."
            }

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        total_missing = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

        # -----------------------------------
        # Dataset Overview
        # -----------------------------------

        dataset_overview = {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "numeric_columns": len(numeric_columns),
            "categorical_columns": len(categorical_columns)
        }

        # -----------------------------------
        # Data Quality Summary
        # -----------------------------------

        total_cells = total_rows * total_columns

        missing_percentage = 0

        if total_cells > 0:
            missing_percentage = round(
                (total_missing / total_cells) * 100,
                2
            )

        if total_missing == 0 and duplicate_rows == 0:
            quality_status = "Excellent"

        elif missing_percentage < 5:
            quality_status = "Good"

        else:
            quality_status = "Needs Attention"

        data_quality_summary = {
            "status": quality_status,
            "missing_values": total_missing,
            "missing_percentage": missing_percentage,
            "duplicate_rows": duplicate_rows
        }

        # -----------------------------------
        # Numeric Summary
        # -----------------------------------

        numeric_summary = {}

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            numeric_summary[column] = {
                "minimum": round(float(series.min()), 2),
                "maximum": round(float(series.max()), 2),
                "average": round(float(series.mean()), 2),
                "median": round(float(series.median()), 2)
            }

        # -----------------------------------
        # Key Findings
        # -----------------------------------

        key_findings = []

        if total_missing == 0:
            key_findings.append(
                "No missing values were detected."
            )
        else:
            key_findings.append(
                f"{total_missing} missing values require review."
            )

        if duplicate_rows == 0:
            key_findings.append(
                "No duplicate records were detected."
            )
        else:
            key_findings.append(
                f"{duplicate_rows} duplicate records were detected."
            )

        if len(numeric_columns) >= 2:
            key_findings.append(
                "Dataset contains multiple numeric variables "
                "suitable for correlation and statistical analysis."
            )

        if total_rows >= 1000:
            key_findings.append(
                "Dataset size is sufficient for advanced analytics."
            )
        # -----------------------------------
        # Context-Based Key Findings
        # -----------------------------------

        if root_cause_intelligence:

            key_findings.append(
                f"{len(root_cause_intelligence)} root cause "
                "findings were identified by previous analysis."
            )

        insights_findings = insights_intelligence.get(
            "key_findings",
            []
        )

        for finding in insights_findings[:5]:

            if isinstance(finding, dict):

                insight_text = finding.get("insight")

                if insight_text:

                    key_findings.append(
                        f"AI Insight: {insight_text}"
                    )

            elif isinstance(finding, str):

                key_findings.append(
                    f"AI Insight: {finding}"
                )

        if decision_intelligence:

            key_findings.append(
                f"{len(decision_intelligence)} business "
                "decisions were generated by the Decision Agent."
            )
        # -----------------------------------
        # Recommended Actions
        # -----------------------------------

        recommended_actions = []

        if total_missing > 0:
            recommended_actions.append(
                {
                    "priority": "High",
                    "action":
                        "Run the Data Cleaning Engine to resolve missing values."
                }
            )

        if duplicate_rows > 0:
            recommended_actions.append(
                {
                    "priority": "High",
                    "action":
                        "Remove duplicate records before advanced analysis."
                }
            )

        if len(numeric_columns) >= 2:
            recommended_actions.append(
                {
                    "priority": "Medium",
                    "action":
                        "Run correlation and statistical analysis."
                }
            )

        if total_rows >= 100:
            recommended_actions.append(
                {
                    "priority": "Medium",
                    "action":
                        "Evaluate forecasting and predictive analysis opportunities."
                }
            )

        recommended_actions.append(
            {
                "priority": "Low",
                "action":
                    "Generate an executive dashboard and export analytics report."
            }
        )

        # -----------------------------------
        # Executive Summary
        # -----------------------------------
        previous_agents_count = len(
            previous_agent_results
        )

        executive_summary = (
            
            f"The dataset contains {total_rows} rows and "
            f"{total_columns} columns. "
            f"Data quality status is {quality_status}. "
        )
        if previous_agents_count > 0:

            executive_summary += (
                f" This report also considered results from "
                f"{previous_agents_count} previous AI agent(s)."
            )
        if total_missing == 0 and duplicate_rows == 0:
            executive_summary += (
                "The dataset is clean and ready for advanced analytics."
            )
        else:
            executive_summary += (
                "Data quality improvements are recommended before "
                "advanced analytics."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Reporting Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "executive_summary":
                executive_summary,

            "dataset_overview":
                dataset_overview,

            "data_quality_summary":
                data_quality_summary,

            "numeric_summary":
                numeric_summary,

            "key_findings":
                key_findings,

                        "recommended_actions":
                recommended_actions,

            "context_information":
                context_information,

            "context_based_report_sources":
                context_based_report_sources
        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_reporting_agent(df, context=None):

    agent = ReportingAgent()

    return agent.analyze(
        df,
        context=context
    )