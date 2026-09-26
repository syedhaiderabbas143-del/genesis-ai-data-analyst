# ============================================================
# GENESIS AI - ADVANCED OUTLIER DETECTION ENGINE
# ============================================================

import pandas as pd
import numpy as np

from scipy import stats


# ============================================================
# SAFE NUMERIC COLUMNS
# ============================================================

def get_numeric_columns(df):

    if df is None or df.empty:

        return []

    return df.select_dtypes(

        include=[
            np.number
        ]

    ).columns.tolist()


# ============================================================
# OUTLIER SEVERITY CLASSIFICATION
# ============================================================

def classify_outlier_severity(

    outlier_percentage

):

    if outlier_percentage >= 20:

        return "Critical"

    elif outlier_percentage >= 10:

        return "High"

    elif outlier_percentage >= 5:

        return "Medium"

    elif outlier_percentage > 0:

        return "Low"

    return "None"


# ============================================================
# IQR OUTLIER DETECTION
# ============================================================

def detect_iqr_outliers(

    series

):

    series = series.dropna()

    if len(series) < 4:

        return {

            "outlier_count": 0,

            "outlier_percentage": 0.0,

            "lower_bound": None,

            "upper_bound": None,

            "outlier_indexes": []

        }


    q1 = series.quantile(

        0.25

    )


    q3 = series.quantile(

        0.75

    )


    iqr = (

        q3

        -

        q1

    )


    lower_bound = (

        q1

        -

        (

            1.5

            *

            iqr

        )

    )


    upper_bound = (

        q3

        +

        (

            1.5

            *

            iqr

        )

    )


    outliers = series[

        (

            series

            <

            lower_bound

        )

        |

        (

            series

            >

            upper_bound

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


    return {

        "outlier_count": int(

            outlier_count

        ),

        "outlier_percentage": round(

            float(

                outlier_percentage

            ),

            2

        ),

        "lower_bound": round(

            float(

                lower_bound

            ),

            4

        ),

        "upper_bound": round(

            float(

                upper_bound

            ),

            4

        ),

        "outlier_indexes": [

            int(index)

            if isinstance(

                index,

                (

                    int,

                    np.integer

                )

            )

            else str(index)

            for index in outliers.index.tolist()

        ]

    }


# ============================================================
# Z-SCORE OUTLIER DETECTION
# ============================================================

def detect_zscore_outliers(

    series,

    threshold=3.0

):

    series = series.dropna()


    if len(series) < 3:

        return {

            "outlier_count": 0,

            "outlier_percentage": 0.0,

            "threshold": threshold,

            "outlier_indexes": []

        }


    if series.nunique() <= 1:

        return {

            "outlier_count": 0,

            "outlier_percentage": 0.0,

            "threshold": threshold,

            "outlier_indexes": []

        }


    z_scores = np.abs(

        stats.zscore(

            series

        )

    )


    outlier_mask = (

        z_scores

        >

        threshold

    )


    outliers = series.iloc[

        np.where(

            outlier_mask

        )[0]

    ]


    outlier_count = len(

        outliers

    )


    outlier_percentage = (

        outlier_count

        /

        len(series)

    ) * 100


    return {

        "outlier_count": int(

            outlier_count

        ),

        "outlier_percentage": round(

            float(

                outlier_percentage

            ),

            2

        ),

        "threshold": threshold,

        "outlier_indexes": [

            int(index)

            if isinstance(

                index,

                (

                    int,

                    np.integer

                )

            )

            else str(index)

            for index in outliers.index.tolist()

        ]

    }


# ============================================================
# MODIFIED Z-SCORE OUTLIER DETECTION
# ============================================================

def detect_modified_zscore_outliers(

    series,

    threshold=3.5

):

    series = series.dropna()


    if len(series) < 3:

        return {

            "outlier_count": 0,

            "outlier_percentage": 0.0,

            "threshold": threshold,

            "median": None,

            "mad": None,

            "outlier_indexes": []

        }


    median = series.median()


    absolute_deviation = np.abs(

        series

        -

        median

    )


    mad = absolute_deviation.median()


    if mad == 0:

        return {

            "outlier_count": 0,

            "outlier_percentage": 0.0,

            "threshold": threshold,

            "median": round(

                float(

                    median

                ),

                4

            ),

            "mad": 0.0,

            "outlier_indexes": []

        }


    modified_z_scores = (

        0.6745

        *

        (

            series

            -

            median

        )

        /

        mad

    )


    outlier_mask = (

        np.abs(

            modified_z_scores

        )

        >

        threshold

    )


    outliers = series[

        outlier_mask

    ]


    outlier_count = len(

        outliers

    )


    outlier_percentage = (

        outlier_count

        /

        len(series)

    ) * 100


    return {

        "outlier_count": int(

            outlier_count

        ),

        "outlier_percentage": round(

            float(

                outlier_percentage

            ),

            2

        ),

        "threshold": threshold,

        "median": round(

            float(

                median

            ),

            4

        ),

        "mad": round(

            float(

                mad

            ),

            4

        ),

        "outlier_indexes": [

            int(index)

            if isinstance(

                index,

                (

                    int,

                    np.integer

                )

            )

            else str(index)

            for index in outliers.index.tolist()

        ]

    }


# ============================================================
# DETECT OUTLIERS FOR ONE COLUMN
# ============================================================

def analyze_column_outliers(

    series,

    column_name

):

    clean_series = series.dropna()


    if len(clean_series) < 3:

        return {

            "column": str(

                column_name

            ),

            "status": "Insufficient Data",

            "valid_records": int(

                len(clean_series)

            )

        }


    # --------------------------------------------------------
    # IQR ANALYSIS
    # --------------------------------------------------------

    iqr_result = detect_iqr_outliers(

        clean_series

    )


    # --------------------------------------------------------
    # Z-SCORE ANALYSIS
    # --------------------------------------------------------

    zscore_result = detect_zscore_outliers(

        clean_series

    )


    # --------------------------------------------------------
    # MODIFIED Z-SCORE ANALYSIS
    # --------------------------------------------------------

    modified_zscore_result = (

        detect_modified_zscore_outliers(

            clean_series

        )

    )


    # --------------------------------------------------------
    # COMBINE ALL DETECTED OUTLIERS
    # --------------------------------------------------------

    combined_indexes = set()


    for index in (

        iqr_result[

            "outlier_indexes"

        ]

    ):

        combined_indexes.add(

            index

        )


    for index in (

        zscore_result[

            "outlier_indexes"

        ]

    ):

        combined_indexes.add(

            index

        )


    for index in (

        modified_zscore_result[

            "outlier_indexes"

        ]

    ):

        combined_indexes.add(

            index

        )


    combined_count = len(

        combined_indexes

    )


    combined_percentage = (

        combined_count

        /

        len(clean_series)

    ) * 100


    severity = (

        classify_outlier_severity(

            combined_percentage

        )

    )


    # --------------------------------------------------------
    # DETERMINE DATA QUALITY STATUS
    # --------------------------------------------------------

    if combined_percentage == 0:

        status = "Healthy"

    elif combined_percentage < 5:

        status = "Minor Outliers Detected"

    elif combined_percentage < 15:

        status = "Moderate Outlier Risk"

    else:

        status = "High Outlier Risk"


    # --------------------------------------------------------
    # BUSINESS INSIGHT
    # --------------------------------------------------------

    if combined_percentage == 0:

        insight = (

            f"No significant outliers were detected in "

            f"{column_name}."

        )

    elif combined_percentage < 5:

        insight = (

            f"A small number of unusual values were detected "

            f"in {column_name}. These records should be reviewed."

        )

    elif combined_percentage < 15:

        insight = (

            f"{column_name} contains a noticeable number of "

            f"outliers that may affect statistical analysis."

        )

    else:

        insight = (

            f"{column_name} contains a high percentage of "

            f"outliers. Data validation is strongly recommended."

        )


    # ========================================================
    # FINAL COLUMN RESULT
    # ========================================================

    return {

        "column": str(

            column_name

        ),

        "status": status,

        "valid_records": int(

            len(clean_series)

        ),

        "combined_outlier_count": int(

            combined_count

        ),

        "combined_outlier_percentage": round(

            float(

                combined_percentage

            ),

            2

        ),

        "severity": severity,

        "methods": {

            "iqr": iqr_result,

            "z_score": zscore_result,

            "modified_z_score": (

                modified_zscore_result

            )

        },

        "insight": insight

    }


# ============================================================
# DATASET OUTLIER INTELLIGENCE
# ============================================================

def generate_outlier_intelligence(

    column_results

):

    if not column_results:

        return {

            "overall_status": (

                "No Numeric Data"

            ),

            "columns_with_outliers": 0,

            "highest_risk_column": None,

            "recommendation": (

                "No numeric columns available "

                "for outlier analysis."

            )

        }


    columns_with_outliers = [


        result


        for result in column_results.values()


        if result.get(

            "combined_outlier_count",

            0

        ) > 0

    ]


    # --------------------------------------------------------
    # SORT BY OUTLIER PERCENTAGE
    # --------------------------------------------------------

    sorted_columns = sorted(

        column_results.values(),

        key=lambda result:

        result.get(

            "combined_outlier_percentage",

            0

        ),

        reverse=True

    )


    highest_risk_column = (

        sorted_columns[0]

        if sorted_columns

        else None

    )


    # --------------------------------------------------------
    # OVERALL STATUS
    # --------------------------------------------------------

    if not columns_with_outliers:

        overall_status = (

            "Healthy"

        )

        recommendation = (

            "No significant outlier issues were detected. "

            "The dataset is suitable for further analysis."

        )


    else:

        highest_percentage = (

            highest_risk_column.get(

                "combined_outlier_percentage",

                0

            )

        )


        if highest_percentage >= 20:

            overall_status = (

                "Critical"

            )

            recommendation = (

                "Significant outliers were detected. "

                "Review data quality before forecasting "

                "or statistical modeling."

            )


        elif highest_percentage >= 10:

            overall_status = (

                "High Risk"

            )

            recommendation = (

                "Review high-risk columns and investigate "

                "unusual records before advanced analysis."

            )


        elif highest_percentage >= 5:

            overall_status = (

                "Moderate Risk"

            )

            recommendation = (

                "Outlier treatment should be considered "

                "for sensitive statistical analysis."

            )


        else:

            overall_status = (

                "Low Risk"

            )

            recommendation = (

                "Only a small number of unusual values "

                "were detected. Review them if necessary."

            )


    # --------------------------------------------------------
    # HIGHEST RISK COLUMN
    # --------------------------------------------------------

    highest_risk_summary = None


    if highest_risk_column:

        highest_risk_summary = {

            "column": highest_risk_column.get(

                "column"

            ),

            "outlier_count": highest_risk_column.get(

                "combined_outlier_count"

            ),

            "outlier_percentage":

                highest_risk_column.get(

                    "combined_outlier_percentage"

                ),

            "severity":

                highest_risk_column.get(

                    "severity"

                )

        }


    return {

        "overall_status": (

            overall_status

        ),

        "columns_analyzed": len(

            column_results

        ),

        "columns_with_outliers": len(

            columns_with_outliers

        ),

        "highest_risk_column": (

            highest_risk_summary

        ),

        "recommendation": (

            recommendation

        )

    }


# ============================================================
# MASTER OUTLIER ANALYSIS ENGINE
# ============================================================

def run_outlier_analysis(

    df

):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None:

        return {

            "success": False,

            "message": (

                "No dataset available "

                "for outlier analysis."

            )

        }


    if df.empty:

        return {

            "success": False,

            "message": (

                "Dataset is empty."

            )

        }


    # --------------------------------------------------------
    # GET NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = (

        get_numeric_columns(

            df

        )

    )


    if not numeric_columns:

        return {

            "success": False,

            "message": (

                "No numeric columns available "

                "for outlier detection."

            )

        }


    # --------------------------------------------------------
    # COLUMN ANALYSIS
    # --------------------------------------------------------

    column_results = {}


    for column in numeric_columns:

        try:

            column_results[

                str(column)

            ] = (

                analyze_column_outliers(

                    df[column],

                    column

                )

            )


        except Exception as error:

            column_results[

                str(column)

            ] = {

                "column": str(

                    column

                ),

                "status": "Analysis Failed",

                "error": str(

                    error

                )

            }


    # --------------------------------------------------------
    # DATASET INTELLIGENCE
    # --------------------------------------------------------

    intelligence = (

        generate_outlier_intelligence(

            column_results

        )

    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "analysis_type": (

            "Advanced Multi-Method Outlier Detection"

        ),

        "dataset_summary": {

            "total_rows": int(

                len(df)

            ),

            "total_columns": int(

                len(df.columns)

            ),

            "numeric_columns_analyzed": len(

                numeric_columns

            )

        },

        "outlier_intelligence": (

            intelligence

        ),

        "column_analysis": (

            column_results

        ),

        "methods_used": [

            "IQR",

            "Z-Score",

            "Modified Z-Score"

        ]

    }