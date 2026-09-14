# ============================================================
# GENESIS AI - ADVANCED ANOMALY DETECTION ENGINE
# ============================================================

import pandas as pd
import numpy as np

from scipy import stats


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_IQR_MULTIPLIER = 1.5
DEFAULT_ZSCORE_THRESHOLD = 3.0
DEFAULT_MODIFIED_ZSCORE_THRESHOLD = 3.5


# ============================================================
# GET NUMERIC COLUMNS
# ============================================================

def get_numeric_columns(df):

    if df is None or df.empty:
        return []

    return df.select_dtypes(
        include=[np.number]
    ).columns.tolist()


# ============================================================
# IQR OUTLIER DETECTION
# ============================================================

def detect_iqr_outliers(
    series,
    multiplier=DEFAULT_IQR_MULTIPLIER
):

    clean_series = series.dropna()

    if len(clean_series) < 4:

        return {
            "indices": [],
            "count": 0,
            "lower_bound": None,
            "upper_bound": None
        }

    q1 = clean_series.quantile(0.25)
    q3 = clean_series.quantile(0.75)

    iqr = q3 - q1

    # No variation
    if iqr == 0:

        return {
            "indices": [],
            "count": 0,
            "lower_bound": float(q1),
            "upper_bound": float(q3)
        }

    lower_bound = q1 - (
        multiplier * iqr
    )

    upper_bound = q3 + (
        multiplier * iqr
    )

    outlier_mask = (

        (clean_series < lower_bound)

        |

        (clean_series > upper_bound)

    )

    indices = clean_series[
        outlier_mask
    ].index.tolist()

    return {

        "indices": indices,

        "count": len(indices),

        "lower_bound": round(
            float(lower_bound),
            4
        ),

        "upper_bound": round(
            float(upper_bound),
            4
        )

    }


# ============================================================
# Z-SCORE OUTLIER DETECTION
# ============================================================

def detect_zscore_outliers(
    series,
    threshold=DEFAULT_ZSCORE_THRESHOLD
):

    clean_series = series.dropna()

    if len(clean_series) < 3:

        return {
            "indices": [],
            "count": 0,
            "threshold": threshold
        }

    # Standard deviation
    std_value = clean_series.std()

    if std_value == 0 or pd.isna(std_value):

        return {
            "indices": [],
            "count": 0,
            "threshold": threshold
        }

    z_scores = np.abs(

        stats.zscore(
            clean_series
        )

    )

    mask = (

        z_scores > threshold

    )

    indices = clean_series.index[
        mask
    ].tolist()

    return {

        "indices": indices,

        "count": len(indices),

        "threshold": threshold

    }


# ============================================================
# MODIFIED Z-SCORE (MAD) DETECTION
# ============================================================

def detect_modified_zscore_outliers(
    series,
    threshold=DEFAULT_MODIFIED_ZSCORE_THRESHOLD
):

    clean_series = series.dropna()

    if len(clean_series) < 3:

        return {
            "indices": [],
            "count": 0,
            "threshold": threshold
        }

    median = clean_series.median()

    mad = np.median(

        np.abs(

            clean_series - median

        )

    )

    # No variation
    if mad == 0 or pd.isna(mad):

        return {
            "indices": [],
            "count": 0,
            "threshold": threshold
        }

    modified_z_scores = (

        0.6745

        *

        (

            clean_series - median

        )

        /

        mad

    )

    mask = (

        np.abs(
            modified_z_scores
        )

        >

        threshold

    )

    indices = clean_series.index[
        mask
    ].tolist()

    return {

        "indices": indices,

        "count": len(indices),

        "threshold": threshold

    }


# ============================================================
# DETERMINE OUTLIER SEVERITY
# ============================================================

def determine_severity(
    methods_detected
):

    method_count = len(
        methods_detected
    )

    if method_count >= 3:

        return "Critical"

    elif method_count == 2:

        return "High"

    elif method_count == 1:

        return "Medium"

    return "Low"


# ============================================================
# COLUMN ANOMALY ANALYSIS
# ============================================================

