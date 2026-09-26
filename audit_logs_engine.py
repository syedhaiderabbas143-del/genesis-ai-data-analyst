import pandas as pd
from datetime import datetime


class AuditLogsEngine:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Audit Logs Engine

        Tracks important dataset analysis events,
        dataset changes, quality information and
        audit history for the current analysis.
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        audit_logs = []

        # -----------------------------------
        # Dataset Loaded Event
        # -----------------------------------

        audit_logs.append({
            "event_id": 1,
            "event_type": "Dataset Loaded",
            "status": "Success",
            "timestamp": timestamp,
            "details": {
                "total_rows": total_rows,
                "total_columns": total_columns
            }
        })

        # -----------------------------------
        # Schema Audit
        # -----------------------------------

        column_types = {}

        for column in df.columns:

            column_types[column] = str(
                df[column].dtype
            )

        audit_logs.append({
            "event_id": 2,
            "event_type": "Schema Inspection",
            "status": "Success",
            "timestamp": timestamp,
            "details": {
                "column_count": total_columns,
                "column_types": column_types
            }
        })

        # -----------------------------------
        # Missing Values Audit
        # -----------------------------------

        total_missing = int(
            df.isna().sum().sum()
        )

        missing_status = (
            "Warning"
            if total_missing > 0
            else "Success"
        )

        audit_logs.append({
            "event_id": 3,
            "event_type": "Missing Data Check",
            "status": missing_status,
            "timestamp": timestamp,
            "details": {
                "total_missing_values":
                    total_missing
            }
        })

        # -----------------------------------
        # Duplicate Records Audit
        # -----------------------------------

        duplicate_rows = int(
            df.duplicated().sum()
        )

        duplicate_status = (
            "Warning"
            if duplicate_rows > 0
            else "Success"
        )

        audit_logs.append({
            "event_id": 4,
            "event_type": "Duplicate Records Check",
            "status": duplicate_status,
            "timestamp": timestamp,
            "details": {
                "duplicate_rows":
                    duplicate_rows
            }
        })

        # -----------------------------------
        # Numeric Columns Audit
        # -----------------------------------

        numeric_columns = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        audit_logs.append({
            "event_id": 5,
            "event_type": "Numeric Columns Detection",
            "status": "Success",
            "timestamp": timestamp,
            "details": {
                "numeric_columns_count":
                    len(numeric_columns),
                "numeric_columns":
                    numeric_columns
            }
        })

        # -----------------------------------
        # Categorical Columns Audit
        # -----------------------------------

        categorical_columns = list(
            df.select_dtypes(
                exclude="number"
            ).columns
        )

        audit_logs.append({
            "event_id": 6,
            "event_type": "Categorical Columns Detection",
            "status": "Success",
            "timestamp": timestamp,
            "details": {
                "categorical_columns_count":
                    len(categorical_columns),
                "categorical_columns":
                    categorical_columns
            }
        })

        # -----------------------------------
        # Dataset Quality Summary
        # -----------------------------------

        quality_issues = 0

        if total_missing > 0:
            quality_issues += 1

        if duplicate_rows > 0:
            quality_issues += 1

        if quality_issues == 0:
            quality_status = "Excellent"

        elif quality_issues == 1:
            quality_status = "Good"

        else:
            quality_status = "Needs Attention"

        audit_logs.append({
            "event_id": 7,
            "event_type": "Dataset Quality Audit",
            "status": quality_status,
            "timestamp": timestamp,
            "details": {
                "quality_issues_detected":
                    quality_issues
            }
        })

        # -----------------------------------
        # Final Audit Summary
        # -----------------------------------

        successful_events = sum(
            1
            for log in audit_logs
            if log["status"] == "Success"
        )

        warning_events = sum(
            1
            for log in audit_logs
            if log["status"] == "Warning"
        )

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Audit Logs",

            "generated_at":
                timestamp,

            "audit_summary": {

                "total_events":
                    len(audit_logs),

                "successful_events":
                    successful_events,

                "warning_events":
                    warning_events,

                "dataset_quality_status":
                    quality_status

            },

            "dataset_overview": {

                "total_rows":
                    total_rows,

                "total_columns":
                    total_columns,

                "total_missing_values":
                    total_missing,

                "duplicate_rows":
                    duplicate_rows

            },

            "audit_logs":
                audit_logs

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_audit_logs_analysis(df):

    engine = AuditLogsEngine()

    return engine.analyze(df)