import pandas as pd
import numpy as np
from datetime import datetime


class EngineerAgent:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Engineer Agent

        Performs engineering-focused dataset analysis:
        - Dataset structure analysis
        - Data type inspection
        - Missing value detection
        - Duplicate detection
        - Numeric column analysis
        - Engineering recommendations
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        # -----------------------------------
        # Dataset Overview
        # -----------------------------------

        numeric_columns = list(
            df.select_dtypes(include=np.number).columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns
        )

        datetime_columns = list(
            df.select_dtypes(
                include=["datetime64", "datetimetz"]
            ).columns
        )

        total_missing = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        # -----------------------------------
        # Column Engineering Profile
        # -----------------------------------

        column_profiles = {}

        for column in df.columns:

            series = df[column]

            missing_count = int(
                series.isna().sum()
            )

            non_null_count = int(
                series.notna().sum()
            )

            unique_values = int(
                series.nunique()
            )

            missing_percentage = 0

            if total_rows > 0:

                missing_percentage = round(
                    (missing_count / total_rows) * 100,
                    2
                )

            column_profiles[column] = {

                "data_type":
                    str(series.dtype),

                "missing_values":
                    missing_count,

                "missing_percentage":
                    missing_percentage,

                "non_null_values":
                    non_null_count,

                "unique_values":
                    unique_values

            }

        # -----------------------------------
        # Numeric Engineering Analysis
        # -----------------------------------

        numeric_analysis = {}

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) > 0:

                numeric_analysis[column] = {

                    "minimum":
                        round(
                            float(series.min()),
                            2
                        ),

                    "maximum":
                        round(
                            float(series.max()),
                            2
                        ),

                    "average":
                        round(
                            float(series.mean()),
                            2
                        ),

                    "median":
                        round(
                            float(series.median()),
                            2
                        ),

                    "standard_deviation":
                        round(
                            float(series.std()),
                            2
                        )
                        if len(series) > 1
                        else 0

                }

        # -----------------------------------
        # Dataset Complexity Score
        # -----------------------------------

        complexity_score = 0

        if total_columns >= 30:
            complexity_score += 40

        elif total_columns >= 15:
            complexity_score += 25

        else:
            complexity_score += 10

        if len(numeric_columns) >= 10:
            complexity_score += 30

        elif len(numeric_columns) >= 5:
            complexity_score += 20

        else:
            complexity_score += 10

        if total_rows >= 10000:
            complexity_score += 30

        elif total_rows >= 1000:
            complexity_score += 20

        else:
            complexity_score += 10

        complexity_score = min(
            complexity_score,
            100
        )

        # -----------------------------------
        # Complexity Status
        # -----------------------------------

        if complexity_score >= 80:

            complexity_status = "Advanced"

        elif complexity_score >= 50:

            complexity_status = "Moderate"

        else:

            complexity_status = "Simple"

        # -----------------------------------
        # Engineering Recommendations
        # -----------------------------------

        recommendations = []

        if total_missing > 0:

            recommendations.append({

                "priority": "High",

                "recommendation":
                    "Run Data Cleaning Engine to handle missing values."

            })

        else:

            recommendations.append({

                "priority": "Low",

                "recommendation":
                    "Dataset has no missing values. Continue with advanced analytics."

            })

        if duplicate_rows > 0:

            recommendations.append({

                "priority": "High",

                "recommendation":
                    "Remove duplicate rows before advanced modeling."

            })

        else:

            recommendations.append({

                "priority": "Low",

                "recommendation":
                    "No duplicate records detected."

            })

        if len(numeric_columns) > 0:

            recommendations.append({

                "priority": "Medium",

                "recommendation":
                    "Numeric columns are suitable for correlation, forecasting and statistical analysis."

            })

        if len(categorical_columns) > 0:

            recommendations.append({

                "priority": "Medium",

                "recommendation":
                    "Categorical columns are suitable for segmentation and group analysis."

            })

        if total_rows >= 1000:

            recommendations.append({

                "priority": "Medium",

                "recommendation":
                    "Dataset size is sufficient for advanced analytics and AI workflows."

            })

        # -----------------------------------
        # Engineering Status
        # -----------------------------------

        if total_missing == 0 and duplicate_rows == 0:

            engineering_status = (
                "Dataset is ready for advanced engineering workflows."
            )

        else:

            engineering_status = (
                "Dataset requires preprocessing before advanced workflows."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Engineer Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "engineering_status":
                engineering_status,

            "dataset_overview": {

                "total_rows":
                    total_rows,

                "total_columns":
                    total_columns,

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

            "dataset_complexity": {

                "complexity_score":
                    complexity_score,

                "status":
                    complexity_status

            },

            "column_profiles":
                column_profiles,

            "numeric_analysis":
                numeric_analysis,

            "recommendations":
                recommendations

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_engineer_agent(df):

    engine = EngineerAgent()

    return engine.analyze(df)