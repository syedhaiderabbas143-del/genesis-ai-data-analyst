import pandas as pd
import numpy as np
from datetime import datetime


def run_root_cause_analysis(df: pd.DataFrame, context=None):
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
    if df is None or df.empty:
        return {
            "success": False,
            "message": "No dataset available for root cause analysis."
        }

    total_rows = len(df)
    total_columns = len(df.columns)

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    root_causes = []

    # -----------------------------------
    # Missing Values Root Cause
    # -----------------------------------

    for column in df.columns:

        missing_count = int(df[column].isnull().sum())

        if missing_count > 0:

            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            )

            root_causes.append({
                "issue_type": "Missing Data",
                "column": column,
                "severity": (
                    "High"
                    if missing_percentage > 20
                    else "Medium"
                    if missing_percentage > 5
                    else "Low"
                ),
                "affected_records": missing_count,
                "percentage": missing_percentage,
                "possible_root_cause": (
                    "Incomplete data collection or "
                    "missing values during data entry."
                )
            })

    # -----------------------------------
    # Duplicate Records Root Cause
    # -----------------------------------

    if duplicate_rows > 0:

        duplicate_percentage = round(
            (duplicate_rows / total_rows) * 100,
            2
        )

        root_causes.append({
            "issue_type": "Duplicate Records",
            "column": "Dataset",
            "severity": (
                "High"
                if duplicate_percentage > 10
                else "Medium"
                if duplicate_percentage > 2
                else "Low"
            ),
            "affected_records": duplicate_rows,
            "percentage": duplicate_percentage,
            "possible_root_cause": (
                "Duplicate data ingestion or repeated "
                "data entry."
            )
        })

    # -----------------------------------
    # Outlier Root Cause Analysis
    # -----------------------------------

    outlier_analysis = {}

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = series[
            (series < lower_bound) |
            (series > upper_bound)
        ]

        outlier_count = len(outliers)

        if outlier_count > 0:

            outlier_percentage = round(
                (outlier_count / len(series)) * 100,
                2
            )

            outlier_analysis[column] = {
                "outlier_count": int(outlier_count),
                "outlier_percentage": outlier_percentage,
                "possible_root_cause": (
                    "Extreme values, unusual business events, "
                    "or possible data entry errors."
                )
            }

    # -----------------------------------
    # Root Cause Summary
    # -----------------------------------

    total_detected_issues = (
        len(root_causes) +
        len(outlier_analysis)
    )

    if total_detected_issues == 0:

        overall_status = "No Major Issues Detected"

        summary_message = (
            "Dataset appears clean. No significant root "
            "causes were detected."
        )

    else:

        overall_status = "Issues Detected"

        summary_message = (
            f"{total_detected_issues} potential root cause "
            "issues were detected."
        )

    # -----------------------------------
    # Final Response
    # -----------------------------------

    return {
        "success": True,

        "analysis_type": "Genesis AI Root Cause Analysis",

        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "dataset_overview": {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "numeric_columns": len(numeric_columns),
            "categorical_columns": len(categorical_columns),
            "total_missing_values": missing_values,
            "duplicate_rows": duplicate_rows
        },

        "root_cause_summary": {
            "status": overall_status,
            "total_detected_issues": total_detected_issues,
            "message": summary_message
        },

                "identified_root_causes": root_causes,

        "outlier_root_causes": outlier_analysis,

        "context_information": context_information
    }