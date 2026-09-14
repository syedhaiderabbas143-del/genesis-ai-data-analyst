# ============================================================
# GENESIS AI - ADVANCED STATISTICS ENGINE
# ============================================================

import pandas as pd
import numpy as np

from scipy import stats


# ============================================================
# SAFE NUMERIC COLUMNS
# ============================================================

def get_numeric_columns(df):

    numeric_columns = df.select_dtypes(
        include=[
            np.number
        ]
    ).columns.tolist()

    return numeric_columns


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

def calculate_descriptive_statistics(df):

    results = {}

    numeric_columns = get_numeric_columns(
        df
    )

    for column in numeric_columns:

        series = df[
            column
        ].dropna()

        if len(series) == 0:

            continue

        results[column] = {

            "count": int(
                series.count()
            ),

            "mean": round(
                float(series.mean()),
                4
            ),

            "median": round(
                float(series.median()),
                4
            ),

            "mode": (
                round(
                    float(series.mode().iloc[0]),
                    4
                )
                if not series.mode().empty
                else None
            ),

            "minimum": round(
                float(series.min()),
                4
            ),

            "maximum": round(
                float(series.max()),
                4
            ),

            "range": round(
                float(
                    series.max()
                    -
                    series.min()
                ),
                4
            ),

            "variance": round(
                float(series.var()),
                4
            ),

            "standard_deviation": round(
                float(series.std()),
                4
            )

        }

    return results


# ============================================================
# DISTRIBUTION ANALYSIS
# ============================================================

def analyze_distribution(df):

    results = {}

    numeric_columns = get_numeric_columns(
        df
    )

    for column in numeric_columns:

        series = df[
            column
        ].dropna()

        if len(series) < 3:

            continue

        skewness = float(
            stats.skew(
                series
            )
        )

        kurtosis = float(
            stats.kurtosis(
                series
            )
        )


        # ----------------------------------------
        # DISTRIBUTION TYPE
        # ----------------------------------------

        if abs(skewness) < 0.5:

            distribution_shape = "Approximately Symmetric"

        elif skewness >= 0.5:

            distribution_shape = "Right Skewed"

        else:

            distribution_shape = "Left Skewed"


        # ----------------------------------------
        # KURTOSIS INTERPRETATION
        # ----------------------------------------

        if kurtosis > 1:

            kurtosis_interpretation = "Heavy Tailed"

        elif kurtosis < -1:

            kurtosis_interpretation = "Light Tailed"

        else:

            kurtosis_interpretation = "Normal Tailed"


        results[column] = {

            "skewness": round(
                skewness,
                4
            ),

            "kurtosis": round(
                kurtosis,
                4
            ),

            "distribution_shape": distribution_shape,

            "kurtosis_interpretation": (
                kurtosis_interpretation
            )

        }

    return results


# ============================================================
# CONFIDENCE INTERVAL
# ============================================================

def calculate_confidence_intervals(

    df,

    confidence_level=0.95

):

    results = {}

    numeric_columns = get_numeric_columns(
        df
    )

    for column in numeric_columns:

        series = df[
            column
        ].dropna()

        n = len(
            series
        )

        if n < 2:

            continue


        mean = float(
            series.mean()
        )

        standard_error = stats.sem(
            series
        )


        interval = stats.t.interval(

            confidence_level,

            df=n - 1,

            loc=mean,

            scale=standard_error

        )


        results[column] = {

            "confidence_level": (
                confidence_level * 100
            ),

            "mean": round(
                mean,
                4
            ),

            "lower_bound": round(
                float(interval[0]),
                4
            ),

            "upper_bound": round(
                float(interval[1]),
                4
            )

        }

    return results


# ============================================================
# STATISTICAL OUTLIER ANALYSIS
# ============================================================

def analyze_statistical_outliers(df):

    results = {}

    numeric_columns = get_numeric_columns(
        df
    )

    for column in numeric_columns:

        series = df[
            column
        ].dropna()

        if len(series) < 4:

            continue


        q1 = series.quantile(
            0.25
        )

        q3 = series.quantile(
            0.75
        )

        iqr = q3 - q1


        lower_bound = q1 - (
            1.5 * iqr
        )

        upper_bound = q3 + (
            1.5 * iqr
        )


        outliers = series[

            (

                series < lower_bound

            )

            |

            (

                series > upper_bound

            )

        ]


        outlier_count = len(
            outliers
        )


        outlier_percentage = (

            outlier_count

            /

            len(series)

        ) * 100


        results[column] = {

            "outlier_count": int(
                outlier_count
            ),

            "outlier_percentage": round(
                float(outlier_percentage),
                2
            ),

            "lower_bound": round(
                float(lower_bound),
                4
            ),

            "upper_bound": round(
                float(upper_bound),
                4
            )

        }

    return results


# ============================================================
# ADVANCED STATISTICS MASTER ENGINE
# ============================================================

def run_advanced_statistics(

    df,

    confidence_level=0.95

):

    descriptive_statistics = (

        calculate_descriptive_statistics(

            df

        )

    )


    distribution_analysis = (

        analyze_distribution(

            df

        )

    )


    confidence_intervals = (

        calculate_confidence_intervals(

            df,

            confidence_level

        )

    )


    outlier_analysis = (

        analyze_statistical_outliers(

            df

        )

    )


    return {

        "success": True,

        "confidence_level": (

            confidence_level * 100
        ),

        "descriptive_statistics": (

            descriptive_statistics
        ),

        "distribution_analysis": (

            distribution_analysis
        ),

        "confidence_intervals": (

            confidence_intervals
        ),

        "statistical_outliers": (

            outlier_analysis
        )

    }