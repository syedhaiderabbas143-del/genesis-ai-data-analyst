import difflib
import numpy as np
import pandas as pd


# ============================================================
# GENESIS AI - AUTOMATED INSIGHT ENGINE
# VERSION: 1.0
# ============================================================


def _safe_number(value, default=0):
    """Safely convert values into JSON-friendly numbers."""
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _clean_number(value, decimals=2):
    """Round numeric values safely."""
    try:
        value = float(value)

        if np.isnan(value) or np.isinf(value):
            return None

        return round(value, decimals)

    except Exception:
        return None


def _resolve_column(df, requested_names):
    """
    Resolve a column dynamically using exact and fuzzy matching.
    """

    if df is None or df.empty:
        return None

    normalized_columns = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    # Exact matching
    for name in requested_names:

        normalized_name = str(name).strip().lower()

        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]

    # Partial matching
    for column in df.columns:

        column_lower = str(column).strip().lower()

        for name in requested_names:

            name_lower = str(name).strip().lower()

            if name_lower in column_lower or column_lower in name_lower:
                return column

    # Fuzzy matching
    available_columns = list(normalized_columns.keys())

    for name in requested_names:

        matches = difflib.get_close_matches(
            str(name).lower(),
            available_columns,
            n=1,
            cutoff=0.75
        )

        if matches:
            return normalized_columns[matches[0]]

    return None


def _impact_level(score):
    """Convert insight score into impact level."""

    if score >= 85:
        return "Critical"

    if score >= 70:
        return "High"

    if score >= 50:
        return "Medium"

    return "Low"


def _confidence_level(confidence):
    """Normalize confidence level."""

    confidence = str(confidence).lower()

    if confidence in ["very high", "high"]:
        return "High"

    if confidence in ["medium", "moderate"]:
        return "Medium"

    return "Low"


def _calculate_insight_score(
    severity_score=50,
    population_score=0,
    financial_score=0,
    confidence_score=50
):
    """
    Professional weighted scoring system.

    Weights:
    Severity       = 35%
    Population     = 25%
    Financial      = 25%
    Confidence     = 15%
    """

    score = (
        severity_score * 0.35
        + population_score * 0.25
        + financial_score * 0.25
        + confidence_score * 0.15
    )

    return round(min(max(score, 0), 100), 2)


def _create_insight(
    category,
    title,
    description,
    business_impact,
    recommendation,
    score,
    confidence="Medium",
    evidence=None,
    affected_records=None,
    affected_percent=None,
    financial_impact=None,
    source="automated_analysis"
):
    """Create standardized insight object."""

    return {
        "category": category,
        "title": title,
        "description": description,
        "business_impact": business_impact,
        "recommendation": recommendation,
        "impact_level": _impact_level(score),
        "confidence": _confidence_level(confidence),
        "score": round(float(score), 2),
        "evidence": evidence or description,
        "affected_records": affected_records,
        "affected_percent": (
            round(float(affected_percent), 2)
            if affected_percent is not None
            else None
        ),
        "financial_impact": (
            round(float(financial_impact), 2)
            if financial_impact is not None
            else None
        ),
        "source": source
    }


# ============================================================
# NUMERIC INSIGHT ANALYSIS
# ============================================================

