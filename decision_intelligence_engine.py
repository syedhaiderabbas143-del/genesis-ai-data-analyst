import re
import pandas as pd
import numpy as np


# ============================================================
# GENESIS AI - PROFESSIONAL DECISION INTELLIGENCE ENGINE V2
# ============================================================
#
# FEATURES:
# - Business Metrics
# - Root Cause Integration
# - Recommendation Integration
# - Anomaly Integration
# - Duplicate Decision Intelligence
# - Advanced Decision Scoring
# - Population Impact Analysis
# - Financial Impact Estimation
# - Action Plan Generation
# - Executive Decision Ranking
# - Business Health Score
#
# ============================================================


# ============================================================
# BASIC HELPERS
# ============================================================

def _find_column(df, possible_names):
    """
    Finds a column using case-insensitive matching.
    """

    if df is None or df.empty:
        return None

    normalized_columns = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:
        key = str(name).strip().lower()

        if key in normalized_columns:
            return normalized_columns[key]

    return None


def _safe_number(value, default=0.0):
    """
    Safely converts a value into float.
    """

    try:
        if value is None:
            return default

        if pd.isna(value):
            return default

        value = float(value)

        if np.isinf(value):
            return default

        return value

    except Exception:
        return default


def _safe_percent(value, default=0.0):
    """
    Ensures percentage remains between 0 and 100.
    """

    value = _safe_number(value, default)

    return max(0.0, min(100.0, value))


# ============================================================
# PRIORITY / CONFIDENCE / IMPACT SCORING
# ============================================================

def _priority_score(priority):

    scores = {
        "critical": 100,
        "high": 75,
        "medium": 50,
        "low": 25
    }

    return scores.get(
        str(priority).strip().lower(),
        10
    )


def _confidence_score(confidence):

    scores = {
        "very_high": 100,
        "high": 85,
        "medium": 60,
        "low": 35,
        "very_low": 15
    }

    confidence = (
        str(confidence)
        .strip()
        .lower()
        .replace(" ", "_")
    )

    return scores.get(confidence, 50)


def _impact_score(impact):

    scores = {
        "very_high": 100,
        "high": 80,
        "medium": 55,
        "low": 30,
        "very_low": 15
    }

    impact = (
        str(impact)
        .strip()
        .lower()
        .replace(" ", "_")
    )

    return scores.get(impact, 50)


def _risk_level(score):

    score = _safe_number(score)

    if score >= 85:
        return "Critical"

    if score >= 70:
        return "High"

    if score >= 45:
        return "Medium"

    return "Low"


def _impact_level(score):

    score = _safe_number(score)

    if score >= 85:
        return "Very High"

    if score >= 70:
        return "High"

    if score >= 45:
        return "Medium"

    return "Low"


def _priority_from_score(score):

    score = _safe_number(score)

    if score >= 85:
        return "critical"

    if score >= 70:
        return "high"

    if score >= 45:
        return "medium"

    return "low"


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize_text(value):
    """
    Converts text into normalized form for duplicate detection.
    """

    if value is None:
        return ""

    text = str(value).lower().strip()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    words = text.split()

    stop_words = {
        "business",
        "decision",
        "analysis",
        "program",
        "case",
        "cases",
        "record",
        "records",
        "reduce",
        "control",
        "improve",
        "investigate",
        "the",
        "and",
        "of",
        "for",
        "to"
    }

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    return " ".join(sorted(set(words)))


def _keyword_set(value):

    normalized = _normalize_text(value)

    if not normalized:
        return set()

    return set(normalized.split())


def _similarity_score(text_a, text_b):
    """
    Calculates keyword similarity.
    """

    words_a = _keyword_set(text_a)
    words_b = _keyword_set(text_b)

    if not words_a or not words_b:
        return 0.0

    intersection = words_a.intersection(words_b)
    union = words_a.union(words_b)

    if not union:
        return 0.0

    return round(
        (len(intersection) / len(union)) * 100,
        2
    )


# ============================================================
# ISSUE / CATEGORY INTELLIGENCE
# ============================================================

