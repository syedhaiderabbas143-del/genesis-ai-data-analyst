# ============================================================
# GENESIS AI
# ADVANCED ROOT CAUSE INTELLIGENCE ENGINE
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# SAFE NUMERIC CONVERSION
# ============================================================

def safe_numeric(value):

    try:

        return float(value)

    except Exception:

        return 0.0


# ============================================================
# ROOT CAUSE SEVERITY CALCULATOR
# ============================================================

def calculate_root_cause_severity(

    affected_percentage,
    evidence_score,
    business_impact_score

):

    severity_score = (

        affected_percentage * 0.4

        +

        evidence_score * 0.3

        +

        business_impact_score * 0.3

    )


    severity_score = min(

        round(severity_score, 2),

        100

    )


    if severity_score >= 80:

        severity = "Critical"

    elif severity_score >= 60:

        severity = "High"

    elif severity_score >= 40:

        severity = "Medium"

    else:

        severity = "Low"


    return {

        "severity_score": severity_score,

        "severity": severity

    }


# ============================================================
# DETECT CONTRIBUTING GROUPS
# ============================================================

def analyze_contributing_groups(

    df,

    target_column,

    problem_mask,

    max_groups=5

):

    contributing_groups = []


    if target_column not in df.columns:

        return contributing_groups


    candidate_columns = []


    for column in df.columns:

        if column == target_column:

            continue


        if (

            df[column].dtype == "object"

            or

            str(df[column].dtype).startswith("category")

        ):

            unique_count = df[column].nunique()


            if 2 <= unique_count <= 30:

                candidate_columns.append(

                    column

                )


    for column in candidate_columns[:10]:

        try:

            grouped_total = (

                df.groupby(column)

                .size()

            )


            grouped_problem = (

                df[problem_mask]

                .groupby(column)

                .size()

            )


            analysis = pd.DataFrame({

                "total": grouped_total,

                "problem_count": grouped_problem

            })


            analysis = analysis.fillna(

                0

            )


            analysis["problem_percentage"] = (

                analysis["problem_count"]

                /

                analysis["total"]

                * 100

            )


            analysis = analysis.sort_values(

                "problem_percentage",

                ascending=False

            )


            for group_name, row in analysis.head(

                max_groups

            ).iterrows():

                if row["problem_count"] <= 0:

                    continue


                contributing_groups.append({

                    "factor": column,

                    "group": str(group_name),

                    "affected_records": int(

                        row["problem_count"]

                    ),

                    "affected_percentage": round(

                        row["problem_percentage"],

                        2

                    )

                })


        except Exception:

            continue


    contributing_groups = sorted(

        contributing_groups,

        key=lambda x: x.get(

            "affected_percentage",

            0

        ),

        reverse=True

    )


    return contributing_groups[:max_groups]


# ============================================================
# ANALYZE NUMERIC FACTORS
# ============================================================

def analyze_numeric_factors(

    df,

    problem_mask,

    max_factors=5

):

    numeric_factors = []


    numeric_columns = (

        df.select_dtypes(

            include=[

                np.number

            ]

        ).columns.tolist()

    )


    if not numeric_columns:

        return numeric_factors


    for column in numeric_columns:

        try:

            problem_values = (

                df.loc[

                    problem_mask,

                    column

                ]

                .dropna()

            )


            normal_values = (

                df.loc[

                    ~problem_mask,

                    column

                ]

                .dropna()

            )


            if (

                len(problem_values) < 5

                or

                len(normal_values) < 5

            ):

                continue


            problem_mean = (

                problem_values.mean()

            )


            normal_mean = (

                normal_values.mean()

            )


            if normal_mean == 0:

                continue


            difference_percent = (

                abs(

                    (

                        problem_mean

                        -

                        normal_mean

                    )

                    /

                    abs(normal_mean)

                )

                * 100

            )


            numeric_factors.append({

                "factor": column,

                "problem_group_average": round(

                    safe_numeric(

                        problem_mean

                    ),

                    2

                ),

                "normal_group_average": round(

                    safe_numeric(

                        normal_mean

                    ),

                    2

                ),

                "difference_percent": round(

                    safe_numeric(

                        difference_percent

                    ),

                    2

                )

            })


        except Exception:

            continue


    numeric_factors = sorted(

        numeric_factors,

        key=lambda x: x.get(

            "difference_percent",

            0

        ),

        reverse=True

    )


    return numeric_factors[:max_factors]


# ============================================================
# MAIN ROOT CAUSE ANALYSIS
# ============================================================