def _analyze_numeric_columns(df):
    """Generate insights from numeric columns."""

    insights = []

    numeric_columns = df.select_dtypes(
        include=[np.number]
    ).columns.tolist()

    for column in numeric_columns:

        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(series) < 3:
            continue

        mean_value = series.mean()
        median_value = series.median()
        std_value = series.std()

        # ----------------------------------------------------
        # HIGH VARIABILITY
        # ----------------------------------------------------

        if mean_value != 0:

            coefficient_variation = abs(
                std_value / mean_value
            ) * 100

            if coefficient_variation >= 100:

                score = _calculate_insight_score(
                    severity_score=80,
                    population_score=70,
                    financial_score=50,
                    confidence_score=80
                )

                insights.append(
                    _create_insight(
                        category="data_variability",
                        title=f"High Variability Detected in {column}",
                        description=(
                            f"{column} has a high level of variation "
                            f"across the dataset."
                        ),
                        business_impact=(
                            "Large variation may indicate inconsistent "
                            "performance, unstable operations or "
                            "significant differences between records."
                        ),
                        recommendation=(
                            f"Investigate the main drivers causing "
                            f"variation in {column}."
                        ),
                        score=score,
                        confidence="High",
                        evidence=(
                            f"Mean: {_clean_number(mean_value)}, "
                            f"Standard Deviation: {_clean_number(std_value)}, "
                            f"Variation: {_clean_number(coefficient_variation)}%"
                        ),
                        source="numeric_analysis"
                    )
                )

        # ----------------------------------------------------
        # MEAN VS MEDIAN SKEW
        # ----------------------------------------------------

        if median_value != 0:

            difference_percent = (
                abs(mean_value - median_value)
                / abs(median_value)
            ) * 100

            if difference_percent >= 25:

                score = _calculate_insight_score(
                    severity_score=60,
                    population_score=50,
                    financial_score=45,
                    confidence_score=75
                )

                insights.append(
                    _create_insight(
                        category="distribution_pattern",
                        title=f"Skewed Distribution in {column}",
                        description=(
                            f"The mean and median of {column} "
                            f"show a significant difference."
                        ),
                        business_impact=(
                            "A skewed distribution may indicate "
                            "outliers or uneven performance patterns."
                        ),
                        recommendation=(
                            f"Review extreme values and outliers "
                            f"in {column}."
                        ),
                        score=score,
                        confidence="High",
                        evidence=(
                            f"Mean: {_clean_number(mean_value)}, "
                            f"Median: {_clean_number(median_value)}, "
                            f"Difference: {_clean_number(difference_percent)}%"
                        ),
                        source="distribution_analysis"
                    )
                )

    return insights


# ============================================================
# MISSING DATA INSIGHTS
# ============================================================

def _analyze_missing_data(df):
    """Detect important missing data patterns."""

    insights = []

    total_rows = len(df)

    if total_rows == 0:
        return insights

    missing_counts = df.isna().sum()

    for column, missing_count in missing_counts.items():

        if missing_count <= 0:
            continue

        missing_percent = (
            missing_count / total_rows
        ) * 100

        if missing_percent >= 5:

            severity = 60

            if missing_percent >= 25:
                severity = 90

            elif missing_percent >= 15:
                severity = 75

            score = _calculate_insight_score(
                severity_score=severity,
                population_score=min(missing_percent * 2, 100),
                financial_score=40,
                confidence_score=90
            )

            insights.append(
                _create_insight(
                    category="data_quality",
                    title=f"Missing Data in {column}",
                    description=(
                        f"{missing_count} records have missing values "
                        f"in {column}."
                    ),
                    business_impact=(
                        "Missing information can reduce analytical "
                        "accuracy and affect business decisions."
                    ),
                    recommendation=(
                        f"Review the source and improve data "
                        f"collection for {column}."
                    ),
                    score=score,
                    confidence="High",
                    evidence=(
                        f"{missing_count} out of {total_rows} records "
                        f"({round(missing_percent, 2)}%) are missing."
                    ),
                    affected_records=int(missing_count),
                    affected_percent=missing_percent,
                    source="data_quality_analysis"
                )
            )

    return insights


# ============================================================
# DUPLICATE DATA INSIGHTS
# ============================================================

