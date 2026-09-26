# ============================================================
# GENESIS AI - SYSTEM DIAGNOSTICS ENGINE
# ============================================================

import platform
import sys
import time
from datetime import datetime

import pandas as pd


# ============================================================
# MAIN SYSTEM DIAGNOSTICS
# ============================================================

def run_system_diagnostics(df=None):

    start_time = time.time()

    diagnostics = {
        "success": True,
        "diagnostic_timestamp": datetime.now().isoformat(),
        "system_status": "Healthy",
        "checks": {}
    }

    # --------------------------------------------------------
    # PYTHON ENVIRONMENT CHECK
    # --------------------------------------------------------

    diagnostics["checks"]["python_environment"] = {
        "status": "Healthy",
        "python_version": sys.version.split()[0],
        "platform": platform.platform()
    }

    # --------------------------------------------------------
    # DATASET CHECK
    # --------------------------------------------------------

    if df is None:

        diagnostics["checks"]["dataset"] = {
            "status": "Warning",
            "message": "No dataset is currently loaded."
        }

    elif not isinstance(df, pd.DataFrame):

        diagnostics["checks"]["dataset"] = {
            "status": "Error",
            "message": "Loaded data is not a valid Pandas DataFrame."
        }

        diagnostics["system_status"] = "Warning"

    else:

        diagnostics["checks"]["dataset"] = {
            "status": "Healthy",
            "total_rows": int(len(df)),
            "total_columns": int(len(df.columns)),
            "memory_usage_mb": round(
                df.memory_usage(
                    deep=True
                ).sum() / (1024 * 1024),
                2
            ),
            "missing_values": int(
                df.isnull().sum().sum()
            ),
            "duplicate_rows": int(
                df.duplicated().sum()
            )
        }

    # --------------------------------------------------------
    # PANDAS CHECK
    # --------------------------------------------------------

    diagnostics["checks"]["pandas"] = {
        "status": "Healthy",
        "version": pd.__version__
    }

    # --------------------------------------------------------
    # ENGINE PERFORMANCE CHECK
    # --------------------------------------------------------

    execution_time = round(
        time.time() - start_time,
        4
    )

    performance_status = (
        "Healthy"
        if execution_time < 2
        else "Warning"
    )

    diagnostics["checks"]["performance"] = {
        "status": performance_status,
        "diagnostic_execution_time_seconds": execution_time
    }

    # --------------------------------------------------------
    # OVERALL STATUS
    # --------------------------------------------------------

    statuses = [

        check.get("status")

        for check in diagnostics[
            "checks"
        ].values()

    ]

    if "Error" in statuses:

        diagnostics["system_status"] = "Error"

    elif "Warning" in statuses:

        diagnostics["system_status"] = "Warning"

    else:

        diagnostics["system_status"] = "Healthy"

    # --------------------------------------------------------
    # SYSTEM SUMMARY
    # --------------------------------------------------------

    diagnostics["summary"] = {

        "total_checks": len(
            diagnostics["checks"]
        ),

        "healthy_checks": statuses.count(
            "Healthy"
        ),

        "warning_checks": statuses.count(
            "Warning"
        ),

        "error_checks": statuses.count(
            "Error"
        )
    }

    return diagnostics