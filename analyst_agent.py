import pandas as pd
import numpy as np
from datetime import datetime


class AnalystAgent:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Analyst Agent

        Automatically analyzes the uploaded dataset and generates:
        - Dataset overview
        - Key metrics
        - Numeric insights
        - Categorical insights
        - Important findings
        - Recommended next analysis
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

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
                include=["datetime64[ns]", "datetimetz"]
            ).columns
        )

        # -----------------------------------
        # Dataset Overview
        # -----------------------------------

        total_missing = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        dataset_overview = {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "numeric_columns": len(numeric_columns),
            "categorical_columns": len(categorical_columns),
            "datetime_columns": len(datetime_columns),
            "missing_values": total_missing,
            "duplicate_rows": duplicate_rows
        }

        # -----------------------------------
        # Numeric Analysis
        # -----------------------------------

        numeric_insights = {}

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            numeric_insights[column] = {

                "minimum": round(
                    float(series.min()), 2
                ),

                "maximum": round(
                    float(series.max()), 2
                ),

                "average": round(
                    float(series.mean()), 2
                ),

                "median": round(
                    float(series.median()), 2
                ),

                "standard_deviation": round(
                    float(series.std()), 2
                ) if len(series) > 1 else 0

            }

        # -----------------------------------
        # Categorical Analysis
        # -----------------------------------

        categorical_insights = {}

        for column in categorical_columns:

            series = df[column].dropna()

            if len(series) == 0:
                continue

            value_counts = series.value_counts()

            top_category = value_counts.index[0]
            top_category_count = int(
                value_counts.iloc[0]
            )

            categorical_insights[column] = {

                "unique_categories": int(
                    series.nunique()
                ),

                "top_category": str(
                    top_category
                ),

                "top_category_count":
                    top_category_count

            }

        # -----------------------------------
        # Important Findings
        # -----------------------------------

        important_findings = []

        if total_missing == 0:

            important_findings.append(
                "Dataset contains no missing values."
            )

        else:

            important_findings.append(
                f"Dataset contains {total_missing} missing values."
            )

        if duplicate_rows == 0:

            important_findings.append(
                "No duplicate records detected."
            )

        else:

            important_findings.append(
                f"{duplicate_rows} duplicate records detected."
            )

        if len(numeric_columns) > 0:

            important_findings.append(
                f"{len(numeric_columns)} numeric columns "
                "are available for statistical analysis."
            )

        if len(categorical_columns) > 0:

            important_findings.append(
                f"{len(categorical_columns)} categorical columns "
                "are available for group analysis."
            )

        # -----------------------------------
        # Analysis Priorities
        # -----------------------------------

        recommended_analysis = []

        if len(numeric_columns) >= 2:

            recommended_analysis.append({

                "priority": "High",

                "analysis":
                    "Correlation Analysis",

                "reason":
                    "Multiple numeric columns are available "
                    "for relationship analysis."

            })

        if len(categorical_columns) > 0:

            recommended_analysis.append({

                "priority": "High",

                "analysis":
                    "Group Comparison",

                "reason":
                    "Categorical columns can be used to "
                    "compare business metrics."

            })

        if len(numeric_columns) > 0:

            recommended_analysis.append({

                "priority": "Medium",

                "analysis":
                    "Outlier Detection",

                "reason":
                    "Numeric columns can be checked for "
                    "unusual values."

            })

        if len(datetime_columns) > 0:

            recommended_analysis.append({

                "priority": "High",

                "analysis":
                    "Trend Analysis",

                "reason":
                    "Datetime columns are available for "
                    "time-series analysis."

            })

        # -----------------------------------
        # Agent Summary
        # -----------------------------------

        if total_rows == 0:

            agent_summary = (
                "Dataset is empty. Please upload "
                "a valid dataset."
            )

        elif total_missing == 0 and duplicate_rows == 0:

            agent_summary = (
                "Dataset appears clean and ready "
                "for advanced analysis."
            )

        else:

            agent_summary = (
                "Dataset analysis completed. "
                "Data quality improvements may be "
                "required before advanced analysis."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Analyst Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "agent_summary":
                agent_summary,

            "dataset_overview":
                dataset_overview,

            "numeric_insights":
                numeric_insights,

            "categorical_insights":
                categorical_insights,

            "important_findings":
                important_findings,

            "recommended_analysis":
                recommended_analysis

        }


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_analyst_agent(df):

    agent = AnalystAgent()

    return agent.analyze(df)