import pandas as pd
from datetime import datetime


class SchemaEvolutionEngine:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Schema Evolution Engine

        Analyzes the current dataset schema and creates
        a baseline snapshot for tracking future schema changes.
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        generated_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # -----------------------------------
        # Current Schema
        # -----------------------------------

        current_schema = {}

        for column in df.columns:

            current_schema[column] = {
                "dtype": str(df[column].dtype),
                "missing_values": int(
                    df[column].isna().sum()
                ),
                "unique_values": int(
                    df[column].nunique()
                )
            }

        # -----------------------------------
        # Column Categories
        # -----------------------------------

        numeric_columns = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        datetime_columns = list(
            df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )

        categorical_columns = [
            column
            for column in df.columns
            if column not in numeric_columns
            and column not in datetime_columns
        ]

        # -----------------------------------
        # Schema Fingerprint
        # -----------------------------------

        schema_signature = []

        for column in df.columns:

            schema_signature.append({
                "column": column,
                "dtype": str(df[column].dtype)
            })

        # -----------------------------------
        # Potential Schema Risks
        # -----------------------------------

        schema_alerts = []

        duplicate_column_names = (
            df.columns[
                df.columns.duplicated()
            ].tolist()
        )

        if duplicate_column_names:

            schema_alerts.append({
                "type": "Duplicate Column Names",
                "severity": "Warning",
                "columns": duplicate_column_names,
                "message":
                    "Duplicate column names detected."
            })

        columns_with_missing = []

        for column in df.columns:

            missing_count = int(
                df[column].isna().sum()
            )

            if missing_count > 0:

                columns_with_missing.append({
                    "column": column,
                    "missing_values": missing_count
                })

        if columns_with_missing:

            schema_alerts.append({
                "type": "Schema Data Quality",
                "severity": "Warning",
                "affected_columns":
                    columns_with_missing,
                "message":
                    "Some schema columns contain missing values."
            })

        # -----------------------------------
        # Schema Status
        # -----------------------------------

        if not schema_alerts:
            schema_status = "Stable"

        else:
            schema_status = "Attention Required"

        # -----------------------------------
        # Evolution Recommendations
        # -----------------------------------

        recommendations = []

        recommendations.append(
            "Store the current schema snapshot as a baseline."
        )

        recommendations.append(
            "Compare future uploaded datasets against this schema."
        )

        if columns_with_missing:

            recommendations.append(
                "Review columns containing missing values."
            )

        if duplicate_column_names:

            recommendations.append(
                "Rename duplicate columns before further analysis."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Schema Evolution",

            "generated_at":
                generated_at,

            "dataset_overview": {

                "total_rows":
                    total_rows,

                "total_columns":
                    total_columns

            },

            "schema_status":
                schema_status,

            "schema_summary": {

                "numeric_columns_count":
                    len(numeric_columns),

                "categorical_columns_count":
                    len(categorical_columns),

                "datetime_columns_count":
                    len(datetime_columns)

            },

            "current_schema":
                current_schema,

            "schema_signature":
                schema_signature,

            "schema_alerts":
                schema_alerts,

            "recommendations":
                recommendations

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_schema_evolution_analysis(df):

    engine = SchemaEvolutionEngine()

    return engine.analyze(df)