def _issue_family(item):
    """
    Identifies broad business issue family.
    """

    category = str(
        item.get("category", "")
    ).lower()

    title = str(
        item.get("title", "")
    ).lower()

    evidence = str(
        item.get("evidence", "")
    ).lower()

    action = str(
        item.get("recommended_action", "")
    ).lower()

    combined = (
        category
        + " "
        + title
        + " "
        + evidence
        + " "
        + action
    )

    if (
        "negative profit" in combined
        or "loss-making" in combined
        or "loss making" in combined
        or "profitability" in combined
    ):
        return "profitability"

    if (
        "expense" in combined
        or "cost" in combined
        or "high cost" in combined
    ):
        return "expense_management"

    if (
        "revenue" in combined
        or "sales revenue" in combined
    ):
        return "revenue_growth"

    if (
        "performance" in combined
        or "rating" in combined
        or "productivity" in combined
    ):
        return "performance"

    if (
        "department" in combined
    ):
        return "department_analysis"

    if (
        "branch" in combined
    ):
        return "branch_analysis"

    if (
        "project" in combined
    ):
        return "project_analysis"

    if (
        "city" in combined
        or "region" in combined
        or "location" in combined
    ):
        return "location_analysis"

    if (
        "anomaly" in combined
        or "outlier" in combined
    ):
        return "business_anomaly"

    return category or "business_analysis"


# ============================================================
# POPULATION IMPACT EXTRACTION
# ============================================================

def _extract_population_impact(item, total_rows):

    if total_rows <= 0:
        return {
            "affected_records": None,
            "affected_percent": 0.0
        }

    affected_records = None
    affected_percent = 0.0

    text_fields = [
        item.get("evidence", ""),
        item.get("business_impact", ""),
        item.get("message", "")
    ]

    combined_text = " ".join(
        str(text)
        for text in text_fields
        if text is not None
    )

    # Example:
    # 2588 records (25.88%)
    match = re.search(
        r"([\d,]+)\s+records?\s*\(\s*([\d.]+)\s*%\s*\)",
        combined_text,
        re.IGNORECASE
    )

    if match:

        try:
            affected_records = int(
                match.group(1).replace(",", "")
            )

        except Exception:
            affected_records = None

        affected_percent = _safe_percent(
            match.group(2)
        )

        return {
            "affected_records": affected_records,
            "affected_percent": affected_percent
        }

    # Only percentage available
    match = re.search(
        r"([\d.]+)\s*%",
        combined_text
    )

    if match:

        affected_percent = _safe_percent(
            match.group(1)
        )

        affected_records = int(
            round(
                total_rows
                * affected_percent
                / 100
            )
        )

    return {
        "affected_records": affected_records,
        "affected_percent": affected_percent
    }


# ============================================================
# BUSINESS METRICS
# ============================================================

