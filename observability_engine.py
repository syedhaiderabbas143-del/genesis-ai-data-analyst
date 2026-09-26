import pandas as pd
import numpy as np
from datetime import datetime


class ObservabilityEngine:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Dataset Observability Engine
        Monitors dataset health, freshness, schema,
        missing values, duplicates and anomalies.
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        # -----------------------------
        # Missing Values
        # -----------------------------
        missing_by_column = {}

        for column in df.columns:
            missing_count = int(df[column].isna().sum())

            if missing_count > 0:
                missing_by_column[column] = {
                    "missing_count": missing_count,
                    "missing_percentage": round(
                        (missing_count / total_rows) * 100, 2
                    ) if total_rows > 0 else 0
                }

        total_missing = int(df.isna().sum().sum())

        # -----------------------------
        # Duplicate Records
        # -----------------------------
        duplicate_rows = int(df.duplicated().sum())

        # -----------------------------
        # Dataset Health Score
        # -----------------------------
        missing_penalty = 0
        duplicate_penalty = 0

        total_cells = total_rows * total_columns

        if total_cells > 0:
            missing_percentage = (
                total_missing / total_cells
            ) * 100

            missing_penalty = min(
                missing_percentage,
                40
            )

        if total_rows > 0:
            duplicate_percentage = (
                duplicate_rows / total_rows
            ) * 100

            duplicate_penalty = min(
                duplicate_percentage,
                30
            )

        health_score = round(
            max(
                0,
                100 - missing_penalty - duplicate_penalty
            ),
            2
        )

        # -----------------------------
        # Dataset Status
        # -----------------------------
        if health_score >= 90:
            health_status = "Excellent"

        elif health_score >= 75:
            health_status = "Good"

        elif health_score >= 50:
            health_status = "Warning"

        else:
            health_status = "Critical"

        # -----------------------------
        # Column Data Types
        # -----------------------------
        schema = {}

        for column in df.columns:

            schema[column] = {
                "dtype": str(df[column].dtype),
                "unique_values": int(
                    df[column].nunique()
                )
            }

        # -----------------------------
        # Numeric Column Monitoring
        # -----------------------------
        numeric_monitoring = {}

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) > 0:

                numeric_monitoring[column] = {
                    "min": round(
                        float(series.min()), 2
                    ),

                    "max": round(
                        float(series.max()), 2
                    ),

                    "mean": round(
                        float(series.mean()), 2
                    ),

                    "median": round(
                        float(series.median()), 2
                    ),

                    "std": round(
                        float(series.std()), 2
                    ) if len(series) > 1 else 0
                }

        # -----------------------------
        # Observability Alerts
        # -----------------------------
        alerts = []

        if total_missing > 0:

            alerts.append({
                "type": "Missing Data",
                "severity": "Warning",
                "message":
                    f"{total_missing} missing values detected."
            })

        if duplicate_rows > 0:

            alerts.append({
                "type": "Duplicate Records",
                "severity": "Warning",
                "message":
                    f"{duplicate_rows} duplicate rows detected."
            })

        if health_score < 50:

            alerts.append({
                "type": "Dataset Health",
                "severity": "Critical",
                "message":
                    "Dataset health requires immediate attention."
            })

        elif health_score < 75:

            alerts.append({
                "type": "Dataset Health",
                "severity": "Warning",
                "message":
                    "Dataset health needs improvement."
            })

        if not alerts:

            alerts.append({
                "type": "System Health",
                "severity": "Success",
                "message":
                    "Dataset observability checks passed successfully."
            })

        # -----------------------------
        # Final Response
        # -----------------------------
        return {

            "success": True,

            "analysis_type":
                "Genesis AI Dataset Observability",

            "observed_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

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

            "dataset_health": {

                "health_score":
                    health_score,

                "status":
                    health_status

            },

            "missing_data_monitoring":
                missing_by_column,

            "schema_monitoring":
                schema,

            "numeric_monitoring":
                numeric_monitoring,

            "alerts":
                alerts

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_observability_analysis(df):

    engine = ObservabilityEngine()

    return engine.analyze(df)