def analyze_column_anomalies(
    df,
    column
):

    series = df[column]

    # --------------------------------------------------------
    # RUN METHODS
    # --------------------------------------------------------

    iqr_result = detect_iqr_outliers(
        series
    )

    zscore_result = detect_zscore_outliers(
        series
    )

    modified_result = (
        detect_modified_zscore_outliers(
            series
        )
    )

    # --------------------------------------------------------
    # COMBINE ALL INDICES
    # --------------------------------------------------------

    all_indices = set(

        iqr_result["indices"]

        +

        zscore_result["indices"]

        +

        modified_result["indices"]

    )

    anomaly_details = []

    for index in all_indices:

        methods_detected = []

        if index in iqr_result["indices"]:

            methods_detected.append(
                "IQR"
            )

        if index in zscore_result["indices"]:

            methods_detected.append(
                "Z-Score"
            )

        if index in modified_result["indices"]:

            methods_detected.append(
                "Modified Z-Score"
            )

        anomaly_details.append({

            "row_index": int(index)
            if isinstance(
                index,
                (int, np.integer)
            )
            else str(index),

            "value": round(
                float(df.loc[index, column]),
                4
            ),

            "methods_detected": (
                methods_detected
            ),

            "method_count": len(
                methods_detected
            ),

            "severity": (
                determine_severity(
                    methods_detected
                )
            )

        })

    # --------------------------------------------------------
    # SORT BY SEVERITY
    # --------------------------------------------------------

    severity_order = {

        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3

    }

    anomaly_details.sort(

        key=lambda item: (

            severity_order.get(
                item["severity"],
                4
            ),

            -item["method_count"]

        )

    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_rows = len(
        series.dropna()
    )

    anomaly_count = len(
        anomaly_details
    )

    anomaly_percentage = (

        anomaly_count
        /
        total_rows
        *
        100

        if total_rows > 0

        else 0

    )

    return {

        "column": column,

        "total_valid_values": total_rows,

        "anomaly_count": anomaly_count,

        "anomaly_percentage": round(
            float(anomaly_percentage),
            2
        ),

        "methods": {

            "iqr": {

                "count":
                    iqr_result["count"],

                "lower_bound":
                    iqr_result["lower_bound"],

                "upper_bound":
                    iqr_result["upper_bound"]

            },

            "z_score": {

                "count":
                    zscore_result["count"],

                "threshold":
                    zscore_result["threshold"]

            },

            "modified_z_score": {

                "count":
                    modified_result["count"],

                "threshold":
                    modified_result["threshold"]

            }

        },

        "anomalies": anomaly_details

    }


# ============================================================
# DATASET ANOMALY RISK
# ============================================================

def calculate_dataset_risk(
    total_anomalies,
    total_values
):

    if total_values == 0:

        return {

            "risk_score": 0,

            "risk_level": "Low"

        }

    anomaly_rate = (

        total_anomalies
        /
        total_values
        *
        100

    )

    risk_score = min(

        round(
            anomaly_rate * 10,
            2
        ),

        100

    )

    if risk_score >= 70:

        risk_level = "Critical"

    elif risk_score >= 40:

        risk_level = "High"

    elif risk_score >= 15:

        risk_level = "Medium"

    else:

        risk_level = "Low"

    return {

        "risk_score": risk_score,

        "risk_level": risk_level

    }


# ============================================================
# GENERATE BUSINESS INSIGHTS
# ============================================================

def generate_anomaly_insights(
    column_results
):

    insights = []

    sorted_columns = sorted(

        column_results,

        key=lambda item:

            item["anomaly_percentage"],

        reverse=True

    )

    for result in sorted_columns[:5]:

        if result[
            "anomaly_count"
        ] == 0:

            continue

        percentage = result[
            "anomaly_percentage"
        ]

        column = result[
            "column"
        ]

        if percentage >= 10:

            insight = (

                f"{column} contains a high anomaly rate "
                f"of {percentage}% and should be investigated."

            )

        elif percentage >= 5:

            insight = (

                f"{column} contains a moderate number of "
                f"unusual values ({percentage}%)."

            )

        else:

            insight = (

                f"{column} contains a small number of "
                f"potential anomalies ({percentage}%)."

            )

        insights.append({

            "column": column,

            "anomaly_percentage":
                percentage,

            "insight": insight

        })

    return insights


# ============================================================
# MAIN ANOMALY DETECTION ENGINE
# ============================================================

def run_anomaly_detection(
    df
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None:

        return {

            "success": False,

            "message":
                "No dataset available."

        }

    if not isinstance(
        df,
        pd.DataFrame
    ):

        return {

            "success": False,

            "message":
                "Dataset must be a Pandas DataFrame."

        }

    if df.empty:

        return {

            "success": False,

            "message":
                "Dataset is empty."

        }

    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = get_numeric_columns(
        df
    )

    if not numeric_columns:

        return {

            "success": False,

            "message":
                "No numeric columns available for anomaly detection."

        }

    # --------------------------------------------------------
    # ANALYZE COLUMNS
    # --------------------------------------------------------

    column_results = []

    total_anomalies = 0

    total_values = 0

    for column in numeric_columns:

        result = analyze_column_anomalies(

            df,

            column

        )

        column_results.append(
            result
        )

        total_anomalies += result[
            "anomaly_count"
        ]

        total_values += result[
            "total_valid_values"
        ]

    # --------------------------------------------------------
    # DATASET RISK
    # --------------------------------------------------------

    risk = calculate_dataset_risk(

        total_anomalies,

        total_values

    )

    # --------------------------------------------------------
    # TOP SUSPICIOUS COLUMNS
    # --------------------------------------------------------

    suspicious_columns = sorted(

        column_results,

        key=lambda item:

            item[
                "anomaly_percentage"
            ],

        reverse=True

    )

    # --------------------------------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------------------------------

    insights = generate_anomaly_insights(

        column_results

    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "success": True,

        "dataset_summary": {

            "total_rows":

                int(len(df)),

            "numeric_columns":

                len(numeric_columns),

            "total_numeric_values":

                total_values

        },

        "anomaly_summary": {

            "total_anomalies":

                total_anomalies,

            "anomaly_rate_percent":

                round(

                    (
                        total_anomalies
                        /
                        total_values
                        *
                        100
                    )

                    if total_values > 0

                    else 0,

                    2

                )

        },

        "dataset_anomaly_risk":

            risk,

        "column_analysis":

            column_results,

        "top_suspicious_columns":

            suspicious_columns[:10],

        "business_insights":

            insights,

        "methods_used": [

            "IQR",

            "Z-Score",

            "Modified Z-Score (MAD)"

        ],

        "disclaimer": (

            "Detected anomalies are statistical observations "
            "and should be validated with business knowledge "
            "before removing or modifying data."

        )

    }