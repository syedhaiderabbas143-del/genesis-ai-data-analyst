import pandas as pd
import numpy as np
from datetime import datetime


class QualityAgent:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Quality Agent

        Performs automatic dataset quality analysis:
        - Missing values
        - Duplicate records
        - Data type checks
        - Unique value analysis
        - Quality score
        - Quality issues
        - Recommendations
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))
        total_cells = total_rows * total_columns

        # -----------------------------------
        # Missing Value Analysis
        # -----------------------------------

        missing_by_column = {}
        total_missing = int(df.isna().sum().sum())

        for column in df.columns:

            missing_count = int(df[column].isna().sum())

            if missing_count > 0:

                missing_percentage = round(
                    (missing_count / total_rows) * 100,
                    2
                ) if total_rows > 0 else 0

                missing_by_column[column] = {
                    "missing_count": missing_count,
                    "missing_percentage": missing_percentage
                }

        # -----------------------------------
        # Duplicate Analysis
        # -----------------------------------

        duplicate_rows = int(df.duplicated().sum())

        duplicate_percentage = round(
            (duplicate_rows / total_rows) * 100,
            2
        ) if total_rows > 0 else 0

        # -----------------------------------
        # Column Quality Analysis
        # -----------------------------------

        column_quality = {}

        for column in df.columns:

            total_values = int(df[column].notna().sum())
            unique_values = int(df[column].nunique())

            column_quality[column] = {

                "data_type":
                    str(df[column].dtype),

                "non_null_values":
                    total_values,

                "unique_values":
                    unique_values

            }

        # -----------------------------------
        # Quality Score Calculation
        # -----------------------------------

        missing_penalty = 0
        duplicate_penalty = 0

        if total_cells > 0:

            missing_percentage_total = (
                total_missing / total_cells
            ) * 100

            missing_penalty = min(
                missing_percentage_total,
                50
            )

        if total_rows > 0:

            duplicate_penalty = min(
                duplicate_percentage,
                30
            )

        quality_score = round(

            max(
                0,
                100
                - missing_penalty
                - duplicate_penalty
            ),

            2
        )

        # -----------------------------------
        # Quality Status
        # -----------------------------------

        if quality_score >= 90:

            quality_status = "Excellent"

        elif quality_score >= 75:

            quality_status = "Good"

        elif quality_score >= 50:

            quality_status = "Warning"

        else:

            quality_status = "Critical"

        # -----------------------------------
        # Quality Issues
        # -----------------------------------

        quality_issues = []

        if total_missing > 0:

            quality_issues.append({

                "issue":
                    "Missing Values",

                "severity":
                    "Warning",

                "details":
                    f"{total_missing} missing values detected."

            })

        if duplicate_rows > 0:

            quality_issues.append({

                "issue":
                    "Duplicate Records",

                "severity":
                    "Warning",

                "details":
                    f"{duplicate_rows} duplicate rows detected."

            })

        if total_rows == 0:

            quality_issues.append({

                "issue":
                    "Empty Dataset",

                "severity":
                    "Critical",

                "details":
                    "The uploaded dataset contains no records."

            })

        if not quality_issues:

            quality_issues.append({

                "issue":
                    "No Critical Issues",

                "severity":
                    "Success",

                "details":
                    "Dataset passed all primary quality checks."

            })

        # -----------------------------------
        # Recommendations
        # -----------------------------------

        recommendations = []

        if total_missing > 0:

            recommendations.append(
                "Review missing values and apply "
                "imputation or remove incomplete records."
            )

        if duplicate_rows > 0:

            recommendations.append(
                "Remove duplicate records before "
                "performing advanced analysis."
            )

        if quality_score >= 90:

            recommendations.append(
                "Dataset quality is excellent and "
                "ready for advanced analytics."
            )

        elif quality_score >= 75:

            recommendations.append(
                "Dataset quality is good. Minor "
                "improvements are recommended."
            )

        else:

            recommendations.append(
                "Improve dataset quality before "
                "performing critical business analysis."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Quality Agent",

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
                    total_missing,

                "duplicate_rows":
                    duplicate_rows

            },

            "quality_assessment": {

                "quality_score":
                    quality_score,

                "quality_status":
                    quality_status

            },

            "missing_value_analysis":
                missing_by_column,

            "duplicate_analysis": {

                "duplicate_rows":
                    duplicate_rows,

                "duplicate_percentage":
                    duplicate_percentage

            },

            "column_quality":
                column_quality,

            "quality_issues":
                quality_issues,

            "recommendations":
                recommendations

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_quality_agent(df):

    agent = QualityAgent()

    return agent.analyze(df)