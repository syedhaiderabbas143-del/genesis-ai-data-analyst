"""
GENESIS AI - PROFESSIONAL RECOMMENDATION ENGINE
Converts root-cause analysis findings into prioritized business actions.
"""

from typing import Any, Dict, List


def _priority_from_score(score: float) -> str:
    if score >= 50:
        return "critical"
    if score >= 25:
        return "high"
    if score >= 10:
        return "medium"
    return "low"


def _action_for_cause(cause: Dict[str, Any], target: str) -> str:
    factor = str(cause.get("factor", "this factor"))
    category = cause.get("category", "")

    if category == "numeric_relationship":
        correlation = float(cause.get("correlation", 0))
        if correlation > 0:
            return (
                f"Investigate how {factor} can be optimized because it shows "
                f"a positive statistical relationship with {target}."
            )
        return (
            f"Review and control {factor} because it shows a negative "
            f"statistical relationship with {target}."
        )

    if category == "group_difference":
        highest_group = cause.get("highest_group")
        lowest_group = cause.get("lowest_group")
        return (
            f"Compare the practices of '{highest_group}' with '{lowest_group}' "
            f"for {factor}. Identify repeatable practices from the stronger "
            f"group and investigate the weaker group's performance gap."
        )

    return f"Investigate {factor} further and validate its impact on {target}."


def _expected_impact(cause: Dict[str, Any]) -> str:
    strength = str(cause.get("impact_strength", "")).lower()

    mapping = {
        "very strong": "Potentially high impact after validation",
        "strong": "Potentially high impact after validation",
        "moderate": "Potentially moderate impact after validation",
        "weak": "Potentially limited impact; validate before action",
        "very high": "Potentially high impact after validation",
        "high": "Potentially high impact after validation",
        "low": "Potentially limited impact; validate before action",
    }

    return mapping.get(strength, "Impact should be validated with further analysis")


def generate_recommendations(
    root_cause_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate prioritized recommendations from Root Cause Engine output.

    This engine does not claim causation. Recommendations are based on
    statistically detected relationships and group differences.
    """

    if not isinstance(root_cause_result, dict):
        return {
            "success": False,
            "recommendations": [],
            "summary": "Invalid root cause analysis result."
        }

    if not root_cause_result.get("success"):
        return {
            "success": False,
            "target": root_cause_result.get("target"),
            "recommendations": [],
            "summary": root_cause_result.get(
                "summary",
                "Root cause analysis was not successful."
            )
        }

    target = str(
        root_cause_result.get("resolved_target")
        or root_cause_result.get("target")
        or "target metric"
    )

    root_causes: List[Dict[str, Any]] = root_cause_result.get(
        "root_causes", []
    )

    recommendations = []

    for cause in root_causes:
        score = float(cause.get("score", 0))
        rank = int(cause.get("rank", len(recommendations) + 1))
        priority = _priority_from_score(score)

        recommendation = {
            "rank": rank,
            "priority": priority,
            "factor": cause.get("factor"),
            "root_cause_category": cause.get("category"),
            "recommended_action": _action_for_cause(cause, target),
            "expected_impact": _expected_impact(cause),
            "evidence": cause.get("evidence"),
            "confidence": cause.get("confidence", "low"),
            "impact_score": round(score, 2),
            "validation_note": (
                "Validate this recommendation with business context and "
                "controlled analysis before making major decisions."
            )
        }

        recommendations.append(recommendation)

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    recommendations.sort(
        key=lambda item: (
            priority_order.get(item["priority"], 4),
            item["rank"]
        )
    )

    for index, recommendation in enumerate(recommendations, start=1):
        recommendation["rank"] = index

    priority_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for item in recommendations:
        priority_counts[item["priority"]] += 1

    if recommendations:
        top = recommendations[0]
        summary = (
            f"Genesis AI generated {len(recommendations)} prioritized "
            f"recommendations for improving or investigating {target}. "
            f"The highest-priority action focuses on '{top['factor']}'."
        )
    else:
        summary = (
            f"No actionable recommendations were generated because no "
            f"meaningful potential drivers were found for {target}."
        )

    return {
        "success": True,
        "target": target,
        "total_recommendations": len(recommendations),
        "priority_counts": priority_counts,
        "recommendations": recommendations,
        "summary": summary,
        "disclaimer": (
            "Recommendations are generated from statistical patterns and "
            "should be validated with domain knowledge before implementation."
        )
    }
