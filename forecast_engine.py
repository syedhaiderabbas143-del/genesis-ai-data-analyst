# ============================================================
# GENESIS AI - FORECAST ENGINE
# ============================================================

import numpy as np
import pandas as pd


# ============================================================
# RUN FORECAST ANALYSIS
# ============================================================

def run_forecast_analysis(
    df,
    target_column,
    periods=12
):

    # ========================================================
    # VALIDATE DATASET
    # ========================================================

    if df is None or df.empty:

        raise ValueError(
            "No dataset available for forecasting."
        )


    # ========================================================
    # VALIDATE TARGET COLUMN
    # ========================================================

    if target_column not in df.columns:

        raise ValueError(
            f"Column not found: {target_column}"
        )


    # ========================================================
    # VALIDATE FORECAST PERIODS
    # ========================================================

    try:

        periods = int(periods)

    except Exception:

        periods = 12


    if periods < 1:

        periods = 1


    if periods > 100:

        periods = 100


    # ========================================================
    # CONVERT TARGET COLUMN TO NUMERIC
    # ========================================================

    values = pd.to_numeric(

        df[target_column],

        errors="coerce"

    )


    # Remove missing values

    values = values.dropna()


    # ========================================================
    # VALIDATE DATA
    # ========================================================

    if len(values) < 3:

        raise ValueError(

            "At least 3 valid numeric values are required "
            "for forecasting."

        )


    # ========================================================
    # CREATE TIME INDEX
    # ========================================================

    x = np.arange(

        len(values)

    )


    y = values.to_numpy()


    # ========================================================
    # LINEAR TREND CALCULATION
    # ========================================================

    slope, intercept = np.polyfit(

        x,

        y,

        1

    )


    # ========================================================
    # GENERATE FUTURE INDEX
    # ========================================================

    future_x = np.arange(

        len(values),

        len(values) + periods

    )


    # ========================================================
    # GENERATE FORECAST
    # ========================================================

    forecast_values = (

        slope * future_x

        + intercept

    )


    # ========================================================
    # CALCULATE HISTORICAL TREND
    # ========================================================

    trend_values = (

        slope * x

        + intercept

    )


    # ========================================================
    # FORECAST DIRECTION
    # ========================================================

    if slope > 0:

        trend_direction = "Increasing"

    elif slope < 0:

        trend_direction = "Decreasing"

    else:

        trend_direction = "Stable"


    # ========================================================
    # TREND STRENGTH
    # ========================================================

    correlation = np.corrcoef(

        x,

        y

    )[0, 1]


    if np.isnan(correlation):

        correlation = 0


    trend_strength_value = abs(

        correlation

    )


    if trend_strength_value >= 0.80:

        trend_strength = "Strong"

    elif trend_strength_value >= 0.50:

        trend_strength = "Moderate"

    else:

        trend_strength = "Weak"


    # ========================================================
    # FORECAST CONFIDENCE
    # ========================================================

    if trend_strength_value >= 0.80:

        confidence = "High"

    elif trend_strength_value >= 0.50:

        confidence = "Medium"

    else:

        confidence = "Low"


    # ========================================================
    # CALCULATE RESIDUAL ERROR
    # ========================================================

    residuals = (

        y - trend_values

    )


    mae = float(

        np.mean(

            np.abs(residuals)

        )

    )


    rmse = float(

        np.sqrt(

            np.mean(

                residuals ** 2

            )

        )

    )


    # ========================================================
    # FORECAST RANGE
    # ========================================================

    forecast_lower = (

        forecast_values - rmse

    )


    forecast_upper = (

        forecast_values + rmse

    )


    # ========================================================
    # CREATE FORECAST RESULTS
    # ========================================================

    forecast_results = []


    for index, value in enumerate(

        forecast_values

    ):

        forecast_results.append({

            "period": int(

                index + 1

            ),

            "forecast": round(

                float(value),

                4

            ),

            "lower_estimate": round(

                float(

                    forecast_lower[index]

                ),

                4

            ),

            "upper_estimate": round(

                float(

                    forecast_upper[index]

                ),

                4

            )

        })


    # ========================================================
    # HISTORICAL SUMMARY
    # ========================================================

    historical_mean = float(

        values.mean()

    )


    historical_min = float(

        values.min()

    )


    historical_max = float(

        values.max()

    )


    latest_value = float(

        values.iloc[-1]

    )


    # ========================================================
    # FORECAST SUMMARY
    # ========================================================

    first_forecast = float(

        forecast_values[0]

    )


    last_forecast = float(

        forecast_values[-1]

    )


    forecast_change = (

        last_forecast

        - first_forecast

    )


    # ========================================================
    # BUSINESS INTERPRETATION
    # ========================================================

    if trend_direction == "Increasing":

        interpretation = (

            f"The {target_column} trend is increasing. "

            f"The forecast suggests continued growth "
            f"over the next {periods} periods."

        )

    elif trend_direction == "Decreasing":

        interpretation = (

            f"The {target_column} trend is decreasing. "

            f"The forecast suggests a continued decline "
            f"over the next {periods} periods."

        )

    else:

        interpretation = (

            f"The {target_column} values appear relatively stable. "

            f"The forecast does not indicate a strong "
            f"upward or downward trend."

        )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if trend_direction == "Increasing":

        recommendation = (

            "Prepare for increased future demand and "
            "monitor whether the growth trend continues."

        )

    elif trend_direction == "Decreasing":

        recommendation = (

            "Investigate the factors contributing to the "
            "declining trend and consider corrective action."

        )

    else:

        recommendation = (

            "Continue monitoring the metric for significant "
            "changes or emerging trends."

        )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "forecast_engine": "Linear Trend Forecast",

        "target_column": target_column,

        "forecast_periods": periods,


        # ----------------------------------------------------
        # HISTORICAL DATA
        # ----------------------------------------------------

        "historical_summary": {

            "total_observations": int(

                len(values)

            ),

            "latest_value": round(

                latest_value,

                4

            ),

            "average": round(

                historical_mean,

                4

            ),

            "minimum": round(

                historical_min,

                4

            ),

            "maximum": round(

                historical_max,

                4

            )

        },


        # ----------------------------------------------------
        # TREND ANALYSIS
        # ----------------------------------------------------

        "trend_analysis": {

            "direction": trend_direction,

            "strength": trend_strength,

            "correlation": round(

                float(correlation),

                4

            ),

            "slope": round(

                float(slope),

                6

            )

        },


        # ----------------------------------------------------
        # FORECAST QUALITY
        # ----------------------------------------------------

        "forecast_quality": {

            "confidence": confidence,

            "mae": round(

                mae,

                4

            ),

            "rmse": round(

                rmse,

                4

            )

        },


        # ----------------------------------------------------
        # FORECAST SUMMARY
        # ----------------------------------------------------

        "forecast_summary": {

            "first_forecast": round(

                first_forecast,

                4

            ),

            "last_forecast": round(

                last_forecast,

                4

            ),

            "forecast_change": round(

                forecast_change,

                4

            )

        },


        # ----------------------------------------------------
        # FORECAST RESULTS
        # ----------------------------------------------------

        "forecast": forecast_results,


        # ----------------------------------------------------
        # AI INSIGHTS
        # ----------------------------------------------------

        "interpretation": interpretation,

        "recommendation": recommendation

    }