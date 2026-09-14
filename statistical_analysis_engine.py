# ============================================================
# GENESIS AI - STATISTICAL ANALYSIS ENGINE
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# MAIN STATISTICAL ANALYSIS FUNCTION
# ============================================================

def run_statistical_analysis(df):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        return {

            "success": False,

            "message": "No dataset available for statistical analysis."

        }


    # --------------------------------------------------------
    # SELECT NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()


    if not numeric_columns:

        return {

            "success": False,

            "message": "No numeric columns available for statistical analysis."

        }


    # --------------------------------------------------------
    # ANALYSIS STORAGE
    # --------------------------------------------------------

    column_statistics = {}


    # ========================================================
    # ANALYZE EACH NUMERIC COLUMN
    # ========================================================

    for column in numeric_columns:

        series = pd.to_numeric(

            df[column],

            errors="coerce"

        ).dropna()


        if series.empty:

            continue


        # ----------------------------------------------------
        # BASIC STATISTICS
        # ----------------------------------------------------

        mean_value = float(
            series.mean()
        )

        median_value = float(
            series.median()
        )

        std_value = float(
            series.std()
        ) if len(series) > 1 else 0.0


        variance_value = float(
            series.var()
        ) if len(series) > 1 else 0.0


        min_value = float(
            series.min()
        )

        max_value = float(
            series.max()
        )


        # ----------------------------------------------------
        # QUARTILES
        # ----------------------------------------------------

        q1 = float(
            series.quantile(0.25)
        )

        q3 = float(
            series.quantile(0.75)
        )

        iqr = float(
            q3 - q1
        )


        # ----------------------------------------------------
        # SKEWNESS
        # ----------------------------------------------------

        skewness = float(
            series.skew()
        ) if len(series) > 2 else 0.0


        # ----------------------------------------------------
        # KURTOSIS
        # ----------------------------------------------------

        kurtosis = float(
            series.kurt()
        ) if len(series) > 3 else 0.0


        # ----------------------------------------------------
        # MODE
        # ----------------------------------------------------

        mode_values = series.mode()


        if not mode_values.empty:

            mode_value = float(
                mode_values.iloc[0]
            )

        else:

            mode_value = None


        # ----------------------------------------------------
        # COEFFICIENT OF VARIATION
        # ----------------------------------------------------

        if mean_value != 0:

            coefficient_variation = (

                std_value
                /
                abs(mean_value)

            ) * 100

        else:

            coefficient_variation = 0


        # ----------------------------------------------------
        # DISTRIBUTION INTERPRETATION
        # ----------------------------------------------------

        if abs(skewness) < 0.5:

            distribution_shape = (

                "Approximately Symmetric"

            )

        elif skewness >= 0.5:

            distribution_shape = (

                "Positively Skewed"

            )

        else:

            distribution_shape = (

                "Negatively Skewed"

            )


        # ----------------------------------------------------
        # VARIABILITY LEVEL
        # ----------------------------------------------------

        if coefficient_variation < 15:

            variability_level = "Low"

        elif coefficient_variation < 35:

            variability_level = "Moderate"

        else:

            variability_level = "High"


        # ====================================================
        # STORE COLUMN RESULTS
        # ====================================================

        column_statistics[column] = {

            "count": int(
                series.count()
            ),

            "mean": round(
                mean_value,
                4
            ),

            "median": round(
                median_value,
                4
            ),

            "mode": (
                round(mode_value, 4)
                if mode_value is not None
                else None
            ),

            "standard_deviation": round(
                std_value,
                4
            ),

            "variance": round(
                variance_value,
                4
            ),

            "minimum": round(
                min_value,
                4
            ),

            "maximum": round(
                max_value,
                4
            ),

            "range": round(
                max_value - min_value,
                4
            ),

            "q1": round(
                q1,
                4
            ),

            "q3": round(
                q3,
                4
            ),

            "interquartile_range": round(
                iqr,
                4
            ),

            "skewness": round(
                skewness,
                4
            ),

            "kurtosis": round(
                kurtosis,
                4
            ),

            "coefficient_of_variation_percent": round(
                coefficient_variation,
                4
            ),

            "distribution_shape": distribution_shape,

            "variability_level": variability_level

        }


    # ========================================================
    # DATASET SUMMARY
    # ========================================================

    total_numeric_columns = len(
        column_statistics
    )


    # --------------------------------------------------------
    # FIND HIGHEST VARIABILITY
    # --------------------------------------------------------

    highest_variability_column = None

    highest_variability = -1


    for column, stats in column_statistics.items():

        variability = stats.get(

            "coefficient_of_variation_percent",

            0

        )


        if variability > highest_variability:

            highest_variability = variability

            highest_variability_column = column


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "analysis_type": (

            "Advanced Statistical Analysis"

        ),

        "dataset_summary": {

            "total_rows": int(
                len(df)
            ),

            "total_columns": int(
                len(df.columns)
            ),

            "numeric_columns_analyzed": (

                total_numeric_columns

            )

        },

        "column_statistics": (

            column_statistics

        ),

        "key_insights": {

            "highest_variability_column": (

                highest_variability_column

            ),

            "highest_variability_percent": (

                round(
                    highest_variability,
                    4
                )

                if highest_variability >= 0

                else None

            )

        }

    }