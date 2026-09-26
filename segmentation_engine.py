# ============================================================
# GENESIS AI - BUSINESS SEGMENTATION & CLUSTERING ENGINE
# ============================================================

import numpy as np
import pandas as pd


# ============================================================
# NORMALIZE DATA
# ============================================================

def normalize_data(data):

    minimum = data.min(axis=0)
    maximum = data.max(axis=0)

    denominator = maximum - minimum

    denominator[denominator == 0] = 1

    return (
        data - minimum
    ) / denominator


# ============================================================
# INITIALIZE CENTROIDS
# ============================================================

def initialize_centroids(data, number_of_clusters):

    if len(data) < number_of_clusters:
        raise ValueError(
            "Number of clusters cannot exceed available records."
        )

    indices = np.linspace(
        0,
        len(data) - 1,
        number_of_clusters,
        dtype=int
    )

    return data[indices].copy()


# ============================================================
# CALCULATE DISTANCE
# ============================================================

def calculate_distances(data, centroids):

    distances = []

    for centroid in centroids:

        distance = np.sqrt(
            np.sum(
                (data - centroid) ** 2,
                axis=1
            )
        )

        distances.append(distance)

    return np.column_stack(distances)


# ============================================================
# K-MEANS CLUSTERING
# ============================================================

def run_kmeans(
    data,
    number_of_clusters=3,
    max_iterations=100
):

    centroids = initialize_centroids(
        data,
        number_of_clusters
    )

    labels = None

    for _ in range(max_iterations):

        distances = calculate_distances(
            data,
            centroids
        )

        new_labels = np.argmin(
            distances,
            axis=1
        )

        new_centroids = []

        for cluster_number in range(number_of_clusters):

            cluster_data = data[
                new_labels == cluster_number
            ]

            if len(cluster_data) == 0:

                new_centroids.append(
                    centroids[cluster_number]
                )

            else:

                new_centroids.append(
                    cluster_data.mean(axis=0)
                )

        new_centroids = np.array(
            new_centroids
        )

        if labels is not None:

            if np.array_equal(
                labels,
                new_labels
            ):

                centroids = new_centroids

                break

        labels = new_labels

        centroids = new_centroids

    return labels, centroids


# ============================================================
# MAIN SEGMENTATION ANALYSIS
# ============================================================

def run_segmentation_analysis(
    df,
    columns=None,
    number_of_clusters=3
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        raise ValueError(
            "No dataset available for segmentation analysis."
        )

    if not isinstance(
        df,
        pd.DataFrame
    ):

        raise ValueError(
            "Dataset must be a valid Pandas DataFrame."
        )


    # --------------------------------------------------------
    # SELECT NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_df = df.select_dtypes(
        include=np.number
    ).copy()


    # --------------------------------------------------------
    # REMOVE ID COLUMNS
    # --------------------------------------------------------

    excluded_columns = []

    for column in numeric_df.columns:

        column_name = str(
            column
        ).lower()

        if (

            column_name == "id"

            or column_name.endswith("_id")

            or column_name.endswith(" id")

            or "employee id" in column_name

            or "customer id" in column_name

        ):

            excluded_columns.append(
                column
            )


    numeric_df = numeric_df.drop(
        columns=excluded_columns,
        errors="ignore"
    )


    # --------------------------------------------------------
    # USER SELECTED COLUMNS
    # --------------------------------------------------------

    if columns:

        valid_columns = [

            column

            for column in columns

            if column in numeric_df.columns

        ]

        if len(valid_columns) < 2:

            raise ValueError(

                "At least two valid numeric columns are required."

            )

        numeric_df = numeric_df[
            valid_columns
        ]


    # --------------------------------------------------------
    # VALIDATE COLUMNS
    # --------------------------------------------------------

    if len(
        numeric_df.columns
    ) < 2:

        raise ValueError(

            "At least two numeric analytical columns are required."

        )


    # --------------------------------------------------------
    # HANDLE MISSING VALUES
    # --------------------------------------------------------

    working_df = numeric_df.copy()

    working_df = working_df.replace(

        [np.inf, -np.inf],

        np.nan

    )


    working_df = working_df.dropna()


    if len(working_df) < number_of_clusters:

        raise ValueError(

            "Not enough valid records for the requested number of clusters."

        )


    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    data = working_df.to_numpy(
        dtype=float
    )


    normalized_data = normalize_data(
        data
    )


    # --------------------------------------------------------
    # RUN K-MEANS
    # --------------------------------------------------------

    labels, centroids = run_kmeans(

        normalized_data,

        number_of_clusters

    )


    # --------------------------------------------------------
    # CLUSTER RESULTS
    # --------------------------------------------------------

    cluster_results = []

    for cluster_number in range(

        number_of_clusters

    ):

        cluster_indices = (

            labels == cluster_number

        )


        cluster_data = working_df.iloc[

            np.where(
                cluster_indices
            )[0]

        ]


        cluster_size = int(

            len(cluster_data)

        )


        percentage = round(

            (
                cluster_size
                /
                len(working_df)
            )
            * 100,

            2

        )


        averages = {

            column: round(

                float(
                    cluster_data[column].mean()
                ),

                4

            )

            for column in working_df.columns

        }


        cluster_results.append({

            "cluster_id":

                int(cluster_number + 1),

            "records":

                cluster_size,

            "percentage":

                percentage,

            "average_metrics":

                averages

        })


    # --------------------------------------------------------
    # SEGMENT INTERPRETATION
    # --------------------------------------------------------

    sorted_clusters = sorted(

        cluster_results,

        key=lambda item:

            item["records"],

        reverse=True

    )


    largest_cluster = (

        sorted_clusters[0]

        if sorted_clusters

        else None

    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "analysis_type":

            "Business Segmentation and Clustering",

        "total_records_analyzed":

            int(
                len(working_df)
            ),

        "features_used":

            list(
                working_df.columns
            ),

        "number_of_clusters":

            int(
                number_of_clusters
            ),

        "clusters":

            cluster_results,

        "largest_segment":

            largest_cluster,

        "insight":

            (
                f"The dataset was divided into "
                f"{number_of_clusters} distinct business segments "
                f"based on similarities across the selected metrics."
            )

    }