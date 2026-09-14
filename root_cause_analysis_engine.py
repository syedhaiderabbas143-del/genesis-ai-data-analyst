# ============================================================
# GENESIS AI - ROOT CAUSE ANALYSIS ENGINE
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# SEVERITY CALCULATION
# ============================================================

def determine_severity(score):

    if score >= 80:
        return "Critical"

    elif score >= 60:
        return "High"

    elif score >= 30:
        return "Medium"

    return "Low"


# ============================================================
# PRIORITY CALCULATION
# ============================================================

def determine_priority(severity):

    if severity == "Critical":
        return "Immediate"

    elif severity == "High":
        return "High"

    elif severity == "Medium":
        return "Medium"

    return "Low"


# ============================================================
# NUMERIC COLUMN ANALYSIS
# ============================================================

def analyze_numeric_column(df, column):

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(series) < 3:

        return None


    mean_value = float(
        series.mean()
    )

    median_value = float(
        series.median()
    )

    minimum_value = float(
        series.min()
    )

    maximum_value = float(
        series.max()
    )

    std_value = float(
        series.std()
    )

    missing_count = int(
        df[column].isnull().sum()
    )

    missing_percentage = (

        missing_count

        /

        len(df)

        *

        100

    ) if len(df) > 0 else 0


    # --------------------------------------------------------
    # VARIABILITY SCORE
    # --------------------------------------------------------

    if mean_value != 0:

        coefficient_variation = (

            abs(std_value)

            /

            abs(mean_value)

            *

            100

        )

    else:

        coefficient_variation = 0


    # --------------------------------------------------------
    # IQR OUTLIERS
    # --------------------------------------------------------

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

        *

        100

    )


    return {

        "column": column,

        "mean": round(
            mean_value,
            4
        ),

        "median": round(
            median_value,
            4
        ),

        "minimum": round(
            minimum_value,
            4
        ),

        "maximum": round(
            maximum_value,
            4
        ),

        "standard_deviation": round(
            std_value,
            4
        ),

        "coefficient_variation": round(
            coefficient_variation,
            2
        ),

        "missing_count": missing_count,

        "missing_percentage": round(
            missing_percentage,
            2
        ),

        "outlier_count": int(
            outlier_count
        ),

        "outlier_percentage": round(
            outlier_percentage,
            2
        )

    }


# ============================================================
# ROOT CAUSE DETECTION
# ============================================================

def identify_root_causes(
    column_analysis
):

    root_causes = []


    # --------------------------------------------------------
    # MISSING DATA
    # --------------------------------------------------------

    missing_percentage = column_analysis.get(
        "missing_percentage",
        0
    )


    if missing_percentage >= 10:

        root_causes.append({

            "cause": "High Missing Data",

            "evidence": (
                f"{missing_percentage}% of values "
                f"are missing."
            ),

            "impact_score": min(
                missing_percentage * 5,
                100
            ),

            "recommended_action": (
                "Investigate data collection processes "
                "and improve data completeness."
            )

        })


    # --------------------------------------------------------
    # OUTLIERS
    # --------------------------------------------------------

    outlier_percentage = column_analysis.get(
        "outlier_percentage",
        0
    )


    if outlier_percentage >= 5:

        root_causes.append({

            "cause": "High Number of Outliers",

            "evidence": (
                f"{outlier_percentage}% of observations "
                f"were identified as outliers."
            ),

            "impact_score": min(
                outlier_percentage * 8,
                100
            ),

            "recommended_action": (
                "Investigate unusual values to determine "
                "whether they represent valid business events "
                "or data quality problems."
            )

        })


    # --------------------------------------------------------
    # HIGH VARIABILITY
    # --------------------------------------------------------

    coefficient_variation = column_analysis.get(
        "coefficient_variation",
        0
    )


    if coefficient_variation >= 50:

        root_causes.append({

            "cause": "High Data Variability",

            "evidence": (
                f"Coefficient of variation is "
                f"{coefficient_variation}%."
            ),

            "impact_score": min(
                coefficient_variation,
                100
            ),

            "recommended_action": (
                "Segment the data to identify the groups "
                "or business factors responsible for "
                "high variability."
            )

        })


    return root_causes


# ============================================================
# DUPLICATE DATA ANALYSIS
# ============================================================

def analyze_duplicate_rows(df):

    duplicate_count = int(
        df.duplicated().sum()
    )


    duplicate_percentage = (

        duplicate_count

        /

        len(df)

        *

        100

    ) if len(df) > 0 else 0


    if duplicate_count == 0:

        return None


    impact_score = min(
        duplicate_percentage * 10,
        100
    )


    return {

        "cause": "Duplicate Records",

        "evidence": (
            f"{duplicate_count} duplicate rows detected "
            f"({round(duplicate_percentage, 2)}%)."
        ),

        "impact_score": round(
            impact_score,
            2
        ),

        "recommended_action": (
            "Review duplicate records and implement "
            "duplicate prevention rules."
        )

    }