def _analyze_duplicates(df):
    """Detect duplicate records."""

    insights = []

    total_rows = len(df)

    if total_rows == 0:
        return insights

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count <= 0:
        return insights

    duplicate_percent = (
        duplicate_count / total_rows
    ) * 100

    severity = 55

    if duplicate_percent >= 20:
        severity = 90

    elif duplicate_percent >= 10:
        severity = 75

    score = _calculate_insight_score(
        severity_score=severity,
        population_score=min(
            duplicate_percent * 3,
            100
        ),
        financial_score=45,
        confidence_score=95
    )

    insights.append(
        _create_insight(
            category="data_quality",
            title="Duplicate Records Detected",
            description=(
                f"{duplicate_count} duplicate records were detected "
                f"in the dataset."
            ),
            business_impact=(
                "Duplicate records can distort totals, averages, "
                "counts and business reporting."
            ),
            recommendation=(
                "Review duplicate records and apply appropriate "
                "deduplication rules."
            ),
            score=score,
            confidence="High",
            evidence=(
                f"{duplicate_count} out of {total_rows} records "
                f"({round(duplicate_percent, 2)}%) are duplicates."
            ),
            affected_records=duplicate_count,
            affected_percent=duplicate_percent,
            source="duplicate_analysis"
        )
    )

    return insights


# ============================================================
# OUTLIER INSIGHTS
# ============================================================

def _analyze_outliers(df):
    """Detect statistical outliers using the IQR method."""

    insights = []

    numeric_columns = df.select_dtypes(
        include=[np.number]
    ).columns.tolist()

    total_rows = len(df)

    if total_rows == 0:
        return insights

    for column in numeric_columns:

        series = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(series) < 10:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = series[
            (series < lower_bound)
            | (series > upper_bound)
        ]

        outlier_count = len(outliers)

        if outlier_count == 0:
            continue

        outlier_percent = (
            outlier_count / len(series)
        ) * 100

        # Ignore very small outlier populations
        if outlier_percent < 1:
            continue

        severity = 55

        if outlier_percent >= 15:
            severity = 85

        elif outlier_percent >= 8:
            severity = 70

        score = _calculate_insight_score(
            severity_score=severity,
            population_score=min(
                outlier_percent * 4,
                100
            ),
            financial_score=50,
            confidence_score=85
        )

        insights.append(
            _create_insight(
                category="outlier_detection",
                title=f"Significant Outliers in {column}",
                description=(
                    f"{outlier_count} potential outliers were "
                    f"detected in {column}."
                ),
                business_impact=(
                    "Extreme values may indicate unusual business "
                    "events, data errors or important exceptional cases."
                ),
                recommendation=(
                    f"Review extreme values in {column} and determine "
                    f"whether they represent valid business events "
                    f"or data quality issues."
                ),
                score=score,
                confidence="High",
                evidence=(
                    f"IQR Method detected {outlier_count} outliers "
                    f"({round(outlier_percent, 2)}%). "
                    f"Expected range: "
                    f"{_clean_number(lower_bound)} to "
                    f"{_clean_number(upper_bound)}."
                ),
                affected_records=int(outlier_count),
                affected_percent=outlier_percent,
                source="outlier_analysis"
            )
        )

    return insights


# ============================================================
# CORRELATION INSIGHTS
# ============================================================

def _analyze_correlations(df):
    """Automatically discover strong numeric relationships."""

    insights = []

    numeric_df = df.select_dtypes(
        include=[np.number]
    )

    if numeric_df.shape[1] < 2:
        return insights

    correlation_matrix = numeric_df.corr(
        method="pearson"
    )

    processed_pairs = set()

    for column_1 in correlation_matrix.columns:

        for column_2 in correlation_matrix.columns:

            if column_1 == column_2:
                continue

            pair = tuple(
                sorted([
                    str(column_1),
                    str(column_2)
                ])
            )

            if pair in processed_pairs:
                continue

            processed_pairs.add(pair)

            correlation = correlation_matrix.loc[
                column_1,
                column_2
            ]

            if pd.isna(correlation):
                continue

            absolute_correlation = abs(
                correlation
            )

            # Strong relationship threshold
            if absolute_correlation < 0.65:
                continue

            if absolute_correlation >= 0.85:

                severity = 90

            elif absolute_correlation >= 0.75:

                severity = 75

            else:

                severity = 60

            direction = (
                "positive"
                if correlation > 0
                else "negative"
            )

            score = _calculate_insight_score(
                severity_score=severity,
                population_score=70,
                financial_score=70,
                confidence_score=95
            )

            insights.append(
                _create_insight(
                    category="correlation",
                    title=(
                        f"Strong {direction.title()} Relationship "
                        f"Between {column_1} and {column_2}"
                    ),
                    description=(
                        f"{column_1} and {column_2} have a "
                        f"{direction} correlation of "
                        f"{round(float(correlation), 4)}."
                    ),
                    business_impact=(
                        "This relationship may represent an important "
                        "business driver or performance pattern."
                    ),
                    recommendation=(
                        "Investigate the business relationship and "
                        "consider the variables during planning and "
                        "performance analysis."
                    ),
                    score=score,
                    confidence="High",
                    evidence=(
                        f"Pearson correlation: "
                        f"{round(float(correlation), 4)}"
                    ),
                    source="correlation_analysis"
                )
            )

    return insights


