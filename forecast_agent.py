import pandas as pd
import numpy as np
from datetime import datetime


class ForecastAgent:

    def analyze(self, df: pd.DataFrame):
        """
        Genesis AI Forecast Agent

        Automatically identifies forecasting readiness and
        analyzes numeric + datetime columns.
        """

        total_rows = int(len(df))
        total_columns = int(len(df.columns))

        # -----------------------------------
        # Identify Datetime Columns
        # -----------------------------------

        datetime_columns = list(
            df.select_dtypes(
                include=["datetime64[ns]", "datetimetz"]
            ).columns
        )

        # -----------------------------------
        # Identify Numeric Columns
        # -----------------------------------

        numeric_columns = list(
            df.select_dtypes(
                include=np.number
            ).columns
        )

        # -----------------------------------
        # Dataset Readiness
        # -----------------------------------

        forecast_ready = False
        readiness_status = "Not Ready"

        if len(datetime_columns) >= 1 and len(numeric_columns) >= 1:

            forecast_ready = True
            readiness_status = "Ready for Forecasting"

        elif len(numeric_columns) >= 1:

            readiness_status = (
                "Partially Ready - Datetime column required "
                "for time-series forecasting."
            )

        # -----------------------------------
        # Datetime Analysis
        # -----------------------------------

        datetime_analysis = {}

        for column in datetime_columns:

            series = df[column].dropna()

            if len(series) > 0:

                datetime_analysis[column] = {

                    "total_dates":
                        int(len(series)),

                    "minimum_date":
                        str(series.min()),

                    "maximum_date":
                        str(series.max()),

                    "unique_dates":
                        int(series.nunique())

                }

        # -----------------------------------
        # Numeric Forecast Candidates
        # -----------------------------------

        forecast_candidates = []

        for column in numeric_columns:

            series = df[column].dropna()

            if len(series) < 2:
                continue

            forecast_candidates.append({

                "column":
                    column,

                "available_records":
                    int(len(series)),

                "minimum":
                    round(float(series.min()), 2),

                "maximum":
                    round(float(series.max()), 2),

                "average":
                    round(float(series.mean()), 2),

                "trend_direction":
                    self.detect_trend(series)

            })

        # -----------------------------------
        # Forecast Recommendations
        # -----------------------------------

        recommendations = []

        if not datetime_columns:

            recommendations.append({

                "priority": "High",

                "recommendation":
                    "Select or create a valid datetime column "
                    "for reliable time-series forecasting."

            })

        if len(numeric_columns) == 0:

            recommendations.append({

                "priority": "High",

                "recommendation":
                    "No numeric target column found for forecasting."

            })

        if forecast_ready:

            recommendations.append({

                "priority": "High",

                "recommendation":
                    "Dataset is ready for time-series forecasting."

            })

        if total_rows < 30:

            recommendations.append({

                "priority": "Warning",

                "recommendation":
                    "Dataset has limited records. Forecast accuracy "
                    "may be reduced."

            })

        elif total_rows >= 1000:

            recommendations.append({

                "priority": "Low",

                "recommendation":
                    "Dataset size is sufficient for advanced "
                    "forecasting workflows."

            })

        # -----------------------------------
        # Recommended Forecasting Methods
        # -----------------------------------

        recommended_models = []

        if forecast_ready:

            recommended_models.extend([
                "Linear Trend Forecasting",
                "Moving Average",
                "Exponential Smoothing"
            ])

            if total_rows >= 100:

                recommended_models.append(
                    "Advanced Time-Series Forecasting"
                )

        # -----------------------------------
        # Agent Summary
        # -----------------------------------

        if forecast_ready:

            agent_summary = (
                "Forecast Agent completed dataset analysis. "
                "The dataset is ready for forecasting workflows."
            )

        else:

            agent_summary = (
                "Forecast Agent completed analysis, but additional "
                "dataset preparation is required before reliable "
                "time-series forecasting."
            )

        # -----------------------------------
        # Final Response
        # -----------------------------------

        return {

            "success": True,

            "analysis_type":
                "Genesis AI Forecast Agent",

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "agent_summary":
                agent_summary,

            "forecast_readiness": {

                "ready":
                    forecast_ready,

                "status":
                    readiness_status

            },

            "dataset_overview": {

                "total_rows":
                    total_rows,

                "total_columns":
                    total_columns,

                "datetime_columns":
                    len(datetime_columns),

                "numeric_columns":
                    len(numeric_columns)

            },

            "datetime_analysis":
                datetime_analysis,

            "forecast_candidates":
                forecast_candidates,

            "recommended_models":
                recommended_models,

            "recommendations":
                recommendations

        }


    # -----------------------------------
    # Trend Detection
    # -----------------------------------

    def detect_trend(self, series):

        if len(series) < 2:
            return "Insufficient Data"

        first_value = float(series.iloc[0])
        last_value = float(series.iloc[-1])

        if last_value > first_value:
            return "Increasing"

        elif last_value < first_value:
            return "Decreasing"

        return "Stable"


# -----------------------------------
# Function for main.py
# -----------------------------------

def run_forecast_agent(df):

    agent = ForecastAgent()

    return agent.analyze(df)