# ============================================================
# OVERALL ROOT CAUSE ANALYSIS
# ============================================================

def run_root_cause_analysis(df):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        return {

            "success": False,

            "message": (
                "No dataset available for "
                "root cause analysis."
            )

        }


    total_rows = len(df)

    numeric_columns = df.select_dtypes(
        include=[
            np.number
        ]
    ).columns.tolist()


    root_causes = []

    column_analysis_results = {}


    # ========================================================
    # NUMERIC COLUMN ANALYSIS
    # ========================================================

    for column in numeric_columns:

        analysis = analyze_numeric_column(
            df,
            column
        )


        if analysis is None:

            continue


        column_analysis_results[
            column
        ] = analysis


        detected_causes = identify_root_causes(
            analysis
        )


        for cause in detected_causes:

            cause[
                "affected_column"
            ] = column


            root_causes.append(
                cause
            )


    # ========================================================
    # DUPLICATE ROW ANALYSIS
    # ========================================================

    duplicate_cause = analyze_duplicate_rows(
        df
    )


    if duplicate_cause:

        duplicate_cause[
            "affected_column"
        ] = "Dataset"


        root_causes.append(
            duplicate_cause
        )


    # ========================================================
    # MISSING DATA ANALYSIS
    # ========================================================

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )


        missing_percentage = (

            missing_count

            /

            total_rows

            *

            100

        ) if total_rows > 0 else 0


        if missing_percentage >= 20:

            already_exists = any(

                cause.get(
                    "affected_column"
                ) == column

                and

                cause.get(
                    "cause"
                ) == "High Missing Data"

                for cause in root_causes

            )


            if not already_exists:

                root_causes.append({

                    "cause": (
                        "Critical Missing Data"
                    ),

                    "affected_column": column,

                    "evidence": (
                        f"{round(missing_percentage, 2)}% "
                        f"of values are missing."
                    ),

                    "impact_score": min(
                        missing_percentage * 5,
                        100
                    ),

                    "recommended_action": (
                        "Investigate the data source and "
                        "improve the data collection process."
                    )

                })


    # ========================================================
    # SORT ROOT CAUSES
    # ========================================================

    root_causes = sorted(

        root_causes,

        key=lambda x: x.get(
            "impact_score",
            0
        ),

        reverse=True

    )


    # ========================================================
    # ADD SEVERITY AND PRIORITY
    # ========================================================

    for cause in root_causes:

        severity = determine_severity(

            cause.get(
                "impact_score",
                0
            )

        )


        cause[
            "severity"
        ] = severity


        cause[
            "priority"
        ] = determine_priority(
            severity
        )


        cause[
            "impact_score"
        ] = round(

            float(

                cause.get(
                    "impact_score",
                    0
                )

            ),

            2

        )


    # ========================================================
    # PRIMARY ROOT CAUSE
    # ========================================================

    if root_causes:

        primary_root_cause = root_causes[0]

    else:

        primary_root_cause = None


    # ========================================================
    # DATASET STATUS
    # ========================================================

    total_causes = len(
        root_causes
    )


    if total_causes == 0:

        overall_status = "Healthy"


    elif total_causes <= 2:

        overall_status = "Minor Issues Detected"


    elif total_causes <= 5:

        overall_status = "Moderate Issues Detected"


    else:

        overall_status = "Critical Data Issues Detected"


    # ========================================================
    # AI MANAGEMENT INSIGHT
    # ========================================================

    if primary_root_cause:

        management_insight = (

            f"The primary root cause detected is "

            f"'{primary_root_cause['cause']}' "

            f"affecting "

            f"'{primary_root_cause['affected_column']}'. "

            f"This should be addressed with "

            f"{primary_root_cause['priority'].lower()} "

            f"priority."

        )

    else:

        management_insight = (

            "No major root causes were automatically "

            "detected in the current dataset."

        )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "dataset_status": overall_status,

        "dataset_summary": {

            "total_rows": int(
                total_rows
            ),

            "total_columns": int(
                len(df.columns)
            ),

            "numeric_columns_analyzed": int(
                len(numeric_columns)
            )

        },

        "primary_root_cause": (
            primary_root_cause
        ),

        "total_root_causes_detected": (
            total_causes
        ),

        "root_causes": root_causes,

        "column_analysis": (
            column_analysis_results
        ),

        "management_insight": (
            management_insight
        ),

        "warning": (

            "Root cause analysis identifies potential "

            "data-driven causes and should be combined "

            "with business knowledge before making "

            "final management decisions."

        )

    }