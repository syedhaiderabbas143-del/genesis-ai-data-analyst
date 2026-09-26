# ============================================================
# GENESIS AI - PROFESSIONAL REPORTING & EXPORT ENGINE
# ============================================================

from datetime import datetime
import json
import os
import uuid


# ============================================================
# REPORT DIRECTORY
# ============================================================

REPORTS_DIRECTORY = "generated_reports"

os.makedirs(
    REPORTS_DIRECTORY,
    exist_ok=True
)


# ============================================================
# JSON SERIALIZATION HELPER
# ============================================================

def make_json_serializable(value):

    try:

        import numpy as np
        import pandas as pd

        if isinstance(
            value,
            (
                np.integer,
                np.int64,
                np.int32
            )
        ):

            return int(value)


        if isinstance(
            value,
            (
                np.floating,
                np.float64,
                np.float32
            )
        ):

            return float(value)


        if isinstance(
            value,
            (
                np.bool_,
            )
        ):

            return bool(value)


        if isinstance(
            value,
            (
                pd.Timestamp,
                datetime
            )
        ):

            return value.isoformat()


    except Exception:

        pass


    if isinstance(value, dict):

        return {

            str(key): make_json_serializable(item)

            for key, item in value.items()

        }


    if isinstance(value, list):

        return [

            make_json_serializable(item)

            for item in value

        ]


    return value


# ============================================================
# BUILD PROFESSIONAL REPORT
# ============================================================

def build_professional_report(

    df,
    autonomous_result

):

    report_id = str(

        uuid.uuid4()

    )


    generated_at = datetime.now().isoformat()


    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    dataset_profile = autonomous_result.get(

        "analysis_results",

        {}

    ).get(

        "dataset_profile",

        {}

    )


    # --------------------------------------------------------
    # ADVANCED STATISTICS
    # --------------------------------------------------------

    advanced_statistics = autonomous_result.get(

        "analysis_results",

        {}

    ).get(

        "advanced_statistics",

        {}

    )


    # --------------------------------------------------------
    # SCENARIO ANALYSIS
    # --------------------------------------------------------

    scenario_analysis = autonomous_result.get(

        "analysis_results",

        {}

    ).get(

        "scenario_analysis",

        {}

    )


    # --------------------------------------------------------
    # DECISION INTELLIGENCE
    # --------------------------------------------------------

    decision_intelligence = autonomous_result.get(

        "analysis_results",

        {}

    ).get(

        "decision_intelligence",

        {}

    )


    # --------------------------------------------------------
    # SENIOR ANALYST REASONING
    # --------------------------------------------------------

    senior_reasoning = autonomous_result.get(

        "analysis_results",

        {}

    ).get(

        "senior_analyst_reasoning",

        {}

    )


    # --------------------------------------------------------
    # EXECUTIVE INTELLIGENCE
    # --------------------------------------------------------

    executive_intelligence = autonomous_result.get(

        "executive_intelligence",

        {}

    )


    # ========================================================
    # BUILD REPORT
    # ========================================================

    report = {

        "success": True,

        "report_id": report_id,

        "report_type": "Genesis AI Professional Analytics Report",

        "generated_at": generated_at,


        # ----------------------------------------------------
        # REPORT STATUS
        # ----------------------------------------------------

        "report_status": {

            "workflow_status":

                autonomous_result.get(
                    "workflow_status"
                ),

            "total_steps":

                autonomous_result.get(
                    "workflow_summary",
                    {}
                ).get(
                    "total_steps",
                    0
                ),

            "completed_steps":

                autonomous_result.get(
                    "workflow_summary",
                    {}
                ).get(
                    "completed_steps",
                    0
                ),

            "failed_steps":

                autonomous_result.get(
                    "workflow_summary",
                    {}
                ).get(
                    "failed_steps",
                    0
                )

        },


        # ----------------------------------------------------
        # DATASET PROFILE
        # ----------------------------------------------------

        "dataset_profile": {

            "total_rows":

                dataset_profile.get(
                    "total_rows",
                    len(df)
                ),

            "total_columns":

                dataset_profile.get(
                    "total_columns",
                    len(df.columns)
                ),

            "columns":

                dataset_profile.get(
                    "columns",
                    []
                )

        },


        # ----------------------------------------------------
        # EXECUTIVE SUMMARY
        # ----------------------------------------------------

        "executive_summary": {

            "primary_business_concern":

                executive_intelligence.get(
                    "primary_business_concern"
                ),

            "recommended_management_action":

                executive_intelligence.get(
                    "recommended_management_action"
                ),

            "workflow_status":

                autonomous_result.get(
                    "workflow_status"
                )

        },


        # ----------------------------------------------------
        # ADVANCED STATISTICS
        # ----------------------------------------------------

        "advanced_statistics":

            advanced_statistics,


        # ----------------------------------------------------
        # SCENARIO ANALYSIS
        # ----------------------------------------------------

        "scenario_analysis":

            scenario_analysis,


        # ----------------------------------------------------
        # DECISION INTELLIGENCE
        # ----------------------------------------------------

        "decision_intelligence":

            decision_intelligence,


        # ----------------------------------------------------
        # SENIOR ANALYST REASONING
        # ----------------------------------------------------

        "senior_analyst_reasoning":

            senior_reasoning


    }


    return make_json_serializable(
        report
    )


