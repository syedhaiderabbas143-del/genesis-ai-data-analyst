import pandas as pd
import numpy as np


def _get_column_type(series):
    """
    Detect the analytical type of a column.
    """

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    return "categorical"


def _find_primary_key_candidates(df):
    """
    Find columns that can potentially act as primary keys.
    """

    candidates = []

    total_rows = len(df)

    if total_rows == 0:
        return candidates

    for column in df.columns:

        series = df[column]

        unique_count = series.nunique(dropna=True)
        null_count = series.isnull().sum()

        if unique_count == total_rows and null_count == 0:

            candidates.append({
                "column": column,
                "unique_values": int(unique_count),
                "confidence": "High"
            })

    return candidates


def _identify_dimensions_and_measures(df):
    """
    Separate columns into dimensions and measures.
    """

    dimensions = []
    measures = []
    datetime_columns = []

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_numeric_dtype(series):

            unique_ratio = (
                series.nunique(dropna=True) / len(series)
                if len(series) > 0 else 0
            )

            # IDs should normally behave as dimensions
            if (
                "id" in column.lower()
                or unique_ratio > 0.95
            ):
                dimensions.append(column)

            else:
                measures.append(column)

        elif pd.api.types.is_datetime64_any_dtype(series):

            datetime_columns.append(column)
            dimensions.append(column)

        else:

            dimensions.append(column)

    return {
        "dimensions": dimensions,
        "measures": measures,
        "datetime_columns": datetime_columns
    }


def _analyze_cardinality(df):
    """
    Analyze column cardinality.
    """

    cardinality_results = []

    total_rows = len(df)

    for column in df.columns:

        unique_count = int(df[column].nunique(dropna=True))

        if total_rows == 0:
            cardinality_type = "Unknown"

        else:

            ratio = unique_count / total_rows

            if unique_count <= 10:
                cardinality_type = "Low"

            elif ratio < 0.10:
                cardinality_type = "Medium"

            else:
                cardinality_type = "High"

        cardinality_results.append({
            "column": column,
            "unique_values": unique_count,
            "cardinality": cardinality_type
        })

    return cardinality_results


def _detect_possible_relationships(df):
    """
    Detect possible relationships between columns
    based on column names and ID patterns.
    """

    relationships = []

    columns = list(df.columns)

    for column in columns:

        column_lower = column.lower()

        if (
            column_lower.endswith("_id")
            or column_lower == "id"
            or "id" in column_lower
        ):

            relationships.append({
                "column": column,
                "relationship_type": "Potential Key / Foreign Key",
                "recommendation":
                    "Check this column against related datasets "
                    "for primary key or foreign key relationships."
            })

    return relationships


def _suggest_data_model(df, dimensions, measures):
    """
    Suggest a Star Schema style data model.
    """

    model_suggestion = {

        "recommended_model": "Star Schema",

        "fact_table": {
            "recommended_name": "Fact_Analytics",
            "columns": measures
        },

        "dimension_tables": []
    }

    for dimension in dimensions:

        model_suggestion["dimension_tables"].append({
            "recommended_name":
                f"Dim_{dimension.replace(' ', '_')}",
            "source_column": dimension
        })

    return model_suggestion


def _generate_model_recommendations(
    df,
    primary_keys,
    dimensions,
    measures,
    datetime_columns
):
    """
    Generate professional data modeling recommendations.
    """

    recommendations = []

    if not primary_keys:

        recommendations.append(
            "No clear primary key was detected. "
            "Consider creating a unique record identifier."
        )

    else:

        recommendations.append(
            "Primary key candidate(s) detected. "
            "Validate uniqueness before production use."
        )

    if measures:

        recommendations.append(
            "Numeric measures were detected and can be "
            "used inside a central fact table."
        )

    if dimensions:

        recommendations.append(
            "Categorical columns can be separated into "
            "dimension tables for improved analytics performance."
        )

    if datetime_columns:

        recommendations.append(
            "Date/time columns detected. Create a dedicated "
            "Date Dimension for time intelligence and trend analysis."
        )

    if len(df.columns) > 20:

        recommendations.append(
            "The dataset contains many columns. Consider "
            "normalization and semantic modeling."
        )

    recommendations.append(
        "Use Star Schema for BI dashboards unless the dataset "
        "requires highly normalized transactional modeling."
    )

    return recommendations


def run_data_modeling(df):
    """
    Main Data Modeling Engine.

    Performs:

    - Schema analysis
    - Primary key detection
    - Dimension detection
    - Measure detection
    - Cardinality analysis
    - Relationship detection
    - Star Schema recommendation
    - Data modeling recommendations
    """

    try:

        if df is None:

            return {
                "success": False,
                "message": "No dataset available for data modeling."
            }

        if df.empty:

            return {
                "success": False,
                "message": "Dataset is empty."
            }


        # =====================================================
        # BASIC DATASET INFORMATION
        # =====================================================

        dataset_info = {

            "total_records": int(len(df)),

            "total_columns": int(len(df.columns)),

            "columns": list(df.columns)
        }


        # =====================================================
        # COLUMN ANALYSIS
        # =====================================================

        column_analysis = []

        for column in df.columns:

            series = df[column]

            column_analysis.append({

                "column": column,

                "data_type":
                    str(series.dtype),

                "analytical_type":
                    _get_column_type(series),

                "missing_values":
                    int(series.isnull().sum()),

                "unique_values":
                    int(series.nunique(dropna=True))

            })


        # =====================================================
        # PRIMARY KEY DETECTION
        # =====================================================

        primary_key_candidates = (
            _find_primary_key_candidates(df)
        )


        # =====================================================
        # DIMENSIONS & MEASURES
        # =====================================================

        modeling_components = (
            _identify_dimensions_and_measures(df)
        )

        dimensions = (
            modeling_components["dimensions"]
        )

        measures = (
            modeling_components["measures"]
        )

        datetime_columns = (
            modeling_components["datetime_columns"]
        )


        # =====================================================
        # CARDINALITY ANALYSIS
        # =====================================================

        cardinality_analysis = (
            _analyze_cardinality(df)
        )


        # =====================================================
        # RELATIONSHIP DETECTION
        # =====================================================

        possible_relationships = (
            _detect_possible_relationships(df)
        )


        # =====================================================
        # DATA MODEL SUGGESTION
        # =====================================================

        data_model = (
            _suggest_data_model(
                df,
                dimensions,
                measures
            )
        )


        # =====================================================
        # PROFESSIONAL RECOMMENDATIONS
        # =====================================================

        recommendations = (
            _generate_model_recommendations(
                df,
                primary_key_candidates,
                dimensions,
                measures,
                datetime_columns
            )
        )


        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {

            "success": True,

            "analysis_type":
                "Advanced Data Modeling Analysis",

            "dataset_info":
                dataset_info,

            "primary_key_candidates":
                primary_key_candidates,

            "dimensions":
                dimensions,

            "measures":
                measures,

            "datetime_columns":
                datetime_columns,

            "column_analysis":
                column_analysis,

            "cardinality_analysis":
                cardinality_analysis,

            "possible_relationships":
                possible_relationships,

            "recommended_data_model":
                data_model,

            "recommendations":
                recommendations

        }


    except Exception as e:

        return {

            "success": False,

            "message":
                "Data modeling analysis failed.",

            "error":
                str(e)

        }