import difflib
import numpy as np
import pandas as pd


# ============================================================
# GENESIS AI - PROFESSIONAL DYNAMIC ROOT CAUSE ENGINE
# ============================================================

def investigate_root_cause(df, target_column):
    """Analyze statistically supported potential drivers of a numeric target."""

    if df is None or df.empty:
        return {
            "success": False,
            "target": target_column,
            "resolved_target": None,
            "root_causes": [],
            "summary": "No dataset is available for root cause analysis."
        }

    if target_column is None or not str(target_column).strip():
        return {
            "success": False,
            "target": target_column,
            "resolved_target": None,
            "root_causes": [],
            "summary": "Please provide a target column for root cause analysis."
        }

    requested_target = str(target_column).strip()

    # Case-insensitive column matching
    normalized_columns = {
        str(column).strip().lower(): column
        for column in df.columns
    }
    resolved_target = normalized_columns.get(requested_target.lower())

    if resolved_target is None:
        matches = difflib.get_close_matches(
            requested_target.lower(),
            list(normalized_columns.keys()),
            n=3,
            cutoff=0.55
        )
        suggestions = [str(normalized_columns[x]) for x in matches]

        summary = f"Column '{requested_target}' was not found in the dataset."
        if suggestions:
            summary += " Did you mean: " + ", ".join(suggestions) + "?"

        return {
            "success": False,
            "target": requested_target,
            "resolved_target": None,
            "available_columns": [str(column) for column in df.columns],
            "suggestions": suggestions,
            "root_causes": [],
            "summary": summary
        }

    target_column = resolved_target
    target_series = pd.to_numeric(df[target_column], errors="coerce")
    valid_target = target_series.dropna()

    if len(valid_target) == 0:
        return {
            "success": False,
            "target": requested_target,
            "resolved_target": str(target_column),
            "root_causes": [],
            "summary": (
                f"'{target_column}' does not contain numeric data "
                "for root cause analysis."
            )
        }

    total_rows = len(df)
    target_mean = float(valid_target.mean())

    results = {
        "success": True,
        "target": requested_target,
        "resolved_target": str(target_column),
        "target_mean": round(target_mean, 4),
        "records_analyzed": int(len(valid_target)),
        "root_causes": [],
        "summary": ""
    }

    excluded_keywords = [
        "id", "employee name", "name", "email", "phone",
        "mobile", "contact", "address", "uuid", "password", "token"
    ]

    def is_identifier_column(column):
        name = str(column).lower().strip()
        if any(keyword in name for keyword in excluded_keywords):
            return True

        if total_rows <= 0:
            return False

        unique_ratio = df[column].nunique(dropna=True) / total_rows
        return unique_ratio > 0.80

    def is_date_column(column):
        name = str(column).lower().strip()
        keywords = ["date", "time", "year", "month", "day"]

        if any(keyword in name for keyword in keywords):
            return True

        return pd.api.types.is_datetime64_any_dtype(df[column])

    def numeric_strength(correlation):
        value = abs(correlation)
        if value >= 0.70:
            return "Very Strong", "high"
        if value >= 0.50:
            return "Strong", "high"
        if value >= 0.30:
            return "Moderate", "medium"
        if value >= 0.10:
            return "Weak", "low"
        return None, None

    def group_strength(percent):
        if percent >= 50:
            return "Very High", "high"
        if percent >= 25:
            return "High", "high"
        if percent >= 10:
            return "Moderate", "medium"
        return "Low", "low"

    # ========================================================
    # NUMERIC FACTOR ANALYSIS
    # ========================================================

    numeric_causes = []

    for column in df.select_dtypes(include=np.number).columns:

        if column == target_column or is_identifier_column(column):
            continue

        data = pd.DataFrame({
            "target": target_series,
            "factor": pd.to_numeric(df[column], errors="coerce")
        }).dropna()

        if len(data) < 10:
            continue

        try:
            correlation = data["target"].corr(data["factor"])
        except Exception:
            continue

        if pd.isna(correlation):
            continue

        correlation = float(correlation)
        impact, confidence = numeric_strength(correlation)

        if impact is None:
            continue

        direction = "increases" if correlation > 0 else "decreases"

        numeric_causes.append({
            "category": "numeric_relationship",
            "factor": str(column),
            "analysis_method": "Pearson correlation",
            "evidence": (
                f"Correlation with {target_column} is "
                f"{round(correlation, 4)} based on {len(data)} valid records."
            ),
            "impact_strength": impact,
            "confidence": confidence,
            "relationship": (
                f"As {column} increases, {target_column} tends to {direction}."
            ),
            "correlation": round(correlation, 4),
            "records_used": int(len(data)),
            "score": round(abs(correlation) * 100, 2)
        })

    numeric_causes = sorted(
        numeric_causes,
        key=lambda item: item["score"],
        reverse=True
    )[:5]

    # ========================================================
    # CATEGORICAL GROUP ANALYSIS
    # ========================================================

    group_causes = []

    for column in df.select_dtypes(exclude=np.number).columns:

        if column == target_column:
            continue
        if is_identifier_column(column) or is_date_column(column):
            continue

        unique_count = df[column].nunique(dropna=True)
        if unique_count < 2:
            continue

        max_categories = min(30, max(10, int(total_rows * 0.05)))
        if unique_count > max_categories:
            continue

        try:
            temp = pd.DataFrame({
                "group": df[column],
                "target": target_series
            }).dropna()

            group_counts = temp.groupby("group").size()
            valid_groups = group_counts[group_counts >= 5].index

            if len(valid_groups) < 2:
                continue

            grouped = temp.groupby("group")["target"].mean()
            grouped = grouped.loc[grouped.index.intersection(valid_groups)]

            if len(grouped) < 2:
                continue

            highest = float(grouped.max())
            lowest = float(grouped.min())
            highest_group = str(grouped.idxmax())
            lowest_group = str(grouped.idxmin())
            difference = highest - lowest

            difference_percent = (
                abs(difference) / abs(target_mean) * 100
                if target_mean != 0 else 0
            )

            if difference_percent < 0.50:
                continue

            impact, confidence = group_strength(difference_percent)

            group_causes.append({
                "category": "group_difference",
                "factor": str(column),
                "analysis_method": "Group mean comparison",
                "highest_group": highest_group,
                "highest_value": round(highest, 2),
                "lowest_group": lowest_group,
                "lowest_value": round(lowest, 2),
                "difference": round(difference, 2),
                "difference_percent": round(difference_percent, 2),
                "impact_strength": impact,
                "confidence": confidence,
                "evidence": (
                    f"{lowest_group} has the lowest average {target_column} "
                    f"({round(lowest, 2)}), while {highest_group} has the "
                    f"highest average {target_column} ({round(highest, 2)})."
                ),
                "relationship": (
                    f"{column} shows meaningful variation in {target_column}."
                ),
                "score": round(difference_percent, 2)
            })

        except Exception:
            continue

    group_causes = sorted(
        group_causes,
        key=lambda item: item["score"],
        reverse=True
    )[:5]

    # ========================================================
    # COMBINE, RANK AND LIMIT RESULTS
    # ========================================================

    results["root_causes"] = sorted(
        numeric_causes + group_causes,
        key=lambda item: item["score"],
        reverse=True
    )[:10]

    for rank, cause in enumerate(results["root_causes"], start=1):
        cause["rank"] = rank

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    if results["root_causes"]:
        top_factor = results["root_causes"][0]["factor"]

        results["summary"] = (
            f"Genesis AI identified {len(results['root_causes'])} "
            f"potential drivers affecting {target_column}. "
            f"The highest-ranked potential driver is '{top_factor}'. "
            "These results indicate statistical relationships and business "
            "patterns, not proven causation."
        )
    else:
        results["summary"] = (
            f"No meaningful potential driver patterns were detected "
            f"for {target_column}."
        )

    return results