# ============================================================
# BUSINESS FINANCIAL INSIGHTS
# ============================================================

def _analyze_business_financials(df):
    """Generate financial and profitability insights dynamically."""

    insights = []

    revenue_column = _resolve_column(
        df,
        [
            "revenue",
            "sales",
            "income",
            "total revenue"
        ]
    )

    expense_column = _resolve_column(
        df,
        [
            "expenses",
            "expense",
            "cost",
            "costs",
            "total expenses"
        ]
    )

    profit_column = _resolve_column(
        df,
        [
            "profit",
            "net profit",
            "earnings"
        ]
    )

    total_rows = len(df)

    # --------------------------------------------------------
    # NEGATIVE PROFIT
    # --------------------------------------------------------

    if profit_column is not None:

        profit_series = pd.to_numeric(
            df[profit_column],
            errors="coerce"
        )

        valid_profit = profit_series.dropna()

        if len(valid_profit) > 0:

            negative_profit = valid_profit[
                valid_profit < 0
            ]

            negative_count = len(
                negative_profit
            )

            if negative_count > 0:

                negative_percent = (
                    negative_count
                    / len(valid_profit)
                ) * 100

                loss_exposure = abs(
                    negative_profit.sum()
                )

                severity = 60

                if negative_percent >= 30:
                    severity = 95

                elif negative_percent >= 20:
                    severity = 85

                elif negative_percent >= 10:
                    severity = 70

                financial_score = min(
                    (
                        loss_exposure
                        / max(
                            abs(valid_profit.sum()),
                            1
                        )
                    ) * 100,
                    100
                )

                score = _calculate_insight_score(
                    severity_score=severity,
                    population_score=min(
                        negative_percent * 3,
                        100
                    ),
                    financial_score=financial_score,
                    confidence_score=95
                )

                insights.append(
                    _create_insight(
                        category="profitability",
                        title="Negative Profit Records Detected",
                        description=(
                            f"{negative_count} records have negative "
                            f"{profit_column}."
                        ),
                        business_impact=(
                            "Loss-making records directly reduce "
                            "overall business profitability."
                        ),
                        recommendation=(
                            "Identify high-loss records and investigate "
                            "their revenue, cost and operational drivers."
                        ),
                        score=score,
                        confidence="High",
                        evidence=(
                            f"{round(negative_percent, 2)}% of valid "
                            f"records have negative {profit_column}. "
                            f"Estimated loss exposure: "
                            f"{round(loss_exposure, 2)}."
                        ),
                        affected_records=int(negative_count),
                        affected_percent=negative_percent,
                        financial_impact=loss_exposure,
                        source="financial_analysis"
                    )
                )

    # --------------------------------------------------------
    # HIGH EXPENSE RATIO
    # --------------------------------------------------------

    if (
        revenue_column is not None
        and expense_column is not None
    ):

        revenue = pd.to_numeric(
            df[revenue_column],
            errors="coerce"
        )

        expenses = pd.to_numeric(
            df[expense_column],
            errors="coerce"
        )

        valid_mask = (
            revenue.notna()
            & expenses.notna()
            & (revenue > 0)
        )

        if valid_mask.sum() > 0:

            expense_ratio = (
                expenses[valid_mask]
                / revenue[valid_mask]
            ) * 100

            high_expense_mask = (
                expense_ratio >= 80
            )

            high_expense_count = int(
                high_expense_mask.sum()
            )

            if high_expense_count > 0:

                high_expense_percent = (
                    high_expense_count
                    / valid_mask.sum()
                ) * 100

                high_expense_values = expenses[
                    valid_mask
                ][high_expense_mask]

                exposure = float(
                    high_expense_values.sum()
                )

                severity = 60

                if high_expense_percent >= 30:
                    severity = 95

                elif high_expense_percent >= 20:
                    severity = 80

                elif high_expense_percent >= 10:
                    severity = 70

                score = _calculate_insight_score(
                    severity_score=severity,
                    population_score=min(
                        high_expense_percent * 3,
                        100
                    ),
                    financial_score=90,
                    confidence_score=95
                )

                insights.append(
                    _create_insight(
                        category="expense_management",
                        title="High Expense Ratio Detected",
                        description=(
                            f"{high_expense_count} records have "
                            f"{expense_column} greater than or equal "
                            f"to 80% of {revenue_column}."
                        ),
                        business_impact=(
                            "High expense ratios can significantly "
                            "reduce profitability and operating margins."
                        ),
                        recommendation=(
                            "Analyze high-expense records and identify "
                            "cost reduction opportunities."
                        ),
                        score=score,
                        confidence="High",
                        evidence=(
                            f"{round(high_expense_percent, 2)}% of "
                            f"valid records have an expense ratio "
                            f"above 80%."
                        ),
                        affected_records=high_expense_count,
                        affected_percent=high_expense_percent,
                        financial_impact=exposure,
                        source="financial_analysis"
                    )
                )

    return insights