# ============================================================
# EXPORT REPORT AS JSON
# ============================================================

def export_report_json(

    report

):

    report_id = report.get(

        "report_id",

        str(uuid.uuid4())

    )


    file_name = (

        f"genesis_report_{report_id}.json"

    )


    file_path = os.path.join(

        REPORTS_DIRECTORY,

        file_name

    )


    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            report,

            file,

            indent=4,

            ensure_ascii=False,

            default=str

        )


    return {

        "success": True,

        "format": "json",

        "file_name": file_name,

        "file_path": file_path

    }


# ============================================================
# EXPORT REPORT AS CSV
# ============================================================

def export_report_csv(

    report

):

    import pandas as pd


    report_id = report.get(

        "report_id",

        str(uuid.uuid4())

    )


    rows = []


    def flatten_data(

        data,

        prefix=""

    ):

        if isinstance(

            data,

            dict

        ):

            for key, value in data.items():

                new_prefix = (

                    f"{prefix}.{key}"

                    if prefix

                    else str(key)

                )


                flatten_data(

                    value,

                    new_prefix

                )


        elif isinstance(

            data,

            list

        ):

            rows.append({

                "section": prefix,

                "value":

                    json.dumps(

                        make_json_serializable(data),

                        ensure_ascii=False,

                        default=str

                    )

            })


        else:

            rows.append({

                "section": prefix,

                "value":

                    make_json_serializable(data)

            })


    flatten_data(
        report
    )


    dataframe = pd.DataFrame(
        rows
    )


    file_name = (

        f"genesis_report_{report_id}.csv"

    )


    file_path = os.path.join(

        REPORTS_DIRECTORY,

        file_name

    )


    dataframe.to_csv(

        file_path,

        index=False,

        encoding="utf-8-sig"

    )


    return {

        "success": True,

        "format": "csv",

        "file_name": file_name,

        "file_path": file_path

    }


# ============================================================
# EXPORT REPORT AS EXCEL
# ============================================================

def export_report_excel(

    report

):

    import pandas as pd


    report_id = report.get(

        "report_id",

        str(uuid.uuid4())

    )


    file_name = (

        f"genesis_report_{report_id}.xlsx"

    )


    file_path = os.path.join(

        REPORTS_DIRECTORY,

        file_name

    )


    summary_rows = [

        {

            "Metric":

                "Report ID",

            "Value":

                report.get(
                    "report_id"
                )

        },

        {

            "Metric":

                "Report Type",

            "Value":

                report.get(
                    "report_type"
                )

        },

        {

            "Metric":

                "Generated At",

            "Value":

                report.get(
                    "generated_at"
                )

        },

        {

            "Metric":

                "Total Rows",

            "Value":

                report.get(
                    "dataset_profile",
                    {}
                ).get(
                    "total_rows"
                )

        },

        {

            "Metric":

                "Total Columns",

            "Value":

                report.get(
                    "dataset_profile",
                    {}
                ).get(
                    "total_columns"
                )

        }

    ]


    summary_dataframe = pd.DataFrame(
        summary_rows
    )


    decisions = report.get(

        "decision_intelligence",

        {}
    ).get(

        "decisions",

        []

    )


    decisions_dataframe = pd.DataFrame(
        decisions
    )


    with pd.ExcelWriter(

        file_path,

        engine="openpyxl"

    ) as writer:


        summary_dataframe.to_excel(

            writer,

            sheet_name="Executive Summary",

            index=False

        )


        if not decisions_dataframe.empty:

            decisions_dataframe.to_excel(

                writer,

                sheet_name="Decision Intelligence",

                index=False

            )


        scenario_dataframe = pd.DataFrame([

            report.get(

                "scenario_analysis",

                {}

            )

        ])


        scenario_dataframe.to_excel(

            writer,

            sheet_name="Scenario Analysis",

            index=False

        )


    return {

        "success": True,

        "format": "excel",

        "file_name": file_name,

        "file_path": file_path

    }


# ============================================================
# EXPORT COMPLETE REPORT
# ============================================================

def export_professional_report(

    report,

    export_format="json"

):

    export_format = str(

        export_format

    ).lower()


    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    if export_format == "json":

        return export_report_json(
            report
        )


    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    if export_format == "csv":

        return export_report_csv(
            report
        )


    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    if export_format in [

        "excel",

        "xlsx"

    ]:

        return export_report_excel(
            report
        )


    # --------------------------------------------------------
    # UNSUPPORTED FORMAT
    # --------------------------------------------------------

    return {

        "success": False,

        "error":

            f"Unsupported export format: {export_format}",

        "supported_formats": [

            "json",

            "csv",

            "excel"

        ]

    }