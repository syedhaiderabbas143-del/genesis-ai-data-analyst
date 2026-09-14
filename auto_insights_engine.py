# ============================================================
# GENESIS AI - AUTOMATIC AI INSIGHTS ENGINE
# ============================================================

import pandas as pd
import numpy as np


def generate_auto_insights(df):

    insights = []

    # --------------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------------

    total_rows = len(df)
    total_columns = len(df.columns)

    insights.append({

        "type": "dataset_overview",

        "title": "Dataset Overview",

        "insight": (
            f"Dataset contains {total_rows:,} rows "
            f"and {total_columns} columns."
        ),

        "priority": "Info"

    })


    # --------------------------------------------------------
    # NUMERIC COLUMN ANALYSIS
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()
    # --------------------------------------------------------
    # REMOVE ID / NON-BUSINESS NUMERIC COLUMNS
    # --------------------------------------------------------

    ignore_keywords = [
        "id",
        "employee id",
        "customer id",
        "phone",
        "mobile",
        "pin",
        "zip",
        "code"
    ]

    numeric_columns = [

        column

        for column in numeric_columns

        if not any(
            keyword in str(column).lower()
            for keyword in ignore_keywords
        )

    ]
    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 2:

            continue


        mean_value = series.mean()

        median_value = series.median()

        std_value = series.std()


        # ----------------------------------------------------
        # HIGH VARIATION DETECTION
        # ----------------------------------------------------

        if mean_value != 0:

            coefficient_variation = (

                abs(std_value / mean_value) * 100

            )

            if coefficient_variation > 50:

                insights.append({

                    "type": "high_variation",

                    "column": column,

                    "title": f"High Variation: {column}",

                    "insight": (
                        f"{column} shows high variation "
                        f"({round(coefficient_variation, 2)}%). "
                        f"This metric may require further investigation."
                    ),

                    "priority": "High",

                    "score": round(
                        coefficient_variation,
                        2
                    )

                })


        # ----------------------------------------------------
        # MEAN VS MEDIAN
        # ----------------------------------------------------

        if median_value != 0:

            difference_percent = (

                abs(
                    mean_value - median_value
                )
                / abs(median_value)
                * 100

            )

            if difference_percent > 20:

                insights.append({

                    "type": "distribution_warning",

                    "column": column,

                    "title": f"Distribution Pattern: {column}",

                    "insight": (
                        f"The average and median of "
                        f"{column} differ significantly "
                        f"({round(difference_percent, 2)}%). "
                        f"This may indicate skewed data "
                        f"or extreme values."
                    ),

                    "priority": "Medium",

                    "score": round(
                        difference_percent,
                        2
                    )

                })


        # ----------------------------------------------------
        # OUTLIER DETECTION
        # ----------------------------------------------------

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1


        lower_bound = q1 - (1.5 * iqr)

        upper_bound = q3 + (1.5 * iqr)


        outliers = series[
            (series < lower_bound)
            |
            (series > upper_bound)
        ]


        if len(outliers) > 0:

            outlier_percent = (

                len(outliers)
                / len(series)
                * 100

            )

            insights.append({

                "type": "outliers",

                "column": column,

                "title": f"Outliers Detected: {column}",

                "insight": (
                    f"{len(outliers):,} potential outliers "
                    f"were detected in {column} "
                    f"({round(outlier_percent, 2)}% of values)."
                ),

                "priority": (
                    "High"
                    if outlier_percent > 5
                    else "Medium"
                ),

                "score": round(
                    outlier_percent,
                    2
                )

            })


    # --------------------------------------------------------
    # MISSING DATA ANALYSIS
    # --------------------------------------------------------

    missing_counts = df.isnull().sum()


    for column, missing in missing_counts.items():

        if missing > 0:

            missing_percent = (

                missing
                / total_rows
                * 100

            )

            if missing_percent >= 5:

                insights.append({

                    "type": "missing_data",

                    "column": column,

                    "title": f"Missing Data: {column}",

                    "insight": (
                        f"{column} contains "
                        f"{missing:,} missing values "
                        f"({round(missing_percent, 2)}%)."
                    ),

                    "priority": (
                        "High"
                        if missing_percent >= 20
                        else "Medium"
                    ),

                    "score": round(
                        missing_percent,
                        2
                    )

                })


    # --------------------------------------------------------
    # CATEGORICAL ANALYSIS
    # --------------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    for column in categorical_columns:

        unique_count = df[column].nunique()


        if unique_count < 2:

            continue


        value_counts = df[column].value_counts()


        if len(value_counts) > 0:

            top_category = value_counts.index[0]

            top_count = value_counts.iloc[0]

            dominance_percent = (

                top_count
                / total_rows
                * 100

            )


            if dominance_percent >= 60:

                insights.append({

                    "type": "category_dominance",

                    "column": column,

                    "title": f"Category Dominance: {column}",

                    "insight": (
                        f"{top_category} represents "
                        f"{round(dominance_percent, 2)}% "
                        f"of all records in {column}."
                    ),

                    "priority": "Medium",

                    "score": round(
                        dominance_percent,
                        2
                    )

                })

    # --------------------------------------------------------
    # BUSINESS INTELLIGENCE INSIGHTS
    # --------------------------------------------------------

    # FIND COMMON BUSINESS COLUMNS

    profit_column = None
    revenue_column = None
    expense_column = None
    performance_column = None
    department_column = None


    for column in df.columns:

        column_name = str(column).lower().strip()


        if "profit" in column_name:

            profit_column = column


        if "revenue" in column_name:

            revenue_column = column


        if (

            "expense" in column_name

            or "cost" in column_name

        ):

            expense_column = column


        if "performance" in column_name:

            performance_column = column


        if "department" in column_name:

            department_column = column


    # --------------------------------------------------------
    # NEGATIVE PROFIT DETECTION
    # --------------------------------------------------------

    if profit_column is not None:

        profit_data = df[
            profit_column
        ].dropna()


        if len(profit_data) > 0:

            negative_profit_count = (

                profit_data < 0

            ).sum()


            negative_profit_percent = (

                negative_profit_count
                / len(profit_data)
                * 100

            )


            if negative_profit_count > 0:

                insights.append({

                    "type": "negative_profit",

                    "column": profit_column,

                    "title":
                        "Negative Profit Risk",

                    "insight": (

                        f"{negative_profit_count:,} records "

                        f"have negative profit "

                        f"({round(negative_profit_percent, 2)}%)."

                    ),

                    "priority": (

                        "Critical"

                        if negative_profit_percent >= 20

                        else "High"

                    ),

                    "score":
                        round(
                            negative_profit_percent,
                            2
                        )

                })


    # --------------------------------------------------------
    # HIGH EXPENSE RATIO DETECTION
    # --------------------------------------------------------

    if (

        expense_column is not None

        and revenue_column is not None

    ):

        valid_business_data = df[

            [
                expense_column,
                revenue_column
            ]

        ].dropna()


        valid_business_data = (

            valid_business_data[

                valid_business_data[
                    revenue_column
                ] > 0

            ]

        )


        if len(valid_business_data) > 0:

            high_expense_count = (

                valid_business_data[
                    expense_column
                ]

                >=

                valid_business_data[
                    revenue_column
                ] * 0.80

            ).sum()


            high_expense_percent = (

                high_expense_count
                / len(valid_business_data)
                * 100

            )


            if high_expense_count > 0:

                insights.append({

                    "type":
                        "high_expense_ratio",

                    "column":
                        expense_column,

                    "title":
                        "High Expense Ratio",

                    "insight": (

                        f"{high_expense_count:,} records "

                        f"have expenses equal to or "

                        f"above 80% of revenue "

                        f"({round(high_expense_percent, 2)}%)."

                    ),

                    "priority": (

                        "Critical"

                        if high_expense_percent >= 20

                        else "High"

                    ),

                    "score":
                        round(
                            high_expense_percent,
                            2
                        )

                })


    # --------------------------------------------------------
    # LOW PERFORMANCE DETECTION
    # --------------------------------------------------------

    if performance_column is not None:

        performance_data = df[
            performance_column
        ].dropna()


        if len(performance_data) > 0:

            low_performance_count = (

                performance_data <= 2

            ).sum()


            low_performance_percent = (

                low_performance_count
                / len(performance_data)
                * 100

            )


            if low_performance_count > 0:

                insights.append({

                    "type":
                        "low_performance",

                    "column":
                        performance_column,

                    "title":
                        "Low Performance Population",

                    "insight": (

                        f"{low_performance_count:,} records "

                        f"have low performance ratings "

                        f"(2 or below), representing "

                        f"{round(low_performance_percent, 2)}% "

                        f"of valid records."

                    ),

                    "priority": (

                        "High"

                        if low_performance_percent >= 20

                        else "Medium"

                    ),

                    "score":
                        round(
                            low_performance_percent,
                            2
                        )

                })


    # --------------------------------------------------------
    # DEPARTMENT PERFORMANCE ANALYSIS
    # --------------------------------------------------------

    if (

        department_column is not None

        and profit_column is not None

    ):

        department_data = df[

            [
                department_column,
                profit_column
            ]

        ].dropna()


        if (

            not department_data.empty

            and department_data[
                department_column
            ].nunique() > 1

        ):

            department_profit = (

                department_data.groupby(

                    department_column

                )[

                    profit_column

                ]

                .mean()

                .sort_values()

            )


            lowest_department = (

                department_profit.index[0]

            )


            lowest_profit = (

                department_profit.iloc[0]

            )


            highest_department = (

                department_profit.index[-1]

            )


            highest_profit = (

                department_profit.iloc[-1]

            )


            profit_difference = (

                highest_profit
                - lowest_profit

            )


            insights.append({

                "type":
                    "department_profit_difference",

                "column":
                    department_column,

                "title":
                    "Department Profitability Difference",

                "insight": (

                    f"{lowest_department} has the lowest "

                    f"average profit "

                    f"({round(lowest_profit, 2)}), while "

                    f"{highest_department} has the highest "

                    f"average profit "

                    f"({round(highest_profit, 2)}). "

                    f"The difference is "

                    f"{round(profit_difference, 2)}."

                ),

                "priority":
                    "Medium",

                "score":
                    round(
                        profit_difference,
                        2
                    )

            })
    # --------------------------------------------------------
    # SORT INSIGHTS BY IMPORTANCE
    # --------------------------------------------------------

    priority_scores = {

        "Critical": 4,

        "High": 3,

        "Medium": 2,

        "Info": 1

    }


    insights = sorted(

        insights,

        key=lambda x: (

            priority_scores.get(
                x.get("priority"),
                0
            ),

            x.get(
                "score",
                0
            )

        ),

        reverse=True

    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    high_priority_count = len([

        item

        for item in insights

        if item.get("priority")

        in ["Critical", "High"]

    ])


    summary = (

        f"Genesis AI automatically generated "

        f"{len(insights)} insights from the dataset. "

        f"{high_priority_count} insights require "

        f"immediate attention."

    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "insights": insights,

        "summary": summary,

        "total_insights": len(insights),

        "high_priority_insights":

            high_priority_count

    }