def analyze_advanced_root_cause(

    df,

    issue_type,

    issue_title,

    issue_message

):

    result = {

        "issue_type": issue_type,

        "issue_title": issue_title,

        "issue_message": issue_message,

        "root_cause_detected": False,

        "root_causes": [],

        "contributing_groups": [],

        "numeric_factors": [],

        "analysis_confidence": "Low",

        "confidence_score": 0

    }


    if df is None:

        return result


    if len(df) == 0:

        return result


    # ========================================================
    # LOW PERFORMANCE ROOT CAUSE
    # ========================================================

    if issue_type == "low_performance":

        possible_columns = [

            "Performance Rating",

            "Performance",

            "Performance_Rating",

            "performance_rating"

        ]


        target_column = None


        for column in possible_columns:

            if column in df.columns:

                target_column = column

                break


        if not target_column:

            return result


        try:

            performance_values = pd.to_numeric(

                df[target_column],

                errors="coerce"

            )


            problem_mask = (

                performance_values <= 2

            )


        except Exception:

            return result


        total_records = len(

            df

        )


        affected_records = int(

            problem_mask.sum()

        )


        if total_records == 0:

            return result


        affected_percentage = (

            affected_records

            /

            total_records

            * 100

        )


        # ====================================================
        # CONTRIBUTING GROUP ANALYSIS
        # ====================================================

        contributing_groups = (

            analyze_contributing_groups(

                df,

                target_column,

                problem_mask

            )

        )


        # ====================================================
        # NUMERIC FACTOR ANALYSIS
        # ====================================================

        numeric_factors = (

            analyze_numeric_factors(

                df,

                problem_mask

            )

        )


        # ====================================================
        # EVIDENCE SCORE
        # ====================================================

        evidence_score = 40


        if contributing_groups:

            evidence_score += 25


        if numeric_factors:

            evidence_score += 25


        evidence_score = min(

            evidence_score,

            100

        )


        # ====================================================
        # BUSINESS IMPACT SCORE
        # ====================================================

        if affected_percentage >= 50:

            business_impact_score = 90

        elif affected_percentage >= 30:

            business_impact_score = 80

        elif affected_percentage >= 15:

            business_impact_score = 60

        else:

            business_impact_score = 40


        # ====================================================
        # ROOT CAUSE SEVERITY
        # ====================================================

        severity_result = (

            calculate_root_cause_severity(

                affected_percentage,

                evidence_score,

                business_impact_score

            )

        )


        # ====================================================
        # BUILD ROOT CAUSES
        # ====================================================

        root_causes = []


        for group in contributing_groups:

            root_causes.append({

                "root_cause_type": "group_factor",

                "factor": group.get(

                    "factor"

                ),

                "group": group.get(

                    "group"

                ),

                "affected_percentage": group.get(

                    "affected_percentage"

                ),

                "evidence": (

                    f"{group.get('group')} in "

                    f"{group.get('factor')} has "

                    f"{group.get('affected_percentage')}% "

                    f"low performance records."

                )

            })


        for factor in numeric_factors:

            root_causes.append({

                "root_cause_type": "numeric_difference",

                "factor": factor.get(

                    "factor"

                ),

                "difference_percent": factor.get(

                    "difference_percent"

                ),

                "evidence": (

                    f"{factor.get('factor')} shows "

                    f"{factor.get('difference_percent')}% "

                    f"difference between low-performing "

                    f"and other records."

                )

            })


        # ====================================================
        # CONFIDENCE CALCULATION
        # ====================================================

        confidence_score = 40


        if affected_records >= 100:

            confidence_score += 20


        if contributing_groups:

            confidence_score += 20


        if numeric_factors:

            confidence_score += 20


        confidence_score = min(

            confidence_score,

            100

        )


        if confidence_score >= 85:

            confidence_level = "Very High"

        elif confidence_score >= 70:

            confidence_level = "High"

        elif confidence_score >= 50:

            confidence_level = "Medium"

        else:

            confidence_level = "Low"


        # ====================================================
        # FINAL RESULT
        # ====================================================

        result.update({

            "root_cause_detected": True,

            "affected_records": affected_records,

            "affected_percentage": round(

                affected_percentage,

                2

            ),

            "contributing_groups": contributing_groups,

            "numeric_factors": numeric_factors,

            "root_causes": root_causes,

            "evidence_score": evidence_score,

            "business_impact_score": business_impact_score,

            "severity_score": severity_result.get(

                "severity_score"

            ),

            "severity": severity_result.get(

                "severity"

            ),

            "analysis_confidence": confidence_level,

            "confidence_score": confidence_score

        })


    return result