# ============================================================
# GENESIS AI - WHAT-IF / SCENARIO ANALYSIS ENGINE
# ============================================================

import pandas as pd


# ============================================================
# MAIN SCENARIO ANALYSIS FUNCTION
# ============================================================

def run_scenario_analysis(
    df,
    revenue_column=None,
    expense_column=None,
    revenue_change_percent=0,
    expense_change_percent=0
):

    if df is None or df.empty:

        return {

            "success": False,

            "message": "No dataset available for scenario analysis."

        }


    # --------------------------------------------------------
    # GET NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()


    if not numeric_columns:

        return {

            "success": False,

            "message": "No numeric columns available for scenario analysis."

        }


    # --------------------------------------------------------
    # AUTO-DETECT REVENUE COLUMN
    # --------------------------------------------------------

    if revenue_column is None:

        revenue_keywords = [

            "revenue",

            "sales",

            "income"

        ]


        for column in numeric_columns:

            column_name = column.lower()


            if any(
                keyword in column_name
                for keyword in revenue_keywords
            ):

                revenue_column = column

                break


    # --------------------------------------------------------
    # AUTO-DETECT EXPENSE COLUMN
    # --------------------------------------------------------

    if expense_column is None:

        expense_keywords = [

            "expense",

            "cost",

            "spending"

        ]


        for column in numeric_columns:

            column_name = column.lower()


            if any(
                keyword in column_name
                for keyword in expense_keywords
            ):

                expense_column = column

                break


    # --------------------------------------------------------
    # VALIDATE COLUMNS
    # --------------------------------------------------------

    if revenue_column not in df.columns:

        return {

            "success": False,

            "message": (
                "Revenue column could not be detected. "
                "Please provide a valid revenue column."
            ),

            "available_numeric_columns": numeric_columns

        }


    if expense_column not in df.columns:

        return {

            "success": False,

            "message": (
                "Expense column could not be detected. "
                "Please provide a valid expense column."
            ),

            "available_numeric_columns": numeric_columns

        }


    # --------------------------------------------------------
    # CALCULATE CURRENT BUSINESS VALUES
    # --------------------------------------------------------

    current_revenue = float(

        df[revenue_column].sum()

    )


    current_expense = float(

        df[expense_column].sum()

    )


    current_profit = (

        current_revenue

        -

        current_expense

    )


    # --------------------------------------------------------
    # APPLY WHAT-IF CHANGES
    # --------------------------------------------------------

    projected_revenue = (

        current_revenue

        *

        (
            1

            +

            (
                revenue_change_percent
                /
                100
            )
        )

    )


    projected_expense = (

        current_expense

        *

        (
            1

            +

            (
                expense_change_percent
                /
                100
            )
        )

    )


    projected_profit = (

        projected_revenue

        -

        projected_expense

    )


    # --------------------------------------------------------
    # CALCULATE IMPACT
    # --------------------------------------------------------

    revenue_impact = (

        projected_revenue

        -

        current_revenue

    )


    expense_impact = (

        projected_expense

        -

        current_expense

    )


    profit_impact = (

        projected_profit

        -

        current_profit

    )


    # --------------------------------------------------------
    # CALCULATE PROFIT CHANGE %
    # --------------------------------------------------------

    if current_profit != 0:

        profit_change_percent = (

            (
                profit_impact
                /
                abs(current_profit)
            )

            *

            100

        )

    else:

        profit_change_percent = 0


    # --------------------------------------------------------
    # DETERMINE SCENARIO RESULT
    # --------------------------------------------------------

    if profit_impact > 0:

        scenario_result = "Positive"

    elif profit_impact < 0:

        scenario_result = "Negative"

    else:

        scenario_result = "Neutral"


    # --------------------------------------------------------
    # GENERATE AI-STYLE INSIGHT
    # --------------------------------------------------------

    if scenario_result == "Positive":

        insight = (

            "The scenario is expected to improve profitability "
            "based on the selected revenue and expense changes."

        )


    elif scenario_result == "Negative":

        insight = (

            "The scenario may reduce profitability and should "
            "be reviewed before implementation."

        )


    else:

        insight = (

            "The scenario is expected to have minimal impact "
            "on overall profitability."

        )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "scenario": {

            "revenue_change_percent":

                revenue_change_percent,

            "expense_change_percent":

                expense_change_percent

        },

        "columns_used": {

            "revenue_column":

                revenue_column,

            "expense_column":

                expense_column

        },

        "current_business_position": {

            "revenue":

                round(
                    current_revenue,
                    2
                ),

            "expense":

                round(
                    current_expense,
                    2
                ),

            "profit":

                round(
                    current_profit,
                    2
                )

        },

        "projected_business_position": {

            "revenue":

                round(
                    projected_revenue,
                    2
                ),

            "expense":

                round(
                    projected_expense,
                    2
                ),

            "profit":

                round(
                    projected_profit,
                    2
                )

        },

        "business_impact": {

            "revenue_impact":

                round(
                    revenue_impact,
                    2
                ),

            "expense_impact":

                round(
                    expense_impact,
                    2
                ),

            "profit_impact":

                round(
                    profit_impact,
                    2
                ),

            "profit_change_percent":

                round(
                    profit_change_percent,
                    2
                )

        },

        "scenario_result":

            scenario_result,

        "ai_insight":

            insight

    }