def calculate_business_metrics(df):

    metrics = {}

    if df is None or df.empty:
        return metrics

    revenue_col = _find_column(
        df,
        [
            "Revenue",
            "Total Revenue",
            "Sales Revenue",
            "Sales"
        ]
    )

    expenses_col = _find_column(
        df,
        [
            "Expenses",
            "Expense",
            "Total Expenses",
            "Cost",
            "Costs"
        ]
    )

    profit_col = _find_column(
        df,
        [
            "Profit",
            "Net Profit",
            "Total Profit"
        ]
    )

    salary_col = _find_column(
        df,
        [
            "Salary",
            "Annual Salary"
        ]
    )

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    if revenue_col:

        revenue_series = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        )

        metrics["total_revenue"] = round(
            _safe_number(revenue_series.sum()),
            2
        )

        metrics["average_revenue"] = round(
            _safe_number(revenue_series.mean()),
            2
        )

    # --------------------------------------------------------
    # EXPENSES
    # --------------------------------------------------------

    if expenses_col:

        expenses_series = pd.to_numeric(
            df[expenses_col],
            errors="coerce"
        )

        metrics["total_expenses"] = round(
            _safe_number(expenses_series.sum()),
            2
        )

        metrics["average_expenses"] = round(
            _safe_number(expenses_series.mean()),
            2
        )

    # --------------------------------------------------------
    # PROFIT
    # --------------------------------------------------------

    if profit_col:

        profit_series = pd.to_numeric(
            df[profit_col],
            errors="coerce"
        )

        metrics["total_profit"] = round(
            _safe_number(profit_series.sum()),
            2
        )

        metrics["average_profit"] = round(
            _safe_number(profit_series.mean()),
            2
        )

        negative_profit_records = int(
            (profit_series < 0).sum()
        )

        valid_profit_records = int(
            profit_series.notna().sum()
        )

        negative_profit_percent = 0.0

        if valid_profit_records > 0:

            negative_profit_percent = round(
                (
                    negative_profit_records
                    / valid_profit_records
                ) * 100,
                2
            )

        metrics[
            "negative_profit_records"
        ] = negative_profit_records

        metrics[
            "negative_profit_percent"
        ] = negative_profit_percent

        # Financial loss exposure
        negative_profit_values = profit_series[
            profit_series < 0
        ]

        if not negative_profit_values.empty:

            total_loss_exposure = abs(
                _safe_number(
                    negative_profit_values.sum()
                )
            )

        else:
            total_loss_exposure = 0.0

        metrics[
            "total_loss_exposure"
        ] = round(
            total_loss_exposure,
            2
        )

    # --------------------------------------------------------
    # PROFIT MARGIN
    # --------------------------------------------------------

    if (
        "total_revenue" in metrics
        and "total_profit" in metrics
        and metrics["total_revenue"] != 0
    ):

        metrics[
            "profit_margin_percent"
        ] = round(
            (
                metrics["total_profit"]
                / metrics["total_revenue"]
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # EXPENSE RATIO
    # --------------------------------------------------------

    if (
        "total_revenue" in metrics
        and "total_expenses" in metrics
        and metrics["total_revenue"] != 0
    ):

        metrics[
            "expense_ratio_percent"
        ] = round(
            (
                metrics["total_expenses"]
                / metrics["total_revenue"]
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # SALARY
    # --------------------------------------------------------

    if salary_col:

        salary_series = pd.to_numeric(
            df[salary_col],
            errors="coerce"
        )

        metrics[
            "average_salary"
        ] = round(
            _safe_number(
                salary_series.mean()
            ),
            2
        )

    return metrics


# ============================================================
# CREATE RAW DECISION PRIORITIES
# ============================================================

def generate_raw_priorities(
    anomalies=None,
    recommendations=None,
    root_causes=None
):

    priorities = []

    anomalies = anomalies or []
    recommendations = recommendations or []
    root_causes = root_causes or []

    # --------------------------------------------------------
    # ROOT CAUSES
    # --------------------------------------------------------

    for item in root_causes:

        priority = str(
            item.get(
                "severity",
                item.get(
                    "priority",
                    "medium"
                )
            )
        ).lower()

        confidence = str(
            item.get(
                "confidence",
                "medium"
            )
        ).lower()

        priorities.append(
            {
                "source": "root_cause",

                "title": item.get(
                    "title",
                    "Business Root Cause"
                ),

                "category": item.get(
                    "category",
                    "business_analysis"
                ),

                "priority": priority,

                "confidence": confidence,

                "business_impact": item.get(
                    "business_impact",
                    ""
                ),

                "evidence": item.get(
                    "evidence",
                    ""
                ),

                "recommended_action": item.get(
                    "recommendation",
                    item.get(
                        "recommended_action",
                        ""
                    )
                )
            }
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    for item in recommendations:

        priority = str(
            item.get(
                "priority",
                "medium"
            )
        ).lower()

        expected_impact = str(
            item.get(
                "expected_impact",
                "medium"
            )
        ).lower()

        priorities.append(
            {
                "source": "recommendation",

                "title": item.get(
                    "title",
                    "Business Recommendation"
                ),

                "category": item.get(
                    "category",
                    "business_strategy"
                ),

                "priority": priority,

                "confidence": item.get(
                    "confidence",
                    "medium"
                ),

                "expected_impact": expected_impact,

                "business_impact": (
                    f"Expected impact: {expected_impact}"
                ),

                "evidence": item.get(
                    "message",
                    item.get(
                        "evidence",
                        ""
                    )
                ),

                "recommended_action": item.get(
                    "recommended_action",
                    item.get(
                        "recommendation",
                        ""
                    )
                )
            }
        )

    # --------------------------------------------------------
    # ANOMALIES
    # --------------------------------------------------------

    for item in anomalies:

        priority = str(
            item.get(
                "priority",
                "medium"
            )
        ).lower()

        category = item.get(
            "category",
            "business_anomaly"
        )

        title = item.get(
            "title",
            str(category)
            .replace("_", " ")
            .title()
        )

        priorities.append(
            {
                "source": "anomaly",

                "title": title,

                "category": category,

                "priority": priority,

                "confidence": item.get(
                    "confidence",
                    "high"
                ),

                "business_impact": item.get(
                    "message",
                    item.get(
                        "business_impact",
                        ""
                    )
                ),

                "evidence": item.get(
                    "message",
                    item.get(
                        "evidence",
                        ""
                    )
                ),

                "recommended_action": item.get(
                    "recommendation",
                    item.get(
                        "recommended_action",
                        ""
                    )
                )
            }
        )

    return priorities


# ============================================================
# DUPLICATE DECISION INTELLIGENCE
# ============================================================

def _are_related_issues(item_a, item_b):

    family_a = _issue_family(item_a)
    family_b = _issue_family(item_b)

    if family_a == family_b:

        return True

    category_a = str(
        item_a.get("category", "")
    ).lower()

    category_b = str(
        item_b.get("category", "")
    ).lower()

    if (
        category_a
        and category_b
        and category_a == category_b
    ):

        return True

    title_similarity = _similarity_score(
        item_a.get("title", ""),
        item_b.get("title", "")
    )

    evidence_similarity = _similarity_score(
        item_a.get("evidence", ""),
        item_b.get("evidence", "")
    )

    if title_similarity >= 60:
        return True

    if evidence_similarity >= 65:
        return True

    return False


def _merge_priority_group(items):

    if not items:
        return None

    sorted_items = sorted(
        items,
        key=lambda x: (
            _priority_score(
                x.get("priority", "medium")
            ),
            _confidence_score(
                x.get("confidence", "medium")
            )
        ),
        reverse=True
    )

    primary = sorted_items[0].copy()

    sources = []

    evidence_list = []

    action_list = []

    categories = []

    for item in sorted_items:

        source = item.get("source")

        if source and source not in sources:
            sources.append(source)

        evidence = str(
            item.get("evidence", "")
        ).strip()

        if evidence and evidence not in evidence_list:
            evidence_list.append(evidence)

        action = str(
            item.get(
                "recommended_action",
                ""
            )
        ).strip()

        if action and action not in action_list:
            action_list.append(action)

        category = item.get("category")

        if category and category not in categories:
            categories.append(category)

    primary["source"] = (
        " + ".join(sources)
        if sources
        else primary.get("source")
    )

    primary["merged_sources"] = sources

    primary["related_categories"] = categories

    primary["merged_issue_count"] = len(items)

    primary["duplicate_merged"] = (
        len(items) > 1
    )

    if evidence_list:

        primary["evidence"] = " | ".join(
            evidence_list[:3]
        )

    if action_list:

        primary["recommended_action"] = " | ".join(
            action_list[:3]
        )

    return primary


def remove_duplicate_priorities(priorities):

    if not priorities:

        return [], 0

    groups = []

    for item in priorities:

        matched_group = None

        for group in groups:

            if _are_related_issues(
                item,
                group[0]
            ):

                matched_group = group

                break

        if matched_group is not None:

            matched_group.append(item)

        else:

            groups.append([item])

    cleaned_priorities = []

    for group in groups:

        merged_item = _merge_priority_group(group)

        if merged_item:

            cleaned_priorities.append(
                merged_item
            )

    duplicates_removed = (
        len(priorities)
        - len(cleaned_priorities)
    )

    return (
        cleaned_priorities,
        duplicates_removed
    )


# ============================================================
# FINANCIAL IMPACT INTELLIGENCE
# ============================================================

def calculate_financial_impact(
    item,
    business_metrics,
    total_rows
):

    family = _issue_family(item)

    total_revenue = _safe_number(
        business_metrics.get(
            "total_revenue",
            0
        )
    )

    total_expenses = _safe_number(
        business_metrics.get(
            "total_expenses",
            0
        )
    )

    total_profit = _safe_number(
        business_metrics.get(
            "total_profit",
            0
        )
    )

    total_loss_exposure = _safe_number(
        business_metrics.get(
            "total_loss_exposure",
            0
        )
    )

    population = _extract_population_impact(
        item,
        total_rows
    )

    affected_percent = population.get(
        "affected_percent",
        0
    )

    financial_exposure = 0.0
    estimated_opportunity = 0.0

    # --------------------------------------------------------
    # PROFITABILITY
    # --------------------------------------------------------

    if family == "profitability":

        financial_exposure = total_loss_exposure

        estimated_opportunity = (
            total_loss_exposure * 0.30
        )

        if (
            financial_exposure == 0
            and affected_percent > 0
        ):

            financial_exposure = abs(
                total_profit
                * affected_percent
                / 100
            )

            estimated_opportunity = (
                financial_exposure * 0.25
            )

    # --------------------------------------------------------
    # EXPENSE MANAGEMENT
    # --------------------------------------------------------

    elif family == "expense_management":

        if affected_percent > 0:

            financial_exposure = (
                total_expenses
                * affected_percent
                / 100
            )

        else:

            financial_exposure = (
                total_expenses * 0.15
            )

        estimated_opportunity = (
            financial_exposure * 0.10
        )

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    elif family == "revenue_growth":

        financial_exposure = (
            total_revenue * 0.10
        )

        estimated_opportunity = (
            total_revenue * 0.05
        )

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    elif family == "performance":

        if affected_percent > 0:

            financial_exposure = (
                total_revenue
                * affected_percent
                / 100
                * 0.10
            )

        else:

            financial_exposure = (
                total_revenue * 0.05
            )

        estimated_opportunity = (
            financial_exposure * 0.20
        )

    # --------------------------------------------------------
    # OTHER ISSUES
    # --------------------------------------------------------

    else:

        financial_exposure = (
            abs(total_profit) * 0.05
        )

        estimated_opportunity = (
            financial_exposure * 0.15
        )

    # Exposure Score
    exposure_reference = max(
        abs(total_revenue),
        abs(total_expenses),
        abs(total_profit),
        1
    )

    exposure_percent = (
        financial_exposure
        / exposure_reference
    ) * 100

    financial_impact_score = min(
        100,
        max(
            0,
            exposure_percent * 5
        )
    )

    return {

        "issue_family": family,

        "affected_records": (
            population.get(
                "affected_records"
            )
        ),

        "affected_percent": round(
            affected_percent,
            2
        ),

        "financial_exposure": round(
            financial_exposure,
            2
        ),

        "estimated_opportunity": round(
            estimated_opportunity,
            2
        ),

        "financial_impact_score": round(
            financial_impact_score,
            2
        )
    }


# ============================================================
# ADVANCED DECISION SCORING
# ============================================================

def calculate_advanced_priority_score(
    item,
    business_metrics,
    total_rows
):

    priority_score = _priority_score(
        item.get(
            "priority",
            "medium"
        )
    )

    confidence_score = _confidence_score(
        item.get(
            "confidence",
            "medium"
        )
    )

    expected_impact = item.get(
        "expected_impact",
        "medium"
    )

    impact_score = _impact_score(
        expected_impact
    )

    financial_impact = calculate_financial_impact(
        item,
        business_metrics,
        total_rows
    )

    population_percent = (
        financial_impact.get(
            "affected_percent",
            0
        )
    )

    # Population impact score
    if population_percent >= 50:
        population_score = 100

    elif population_percent >= 30:
        population_score = 80

    elif population_percent >= 15:
        population_score = 60

    elif population_percent >= 5:
        population_score = 40

    elif population_percent > 0:
        population_score = 20

    else:
        population_score = 35

    financial_score = (
        financial_impact.get(
            "financial_impact_score",
            0
        )
    )

    # --------------------------------------------------------
    # FINAL WEIGHTED SCORE
    # --------------------------------------------------------

    final_score = (

        priority_score * 0.35

        + impact_score * 0.20

        + confidence_score * 0.15

        + population_score * 0.15

        + financial_score * 0.15
    )

    final_score = min(
        100,
        max(
            0,
            final_score
        )
    )

    return {

        "final_score": round(
            final_score,
            2
        ),

        "priority_score": round(
            priority_score,
            2
        ),

        "confidence_score": round(
            confidence_score,
            2
        ),

        "impact_score": round(
            impact_score,
            2
        ),

        "population_score": round(
            population_score,
            2
        ),

        "financial_score": round(
            financial_score,
            2
        ),

        "financial_impact": financial_impact
    }


# ============================================================
# ACTION PLAN GENERATOR
# ============================================================

def generate_action_plan(item):

    family = _issue_family(item)

    title = item.get(
        "title",
        "Business Issue"
    )

    action = item.get(
        "recommended_action",
        ""
    )

    if family == "profitability":

        return {

            "immediate_action": (
                "Identify the highest loss-making records "
                "and investigate their revenue and expense patterns."
            ),

            "short_term_action": (
                "Prioritize high-loss segments and implement "
                "corrective pricing, cost-control or operational actions."
            ),

            "medium_term_action": (
                "Create profitability monitoring rules and "
                "track loss-making segments continuously."
            ),

            "strategic_action": (
                "Develop a long-term profitability recovery "
                "strategy based on margin optimization and "
                "business segment performance."
            )
        }

    if family == "expense_management":

        return {

            "immediate_action": (
                "Identify records and segments with the "
                "highest expense ratios."
            ),

            "short_term_action": (
                "Review major cost drivers and eliminate "
                "unnecessary operational expenses."
            ),

            "medium_term_action": (
                "Implement expense controls and budget "
                "monitoring thresholds."
            ),

            "strategic_action": (
                "Develop a sustainable cost optimization "
                "program across business operations."
            )
        }

    if family == "revenue_growth":

        return {

            "immediate_action": (
                "Identify the highest-performing revenue "
                "segments and growth opportunities."
            ),

            "short_term_action": (
                "Prioritize revenue growth initiatives while "
                "protecting profit margins."
            ),

            "medium_term_action": (
                "Build revenue forecasting and segment "
                "performance monitoring."
            ),

            "strategic_action": (
                "Develop a long-term sustainable revenue "
                "growth strategy."
            )
        }

    if family == "performance":

        return {

            "immediate_action": (
                "Identify low-performing individuals or "
                "business groups."
            ),

            "short_term_action": (
                "Provide targeted coaching, training and "
                "performance support."
            ),

            "medium_term_action": (
                "Introduce continuous performance monitoring "
                "and improvement plans."
            ),

            "strategic_action": (
                "Build a long-term performance development "
                "and productivity strategy."
            )
        }

    return {

        "immediate_action": (
            action
            if action
            else (
                f"Investigate the primary drivers behind "
                f"'{title}'."
            )
        ),

        "short_term_action": (
            "Analyze affected business segments and "
            "implement targeted corrective actions."
        ),

        "medium_term_action": (
            "Establish monitoring metrics and track "
            "improvement over time."
        ),

        "strategic_action": (
            "Integrate the findings into long-term "
            "business planning and performance management."
        )
    }


# ============================================================
# BUILD FINAL PRIORITIES
# ============================================================

def generate_decision_priorities(
    anomalies=None,
    recommendations=None,
    root_causes=None,
    business_metrics=None,
    total_rows=0
):

    business_metrics = business_metrics or {}

    raw_priorities = generate_raw_priorities(
        anomalies=anomalies,
        recommendations=recommendations,
        root_causes=root_causes
    )

    raw_priority_count = len(
        raw_priorities
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    priorities, duplicates_removed = (
        remove_duplicate_priorities(
            raw_priorities
        )
    )

    # --------------------------------------------------------
    # ADVANCED SCORING
    # --------------------------------------------------------

    final_priorities = []

    for item in priorities:

        scoring = calculate_advanced_priority_score(
            item=item,
            business_metrics=business_metrics,
            total_rows=total_rows
        )

        financial_impact = scoring.get(
            "financial_impact",
            {}
        )

        item["score"] = scoring.get(
            "final_score",
            0
        )

        item["priority"] = _priority_from_score(
            item["score"]
        )

        item["issue_family"] = (
            financial_impact.get(
                "issue_family"
            )
        )

        item["affected_records"] = (
            financial_impact.get(
                "affected_records"
            )
        )

        item["affected_percent"] = (
            financial_impact.get(
                "affected_percent",
                0
            )
        )

        item["financial_exposure"] = (
            financial_impact.get(
                "financial_exposure",
                0
            )
        )

        item["estimated_opportunity"] = (
            financial_impact.get(
                "estimated_opportunity",
                0
            )
        )

        item["scoring_breakdown"] = {

            "priority_score": scoring.get(
                "priority_score"
            ),

            "confidence_score": scoring.get(
                "confidence_score"
            ),

            "business_impact_score": scoring.get(
                "impact_score"
            ),

            "population_impact_score": scoring.get(
                "population_score"
            ),

            "financial_impact_score": scoring.get(
                "financial_score"
            )
        }

        item["action_plan"] = (
            generate_action_plan(item)
        )

        final_priorities.append(
            item
        )

    # --------------------------------------------------------
    # FINAL SORT
    # --------------------------------------------------------

    final_priorities = sorted(
        final_priorities,
        key=lambda x: (
            _safe_number(
                x.get(
                    "score",
                    0
                )
            ),
            _safe_number(
                x.get(
                    "financial_exposure",
                    0
                )
            )
        ),
        reverse=True
    )

    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    for index, item in enumerate(
        final_priorities,
        start=1
    ):

        item["rank"] = index

    metadata = {

        "raw_priorities": raw_priority_count,

        "final_priorities": len(
            final_priorities
        ),

        "duplicates_removed": (
            duplicates_removed
        )
    }

    return (
        final_priorities,
        metadata
    )


# ============================================================
# EXECUTIVE DECISION GENERATOR V2
# ============================================================

def generate_executive_decisions(
    priorities,
    business_metrics
):

    decisions = []

    if not priorities:
        return decisions

    # Maximum top 6 decisions
    top_priorities = priorities[:6]

    for item in top_priorities:

        score = _safe_number(
            item.get(
                "score",
                0
            )
        )

        action_plan = item.get(
            "action_plan",
            {}
        )

        decision = {

            "decision_id": (
                f"DEC-{len(decisions) + 1:03d}"
            ),

            "rank": (
                len(decisions) + 1
            ),

            "decision_title": item.get(
                "title",
                "Business Decision"
            ),

            "decision_category": item.get(
                "issue_family",
                item.get(
                    "category",
                    "business_analysis"
                )
            ),

            "priority": item.get(
                "priority",
                "medium"
            ),

            "decision_urgency": _risk_level(
                score
            ),

            "impact_level": _impact_level(
                score
            ),

            "decision_score": round(
                score,
                2
            ),

            "confidence": item.get(
                "confidence",
                "medium"
            ),

            "evidence": item.get(
                "evidence",
                ""
            ),

            "recommended_decision": item.get(
                "recommended_action",
                ""
            ),

            "affected_records": item.get(
                "affected_records"
            ),

            "affected_percent": item.get(
                "affected_percent",
                0
            ),

            "financial_exposure": item.get(
                "financial_exposure",
                0
            ),

            "estimated_opportunity": item.get(
                "estimated_opportunity",
                0
            ),

            "action_plan": action_plan
        }

        decisions.append(
            decision
        )

    return decisions


# ============================================================
# BUSINESS HEALTH SCORE V2
# ============================================================

def calculate_decision_score(
    priorities,
    business_metrics
):

    if not priorities:

        return {

            "business_health_score": 100,

            "overall_risk": "Low"
        }

    scores = [

        _safe_number(
            item.get(
                "score",
                0
            )
        )

        for item in priorities
    ]

    average_risk = (
        sum(scores)
        / len(scores)
        if scores
        else 0
    )

    negative_profit_percent = _safe_percent(
        business_metrics.get(
            "negative_profit_percent",
            0
        )
    )

    expense_ratio_percent = _safe_percent(
        business_metrics.get(
            "expense_ratio_percent",
            0
        )
    )

    critical_count = len(
        [

            item

            for item in priorities

            if item.get("priority")
            == "critical"
        ]
    )

    high_count = len(
        [

            item

            for item in priorities

            if item.get("priority")
            == "high"
        ]
    )

    # --------------------------------------------------------
    # RISK PENALTY
    # --------------------------------------------------------

    risk_penalty = (

        average_risk * 0.35

        + negative_profit_percent * 0.30

        + max(
            expense_ratio_percent - 60,
            0
        ) * 0.20

        + min(
            critical_count * 5,
            15
        )

        + min(
            high_count * 2,
            10
        )
    )

    health_score = max(
        0,
        min(
            100,
            100 - risk_penalty
        )
    )

    health_score = round(
        health_score,
        2
    )

    if health_score < 30:

        overall_risk = "Critical"

    elif health_score < 50:

        overall_risk = "High"

    elif health_score < 70:

        overall_risk = "Medium"

    else:

        overall_risk = "Low"

    return {

        "business_health_score": health_score,

        "overall_risk": overall_risk
    }


# ============================================================
# PRIORITY SUMMARY
# ============================================================

def generate_priority_counts(priorities):

    counts = {

        "critical": 0,

        "high": 0,

        "medium": 0,

        "low": 0
    }

    for item in priorities:

        priority = str(
            item.get(
                "priority",
                "low"
            )
        ).lower()

        if priority in counts:

            counts[priority] += 1

    return counts


# ============================================================
# FINANCIAL SUMMARY
# ============================================================

def generate_financial_summary(
    priorities,
    business_metrics
):

    total_exposure = sum(

        _safe_number(
            item.get(
                "financial_exposure",
                0
            )
        )

        for item in priorities
    )

    total_opportunity = sum(

        _safe_number(
            item.get(
                "estimated_opportunity",
                0
            )
        )

        for item in priorities
    )

    return {

        "identified_financial_exposure": round(
            total_exposure,
            2
        ),

        "estimated_improvement_opportunity": round(
            total_opportunity,
            2
        ),

        "recorded_loss_exposure": round(
            _safe_number(
                business_metrics.get(
                    "total_loss_exposure",
                    0
                )
            ),
            2
        ),

        "note": (
            "Financial estimates are directional decision-support "
            "estimates based on detected patterns and should be "
            "validated before financial planning or execution."
        )
    }


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

def generate_decision_summary(
    decisions,
    overall_risk,
    health_score,
    duplicate_metadata
):

    if not decisions:

        return (

            "Genesis AI did not identify any major "
            "business decision risks in the current dataset."
        )

    top_decision = decisions[0]

    duplicates_removed = (
        duplicate_metadata.get(
            "duplicates_removed",
            0
        )
    )

    return (

        f"Genesis AI Decision Intelligence V2 analyzed "
        f"{len(decisions)} executive decisions. "

        f"The current business health score is "
        f"{health_score}/100 with an overall risk level "
        f"of {overall_risk}. "

        f"Duplicate Intelligence removed or merged "
        f"{duplicates_removed} overlapping decision signals. "

        f"The highest priority decision is "
        f"'{top_decision.get('decision_title')}'. "

        f"Management should prioritize Critical and High "
        f"impact decisions first."
    )


# ============================================================
# MAIN GENESIS AI DECISION INTELLIGENCE ENGINE V2
# ============================================================

def generate_decision_intelligence(
    df,
    anomalies=None,
    recommendations=None,
    root_causes=None
):

    """
    MAIN GENESIS AI DECISION INTELLIGENCE ENGINE V2

    Pipeline:

    Business Metrics
        ↓
    Root Causes
        ↓
    Recommendations
        ↓
    Anomalies
        ↓
    Duplicate Intelligence
        ↓
    Advanced Decision Scoring
        ↓
    Population Impact
        ↓
    Financial Impact
        ↓
    Action Plan
        ↓
    Executive Decisions
        ↓
    Business Health Score
    """

    # --------------------------------------------------------
    # DATASET VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        return {

            "success": False,

            "message": (
                "No dataset available for "
                "decision intelligence."
            )
        }

    total_rows = int(
        len(df)
    )

    # --------------------------------------------------------
    # STEP 1
    # BUSINESS METRICS
    # --------------------------------------------------------

    business_metrics = calculate_business_metrics(
        df
    )

    # --------------------------------------------------------
    # STEP 2
    # ADVANCED DECISION PRIORITIES
    # --------------------------------------------------------

    priorities, duplicate_metadata = (
        generate_decision_priorities(

            anomalies=anomalies,

            recommendations=recommendations,

            root_causes=root_causes,

            business_metrics=business_metrics,

            total_rows=total_rows
        )
    )

    # --------------------------------------------------------
    # STEP 3
    # BUSINESS HEALTH SCORE
    # --------------------------------------------------------

    score_data = calculate_decision_score(

        priorities,

        business_metrics
    )

    business_health_score = (
        score_data.get(
            "business_health_score",
            100
        )
    )

    overall_risk = score_data.get(

        "overall_risk",

        "Low"
    )

    # --------------------------------------------------------
    # STEP 4
    # EXECUTIVE DECISIONS
    # --------------------------------------------------------

    decisions = generate_executive_decisions(

        priorities,

        business_metrics
    )

    # --------------------------------------------------------
    # STEP 5
    # PRIORITY COUNTS
    # --------------------------------------------------------

    priority_counts = generate_priority_counts(
        priorities
    )

    # --------------------------------------------------------
    # STEP 6
    # FINANCIAL SUMMARY
    # --------------------------------------------------------

    financial_summary = (
        generate_financial_summary(

            priorities,

            business_metrics
        )
    )

    # --------------------------------------------------------
    # STEP 7
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------

    summary = generate_decision_summary(

        decisions,

        overall_risk,

        business_health_score,

        duplicate_metadata
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "analysis_type": (
            "genesis_ai_decision_intelligence_v2"
        ),

        "dataset": {

            "rows": total_rows,

            "columns": int(
                len(df.columns)
            )
        },

        # ----------------------------------------------------
        # BUSINESS HEALTH
        # ----------------------------------------------------

        "business_health": {

            "score": business_health_score,

            "overall_risk": overall_risk
        },

        # ----------------------------------------------------
        # BUSINESS METRICS
        # ----------------------------------------------------

        "business_metrics": business_metrics,

        # ----------------------------------------------------
        # DUPLICATE INTELLIGENCE
        # ----------------------------------------------------

        "duplicate_intelligence": {

            "raw_priority_signals": (
                duplicate_metadata.get(
                    "raw_priorities",
                    0
                )
            ),

            "final_unique_priorities": (
                duplicate_metadata.get(
                    "final_priorities",
                    0
                )
            ),

            "duplicates_removed_or_merged": (
                duplicate_metadata.get(
                    "duplicates_removed",
                    0
                )
            )
        },

        # ----------------------------------------------------
        # PRIORITIES
        # ----------------------------------------------------

        "priority_summary": priority_counts,

        "total_priorities": len(
            priorities
        ),

        "decision_priorities": priorities[:10],

        # ----------------------------------------------------
        # FINANCIAL IMPACT
        # ----------------------------------------------------

        "financial_intelligence": financial_summary,

        # ----------------------------------------------------
        # EXECUTIVE DECISIONS
        # ----------------------------------------------------

        "total_executive_decisions": len(
            decisions
        ),

        "executive_decisions": decisions,

        # ----------------------------------------------------
        # EXECUTIVE SUMMARY
        # ----------------------------------------------------

        "executive_summary": summary,

        # ----------------------------------------------------
        # DISCLAIMER
        # ----------------------------------------------------

        "disclaimer": (

            "Genesis AI Decision Intelligence V2 provides "
            "data-driven decision support based on statistical "
            "patterns, anomalies, recommendations and business "
            "rules. Duplicate signals are merged where possible. "
            "Financial impact values are directional estimates "
            "and should be validated before business execution. "
            "Results support, but do not replace, human "
            "management decisions."
        )
    }