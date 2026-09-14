import pandas as pd
import numpy as np
from datetime import datetime


class MetadataEngine:
    """
    Genesis AI Metadata Intelligence Engine

    Automatically analyzes dataset structure and identifies:
    - Column types
    - Identifier candidates
    - Primary key candidates
    - Numeric columns
    - Categorical columns
    - Date columns
    - High-cardinality columns
    - Missing values
    - Dataset metadata
    """

    def analyze(self, df: pd.DataFrame):

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        columns_metadata = {}

        numeric_columns = []
        categorical_columns = []
        datetime_columns = []
        identifier_candidates = []
        primary_key_candidates = []
        high_cardinality_columns = []

        # ==========================================
        # ANALYZE EVERY COLUMN
        # ==========================================

        for column in df.columns:

            series = df[column]

            dtype = str(series.dtype)

            missing_count = int(series.isna().sum())

            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            ) if total_rows > 0 else 0

            unique_count = int(series.nunique(dropna=True))

            unique_percentage = round(
                (unique_count / total_rows) * 100,
                2
            ) if total_rows > 0 else 0

            # --------------------------------------
            # COLUMN TYPE DETECTION
            # --------------------------------------

            detected_type = "Text"

            if pd.api.types.is_numeric_dtype(series):

                detected_type = "Numeric"
                numeric_columns.append(column)

            elif pd.api.types.is_datetime64_any_dtype(series):

                detected_type = "DateTime"
                datetime_columns.append(column)

            else:

                # Try detecting date-like object columns
                if self._is_date_column(series):

                    detected_type = "Date"
                    datetime_columns.append(column)

                elif unique_count <= max(20, total_rows * 0.05):

                    detected_type = "Categorical"
                    categorical_columns.append(column)

                else:

                    detected_type = "Text"

            # --------------------------------------
            # IDENTIFIER DETECTION
            # --------------------------------------

            is_identifier = False

            column_name_lower = str(column).lower()

            identifier_keywords = [
                "id",
                "code",
                "employee",
                "customer",
                "user",
                "account",
                "transaction",
                "invoice",
                "order"
            ]

            if (
                unique_count == total_rows
                and missing_count == 0
                and total_rows > 0
            ):

                is_identifier = True

            if any(
                keyword in column_name_lower
                for keyword in identifier_keywords
            ):

                if unique_percentage >= 90:

                    is_identifier = True

            if is_identifier:

                identifier_candidates.append(column)

            # --------------------------------------
            # PRIMARY KEY CANDIDATE
            # --------------------------------------

            is_primary_key_candidate = (
                unique_count == total_rows
                and missing_count == 0
                and total_rows > 0
            )

            if is_primary_key_candidate:

                primary_key_candidates.append(column)

            # --------------------------------------
            # HIGH CARDINALITY
            # --------------------------------------

            is_high_cardinality = False

            if total_rows > 0:

                if unique_percentage >= 50:

                    is_high_cardinality = True

                    high_cardinality_columns.append(column)

            # --------------------------------------
            # SAMPLE VALUES
            # --------------------------------------

            sample_values = []

            try:

                values = series.dropna().head(5).tolist()

                for value in values:

                    if isinstance(
                        value,
                        (np.integer, np.floating)
                    ):

                        value = value.item()

                    sample_values.append(str(value))

            except Exception:

                sample_values = []

            # --------------------------------------
            # COLUMN METADATA
            # --------------------------------------

            columns_metadata[column] = {

                "original_dtype":
                    dtype,

                "detected_type":
                    detected_type,

                "missing_count":
                    missing_count,

                "missing_percentage":
                    missing_percentage,

                "unique_values":
                    unique_count,

                "unique_percentage":
                    unique_percentage,

                "is_identifier":
                    is_identifier,

                "is_primary_key_candidate":
                    is_primary_key_candidate,

                "is_high_cardinality":
                    is_high_cardinality,

                "sample_values":
                    sample_values
            }

        # ==========================================
        # DATASET CLASSIFICATION
        # ==========================================

        dataset_type = self._detect_dataset_type(
            df,
            numeric_columns,
            categorical_columns,
            datetime_columns
        )

        # ==========================================
        # DATASET SUMMARY
        # ==========================================

        total_missing_values = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        # ==========================================
        # INTELLIGENCE INSIGHTS
        # ==========================================

        insights = []

        if primary_key_candidates:

            insights.append(
                f"Primary key candidate detected: "
                f"{primary_key_candidates[0]}"
            )

        if datetime_columns:

            insights.append(
                f"{len(datetime_columns)} date/time "
                f"column(s) detected."
            )

        if numeric_columns:

            insights.append(
                f"{len(numeric_columns)} numeric "
                f"column(s) available for analysis."
            )

        if categorical_columns:

            insights.append(
                f"{len(categorical_columns)} categorical "
                f"column(s) detected for grouping."
            )

        if high_cardinality_columns:

            insights.append(
                f"{len(high_cardinality_columns)} high-cardinality "
                f"column(s) detected."
            )

        if not insights:

            insights.append(
                "Dataset metadata analysis completed successfully."
            )

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Metadata Intelligence",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "dataset_overview": {

                "total_rows":
                    total_rows,

                "total_columns":
                    total_columns,

                "total_missing_values":
                    total_missing_values,

                "duplicate_rows":
                    duplicate_rows,

                "dataset_type":
                    dataset_type
            },

            "column_summary": {

                "numeric_columns":
                    numeric_columns,

                "categorical_columns":
                    categorical_columns,

                "datetime_columns":
                    datetime_columns,

                "identifier_candidates":
                    identifier_candidates,

                "primary_key_candidates":
                    primary_key_candidates,

                "high_cardinality_columns":
                    high_cardinality_columns
            },

            "columns_metadata":
                columns_metadata,

            "intelligence_insights":
                insights
        }

    # ==============================================
    # DATE DETECTION
    # ==============================================

    def _is_date_column(self, series):

        try:

            clean_series = series.dropna()

            if len(clean_series) == 0:

                return False

            sample = clean_series.head(50)

            converted = pd.to_datetime(
                sample,
                errors="coerce"
            )

            success_rate = converted.notna().mean()

            return bool(success_rate >= 0.8)

        except Exception:

            return False

    # ==============================================
    # DATASET TYPE DETECTION
    # ==============================================

    def _detect_dataset_type(
        self,
        df,
        numeric_columns,
        categorical_columns,
        datetime_columns
    ):

        column_names = " ".join(
            [str(column).lower() for column in df.columns]
        )

        # Business / Sales Dataset

        if any(
            keyword in column_names
            for keyword in [
                "sales",
                "revenue",
                "profit",
                "customer",
                "order"
            ]
        ):

            return "Business / Sales Dataset"

        # Employee / HR Dataset

        if any(
            keyword in column_names
            for keyword in [
                "employee",
                "salary",
                "department",
                "designation"
            ]
        ):

            return "Employee / HR Dataset"

        # Financial Dataset

        if any(
            keyword in column_names
            for keyword in [
                "balance",
                "expense",
                "income",
                "transaction",
                "amount"
            ]
        ):

            return "Financial Dataset"

        # Time Series Dataset

        if datetime_columns:

            return "Time Series Dataset"

        # General Dataset

        return "General Structured Dataset"


# ==================================================
# FUNCTION FOR MAIN.PY
# ==================================================

def run_metadata_analysis(df):

    engine = MetadataEngine()

    return engine.analyze(df)