# ============================================================
# CATEGORICAL INSIGHTS
# ============================================================

def _analyze_categorical_columns(df):
    """Detect significant categorical concentration patterns."""

    insights = []

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    total_rows = len(df)

    if total_rows == 0:
        return insights

    for column in categorical_columns:

        series = df[column].dropna()

        if len(series) < 5:
            continue

        value_counts = series.value_counts()

        if len(value_counts) == 0:
            continue

        top_category = value_counts.index[0]
        top_count = value_counts.iloc[0]

        top_percent = (
            top_count / len(series)
        ) * 100

        # High concentration threshold
        if top_percent < 60:
            continue

        severity = 55

        if top_percent >= 85:
            severity = 90

        elif top_percent >= 75:
            severity = 75

        score = _calculate_insight_score(
            severity_score=severity,
            population_score=min(
                top_percent,
                100
            ),
            financial_score=35,
            confidence_score=90
        )

        insights.append(
            _create_insight(
                category="categorical_pattern",
                title=f"High Concentration in {column}",
                description=(
                    f"{top_percent:.2f}% of records belong to "
                    f"'{top_category}'."
                ),
                business_impact=(
                    "High concentration may indicate dependency on "
                    "a single category, segment or business group."
                ),
                recommendation=(
                    f"Review whether dependence on '{top_category}' "
                    f"in {column} represents a business risk."
                ),
                score=score,
                confidence="High",
                evidence=(
                    f"{top_count} out of {len(series)} valid records "
                    f"belong to '{top_category}'."
                ),
                affected_records=int(top_count),
                affected_percent=top_percent,
                source="categorical_analysis"
            )
        )

    return insights


# ============================================================
# INSIGHT DEDUPLICATION
# ============================================================

def _deduplicate_insights(insights):
    """Remove overlapping automated insights."""

    if not insights:
        return []

    unique_insights = []

    seen = set()

    for insight in insights:

        category = str(
            insight.get("category", "")
        ).lower()

        title = str(
            insight.get("title", "")
        ).lower()

        key = (
            category,
            title
        )

        if key in seen:
            continue

        seen.add(key)

        unique_insights.append(
            insight
        )

    return unique_insights


# ============================================================
# MAIN AUTOMATED INSIGHT ENGINE
# ============================================================

def generate_automated_insights(
    df,
    max_insights=20
):
    """
    Genesis AI Automated Insight Engine.

    Automatically analyzes:
    - Financial patterns
    - Numeric variation
    - Missing data
    - Duplicate records
    - Outliers
    - Correlations
    - Categorical patterns
    """

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        return {
            "success": False,
            "analysis_type": "genesis_ai_automated_insights_v1",
            "dataset": {
                "rows": 0,
                "columns": 0
            },
            "total_insights": 0,
            "insights": [],
            "summary": (
                "No dataset is available for automated insight analysis."
            )
        }

    total_rows = len(df)

    total_columns = len(df.columns)

    all_insights = []

    # --------------------------------------------------------
    # RUN ANALYSIS MODULES
    # --------------------------------------------------------

    try:
        all_insights.extend(
            _analyze_business_financials(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_numeric_columns(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_missing_data(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_duplicates(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_outliers(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_correlations(df)
        )
    except Exception:
        pass

    try:
        all_insights.extend(
            _analyze_categorical_columns(df)
        )
    except Exception:
        pass

    # --------------------------------------------------------
    # DEDUPLICATION
    # --------------------------------------------------------

    raw_insight_count = len(
        all_insights
    )

    all_insights = _deduplicate_insights(
        all_insights
    )

    # --------------------------------------------------------
    # SORT BY IMPORTANCE
    # --------------------------------------------------------

    all_insights = sorted(
        all_insights,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    # Limit results
    all_insights = all_insights[
        :max_insights
    ]

    # --------------------------------------------------------
    # ADD RANKING
    # --------------------------------------------------------

    for index, insight in enumerate(
        all_insights,
        start=1
    ):

        insight["rank"] = index

    # --------------------------------------------------------
    # INSIGHT SUMMARY
    # --------------------------------------------------------

    impact_summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    category_summary = {}

    for insight in all_insights:

        impact = str(
            insight.get(
                "impact_level",
                "Low"
            )
        ).lower()

        if impact in impact_summary:
            impact_summary[impact] += 1

        category = insight.get(
            "category",
            "other"
        )

        category_summary[category] = (
            category_summary.get(
                category,
                0
            )
            + 1
        )

    duplicates_removed = (
        raw_insight_count
        - len(_deduplicate_insights(all_insights))
    )

    # --------------------------------------------------------
    # TOP INSIGHT
    # --------------------------------------------------------

    if all_insights:

        top_insight = all_insights[0]

        summary = (
            f"Genesis AI automatically generated "
            f"{len(all_insights)} important business insights "
            f"from {total_rows} records and {total_columns} columns. "
            f"The highest priority insight is "
            f"'{top_insight.get('title')}' with a score of "
            f"{top_insight.get('score')}/100."
        )

    else:

        summary = (
            f"Genesis AI analyzed {total_rows} records and "
            f"{total_columns} columns but did not detect any "
            f"significant automated insights."
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,

        "analysis_type": (
            "genesis_ai_automated_insights_v1"
        ),

        "dataset": {
            "rows": total_rows,
            "columns": total_columns
        },

        "insight_generation": {
            "raw_insights_detected": raw_insight_count,
            "final_insights": len(all_insights),
            "max_insights_requested": max_insights
        },

        "impact_summary": impact_summary,

        "category_summary": category_summary,

        "total_insights": len(
            all_insights
        ),

        "insights": all_insights,

        "summary": summary,

        "disclaimer": (
            "Genesis AI Automated Insights identifies statistical "
            "patterns, anomalies and potential business signals. "
            "Insights should be validated with business context "
            "before making major decisions."
        )
    }


# ============================================================
# END OF FILE
# ============================================================