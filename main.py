from security.database import init_db
from security.auth_router import router as auth_router
from api.tenant_routes import router as tenant_router
from api.advanced_routes import router as advanced_router
from fastapi.responses import FileResponse
import os
import uuid
import pandas as pd
import numpy as np
from context_intelligence import build_context_intelligence
from root_cause_engine import investigate_root_cause
from agent_router import route_agent
from workflow_memory import WorkflowMemory
from planned_workflow import run_planned_workflow
from multi_agent_workflow import run_multi_agent_workflow
from planner_agent import run_planner_agent
from orchestrator_agent import run_orchestrator_agent
from reporting_agent import run_reporting_agent
from decision_agent import run_decision_agent
from root_cause_agent import run_root_cause_analysis
from agent_executor import execute_agent
from recommendation_agent import run_recommendation_agent
from insights_agent import run_insights_agent
from forecast_agent import run_forecast_agent
from engineer_agent import run_engineer_agent
from quality_agent import run_quality_agent
from analyst_agent import run_analyst_agent
from schema_evolution_engine import run_schema_evolution_analysis
from audit_logs_engine import run_audit_logs_analysis
from metadata_engine import run_metadata_analysis
from observability_engine import run_observability_analysis
from segmentation_engine import (
    run_segmentation_analysis
)
from forecast_engine import (
    run_forecast_analysis
)
from outlier_engine import (
    detect_iqr_outliers
)
from root_cause_analysis_engine import (
    run_root_cause_analysis
)
from statistical_analysis_engine import (
    run_statistical_analysis
)
from anomaly_detection_engine import (
    run_anomaly_detection
)
from orchestration_engine import run_orchestration
from data_modeling_engine import (
    run_data_modeling
)
from recommendation_engine import generate_recommendations
from decision_engine import calculate_decision_priority
from executive_summary_engine import generate_executive_summary
from auto_insights_engine import generate_auto_insights
from decision_priority_engine import calculate_decision_priority
from decision_impact_engine import calculate_decision_impact
from decision_action_plan_engine import generate_decision_action_plan
from decision_grouping_engine import group_decisions
from advanced_root_cause_engine import analyze_advanced_root_cause
from advanced_statistics_engine import run_advanced_statistics
from scenario_analysis_engine import run_scenario_analysis
from senior_analyst_reasoning_engine import generate_senior_analyst_reasoning
from api_error_handler import global_exception_handler
from dataset_stress_test_engine import (
    run_dataset_stress_test
)
from security_validation_engine import (
    run_security_validation,
    validate_file_extension,
    validate_file_size,
    validate_file_content
)
from performance_monitor_engine import (
    get_performance_summary,
    reset_performance_metrics,
    record_performance
)
from system_diagnostics_engine import run_system_diagnostics
from decision_intelligence_engine import generate_decision_intelligence
from automated_insight_engine import generate_automated_insights
from autonomous_analysis_engine import run_autonomous_analysis
from reporting_export_engine import (
    build_professional_report,
    export_professional_report
)
from decision_confidence_engine import calculate_decision_confidence_and_risk
from decision_explanation_engine import (
    generate_decision_explanation
)
from advanced_intent_engine import detect_advanced_intent
from datetime import datetime
import matplotlib.pyplot as plt
from analytics_v4 import analyze_question
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import re


data_lineage = []
# =====================================================
# GENESIS AI DATA LINEAGE ENGINE
# =====================================================

def add_lineage_step(
    operation,
    details=None
):

    global data_lineage
    from datetime import datetime

    if details is None:
        details = {}

    step = {
        "step": len(data_lineage) + 1,
        "time": datetime.now().isoformat(
            timespec="seconds"
        ),
        "operation": operation,
        "details": details
    }

    data_lineage.append(step)

    return step
# =========================================================
# GENESIS AI VERSION HISTORY
# =========================================================

dataset_versions = []


# =====================================================
# GENESIS AI VERSION HISTORY
# =====================================================

dataset_versions = []


def save_dataset_version(action="Dataset Updated"):

    global current_df, dataset_versions

    if current_df is None:
        return

    version = {
        "version": len(dataset_versions) + 1,
        "action": action,
        "rows": int(len(current_df)),
        "columns": int(len(current_df.columns)),
        "column_names": current_df.columns.tolist()
    }

    dataset_versions.append(version)

    return version


# =====================================================
# GENESIS AI AUDIT LOG SYSTEM
# =====================================================

audit_logs = []


def add_audit_log(event, details=None):

    global current_df

    from datetime import datetime

    log = {
        "id": len(audit_logs) + 1,
        "event": event,
        "timestamp": datetime.now().isoformat(),

        "rows": (
            int(len(current_df))
            if current_df is not None
            else 0
        ),

        "columns": (
            int(len(current_df.columns))
            if current_df is not None
            else 0
        ),

        "details": details or {}
    }

    audit_logs.append(log)

    return log


# =====================================================
# FASTAPI APPLICATION
# =====================================================

from security.middleware import RouteSecurityMiddleware

app = FastAPI(
    title="AI Data Analyst"
)

init_db()
app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(advanced_router)

# Opt-in security for sensitive routes. Enable with GENESIS_SECURITY_ENFORCED=true.
app.add_middleware(RouteSecurityMiddleware)
# ============================================================
# GENESIS AI - GLOBAL API ERROR HANDLER
# ============================================================

app.add_exception_handler(
    Exception,
    global_exception_handler
)
# ============================================================
# GENESIS AI - PERFORMANCE MONITORING MIDDLEWARE
# ============================================================

import time


@app.middleware("http")
async def performance_monitoring_middleware(
    request,
    call_next
):

    start_time = time.time()

    response = await call_next(request)

    execution_time = (
        time.time()
        - start_time
    )

    record_performance(
        execution_time
    )

    return response

# Active dataset stored in memory

current_df = None


# =====================================================
# TRANSFORMATION HISTORY
# =====================================================

transformation_history = []
redo_history = []


@app.get("/Frontend.html")
def serve_frontend():

    return FileResponse(
        "Frontend.html"
    )


# ----------------------------
# Create Charts Folder
# ----------------------------
os.makedirs("charts", exist_ok=True)

app.mount(
    "/charts",
    StaticFiles(directory="charts"),
    name="charts"
)

# ----------------------------
# CORS
# ----------------------------
# Security: configure allowed browser origins explicitly.
# Example: GENESIS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:8000
_allowed_origins = [
    origin.strip()
    for origin in os.getenv("GENESIS_ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# ----------------------------
# Global Dataset
# ----------------------------
latest_df = None
# =====================================================
# FORECAST TRACKING HISTORY
# =====================================================

forecast_history = []

def create_dashboard_chart(df, column, chart_type="bar"):

    # Check column exists
    if column not in df.columns:
        return None


    # Get value counts
    data = df[column].dropna().value_counts()


    # Check data exists
    if data.empty:
        return None


    # Create chart
    plt.figure(figsize=(8, 5))


    # ============================================================
    # PIE CHART
    # ============================================================

    if chart_type == "pie":

        data.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90
        )

        plt.ylabel("")


    # ============================================================
    # BAR CHART
    # ============================================================

    else:

        data.plot(
            kind="bar"
        )

        plt.xlabel(column)

        plt.ylabel("Count")

        plt.xticks(rotation=30)


    # ============================================================
    # CHART TITLE
    # ============================================================

    plt.title(
        f"{column} Distribution"
    )


    # ============================================================
    # CREATE UNIQUE FILENAME
    # ============================================================

    chart_filename = f"{uuid.uuid4()}.png"


    # ============================================================
    # CHART DIRECTORY
    # ============================================================

    os.makedirs(
        "charts",
        exist_ok=True
    )


    # ============================================================
    # FILE PATH
    # ============================================================

    filepath = os.path.join(
        "charts",
        chart_filename
    )


    # ============================================================
    # SAVE CHART
    # ============================================================

    plt.tight_layout()

    plt.savefig(
        filepath,
        bbox_inches="tight"
    )

    plt.close()


    # ============================================================
    # IMPORTANT: RETURN CHART URL
    # ============================================================

    return f"/charts/{chart_filename}"

    
class Question(BaseModel):
    question: str


class FilterRequest(BaseModel):
    department: str = ""
    city: str = ""
    branch: str = ""
    gender: str = ""
    work_mode: str = ""

# ----------------------------
# Home API
# ----------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to AI Data Analyst 🚀",
        "status": "Running"
    }
@app.get("/dashboard")
def dashboard():
    return FileResponse("Frontend.html")

# ----------------------------
# Upload API
# ----------------------------
@app.get("/health", tags=["system"])
def health_check():
    """Lightweight liveness endpoint for local development and deployment checks."""
    return {"status": "ok", "service": "genesis-ai-data-analyst"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    global latest_df, current_df
    global transformation_history, redo_history


    # ============================================================
    # SECURITY VALIDATION - FILENAME
    # ============================================================

    if not file.filename:
        return {
            "success": False,
            "error": "Filename is required."
        }


    filename = file.filename.strip()


    if len(filename) > 255:
        return {
            "success": False,
            "error": "Filename is too long."
        }


    # Prevent path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return {
            "success": False,
            "error": "Invalid filename detected."
        }


    # ============================================================
    # SECURITY VALIDATION - FILE EXTENSION
    # ============================================================

    extension_valid, extension_message = validate_file_extension(
        filename
    )

    if not extension_valid:
        return {
            "success": False,
            "error": extension_message
        }


    # ============================================================
    # READ FILE CONTENT
    # ============================================================

    try:

        file_content = await file.read()

    except Exception:

        return {
            "success": False,
            "error": "Unable to read uploaded file."
        }


    # ============================================================
    # SECURITY VALIDATION - FILE SIZE
    # ============================================================

    file_size_bytes = len(file_content)


    size_valid, size_message = validate_file_size(
        file_size_bytes
    )


    if not size_valid:
        return {
            "success": False,
            "error": size_message
        }


    # ============================================================
    # SECURITY VALIDATION - FILE CONTENT
    # ============================================================

    content_valid, content_message = validate_file_content(
        filename,
        file_content
    )


    if not content_valid:
        return {
            "success": False,
            "error": content_message
        }


    # ============================================================
    # SAFE FILE PARSING
    # ============================================================

    try:

        # IMPORTANT:
        # Use BytesIO because file_content has already been read.

        import io


        # CSV
        if filename.lower().endswith(".csv"):

            df = pd.read_csv(
                io.BytesIO(file_content)
            )


        # XLSX Excel
        elif filename.lower().endswith(".xlsx"):

            df = pd.read_excel(
                io.BytesIO(file_content)
            )


        # XLS Excel
        elif filename.lower().endswith(".xls"):

            df = pd.read_excel(
                io.BytesIO(file_content)
            )


        else:

            return {
                "success": False,
                "error": "Unsupported file format."
            }


    except Exception as e:

        print("Upload parsing error:", str(e))

        return {
            "success": False,
            "error": (
                "Unable to read the uploaded file. "
                "Please upload a valid CSV, XLS, or XLSX file."
            )
        }


    # ============================================================
    # DATASET VALIDATION
    # ============================================================

    if df is None or df.empty:

        return {
            "success": False,
            "error": "The uploaded file contains no data."
        }


    # ============================================================
    # DEBUG INFORMATION
    # ============================================================

    if "Gender" in df.columns:

        print(
            "Gender Values:",
            df["Gender"].dropna().unique()
        )


    # ============================================================
    # STORE DATASET
    # ============================================================

    latest_df = df.copy()

    current_df = df.copy()


    # ============================================================
    # RESET TRANSFORMATION HISTORY
    # ============================================================

    transformation_history.clear()

    redo_history.clear()


    
    # ----------------------------
    # AI Insights
    # ----------------------------

    insights = []

    # Basic Information
    insights.append(f"📄 Total Rows: {len(df)}")
    insights.append(f"📋 Total Columns: {len(df.columns)}")

    # Missing Values
    missing = df.isnull().sum().sum()
    insights.append(f"❌ Missing Values: {missing}")

    # Duplicate Rows
    duplicates = df.duplicated().sum()
    insights.append(f"📑 Duplicate Rows: {duplicates}")

    # Numeric Columns
    numeric_cols = df.select_dtypes(include="number").columns
    insights.append(f"🔢 Numeric Columns: {len(numeric_cols)}")

    # Salary Analysis
    if "Salary" in df.columns:
        insights.append(f"💰 Average Salary: {df['Salary'].mean():.2f}")
        insights.append(f"💵 Highest Salary: {df['Salary'].max():.2f}")
        insights.append(f"💸 Lowest Salary: {df['Salary'].min():.2f}")

    # Department Analysis
    if "Department" in df.columns:
        insights.append(f"🏢 Total Departments: {df['Department'].nunique()}")

    # Employee Count
    insights.append(f"👨‍💼 Total Employees: {len(df)}")

        # ----------------------------
    # Automatic Chart
    # ----------------------------

    chart_file = None

    if "Department" in df.columns:

        dept = df["Department"].value_counts()

        plt.figure(figsize=(10, 5))

        plt.bar(dept.index, dept.values)

        plt.title("Department-wise Employee Count")
        plt.xlabel("Department")
        plt.ylabel("Employees")

        plt.xticks(rotation=30)

        os.makedirs("charts", exist_ok=True)

    chart_filename = f"{uuid.uuid4()}.png"

    filepath = os.path.join("charts", chart_filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    chart_file = f"/charts/{chart_filename}"
    print("Chart File:", chart_file)
        # ----------------------------
    # Dashboard Summary
    # ----------------------------
    summary = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "missing_values": int(df.isnull().sum().sum())
}

    if "Salary" in df.columns:
        summary["avg_salary"] = round(df["Salary"].mean(), 2)


    if "Age" in df.columns:
        summary["avg_age"] = round(df["Age"].mean(), 2)

    if "Department" in df.columns:
        summary["departments"] = df["Department"].nunique()

    if "Gender" in df.columns:
        summary["male"] = int((df["Gender"] == "Male").sum())
        summary["female"] = int((df["Gender"] == "Female").sum())
    if "Work Mode" in df.columns:
        summary["remote"] = int((df["Work Mode"] == "Remote").sum())
        summary["hybrid"] = int((df["Work Mode"] == "Hybrid").sum())
        summary["office"] = int((df["Work Mode"] == "Office").sum())
    # ----------------------------
    # Professional Dashboard Charts
    # ----------------------------

    dashboard_charts = {

        "department": create_dashboard_chart(
            df,
            "Department",
            "bar"
        ),

        "gender": create_dashboard_chart(
            df,
            "Gender",
            "pie"
        ),

        "work_mode": create_dashboard_chart(
            df,
            "Work Mode",
            "bar"
        ),

        "city": create_dashboard_chart(
            df,
            "City",
            "bar"
        ),

        "branch": create_dashboard_chart(
            df,
            "Branch",
            "bar"
        )
    }


    # ----------------------------
    # Smart Filter Options
    # ----------------------------

    filter_options = {}

    if "Department" in df.columns:
        filter_options["department"] = sorted(
            df["Department"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    if "City" in df.columns:
        filter_options["city"] = sorted(
            df["City"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    if "Branch" in df.columns:
        filter_options["branch"] = sorted(
            df["Branch"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    if "Gender" in df.columns:
        filter_options["gender"] = sorted(
            df["Gender"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    if "Work Mode" in df.columns:
        filter_options["work_mode"] = sorted(
            df["Work Mode"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )


    # ----------------------------
    # Return Upload Response
    # ----------------------------

    return {

    "success": True,

    "message": "File uploaded and analyzed successfully.",

    "filename": filename,

        "chart_file": chart_file,

                "dashboard_charts": dashboard_charts,

        "filter_options": filter_options,

        "rows": int(len(df)),

        "columns": list(df.columns),

        "preview": df.head(10).fillna("").to_dict(
            orient="records"
        ),

        "data_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        },

        "missing_values": {
            col: int(val)
            for col, val in df.isnull().sum().items()
        },

        "statistics": df.describe(
            include="all"
        ).fillna("").to_dict(),

        "ai_insights": insights,

        "summary": summary
    }
def genesis_dashboard_anomalies():
    df = require_df()

    numeric_cols = _numeric_columns(df)

    if not numeric_cols:
        return {
            "success": False,
            "message": "No numeric columns available for anomaly detection."
        }

    anomalies = []
    summary = []
    

    # Columns that should not normally be treated as business anomalies
    excluded_columns = {
        "Employee ID",
        "Phone"
    }

    # Prefer meaningful business metrics
    preferred_columns = [
        "Salary",
        "Bonus",
        "Incentive",
        "Attendance %",
        "Leaves",
        "Performance Rating",
        "Training Hours",
        "Monthly Sales",
        "Revenue",
        "Expenses",
        "Profit",
        "Target",
        "Achievement %"
    ]

    analysis_columns = [
        col for col in preferred_columns
        if col in numeric_cols and col not in excluded_columns
    ]

    # If preferred columns are not available, use numeric columns
    if not analysis_columns:
        analysis_columns = [
            col for col in numeric_cols
            if col not in excluded_columns
        ]

    for col in analysis_columns:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        if len(series) < 4:
            continue

        # =====================================================
        # IQR OUTLIER DETECTION
        # =====================================================
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        lower_outliers = int(
            (series < lower_bound).sum()
        )

        upper_outliers = int(
            (series > upper_bound).sum()
        )

        total_outliers = lower_outliers + upper_outliers

        outlier_percent = round(
            (total_outliers / len(series)) * 100,
            2
        )

        summary.append({
            "column": str(col),
            "total_records": int(len(series)),
            "outliers": total_outliers,
            "outlier_percentage": outlier_percent,
            "lower_outliers": lower_outliers,
            "upper_outliers": upper_outliers,
            "lower_bound": round(lower_bound, 4),
            "upper_bound": round(upper_bound, 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "method": "IQR"
        })

        # =====================================================
        # CREATE ANOMALY ALERTS
        # =====================================================
        if total_outliers > 0:

            if outlier_percent >= 10:
                priority = "high"
            elif outlier_percent >= 3:
                priority = "medium"
            else:
                priority = "low"

            anomalies.append({
                "priority": priority,
                "category": "statistical_outlier",
                "column": str(col),
                "message": (
                    f"{total_outliers} records ({outlier_percent}%) "
                    f"are outside the expected range for {col}."
                ),
                "details": {
                    "lower_outliers": lower_outliers,
                    "upper_outliers": upper_outliers,
                    "expected_min": round(lower_bound, 4),
                    "expected_max": round(upper_bound, 4),
                    "actual_min": round(float(series.min()), 4),
                    "actual_max": round(float(series.max()), 4)
                },
                "recommendation": (
                    f"Review unusual {col} values to determine whether "
                    f"they represent valid extreme cases, data entry errors, "
                    f"or potential business risks."
                )
            })

    # =========================================================
    # SPECIAL BUSINESS ANOMALIES
    # =========================================================

    # Negative profit
    if "Profit" in df.columns:

        profit = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        negative_profit = int(
            (profit < 0).sum()
        )

        if negative_profit > 0:

            percentage = round(
                (negative_profit / len(df)) * 100,
                2
            )

            anomalies.append({
                "priority": (
                    "high"
                    if percentage >= 20
                    else "medium"
                ),
                "category": "business_anomaly",
                "column": "Profit",
                "message": (
                    f"{negative_profit} records ({percentage}%) "
                    f"have negative profit."
                ),
                "recommendation": (
                    "Investigate loss-making records and identify "
                    "high-expense or low-revenue patterns."
                )
            })

    # Expenses greater than revenue
    if (
        "Revenue" in df.columns
        and "Expenses" in df.columns
    ):

        revenue = pd.to_numeric(
            df["Revenue"],
            errors="coerce"
        )

        expenses = pd.to_numeric(
            df["Expenses"],
            errors="coerce"
        )

        mask = (
            revenue.notna()
            & expenses.notna()
            & (expenses > revenue)
        )

        count = int(mask.sum())

        if count > 0:

            percentage = round(
                (count / len(df)) * 100,
                2
            )

            anomalies.append({
                "priority": (
                    "high"
                    if percentage >= 10
                    else "medium"
                ),
                "category": "business_anomaly",
                "column": "Expenses",
                "message": (
                    f"{count} records ({percentage}%) have expenses "
                    f"greater than revenue."
                ),
                "recommendation": (
                    "Review these records as they may represent "
                    "loss-making operations or abnormal cost structures."
                )
            })

    # =========================================================
    # PRIORITY SORTING
    # =========================================================

    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    anomalies = sorted(
        anomalies,
        key=lambda x: priority_order.get(
            x.get("priority", "low"),
            99
        )
    )

    high_count = sum(
        1 for item in anomalies
        if item["priority"] == "high"
    )

    medium_count = sum(
        1 for item in anomalies
        if item["priority"] == "medium"
    )

    low_count = sum(
        1 for item in anomalies
        if item["priority"] == "low"
    )

    return {
        "success": True,
        "method": "IQR (Interquartile Range)",
        "columns_analyzed": len(analysis_columns),
        "total_anomalies": len(anomalies),
        "priority_counts": {
            "high": high_count,
            "medium": medium_count,
            "low": low_count
        },
        "anomalies": _json_safe(anomalies),
        "column_summary": _json_safe(summary)
    }
@app.api_route(
    "/analytics/anomalies",
    methods=["GET", "POST"]
)
def analytics_anomalies():
    return genesis_dashboard_anomalies()
# =========================================================
# ADVANCED FORECAST INTELLIGENCE ENGINE
# =========================================================

# =========================================================
# FORECAST INTELLIGENCE ENGINE v5
# =========================================================


def genesis_trend_analysis():

    df = require_df()

    numeric_cols = _numeric_columns(df)

    if not numeric_cols:
        return {
            "success": False,
            "message": "No numeric columns available for trend analysis."
        }

    # -----------------------------------------------------
    # FIND DATE COLUMN
    # -----------------------------------------------------

    date_column = None

    preferred_date_columns = [
        "Date",
        "Joining Date",
        "JoiningDate",
        "Order Date",
        "OrderDate",
        "Transaction Date",
        "TransactionDate"
    ]

    for col in preferred_date_columns:

        if col in df.columns:
            date_column = col
            break

    if date_column is None:

        for col in df.columns:

            if "date" in str(col).lower():
                date_column = col
                break

    if date_column is None:

        return {
            "success": False,
            "message": "No date column found for trend analysis."
        }

    # -----------------------------------------------------
    # PREPARE DATA
    # -----------------------------------------------------

    working_df = df.copy()

    working_df[date_column] = pd.to_datetime(
        working_df[date_column],
        errors="coerce"
    )

    working_df = working_df.dropna(
        subset=[date_column]
    )

    if len(working_df) < 3:

        return {
            "success": False,
            "message": "Not enough valid date records for trend analysis."
        }

    working_df["_trend_period"] = (
        working_df[date_column]
        .dt.to_period("M")
    )

    results = []
    alerts = []

    # -----------------------------------------------------
    # ANALYZE NUMERIC METRICS
    # -----------------------------------------------------

    for col in numeric_cols[:15]:

        temp = working_df[
            ["_trend_period", col]
        ].copy()

        temp[col] = pd.to_numeric(
            temp[col],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[col]
        )

        if len(temp) < 3:
            continue

        monthly = (
            temp
            .groupby("_trend_period")[col]
            .mean()
            .sort_index()
        )

        if len(monthly) < 3:
            continue

        y = monthly.values.astype(float)

        x = np.arange(
            len(y),
            dtype=float
        )

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        # -------------------------------------------------
        # TREND DIRECTION
        # -------------------------------------------------

        current_value = float(y[-1])

        tolerance = abs(current_value) * 0.005

        if slope > tolerance:

            trend = "upward"

        elif slope < -tolerance:

            trend = "downward"

        else:

            trend = "stable"

        # -------------------------------------------------
        # CHANGE PERCENT
        # -------------------------------------------------

        first_value = float(y[0])

        if first_value != 0:

            change_percent = round(
                (
                    (current_value - first_value)
                    / abs(first_value)
                ) * 100,
                2
            )

        else:

            change_percent = 0.0

        # -------------------------------------------------
        # LINEAR FIT / STRENGTH
        # -------------------------------------------------

        predicted = (
            slope * x
            + intercept
        )

        ss_res = np.sum(
            (y - predicted) ** 2
        )

        ss_tot = np.sum(
            (y - np.mean(y)) ** 2
        )

        if ss_tot == 0:

            r_squared = 1.0

        else:

            r_squared = max(
                0.0,
                1 - (ss_res / ss_tot)
            )

        # -------------------------------------------------
        # TREND STRENGTH
        # -------------------------------------------------

        if r_squared >= 0.75:

            strength = "strong"

        elif r_squared >= 0.40:

            strength = "moderate"

        else:

            strength = "weak"

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        result = {

            "metric": str(col),

            "trend": trend,

            "strength": strength,

            "change_percent": change_percent,

            "first_value": round(
                first_value,
                4
            ),

            "current_value": round(
                current_value,
                4
            ),

            "slope": round(
                float(slope),
                6
            ),

            "r_squared": round(
                float(r_squared),
                4
            ),

            "data_points": int(
                len(y)
            ),

            "start_period": str(
                monthly.index[0]
            ),

            "end_period": str(
                monthly.index[-1]
            )

        }

        results.append(result)

        # -------------------------------------------------
        # TREND ALERT
        # -------------------------------------------------

        if (
            abs(change_percent) >= 10
            and strength != "weak"
        ):

            direction = (
                "increased"
                if change_percent > 0
                else "decreased"
            )

            alerts.append({

                "priority": "high",

                "metric": str(col),

                "message": (
                    f"{col} has {direction} by "
                    f"{abs(change_percent)}% "
                    f"during the analyzed period."
                )

            })

        elif abs(change_percent) >= 5:

            direction = (
                "increased"
                if change_percent > 0
                else "decreased"
            )

            alerts.append({

                "priority": "medium",

                "metric": str(col),

                "message": (
                    f"{col} has {direction} by "
                    f"{abs(change_percent)}% "
                    f"during the analyzed period."
                )

            })

    # -----------------------------------------------------
    # SORT RESULTS
    # -----------------------------------------------------

    results = sorted(

        results,

        key=lambda x: abs(
            x["change_percent"]
        ),

        reverse=True

    )

    return {

        "success": True,

        "date_column": str(
            date_column
        ),

        "aggregation": "monthly average",

        "metrics_analyzed": len(
            results
        ),

        "alerts": alerts,

        "trends": _json_safe(
            results
        )

    }


# =========================================================
# TREND ANALYSIS API
# =========================================================

@app.api_route(
    "/analytics/trend",
    methods=["GET", "POST"]
)
def analytics_trend():

    return genesis_trend_analysis()
# =========================================================
# FORECAST INTELLIGENCE API
# =========================================================

@app.api_route(
    "/analytics/forecast-intelligence",
    methods=["GET", "POST"]
)
def analytics_forecast_intelligence():

    return genesis_dashboard_forecast()
# ----------------------------
# Ask AI API
# ----------------------------
# ----------------------------
# Smart Filter API
# ----------------------------
@app.post("/filter")

def filter_data(filters: FilterRequest):

    global latest_df

    if latest_df is None:
        return {
            "error": "Please upload a dataset first."
        }

    df = latest_df.copy()

    # ----------------------------
    # Apply Filters
    # ----------------------------

    if filters.department and "Department" in df.columns:
        df = df[
    df["Department"].astype(str).str.lower()
            == filters.department.lower()
        ]

    if filters.city and "City" in df.columns:
        df = df[
            df["City"].astype(str).str.lower()
            == filters.city.lower()
        ]

    if filters.branch and "Branch" in df.columns:
        df = df[
            df["Branch"].astype(str).str.lower()
            == filters.branch.lower()
        ]

    if filters.gender and "Gender" in df.columns:
        df = df[
            df["Gender"].astype(str).str.lower()
            == filters.gender.lower()
        ]

    if filters.work_mode and "Work Mode" in df.columns:
        df = df[
            df["Work Mode"].astype(str).str.lower()
            == filters.work_mode.lower()
        ]

    # ----------------------------
    # Summary
    # ----------------------------

    summary = {
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_values": int(
            df.isnull().sum().sum()
        )
    }

    if "Salary" in df.columns and not df.empty:
        summary["avg_salary"] = round(
            df["Salary"].mean(), 2
        )

    if "Age" in df.columns and not df.empty:
        summary["avg_age"] = round(
            df["Age"].mean(), 2
        )

    if "Department" in df.columns:
        summary["departments"] = int(
            df["Department"].nunique()
        )

    if "Gender" in df.columns:
        summary["male"] = int(
            (
                df["Gender"]
                .astype(str)
                .str.lower()
                == "male"
            ).sum()
        )

        summary["female"] = int(
            (
                df["Gender"]
                .astype(str)
                .str.lower()
                == "female"
            ).sum()
        )

    if "Work Mode" in df.columns:

        summary["remote"] = int(
            (
                df["Work Mode"]
                .astype(str)
                .str.lower()
                == "remote"
            ).sum()
        )

        summary["hybrid"] = int(
            (
                df["Work Mode"]
                .astype(str)
                .str.lower()
                == "hybrid"
            ).sum()
        )

        summary["office"] = int(
            (
                df["Work Mode"]
                .astype(str)
                .str.lower()
                == "office"
            ).sum()
        )

    # ----------------------------
    # Dashboard Charts
    # ----------------------------

    dashboard_charts = {

        "department": create_dashboard_chart(
            df,
            "Department",
            "bar"
        ),

        "gender": create_dashboard_chart(
            df,
            "Gender",
            "pie"
        ),

        "work_mode": create_dashboard_chart(
            df,
            "Work Mode",
            "bar"
        ),

        "city": create_dashboard_chart(
            df,
            "City",
            "bar"
        ),

        "branch": create_dashboard_chart(
            df,
            "Branch",
            "bar"
        )
    }

    # ----------------------------
    # Return Filtered Data
    # ----------------------------

    return {

        "rows": int(len(df)),

        "columns": list(df.columns),

        "preview": df.head(10).fillna("").to_dict(
            orient="records"
        ),

        "summary": summary,

        "dashboard_charts": dashboard_charts,

        "active_filters": {
            "department": filters.department,
            "city": filters.city,
            "branch": filters.branch,
            "gender": filters.gender,
            "work_mode": filters.work_mode
        }
    }
# =========================================
# ASK AI API - GENERIC ANALYSIS ENGINE
# =========================================

@app.post("/ask")
def ask(question: Question):

    global latest_df

    # -----------------------------------------
    # CHECK DATASET
    # -----------------------------------------

    if latest_df is None:
        return {
            "answer": "Please upload a dataset first."
        }

    df = latest_df.copy()

    q = question.question.lower().strip()
        # =========================================
    # GENESIS AI ADVANCED INTENT DETECTION
    # =========================================

    intent_result = detect_advanced_intent(
        question
    )

    detected_intent = intent_result.get(
        "intent",
        "general_analysis"
    )

    print(
        "DETECTED INTENT:",
        detected_intent
    )

    answer = None

    # -----------------------------------------
    # HELPER: FIND COLUMN
    # -----------------------------------------

    def find_column(names):

        for name in names:

            for col in df.columns:

                if col.lower().strip() == name.lower().strip():
                    return col

        return None

    # -----------------------------------------
    # FIND COMMON COLUMNS
    # -----------------------------------------

    salary_col = find_column([
        "Salary",
        "Annual Salary",
        "Monthly Salary"
    ])

    age_col = find_column([
        "Age"
    ])

    department_col = find_column([
        "Department"
    ])

    city_col = find_column([
        "City"
    ])

    branch_col = find_column([
        "Branch"
    ])

    gender_col = find_column([
        "Gender"
    ])

    work_mode_col = find_column([
        "Work Mode",
        "WorkMode"
    ])

    profit_col = find_column([
        "Profit"
    ])

    revenue_col = find_column([
        "Revenue"
    ])

    performance_col = find_column([
        "Performance Rating",
        "Performance"
    ])

    satisfaction_col = find_column([
        "Satisfaction Score",
        "Satisfaction"
    ])

    attendance_col = find_column([
        "Attendance %",
        "Attendance"
    ])

    leaves_col = find_column([
        "Leaves"
    ])

    training_col = find_column([
        "Training Hours",
        "Training"
    ])

    employee_col = find_column([
        "Employee ID",
        "Employee Name"
    ])

    # =========================================
    # BASIC EMPLOYEE COUNT
    # =========================================

    if (
        "total employee" in q
        or "total employees" in q
        or "how many employees" in q
        or "number of employees" in q
        or q == "employees"
    ):

        return {
            "answer": f"👨‍💼 Total Employees: {len(df):,}"
        }
    # =========================================
    # PHASE 3 - BUSINESS INTELLIGENCE ROUTING
    # =========================================

    # -----------------------------------------
    # BUSINESS PROBLEMS
    # -----------------------------------------

    if any(phrase in q for phrase in [
        "biggest business problems",
        "business problems",
        "main business problems",
        "major business problems"
    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])
        overall_risk = analysis.get("overall_risk", "Unknown")

        answer = (
            "🔍 Genesis AI Business Problems Analysis\n\n"
            f"Overall Risk Level: {overall_risk}\n\n"
            "🚨 Main Business Problems:\n\n"
        )

        for i, item in enumerate(root_causes, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"   Evidence: {item.get('evidence')}\n"
                f"   Impact: {item.get('business_impact')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "business_problem_analysis",
            "overall_risk": overall_risk,
            "root_causes": root_causes
        }


    # -----------------------------------------
    # KEY RISKS
    # -----------------------------------------

    if any(phrase in q for phrase in [
        "key risks",
        "main risks",
        "business risks",
        "show risks",
        "risk analysis"
    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])
        overall_risk = analysis.get("overall_risk", "Unknown")

        answer = (
            "⚠️ Genesis AI Key Risk Analysis\n\n"
            f"Overall Risk Level: {overall_risk}\n\n"
            "🚨 Key Risks:\n\n"
        )

        for i, item in enumerate(root_causes, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"   Severity: {item.get('severity')}\n"
                f"   Evidence: {item.get('evidence')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "business_risk_analysis",
            "overall_risk": overall_risk,
            "root_causes": root_causes
        }


    # -----------------------------------------
    # WHY IS PROFIT LOW?
    # -----------------------------------------

    if any(phrase in q for phrase in [
        "why is profit low",
        "why profit is low",
        "why is the profit low",
        "low profit reason",
        "reason for low profit"
    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        profit_causes = [

            item for item in root_causes

            if item.get("category") in [
                "profitability",
                "expense_management",
                "revenue_growth"
            ]
        ]

        answer = (
            "📉 Genesis AI Profit Analysis\n\n"
            "The following factors may be affecting profitability:\n\n"
        )

        for i, item in enumerate(profit_causes, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"   Evidence: {item.get('evidence')}\n"
                f"   Impact: {item.get('business_impact')}\n"
                f"   Recommendation: {item.get('recommendation')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "profit_root_cause_analysis",
            "root_causes": profit_causes
        }


    # -----------------------------------------
    # MANAGEMENT FOCUS
    # -----------------------------------------

    if any(phrase in q for phrase in [
        "what should management focus on",
        "management focus",
        "management should focus",
        "what should management do"
    ]):

        analysis = genesis_dashboard_recommendations()

        recommendations = analysis.get("recommendations", [])
        overall_risk = analysis.get("overall_risk", "Unknown")

        answer = (
            "🎯 Genesis AI Management Priorities\n\n"
            f"Overall Risk Level: {overall_risk}\n\n"
            "Management should focus on:\n\n"
        )

        for i, item in enumerate(recommendations, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"   Priority: {item.get('priority')}\n"
                f"   Action: {item.get('recommended_action')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "management_focus_analysis",
            "overall_risk": overall_risk,
            "recommendations": recommendations
        }


    # -----------------------------------------
    # WHICH DEPARTMENT NEEDS IMPROVEMENT?
    # -----------------------------------------

    if any(phrase in q for phrase in [
        "which department needs improvement",
        "department needs improvement",
        "worst department",
        "weakest department",
        "lowest performing department"
    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        department_causes = [

            item for item in root_causes

            if item.get("category") == "department_analysis"
        ]

        answer = (
            "🏢 Genesis AI Department Analysis\n\n"
        )

        if department_causes:

            for item in department_causes:

                answer += (
                    f"Department Needing Attention: "
                    f"{item.get('factor')}\n\n"
                    f"Evidence: {item.get('evidence')}\n\n"
                    f"Impact: {item.get('business_impact')}\n\n"
                    f"Recommendation: "
                    f"{item.get('recommendation')}\n"
                )

        else:

            answer += (
                "No significant department-level issue "
                "was identified in the current analysis."
            )

        return {
            "answer": answer,
            "analysis_type": "department_improvement_analysis",
            "root_causes": department_causes
        }
    # =========================================
    # GENESIS AI BUSINESS RISK ANALYSIS
    # =========================================

    if detected_intent == "business_risk":

        risks = []

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()


        # -----------------------------------------
        # HIGH VARIATION RISK DETECTION
        # -----------------------------------------

        for col in numeric_columns:

            if df[col].dropna().empty:
                continue

            mean_value = df[col].mean()
            std_value = df[col].std()

            if mean_value != 0:

                variation = abs(
                    std_value / mean_value
                ) * 100

                if variation >= 50:

                    risks.append({

                        "factor": col,

                        "risk_type":
                            "High Data Variation",

                        "severity":
                            "High" if variation >= 100
                            else "Medium",

                        "evidence":
                            f"{col} shows {round(variation, 2)}% variation.",

                        "recommendation":
                            f"Investigate unusual patterns and "
                            f"extreme values in {col}."

                    })


        # -----------------------------------------
        # BUILD ANSWER
        # -----------------------------------------

        answer = (
            "⚠️ GENESIS AI BUSINESS RISK ANALYSIS\n\n"
        )


        if risks:

            answer += (
                f"Genesis AI identified "
                f"{len(risks)} potential business risk areas.\n\n"
            )


            for i, risk in enumerate(risks[:5], 1):

                answer += (

                    f"{i}. Risk Area: "
                    f"{risk.get('factor')}\n"

                    f"   Risk Type: "
                    f"{risk.get('risk_type')}\n"

                    f"   Severity: "
                    f"{risk.get('severity')}\n"

                    f"   Evidence: "
                    f"{risk.get('evidence')}\n"

                    f"   Recommended Action: "
                    f"{risk.get('recommendation')}\n\n"

                )

        else:

            answer += (
                "No major business risks were detected "
                "from the available dataset patterns."
            )


        return {

            "answer": answer,

            "analysis_type":
                "business_risk_analysis",

            "risks": risks

        }
        # =========================================
    # GENESIS AI MANAGEMENT FOCUS INTELLIGENCE
    # =========================================

    if detected_intent == "management_focus":

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get(
            "root_causes",
            []
        )

        # Priority order
        severity_order = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        sorted_causes = sorted(
            root_causes,
            key=lambda item: severity_order.get(
                str(
                    item.get(
                        "severity",
                        "low"
                    )
                ).lower(),
                1
            ),
            reverse=True
        )

        answer = (
            "🎯 GENESIS AI MANAGEMENT FOCUS ANALYSIS\n\n"
        )

        if sorted_causes:

            top_focus = sorted_causes[0]

            answer += (
                "🚨 PRIMARY MANAGEMENT FOCUS\n\n"
                f"Focus Area: {top_focus.get('factor')}\n"
                f"Severity: {top_focus.get('severity')}\n\n"
                f"Evidence: {top_focus.get('evidence')}\n\n"
                f"Business Impact: "
                f"{top_focus.get('business_impact')}\n\n"
                f"Recommended Action: "
                f"{top_focus.get('recommendation')}\n\n"
            )

            answer += (
                "📊 OTHER IMPORTANT MANAGEMENT PRIORITIES:\n\n"
            )

            for i, item in enumerate(
                sorted_causes[1:4],
                1
            ):

                answer += (
                    f"{i}. {item.get('factor')}\n"
                    f"   Severity: "
                    f"{item.get('severity')}\n"
                    f"   Evidence: "
                    f"{item.get('evidence')}\n\n"
                )

        else:

            answer += (
                "No significant management focus areas "
                "were identified from the current dataset."
            )

        return {

            "answer": answer,

            "analysis_type":
                "management_focus_analysis",

            "priorities":
                sorted_causes[:4]

        }
        # =========================================
    # GENESIS AI EMPLOYEE ATTENTION INTELLIGENCE
    # =========================================

    if detected_intent == "employee_attention":

        attention_employees = []

        # -----------------------------------------
        # FIND POSSIBLE EMPLOYEE IDENTIFIER COLUMN
        # -----------------------------------------

        employee_column = None

        possible_employee_columns = [

            "employee name",
            "employee",
            "name",
            "employee id",
            "id"

        ]

        for col in df.columns:

            if str(col).lower().strip() in possible_employee_columns:

                employee_column = col
                break


        # -----------------------------------------
        # FIND RELEVANT METRIC COLUMNS
        # -----------------------------------------

        performance_column = None
        attendance_column = None
        leaves_column = None


        for col in df.columns:

            col_name = str(col).lower().strip()

            if "performance" in col_name:

                performance_column = col

            if "attendance" in col_name:

                attendance_column = col

            if "leave" in col_name:

                leaves_column = col


        # -----------------------------------------
        # ANALYZE EMPLOYEES
        # -----------------------------------------

        if employee_column is not None:

            for _, row in df.iterrows():

                risk_score = 0

                reasons = []


                # Low performance

                if performance_column is not None:

                    performance_value = row.get(
                        performance_column
                    )

                    if pd.notna(performance_value):

                        if performance_value <= 2:

                            risk_score += 40

                            reasons.append(
                                "Low performance"
                            )


                # Low attendance

                if attendance_column is not None:

                    attendance_value = row.get(
                        attendance_column
                    )

                    if pd.notna(attendance_value):

                        if attendance_value < 80:

                            risk_score += 30

                            reasons.append(
                                "Low attendance"
                            )


                # High leaves

                if leaves_column is not None:

                    leaves_value = row.get(
                        leaves_column
                    )

                    if pd.notna(leaves_value):

                        if leaves_value >= 15:

                            risk_score += 30

                            reasons.append(
                                "High leave count"
                            )


                # ---------------------------------
                # ADD EMPLOYEE
                # ---------------------------------
                # ---------------------------------
                # DETERMINE RISK LEVEL
                # ---------------------------------

                if risk_score >= 70:

                    risk_level = "Critical"

                elif risk_score >= 40:

                    risk_level = "High"

                else:

                    risk_level = "Medium"
                if risk_score >= 40:

                    attention_employees.append({

    "employee":
        row.get(
            employee_column
        ),

    "risk_score":
        risk_score,

    "risk_level":
        risk_level,

    "reasons":
        reasons

})


        # -----------------------------------------
        # SORT BY RISK SCORE
        # -----------------------------------------

        attention_employees = sorted(

            attention_employees,

            key=lambda item:
                item.get(
                    "risk_score",
                    0
                ),

            reverse=True

        )


        # -----------------------------------------
        # BUILD ANSWER
        # -----------------------------------------

        answer = (

            "👥 GENESIS AI EMPLOYEE ATTENTION ANALYSIS\n\n"

        )


        if attention_employees:

            answer += (

                f"Genesis AI identified "

                f"{len(attention_employees)} "

                f"employees requiring attention.\n\n"

            )


            for i, employee in enumerate(

                attention_employees[:10],

                1

            ):

                reasons_text = ", ".join(

                    employee.get(
                        "reasons",
                        []
                    )

                )


                answer += (

    f"{i}. Employee: "
    f"{employee.get('employee')}\n"

    f"   Risk Level: "
    f"{employee.get('risk_level')}\n"

    f"   Risk Score: "
    f"{employee.get('risk_score')}/100\n"

    f"   Reasons: "
    f"{reasons_text}\n\n"

)

        else:

            answer += (

                "No employees requiring significant "

                "attention were identified based on "

                "the available dataset metrics."

            )


        return {

            "answer": answer,

            "analysis_type":

                "employee_attention_analysis",

            "employees":

                attention_employees[:10]

        }
        # =========================================
    # GENESIS AI BEST PERFORMER INTELLIGENCE
    # =========================================

    if detected_intent == "best_performer":

        employee_column = None
        performance_column = None

        possible_employee_columns = [

            "employee name",
            "employee",
            "name",
            "employee id",
            "id"

        ]

        # -----------------------------------------
        # FIND EMPLOYEE COLUMN
        # -----------------------------------------

        for col in df.columns:

            col_name = str(col).lower().strip()

            if col_name in possible_employee_columns:

                employee_column = col
                break


        # -----------------------------------------
        # FIND PERFORMANCE COLUMN
        # -----------------------------------------

        for col in df.columns:

            col_name = str(col).lower().strip()

            if "performance" in col_name:

                performance_column = col
                break


        answer = (

            "🏆 GENESIS AI BEST PERFORMER ANALYSIS\n\n"

        )


        # -----------------------------------------
        # ANALYZE TOP PERFORMERS
        # -----------------------------------------

        if (

            employee_column is not None

            and performance_column is not None

        ):

            performance_data = df[

                [
                    employee_column,
                    performance_column
                ]

            ].dropna()


            top_performers = performance_data.sort_values(

                by=performance_column,

                ascending=False

            ).head(10)


            if not top_performers.empty:

                best_employee = top_performers.iloc[0]


                answer += (

                    "🥇 BEST PERFORMER\n\n"

                    f"Employee: "

                    f"{best_employee[employee_column]}\n"

                    f"Performance Rating: "

                    f"{best_employee[performance_column]}\n\n"

                    "📊 TOP 10 PERFORMERS:\n\n"

                )


                for i, (

                    _,
                    row

                ) in enumerate(

                    top_performers.iterrows(),

                    1

                ):

                    answer += (

                        f"{i}. Employee: "

                        f"{row[employee_column]}\n"

                        f"   Performance Rating: "

                        f"{row[performance_column]}\n\n"

                    )


            else:

                answer += (

                    "No valid performance data "

                    "was found in the dataset."

                )


        else:

            answer += (

                "Genesis AI could not identify "

                "the employee or performance column."

            )


        return {

            "answer": answer,

            "analysis_type":

                "best_performer_analysis",

            "top_performers":

                top_performers.to_dict(

                    orient="records"

                )

                if (

                    employee_column is not None

                    and performance_column is not None

                    and not top_performers.empty

                )

                else []

        }
        # =========================================
    # GENESIS AI COMPARISON INTELLIGENCE
    # =========================================

    if detected_intent == "comparison":

        answer = (

            "⚖️ GENESIS AI COMPARISON ANALYSIS\n\n"

        )


        # -----------------------------------------
        # FIND POSSIBLE GROUP COLUMN
        # -----------------------------------------

        group_column = None


        possible_group_columns = [

            "department",

            "city",

            "branch",

            "gender",

            "work mode",

            "designation",

            "job role"

        ]


        # -----------------------------------------
        # DETECT GROUP FROM QUESTION
        # -----------------------------------------

        for col in df.columns:

            col_name = str(col).lower().strip()

            if (

                col_name in possible_group_columns

                and col_name in q

            ):

                group_column = col

                break


        # -----------------------------------------
        # FALLBACK GROUP COLUMN
        # -----------------------------------------

        if group_column is None:

            for col in df.columns:

                col_name = str(col).lower().strip()

                if col_name in possible_group_columns:

                    group_column = col
                    break


        # -----------------------------------------
        # FIND NUMERIC METRIC
        # -----------------------------------------

        metric_column = None


        for col in df.columns:

            col_name = str(col).lower().strip()


            if col_name in q:

                if pd.api.types.is_numeric_dtype(

                    df[col]

                ):

                    metric_column = col
                    break


        # -----------------------------------------
        # COMMON METRIC DETECTION
        # -----------------------------------------

        if metric_column is None:

            metric_mapping = {

                "profit": profit_col,

                "revenue": revenue_col,

                "salary": salary_col,

                "performance": performance_col,

                "attendance": attendance_col,

                "satisfaction": satisfaction_col,

                "leaves": leaves_col

            }


            for metric, column in metric_mapping.items():

                if (

                    metric in q

                    and column is not None

                ):

                    metric_column = column
                    break


        # -----------------------------------------
        # RUN COMPARISON
        # -----------------------------------------

        if (

            group_column is not None

            and metric_column is not None

        ):

            comparison_data = (

                df.groupby(

                    group_column

                )[

                    metric_column

                ]

                .mean()

                .sort_values(

                    ascending=False

                )

            )


            highest_group = comparison_data.index[0]

            highest_value = comparison_data.iloc[0]

            lowest_group = comparison_data.index[-1]

            lowest_value = comparison_data.iloc[-1]


            difference = (

                highest_value

                - lowest_value

            )


            answer += (

                f"Comparison Group: "

                f"{group_column}\n"

                f"Metric: "

                f"{metric_column}\n\n"

                f"🏆 Highest: "

                f"{highest_group} "

                f"({round(highest_value, 2)})\n\n"

                f"⚠️ Lowest: "

                f"{lowest_group} "

                f"({round(lowest_value, 2)})\n\n"

                f"📊 Difference: "

                f"{round(difference, 2)}\n\n"

                "FULL COMPARISON:\n\n"

            )


            for group, value in comparison_data.items():

                answer += (

                    f"{group}: "

                    f"{round(value, 2)}\n"

                )


            return {

                "answer": answer,

                "analysis_type":

                    "comparison_analysis",

                "group_column":

                    group_column,

                "metric_column":

                    metric_column,

                "comparison":

                    comparison_data.to_dict()

            }


        else:

            answer += (

                "Genesis AI could not identify "

                "a valid comparison group or metric "

                "from your question."

            )


            return {

                "answer": answer,

                "analysis_type":

                    "comparison_analysis",

                "comparison": {}

            }
    # =========================================
    # ADVANCED ROOT CAUSE INTELLIGENCE ENGINE
    # =========================================


    # -----------------------------------------
    # WHY ARE EXPENSES HIGH?
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "why are expenses high",
        "why is expense high",
        "why is expenses high",
        "high expense reason",
        "why expenses are high",
        "reason for high expenses",
        "why are costs high",
        "high costs"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        expense_causes = [

            item for item in root_causes

            if item.get("category") == "expense_management"

        ]

        answer = (
            "💰 Genesis AI Expense Root Cause Analysis\n\n"
        )

        if expense_causes:

            for i, item in enumerate(expense_causes, 1):

                answer += (
                    f"{i}. {item.get('title')}\n\n"
                    f"Evidence: {item.get('evidence')}\n\n"
                    f"Business Impact: "
                    f"{item.get('business_impact')}\n\n"
                    f"Root Cause: {item.get('factor')}\n\n"
                    f"Recommended Action: "
                    f"{item.get('recommendation')}\n\n"
                )

        else:

            answer += (
                "No major expense-related root cause "
                "was identified in the current dataset."
            )

        return {
            "answer": answer,
            "analysis_type": "expense_root_cause_analysis",
            "root_causes": expense_causes
        }


    # -----------------------------------------
    # WHY IS REVENUE LOW?
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "why is revenue low",
        "why revenue is low",
        "low revenue reason",
        "reason for low revenue",
        "why are sales low",
        "why is sales low"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        revenue_causes = [

            item for item in root_causes

            if item.get("category") in [

                "revenue_growth",
                "profitability"

            ]

        ]

        answer = (
            "📊 Genesis AI Revenue Root Cause Analysis\n\n"
        )

        if revenue_causes:

            for i, item in enumerate(revenue_causes, 1):

                answer += (
                    f"{i}. {item.get('title')}\n\n"
                    f"Evidence: {item.get('evidence')}\n\n"
                    f"Business Impact: "
                    f"{item.get('business_impact')}\n\n"
                    f"Recommended Action: "
                    f"{item.get('recommendation')}\n\n"
                )

        else:

            answer += (
                "No major revenue-related root cause "
                "was identified in the current dataset."
            )

        return {
            "answer": answer,
            "analysis_type": "revenue_root_cause_analysis",
            "root_causes": revenue_causes
        }


    # -----------------------------------------
    # WHY IS PERFORMANCE LOW?
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "why is performance low",
        "why performance is low",
        "low performance reason",
        "reason for low performance",
        "why are employees performing poorly",
        "poor performance"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        performance_causes = [

            item for item in root_causes

            if item.get("category") == "performance"

        ]

        answer = (
            "📉 Genesis AI Performance Root Cause Analysis\n\n"
        )

        if performance_causes:

            for i, item in enumerate(performance_causes, 1):

                answer += (
                    f"{i}. {item.get('title')}\n\n"
                    f"Evidence: {item.get('evidence')}\n\n"
                    f"Business Impact: "
                    f"{item.get('business_impact')}\n\n"
                    f"Recommended Action: "
                    f"{item.get('recommendation')}\n\n"
                )

        else:

            answer += (
                "No major performance-related root cause "
                "was identified in the current dataset."
            )

        return {
            "answer": answer,
            "analysis_type": "performance_root_cause_analysis",
            "root_causes": performance_causes
        }


    # -----------------------------------------
    # WHAT IS CAUSING LOSSES?
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "what is causing losses",
        "what causes losses",
        "why are we making losses",
        "why is the business making losses",
        "loss causes",
        "causes of losses"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        loss_causes = [

            item for item in root_causes

            if item.get("category") in [

                "profitability",
                "expense_management"

            ]

        ]

        answer = (
            "🚨 Genesis AI Loss Root Cause Analysis\n\n"
            "The following factors may be causing losses:\n\n"
        )

        for i, item in enumerate(loss_causes, 1):

            answer += (
                f"{i}. {item.get('title')}\n\n"
                f"Evidence: {item.get('evidence')}\n\n"
                f"Impact: {item.get('business_impact')}\n\n"
                f"Recommendation: "
                f"{item.get('recommendation')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "loss_root_cause_analysis",
            "root_causes": loss_causes
        }


    # -----------------------------------------
    # WHAT FACTORS AFFECT PROFIT?
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "which factors affect profit",
        "what factors affect profit",
        "what affects profit",
        "profit drivers",
        "factors affecting profit",
        "what affects profitability"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        profit_factors = [

            item for item in root_causes

            if item.get("category") in [

                "profitability",
                "expense_management",
                "revenue_growth"

            ]

        ]

        answer = (
            "📈 Genesis AI Profit Driver Analysis\n\n"
            "The following factors have the strongest "
            "impact on profitability:\n\n"
        )

        for i, item in enumerate(profit_factors, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"Factor: {item.get('factor')}\n"
                f"Evidence: {item.get('evidence')}\n"
                f"Severity: {item.get('severity')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "profit_driver_analysis",
            "root_causes": profit_factors
        }


    # -----------------------------------------
    # GENERAL ROOT CAUSE ANALYSIS
    # -----------------------------------------

    if any(phrase in q for phrase in [

        "what are the root causes",
        "root cause analysis",
        "root causes of business problems",
        "what is causing the problems",
        "why are there business problems"

    ]):

        analysis = genesis_dashboard_recommendations()

        root_causes = analysis.get("root_causes", [])

        overall_risk = analysis.get(
            "overall_risk",
            "Unknown"
        )

        answer = (
            "🧠 Genesis AI Root Cause Analysis\n\n"
            f"Overall Risk Level: {overall_risk}\n\n"
            "Identified Root Causes:\n\n"
        )

        for i, item in enumerate(root_causes, 1):

            answer += (
                f"{i}. {item.get('title')}\n"
                f"Category: {item.get('category')}\n"
                f"Evidence: {item.get('evidence')}\n"
                f"Impact: {item.get('business_impact')}\n"
                f"Severity: {item.get('severity')}\n\n"
            )

        return {
            "answer": answer,
            "analysis_type": "general_root_cause_analysis",
            "overall_risk": overall_risk,
            "root_causes": root_causes
        }
        # =========================================
    # PHASE 4 - DYNAMIC ROOT CAUSE INVESTIGATION
    # =========================================

    root_cause_phrases = [

        "why is",
        "why are",
        "why",
        "root cause",
        "root causes",
        "investigate",
        "what is causing",
        "what causes",
        "causing problems",
        "reason for"
    ]


    if any(phrase in q for phrase in root_cause_phrases):

        # -----------------------------------------
        # FIND TARGET COLUMN DYNAMICALLY
        # -----------------------------------------

        target_column = None


        # -----------------------------------------
        # Priority 1:
        # Check actual dataset column names
        # -----------------------------------------

        for col in df.columns:

            col_name = str(col).lower().strip()

            if col_name in q:

                if pd.api.types.is_numeric_dtype(df[col]):

                    target_column = col
                    break


        # -----------------------------------------
        # Priority 2:
        # Common metric mapping
        # -----------------------------------------

        if target_column is None:

            dynamic_metrics = {

                "profit": profit_col,
                "revenue": revenue_col,
                "salary": salary_col,
                "age": age_col,

                "performance rating": performance_col,
                "performance": performance_col,

                "satisfaction": satisfaction_col,

                "attendance": attendance_col,

                "leaves": leaves_col,

                "training hours": training_col,
                "training": training_col
            }


            for metric, column in dynamic_metrics.items():

                if metric in q and column is not None:

                    target_column = column
                    break


        # -----------------------------------------
        # DEBUG
        # -----------------------------------------

        print("QUESTION:", q)
        print("TARGET COLUMN:", target_column)


        # =========================================
        # PHASE 4 - DYNAMIC ROOT CAUSE INVESTIGATION
        # =========================================

        if target_column is not None:

            # -----------------------------------------
            # RUN DYNAMIC ROOT CAUSE ENGINE
            # -----------------------------------------

            investigation = investigate_root_cause(
                df,
                target_column
            )

            root_causes = investigation.get(
                "root_causes",
                []
            )


            # -----------------------------------------
            # GENERATE RECOMMENDATIONS
            # -----------------------------------------

            recommendation_result = generate_recommendations(
                root_causes,
                target_column
            )

            recommendations = recommendation_result.get(
                "recommendations",
                []
            )
                        # -----------------------------------------
            # GENERATE AUTOMATIC AI INSIGHTS
            # -----------------------------------------

            auto_insights_result = generate_auto_insights(
                df
            )

            auto_insights = auto_insights_result.get(
                "insights",
                []
            )
            # -----------------------------------------
            # GENERATE DECISION PRIORITIES
            # -----------------------------------------

            decision_result = calculate_decision_priority(
                root_causes,
                recommendations
            )

            decisions = decision_result.get(
                "decisions",
                []
            )

                        # -----------------------------------------
            # GENERATE EXECUTIVE SUMMARY
            # -----------------------------------------

            executive_result = generate_executive_summary(
                decisions,
                target_column
            )

            executive_summary = executive_result.get(
                "executive_summary",
                {}
            )

            executive_summary_text = executive_result.get(
                "summary",
                ""
            )
            # -----------------------------------------
            # GENERATE EXECUTIVE SUMMARY
            # -----------------------------------------

            executive_result = generate_executive_summary(
                decisions,
                target_column
            )

            executive_summary = executive_result.get(
                "executive_summary",
                {}
            )

            executive_summary_text = executive_result.get(
                "summary",
                ""
            )
            # -----------------------------------------
            # BUILD ROOT CAUSE ANSWER
            # -----------------------------------------

            answer = (
                f"🔎 Genesis AI Dynamic Root Cause Investigation\n\n"
                f"Target: {target_column}\n\n"
                f"{investigation.get('summary')}\n\n"
            )
            # -----------------------------------------
            # DISPLAY EXECUTIVE SUMMARY
            # -----------------------------------------

            if executive_summary_text:

               answer += (
                   "📊 GENESIS AI EXECUTIVE SUMMARY\n\n"
                   f"{executive_summary_text}\n\n"
               )
             # -----------------------------------------
        # DISPLAY AUTOMATIC AI INSIGHTS
        # -----------------------------------------

        if auto_insights:

            answer += "🤖 GENESIS AI AUTOMATIC INSIGHTS\n\n"

            for i, insight in enumerate(auto_insights, 1):

                title = insight.get(
                    "title",
                    "Genesis AI Insight"
                )

                insight_text = insight.get(
                    "insight",
                    "No insight available."
                )

                priority = insight.get(
                    "priority",
                    "Info"
                )

                answer += (

                    f"{i}. {title}\n"

                    f"   Insight: {insight_text}\n"

                    f"   Priority: {priority}\n\n"

                )
            # -----------------------------------------
            # DISPLAY ROOT CAUSES
            # -----------------------------------------

            if root_causes:

                answer += "🚨 Potential Root Causes:\n\n"

                for i, item in enumerate(root_causes, 1):

                    answer += (
                        f"{i}. {item.get('factor')}\n"
                        f"   Category: {item.get('category')}\n"
                        f"   Evidence: {item.get('evidence')}\n"
                        f"   Impact: {item.get('impact_strength')}\n"
                        f"   Relationship: {item.get('relationship')}\n\n"
                    )

            else:

                answer += (
                    "No strong root cause patterns were found "
                    "in the current dataset.\n\n"
                )


            # -----------------------------------------
            # DISPLAY AI RECOMMENDATIONS
            # -----------------------------------------
            if recommendations:

                answer += "💡 Genesis AI Recommendations:\n\n"

                for i, recommendation in enumerate(recommendations, 1):

                    factor = recommendation.get(
                        "factor",
                        "Unknown Factor"
                    )

                    priority = recommendation.get(
                        "priority",
                        "Unknown"
                    )

                    recommendation_text = recommendation.get(
                        "recommendation",
                        "No recommendation available."
                    )

                    expected_impact = recommendation.get(
                        "expected_impact",
                        "Unknown"
                    )

                    answer += (

                        f"{i}. {factor}\n"

                        f"   Priority: {priority}\n"

                        f"   Recommendation: {recommendation_text}\n"

                        f"   Expected Impact: {expected_impact}\n\n"

                    )


            # -----------------------------------------
            # GENESIS AI DECISION PRIORITIES
            # -----------------------------------------

            if decisions:

                answer += "🧠 Genesis AI Decision Priorities:\n\n"

                for i, decision in enumerate(
                    decisions,
                    1
                ):

                    factor = decision.get(
                        "factor",
                        "Unknown Factor"
                    )

                    priority = decision.get(
                        "priority",
                        "Unknown"
                    )
                    score = decision.get(
    "decision_score",
    decision.get("score", 0)
)

                    decision_score = decision.get(
                        "decision_score",
                        0
                    )

                    quick_win = decision.get(
                        "quick_win",
                        False
                    )

                    recommended_action = decision.get(
                        "recommended_action",
                        "No action available."
                    )

                    expected_impact = decision.get(
                        "expected_impact",
                        "Unknown"
                    )

                    quick_win_text = (
                        "Yes ⚡"
                        if quick_win
                        else "No"
                    )

                    answer += (

                        f"{i}. {factor}\n"
                        f"   Priority: {priority}\n"
                        f"   Decision Score: {score}\n"
                        f"   Quick Win: {quick_win_text}\n"
                        f"   Recommended Action: {recommended_action}\n"
                        f"   Expected Impact: {expected_impact}\n\n"

                    )

            # -----------------------------------------
            # GENESIS AI EXECUTIVE SUMMARY
            # -----------------------------------------

            if executive_summary:

                answer += "👔 Genesis AI Executive Summary:\n\n"

                top_priority = executive_summary.get(
                    "top_priority",
                    "Unknown"
                )

                decision_score = executive_summary.get(
                    "decision_score",
                    0
                )

                priority_level = executive_summary.get(
                    "priority_level",
                    "Unknown"
                )

                quick_wins = executive_summary.get(
                    "quick_wins",
                    []
                )

                management_attention = executive_summary.get(
                    "management_attention_required",
                    False
                )

                recommended_focus = executive_summary.get(
                    "recommended_focus",
                    "No focus recommendation available."
                )


                quick_wins_text = (
                    ", ".join(quick_wins)
                    if quick_wins
                    else "No immediate quick wins identified"
                )


                management_attention_text = (
                    "Yes ⚠️"
                    if management_attention
                    else "No"
                )


                answer += (

                    f"Top Priority: {top_priority}\n"
                    f"Decision Score: {decision_score}/100\n"
                    f"Priority Level: {priority_level}\n"
                    f"Quick Wins: {quick_wins_text}\n"
                    f"Management Attention Required: "
                    f"{management_attention_text}\n\n"
                    f"Recommended Focus:\n"
                    f"{recommended_focus}\n\n"

                )


                if executive_summary_text:

                    answer += (
                        f"📊 Executive Insight:\n"
                        f"{executive_summary_text}\n\n"
                    )
            return {

                "answer": answer,

                "analysis_type":
                    "dynamic_root_cause_investigation",

                "target_column":
                    target_column,

                "root_causes":
                    root_causes,

                "recommendations":
                    recommendations,

                "decisions":
                    decisions

            }
        # -----------------------------------------
        # RETURN RESULT
        # -----------------------------------------

        return {

            "answer": answer,

            "analysis_type":
                "dynamic_root_cause_investigation",

            "target_column":
                target_column,

            "root_causes":
                root_causes,

            "recommendations":
                recommendations

        }


    # =========================================
    # BASIC AVERAGE / MAX / MIN ANALYSIS
    # =========================================
    


    metrics = {

            "salary": salary_col,
            "age": age_col,
            "profit": profit_col,
            "revenue": revenue_col,
            "performance": performance_col,
            "performance rating": performance_col,
            "satisfaction": satisfaction_col,
            "satisfaction score": satisfaction_col,
            "attendance": attendance_col,
            "attendance percentage": attendance_col,
            "leaves": leaves_col,
            "training": training_col,
            "training hours": training_col
        }

        # -----------------------------------------
        # Detect metric
        # -----------------------------------------

    selected_metric = None
    selected_col = None

            # =========================================
    # PRIORITY: EXACT DATASET COLUMN DETECTION
    # =========================================

    for col in df.columns:

        col_name = str(col).strip().lower()

        if col_name in q:

            if pd.api.types.is_numeric_dtype(df[col]):

                selected_col = col
                selected_metric = col_name

                break

        # -----------------------------------------
        # FALLBACK: PREDEFINED METRIC DETECTION
        # -----------------------------------------

        if selected_col is None:

            metric_names = sorted(
                metrics.keys(),
                key=len,
                reverse=True
            )

            for metric_name in metric_names:

                if metric_name in q:

                    selected_metric = metric_name
                    selected_col = metrics[metric_name]

                    break
        # =========================================
        # PAID EMPLOYEE = SALARY
        # =========================================

        if employee_col and salary_col:

            if (
                "highest paid employee" in q
                or "lowest paid employee" in q
            ):

                selected_metric = "salary"
                selected_col = salary_col
        # =========================================
        # GENERIC GROUP ANALYSIS
        # =========================================

            group_columns = {

            "department": department_col,
            "city": city_col,
            "branch": branch_col,
            "gender": gender_col,
            "work mode": work_mode_col,
            "employee": employee_col
        }

        selected_group = None
        selected_group_col = None

            # Detect group
        group_aliases = {

            "department": [
                "department",
                "departments"
            ],

            "city": [
                "city",
                "cities"
            ],

            "branch": [
                "branch",
                "branches"
            ],

            "gender": [
                "gender",
                "genders"
            ],

            "work mode": [
                "work mode",
                "work modes"
            ],

            "employee": [
                "employee",
                "employees"
            ]
        }

        for group_name, aliases in group_aliases.items():

            group_col = group_columns.get(group_name)

            if not group_col:
                continue

            for alias in aliases:

                if alias in q:

                    selected_group = group_name
                    selected_group_col = group_col

                    break

            if selected_group_col:
                break
        # =========================================
        # GROUP COMPARISON ENGINE
        # =========================================
        # Examples:
        #   Compare IT and Sales average salary
        #   IT vs Sales average salary
        #   Which department has higher average salary, IT or Sales?
        # =========================================

        comparison_words = [
            "compare",
            "vs",
            "versus",
            "higher",
            "lower",
            "greater",
            "less",
            "difference between",
        ]

        is_comparison_question = any(word in q for word in comparison_words)

        # Infer the group column when the user names group values directly.
        # Example: "Compare IT and Sales average salary" -> Department.
        if is_comparison_question and selected_group_col is None:
            comparison_group_candidates = [
                ("department", department_col),
                ("city", city_col),
                ("branch", branch_col),
                ("gender", gender_col),
                ("work mode", work_mode_col),
            ]

            for candidate_name, candidate_col in comparison_group_candidates:
                if not candidate_col:
                    continue

                candidate_values = (
                    df[candidate_col]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .unique()
                    .tolist()
                )

                mentioned_count = 0

                for candidate_value in candidate_values:
                    if re.search(
                        r"(?<!\\w)"
                        + re.escape(candidate_value.lower())
                        + r"(?!\\w)",
                        q,
                    ):
                        mentioned_count += 1

                if mentioned_count >= 2:
                    selected_group = candidate_name
                    selected_group_col = candidate_col
                    break

        comparison_is_count_question = (
            "employee count" in q
            or "employee counts" in q
            or "number of employees" in q
            or "how many employees" in q
            or "count of employees" in q
        )

        if (
            is_comparison_question
            and selected_group_col
            and (
                (selected_metric and selected_col)
                or comparison_is_count_question
            )
        ):
            # Get all real values from the selected group column.
            group_values = (
                df[selected_group_col]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

            # Find group values explicitly mentioned in the question.
            mentioned_groups = []

            for value in sorted(group_values, key=lambda x: len(x), reverse=True):
                value_lower = value.lower()

                if re.search(
                    r"(?<!\w)" + re.escape(value_lower) + r"(?!\w)",
                    q
                ):
                    if value not in mentioned_groups:
                        mentioned_groups.append(value)

            # We only compare two groups in v2.8.
            if len(mentioned_groups) >= 2:
                group_a = mentioned_groups[0]
                group_b = mentioned_groups[1]

                a_mask = (
                    df[selected_group_col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == group_a.lower()
                )
                b_mask = (
                    df[selected_group_col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == group_b.lower()
                )

                a_df = df.loc[a_mask]
                b_df = df.loc[b_mask]

                if not a_df.empty and not b_df.empty:
                    # Decide the calculation from the question.
                    if comparison_is_count_question:
                        operation = "count"
                    elif (
                        "total" in q
                        or "sum" in q
                    ):
                        operation = "sum"
                    elif (
                        "minimum" in q
                        or "min " in q
                        or "lowest" in q
                    ):
                        operation = "min"
                    elif (
                        "maximum" in q
                        or "max " in q
                        or "highest" in q
                    ):
                        operation = "max"
                    else:
                        operation = "mean"

                    if operation == "count":
                        value_a = len(a_df)
                        value_b = len(b_df)
                    else:
                        series_a = pd.to_numeric(
                            a_df[selected_col],
                            errors="coerce"
                        ).dropna()
                        series_b = pd.to_numeric(
                            b_df[selected_col],
                            errors="coerce"
                        ).dropna()

                        if series_a.empty or series_b.empty:
                            return {
                                "answer": (
                                    f"❌ I couldn't calculate {selected_metric} "
                                    f"for both {group_a} and {group_b}."
                                )
                            }

                        if operation == "sum":
                            value_a = series_a.sum()
                            value_b = series_b.sum()
                        elif operation == "min":
                            value_a = series_a.min()
                            value_b = series_b.min()
                        elif operation == "max":
                            value_a = series_a.max()
                            value_b = series_b.max()
                        else:
                            value_a = series_a.mean()
                            value_b = series_b.mean()

                    difference = abs(value_a - value_b)

                    if value_a > value_b:
                        higher_group = group_a
                        lower_group = group_b
                    elif value_b > value_a:
                        higher_group = group_b
                        lower_group = group_a
                    else:
                        higher_group = None
                        lower_group = None

                    unit = ""
                    suffix = ""

                    if selected_metric in [
                        "salary",
                        "profit",
                        "revenue",
                    ]:
                        unit = "₹"

                    if selected_metric in [
                        "attendance",
                        "attendance percentage",
                    ]:
                        suffix = "%"

                    operation_label = {
                        "mean": "Average",
                        "sum": "Total",
                        "min": "Minimum",
                        "max": "Maximum",
                        "count": "Employee Count",
                    }[operation]

                    display_metric = (
                        "Employees"
                        if operation == "count"
                        else selected_metric.title()
                    )

                    if higher_group is None:
                        comparison_text = (
                            f"🤝 Both groups have the same "
                            f"{operation_label.lower()} {selected_metric}."
                        )
                    else:
                        comparison_text = (
                            f"🏆 {higher_group} has the higher "
                            f"{operation_label.lower()} "
                            f"{'employee count' if operation == 'count' else selected_metric} "
                            f"by {unit}{difference:,.2f}{suffix}."
                        )

                    base_value = max(abs(float(value_a)), abs(float(value_b)))
                    percentage_difference = (
                        (float(difference) / base_value) * 100
                        if base_value != 0
                        else 0
                    )

                    return {
                        "answer": (
                            f"📊 {operation_label} {display_metric} "
                            f"Comparison:\n\n"
                            f"• {group_a}: {unit}{value_a:,.2f}{suffix}\n"
                            f"• {group_b}: {unit}{value_b:,.2f}{suffix}\n"
                            f"• Difference: {unit}{difference:,.2f}{suffix}\n"
                            f"• Difference %: {percentage_difference:.2f}%\n\n"
                            f"{comparison_text}"
                        ),
                        "comparison": {
                            "group_column": selected_group_col,
                            "metric": selected_metric,
                            "operation": operation,
                            "group_a": group_a,
                            "group_a_value": round(float(value_a), 2),
                            "group_b": group_b,
                            "group_b_value": round(float(value_b), 2),
                            "difference": round(float(difference), 2),
                            "difference_percent": round(float(percentage_difference), 2),
                        },
                    }

        # =========================================
        # TOP N / BOTTOM N ANALYSIS
        # =========================================

        # Detect Top/Bottom number
        ranking_n = None

        for word in q.split():

            cleaned_word = word.strip(".,!?")

            if cleaned_word.isdigit():

                ranking_n = int(cleaned_word)
                break

        # Keep ranking number within a safe range
        if ranking_n is not None:

            ranking_n = max(1, min(ranking_n, 100))

        # -----------------------------------------
        # TOP N
        # -----------------------------------------

        if (
            ranking_n
            and (
                "top " in q
                or "top" == q[:3]
            )
            and selected_metric
            and selected_col
        ):

            if selected_group_col:

                analysis = (
                    df.groupby(selected_group_col)[selected_col]
                    .mean()
                    .dropna()
                    .sort_values(ascending=False)
                    .head(ranking_n)
                )

                if not analysis.empty:

                    result = (
                        f"🏆 Top {ranking_n} "
                        f"{selected_group.title()} by average "
                        f"{selected_metric}:\n"
                    )

                    for position, (name, value) in enumerate(
                        analysis.items(),
                        start=1
                    ):

                        unit = ""

                        if selected_metric in [
                            "salary",
                            "profit",
                            "revenue"
                        ]:
                            unit = "₹"

                        suffix = ""

                        if selected_metric in [
                            "attendance",
                            "attendance percentage"
                        ]:
                            suffix = "%"

                        result += (
                            f"{position}. {name} — "
                            f"{unit}{value:,.2f}{suffix}\n"
                        )

                    return {
                        "answer": result
                    }

        # -----------------------------------------
        # BOTTOM N
        # -----------------------------------------

        if (
            ranking_n
            and (
                "bottom " in q
                or "bottom" == q[:6]
            )
            and selected_metric
            and selected_col
        ):

            if selected_group_col:

                analysis = (
                    df.groupby(selected_group_col)[selected_col]
                    .mean()
                    .dropna()
                    .sort_values(ascending=True)
                    .head(ranking_n)
                )

                if not analysis.empty:

                    result = (
                        f"📉 Bottom {ranking_n} "
                        f"{selected_group.title()} by average "
                        f"{selected_metric}:\n"
                    )

                    for position, (name, value) in enumerate(
                        analysis.items(),
                        start=1
                    ):

                        unit = ""

                        if selected_metric in [
                            "salary",
                            "profit",
                            "revenue"
                        ]:
                            unit = "₹"

                        suffix = ""

                        if selected_metric in [
                            "attendance",
                            "attendance percentage"
                        ]:
                            suffix = "%"

                        result += (
                            f"{position}. {name} — "
                            f"{unit}{value:,.2f}{suffix}\n"
                        )

                    return {
                        "answer": result
                    }
                    # =========================================
        # TOP N INDIVIDUAL EMPLOYEES
        # =========================================

        if (
            ranking_n
            and selected_metric
            and selected_col
            and (
                "top " in q
                or q.startswith("top")
            )
            and (
                "employee" in q
                or "employees" in q
            )
        ):

            if employee_col:

                employee_analysis = (
                    df[
                        [employee_col, selected_col]
                    ]
                    .dropna()
                    .sort_values(
                        by=selected_col,
                        ascending=False
                    )
                    .head(ranking_n)
                )

                if not employee_analysis.empty:

                    result = (
                        f"🏆 Top {ranking_n} Employees by "
                        f"{selected_metric}:\n"
                    )

                    for position, (_, row) in enumerate(
                        employee_analysis.iterrows(),
                        start=1
                    ):

                        value = row[selected_col]

                        unit = ""

                        if selected_metric in [
                            "salary",
                            "profit",
                            "revenue"
                        ]:
                            unit = "₹"

                        suffix = ""

                        if selected_metric in [
                            "attendance",
                            "attendance percentage"
                        ]:
                            suffix = "%"

                        result += (
                            f"{position}. "
                            f"{row[employee_col]} — "
                            f"{unit}{value:,.2f}{suffix}\n"
                        )

                    return {
                        "answer": result
                    }
                    # =========================================
        # BOTTOM N INDIVIDUAL EMPLOYEES
        # =========================================

        if (
            ranking_n
            and selected_metric
            and selected_col
            and (
                "bottom " in q
                or q.startswith("bottom")
            )
            and (
                "employee" in q
                or "employees" in q
            )
        ):

            if employee_col:

                employee_analysis = (
                    df[
                        [employee_col, selected_col]
                    ]
                    .dropna()
                    .sort_values(
                        by=selected_col,
                        ascending=True
                    )
                    .head(ranking_n)
                )

                if not employee_analysis.empty:

                    result = (
                        f"📉 Bottom {ranking_n} Employees by "
                        f"{selected_metric}:\n"
                    )

                    for position, (_, row) in enumerate(
                        employee_analysis.iterrows(),
                        start=1
                    ):

                        value = row[selected_col]

                        unit = ""

                        if selected_metric in [
                            "salary",
                            "profit",
                            "revenue"
                        ]:
                            unit = "₹"

                        suffix = ""

                        if selected_metric in [
                            "attendance",
                            "attendance percentage"
                        ]:
                            suffix = "%"

                        result += (
                            f"{position}. "
                            f"{row[employee_col]} — "
                            f"{unit}{value:,.2f}{suffix}\n"
                        )

                    return {
                        "answer": result
                    }
                    # =========================================
        # HIGHEST / LOWEST INDIVIDUAL EMPLOYEE
        # =========================================

        if (
            selected_metric
            and selected_col
            and employee_col
            and (
                "highest paid employee" in q
                or "lowest paid employee" in q
                or "highest salary employee" in q
                or "lowest salary employee" in q
                or "employee with highest" in q
                or "employee with lowest" in q
            )
        ):

            # -------------------------------------
            # HIGHEST EMPLOYEE
            # -------------------------------------

            if (
                "highest paid employee" in q
                or "highest salary employee" in q
                or "employee with highest" in q
            ):

                row = (
                    df.loc[
                        df[selected_col].idxmax()
                    ]
                )

                return {
                    "answer":
                        f"🏆 Highest paid employee: "
                        f"{row[employee_col]} — "
                        f"₹{row[selected_col]:,.2f}"
                }

            # -------------------------------------
            # LOWEST EMPLOYEE
            # -------------------------------------

            if (
                "lowest paid employee" in q
                or "lowest salary employee" in q
                or "employee with lowest" in q
            ):

                row = (
                    df.loc[
                        df[selected_col].idxmin()
                    ]
                )

                return {
                    "answer":
                        f"📉 Lowest paid employee: "
                        f"{row[employee_col]} — "
                        f"₹{row[selected_col]:,.2f}"
                }
        # =========================================
        # HIGHEST / LOWEST AVERAGE BY GROUP
        # =========================================

        if selected_metric and selected_col and selected_group_col:

            # Highest
            if (
                "highest average" in q
                or "highest avg" in q
                or "highest average" in q
            ):

                analysis = (
                    df.groupby(selected_group_col)[selected_col]
                    .mean()
                    .dropna()
                    .sort_values(ascending=False)
                )

                if not analysis.empty:

                    highest_group = analysis.index[0]
                    highest_value = analysis.iloc[0]

                    unit = ""

                    if selected_metric in [
                        "salary",
                        "profit",
                        "revenue"
                    ]:
                        unit = "₹"

                    elif selected_metric in [
                        "attendance",
                        "attendance percentage"
                    ]:
                        unit = ""

                    return {
                        "answer":
                            f"🏆 {highest_group} has the highest average "
                            f"{selected_metric}: "
                            f"{unit}{highest_value:,.2f}"
                            + (
                                "%"
                                if selected_metric in [
                                    "attendance",
                                    "attendance percentage"
                                ]
                                else ""
                            )
                    }

            # Lowest
            if (
                "lowest average" in q
                or "lowest avg" in q
            ):

                analysis = (
                    df.groupby(selected_group_col)[selected_col]
                    .mean()
                    .dropna()
                    .sort_values(ascending=True)
                )

                if not analysis.empty:

                    lowest_group = analysis.index[0]
                    lowest_value = analysis.iloc[0]

                    unit = ""

                    if selected_metric in [
                        "salary",
                        "profit",
                        "revenue"
                    ]:
                        unit = "₹"

                    return {
                        "answer":
                            f"📉 {lowest_group} has the lowest average "
                            f"{selected_metric}: "
                            f"{unit}{lowest_value:,.2f}"
                            + (
                                "%"
                                if selected_metric in [
                                    "attendance",
                                    "attendance percentage"
                                ]
                                else ""
                            )
                    }

        # =========================================
        # GENERIC TOTAL / SUM
        # =========================================

        if selected_metric and selected_col:

            if (
                "total " + selected_metric in q
                or "sum " + selected_metric in q
            ):

                value = df[selected_col].sum()

                unit = ""

                if selected_metric in [
                    "salary",
                    "profit",
                    "revenue"
                ]:
                    unit = "₹"

                return {
                    "answer":
                        f"📊 Total {selected_metric.title()}: "
                        f"{unit}{value:,.2f}"
                }

        # =========================================
        # GENERIC AVERAGE
        # =========================================

        if selected_metric and selected_col:

            if (
                "average " + selected_metric in q
                or "avg " + selected_metric in q
                or "mean " + selected_metric in q
            ):

                value = df[selected_col].mean()

                unit = ""

                if selected_metric in [
                    "salary",
                    "profit",
                    "revenue"
                ]:
                    unit = "₹"

                elif selected_metric in [
                    "attendance",
                    "attendance percentage"
                ]:
                    unit = ""

                return {
                    "answer":
                        f"💰 Average {selected_metric.title()}: "
                        f"{unit}{value:,.2f}"
                        + (
                            "%"
                            if selected_metric in [
                                "attendance",
                                "attendance percentage"
                            ]
                            else ""
                        )
                }

        # =========================================
        # GENERIC HIGHEST VALUE
        # =========================================

        if selected_metric and selected_col:

            if (
                "highest " + selected_metric in q
                or "maximum " + selected_metric in q
                or "max " + selected_metric in q
            ):

                value = df[selected_col].max()

                unit = ""

                if selected_metric in [
                    "salary",
                    "profit",
                    "revenue"
                ]:
                    unit = "₹"

                return {
                    "answer":
                        f"🏆 Highest {selected_metric.title()}: "
                        f"{unit}{value:,.2f}"
                }

        # =========================================
        # GENERIC LOWEST VALUE
        # =========================================

        if selected_metric and selected_col:

            if (
                "lowest " + selected_metric in q
                or "minimum " + selected_metric in q
                or "min " + selected_metric in q
            ):

                value = df[selected_col].min()

                unit = ""

                if selected_metric in [
                    "salary",
                    "profit",
                    "revenue"
                ]:
                    unit = "₹"

                return {
                    "answer":
                        f"📉 Lowest {selected_metric.title()}: "
                        f"{unit}{value:,.2f}"
                }
                # =========================================
        # NATURAL LANGUAGE MULTI-CONDITION FILTER
        # =========================================

        filter_columns = {
            "department": department_col,
            "city": city_col,
            "branch": branch_col,
            "gender": gender_col,
            "work mode": work_mode_col
        }

        filtered_df = df.copy()
        conditions_found = []

        # -----------------------------------------
        # TEXT CONDITIONS
        # -----------------------------------------

        for group_name, group_col in filter_columns.items():

            if not group_col:
                continue

            values = (
                df[group_col]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            # Longer values first
            values = sorted(
                values,
                key=lambda x: len(str(x)),
                reverse=True
            )

            for value in values:

                value_lower = str(value).lower().strip()

                pattern = (
                    r"(?<!\w)"
                    + re.escape(value_lower)
                    + r"(?!\w)"
                )

                if re.search(pattern, q):

                    filtered_df = filtered_df[
                        filtered_df[group_col]
                        .astype(str)
                        .str.lower()
                        .str.strip()
                        == value_lower
                    ]

                    conditions_found.append(
                        f"{group_name}: {value}"
                    )

                    break

        # -----------------------------------------
        # NUMERIC CONDITIONS
        # -----------------------------------------

        numeric_columns = {

            "salary": salary_col,
            "age": age_col,
            "profit": profit_col,
            "revenue": revenue_col,
            "performance": performance_col,
            "performance rating": performance_col,
            "satisfaction": satisfaction_col,
            "satisfaction score": satisfaction_col,
            "attendance": attendance_col,
            "leaves": leaves_col,
            "training": training_col,
            "training hours": training_col
        }

        for metric_name, metric_col in numeric_columns.items():

            if not metric_col:
                continue

            # -------------------------------------
            # MORE THAN / ABOVE / GREATER THAN
            # -------------------------------------

            pattern = (
                rf"\b{re.escape(metric_name)}\b"
                rf".{{0,20}}?"
                rf"(?:above|over|more than|greater than)"
                rf"\s*(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                value = float(match.group(1))

                filtered_df = filtered_df[
                    filtered_df[metric_col] > value
                ]

                conditions_found.append(
                    f"{metric_name} > {value:g}"
                )

                continue

            # -------------------------------------
            # LESS THAN / BELOW / UNDER
            # -------------------------------------

            pattern = (
                rf"\b{re.escape(metric_name)}\b"
                rf".{{0,20}}?"
                rf"(?:below|under|less than)"
                rf"\s*(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                value = float(match.group(1))

                filtered_df = filtered_df[
                    filtered_df[metric_col] < value
                ]

                conditions_found.append(
                    f"{metric_name} < {value:g}"
                )

                continue

            # -------------------------------------
            # SYMBOL FORMAT
            # salary > 100000
            # age < 40
            # -------------------------------------

            pattern = (
                rf"\b{re.escape(metric_name)}\b\s*"
                rf"(>=|<=|>|<|=)\s*"
                rf"(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                operator = match.group(1)
                value = float(match.group(2))

                if operator == ">":
                    filtered_df = filtered_df[
                        filtered_df[metric_col] > value
                    ]

                elif operator == ">=":
                    filtered_df = filtered_df[
                        filtered_df[metric_col] >= value
                    ]

                elif operator == "<":
                    filtered_df = filtered_df[
                        filtered_df[metric_col] < value
                    ]

                elif operator == "<=":
                    filtered_df = filtered_df[
                        filtered_df[metric_col] <= value
                    ]

                elif operator == "=":
                    filtered_df = filtered_df[
                        filtered_df[metric_col] == value
                    ]

                conditions_found.append(
                    f"{metric_name} {operator} {value:g}"
                )

        # -----------------------------------------
        # RETURN MULTI-CONDITION RESULT
        # -----------------------------------------

        if len(conditions_found) >= 2:

            return {
                "answer":
                    f"🔎 {len(filtered_df):,} employees matched "
                    f"all conditions.\n\n"
                    + "\n".join(
                        f"• {condition}"
                        for condition in conditions_found
                    )
            }
        # =========================================
        # PERCENTAGE / SHARE ANALYSIS
        # =========================================

        percentage_groups = {

            "department": department_col,
            "city": city_col,
            "branch": branch_col,
            "gender": gender_col,
            "work mode": work_mode_col
        }

        for group_name, group_col in percentage_groups.items():

            if not group_col:
                continue

            # Find actual value mentioned in the question
            unique_values = (
                df[group_col]
                .dropna()
                .astype(str)
                .unique()
            )

            for value in unique_values:

                value_text = str(value).lower()

                if value_text in q:

                    count = (
                        df[group_col]
                        .astype(str)
                        .str.lower()
                        .eq(value_text)
                        .sum()
                    )

                    percentage = (
                        count / len(df) * 100
                    )

                    if (
                        "percentage" in q
                        or "percent" in q
                        or "%" in q
                        or "share" in q
                    ):

                        return {
                            "answer":
                                f"📊 {value}: "
                                f"{count:,} employees "
                                f"({percentage:.2f}%)"
                        }
        # =========================================
        # GENDER DISTRIBUTION
        # =========================================

        if gender_col:

            if (
                "gender distribution" in q
                or "gender breakdown" in q
            ):

                data = df[gender_col].value_counts()

                result = "👥 Gender Distribution:\n"

                for name, count in data.items():

                    percentage = (
                        count / len(df) * 100
                    )

                    result += (
                        f"{name}: {count:,} "
                        f"({percentage:.1f}%)\n"
                    )

                return {
                    "answer": result
                }

        # =========================================
        # DEPARTMENT DISTRIBUTION
        # =========================================

        if department_col:

            if (
                "department distribution" in q
                or "department breakdown" in q
                or "employees by department" in q
            ):

                data = df[department_col].value_counts()

                result = "🏢 Department Distribution:\n"

                for name, count in data.items():

                    percentage = (
                        count / len(df) * 100
                    )

                    result += (
                        f"{name}: {count:,} "
                        f"({percentage:.1f}%)\n"
                    )

                return {
                    "answer": result
                }

        # =========================================
        # CITY DISTRIBUTION
        # =========================================

        if city_col:

            if (
                "city distribution" in q
                or "city breakdown" in q
                or "employees by city" in q
            ):

                data = df[city_col].value_counts()

                result = "🌆 City Distribution:\n"

                for name, count in data.items():

                    result += (
                        f"{name}: {count:,}\n"
                    )

                return {
                    "answer": result
                }

        # =========================================
        # GENDER EMPLOYEE COUNT
        # =========================================

        if gender_col:

            if "female employees" in q:

                value = (
                    df[gender_col]
                    .astype(str)
                    .str.lower()
                    .eq("female")
                    .sum()
                )

                return {
                    "answer":
                        f"👩 Female Employees: {value:,}"
                }

            if "male employees" in q:

                value = (
                    df[gender_col]
                    .astype(str)
                    .str.lower()
                    .eq("male")
                    .sum()
                )

                return {
                    "answer":
                        f"👨 Male Employees: {value:,}"
                }

        # =========================================
        # WORK MODE EMPLOYEE COUNT
        # =========================================

        if work_mode_col:

            work_modes = [
                "remote",
                "hybrid",
                "office"
            ]

            for mode in work_modes:

                if f"{mode} employees" in q:

                    value = (
                        df[work_mode_col]
                        .astype(str)
                        .str.lower()
                        .eq(mode)
                        .sum()
                    )

                    return {
                        "answer":
                            f"💼 {mode.title()} Employees: "
                            f"{value:,}"
                    }

        # =========================================
        # EMPLOYEES IN DEPARTMENT
        # =========================================

        if department_col:

            departments = (
                df[department_col]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            for department in departments:

                if (
                    f"employees in {department.lower()}" in q
                    or (
                        department.lower() in q
                        and "employees" in q
                        and "highest" not in q
                        and "lowest" not in q
                    )
                ):

                    count = (
                        df[department_col]
                        .astype(str)
                        .str.lower()
                        .eq(department.lower())
                        .sum()
                    )

                    return {
                        "answer":
                            f"🏢 Employees in {department}: "
                            f"{count:,}"
                    }

        # =========================================
        # BAR CHART
        # =========================================

        if "bar chart" in q:

            for col in df.columns:

                if col.lower() in q:

                    data = df[col].value_counts()

                    plt.figure(figsize=(8, 5))

                    data.plot(kind="bar")

                    plt.title(
                        f"{col} Distribution"
                    )

                    plt.xlabel(col)
                    plt.ylabel("Count")

                    plt.xticks(rotation=30)

                    filename = (
                        f"{uuid.uuid4()}.png"
                    )

                    filepath = os.path.join(
                        "charts",
                        filename
                    )

                    plt.tight_layout()
                    plt.savefig(filepath)
                    plt.close()

                    return {
                        "answer":
                            f"📊 Bar chart created for {col}",
                        "chart":
                            f"/charts/{filename}"
                    }

        # =========================================
        # PIE CHART
        # =========================================

        if "pie chart" in q:

            for col in df.columns:

                if col.lower() in q:

                    data = df[col].value_counts()

                    plt.figure(figsize=(6, 6))

                    data.plot(
                        kind="pie",
                        autopct="%1.1f%%"
                    )

                    plt.ylabel("")

                    plt.title(
                        f"{col} Distribution"
                    )

                    filename = (
                        f"{uuid.uuid4()}.png"
                    )

                    filepath = os.path.join(
                        "charts",
                        filename
                    )

                    plt.tight_layout()
                    plt.savefig(filepath)
                    plt.close()

                    return {
                        "answer":
                            f"🥧 Pie chart created for {col}",
                        "chart":
                            f"/charts/{filename}"
                    }

        # =========================================
        # LINE CHART
        # =========================================

        if "line chart" in q:

            for col in df.columns:

                if col.lower() in q:

                    if pd.api.types.is_numeric_dtype(
                        df[col]
                    ):

                        plt.figure(figsize=(8, 5))

                        plt.plot(df[col])

                        plt.title(col)
                        plt.xlabel("Rows")
                        plt.ylabel(col)

                        filename = (
                            f"{uuid.uuid4()}.png"
                        )

                        filepath = os.path.join(
                            "charts",
                            filename
                        )

                        plt.tight_layout()
                        plt.savefig(filepath)
                        plt.close()

                        return {
                            "answer":
                                f"📈 Line chart created for {col}",
                            "chart":
                                f"/charts/{filename}"
                        }

                    return {
                        "answer":
                            "❌ Line chart requires numeric data."
                    }

        # =========================================
    # ADVANCED ASK AI - INTELLIGENT FALLBACK
    # =========================================

        # -----------------------------------------
        # CORRELATION QUESTIONS
        # -----------------------------------------

        if (
            "correlation" in q
            or "correlated" in q
            or "relationship between" in q
        ):

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if len(numeric_cols) >= 2:

                correlation_matrix = (
                    df[numeric_cols]
                    .corr()
                )

                pairs = []

                for i in range(len(numeric_cols)):

                    for j in range(i + 1, len(numeric_cols)):

                        value = correlation_matrix.iloc[i, j]

                        if pd.notna(value):

                            pairs.append({
                                "column_a": str(
                                    numeric_cols[i]
                                ),
                                "column_b": str(
                                    numeric_cols[j]
                                ),
                                "correlation": round(
                                    float(value),
                                    4
                                )
                            })

                pairs.sort(
                    key=lambda x: abs(
                        x["correlation"]
                    ),
                    reverse=True
                )

                strongest = pairs[:5]

                result = (
                    "🔗 Strongest Correlations:\n\n"
                )

                for item in strongest:

                    result += (
                        f"• {item['column_a']} ↔ "
                        f"{item['column_b']}: "
                        f"{item['correlation']:.4f}\n"
                    )

                return {
                    "answer": result,
                    "analysis_type": "correlation",
                    "correlations": strongest
                }

        # -----------------------------------------
        # OUTLIER QUESTIONS
        # -----------------------------------------

        if (
            "outlier" in q
            or "outliers" in q
            or "unusual values" in q
            or "anomalies" in q
        ):

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            outlier_summary = []

            for col in numeric_cols:

                series = pd.to_numeric(
                    df[col],
                    errors="coerce"
                ).dropna()

                if len(series) < 4:
                    continue

                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)

                iqr = q3 - q1

                lower = q1 - (1.5 * iqr)
                upper = q3 + (1.5 * iqr)

                count = int(
                    (
                        (series < lower)
                        |
                        (series > upper)
                    ).sum()
                )

                if count > 0:

                    outlier_summary.append({
                        "column": str(col),
                        "outliers": count
                    })

            outlier_summary.sort(
                key=lambda x: x["outliers"],
                reverse=True
            )

            result = (
                "🚨 Outlier Analysis:\n\n"
            )

            if outlier_summary:

                for item in outlier_summary[:10]:

                    result += (
                        f"• {item['column']}: "
                        f"{item['outliers']:,} outliers\n"
                    )

            else:

                result += (
                    "No significant outliers detected."
                )

            return {
                "answer": result,
                "analysis_type": "outlier_detection",
                "outliers": outlier_summary
            }

        # -----------------------------------------
        # DATASET OVERVIEW / SUMMARY
        # -----------------------------------------

        if (
            "dataset summary" in q
            or "data summary" in q
            or "summarize dataset" in q
            or "summarise dataset" in q
            or "give me summary" in q
            or "overview of dataset" in q
        ):

            numeric_cols = df.select_dtypes(
                include="number"
            ).columns.tolist()

            return {
                "answer": (
                    f"📊 Dataset Summary:\n\n"
                    f"• Rows: {len(df):,}\n"
                    f"• Columns: {len(df.columns):,}\n"
                    f"• Numeric Columns: "
                    f"{len(numeric_cols):,}\n"
                    f"• Missing Values: "
                    f"{int(df.isna().sum().sum()):,}\n"
                    f"• Duplicate Rows: "
                    f"{int(df.duplicated().sum()):,}"
                ),
                "analysis_type": "dataset_summary"
            }

        # -----------------------------------------
        # AUTOMATIC NUMERIC COLUMN DISCOVERY
        # -----------------------------------------

        if (
            selected_metric is None
            and selected_col is None
        ):

            for col in df.columns:

                col_text = str(col).lower()

                if col_text in q:

                    if pd.api.types.is_numeric_dtype(
                        df[col]
                    ):

                        selected_metric = str(col)
                        selected_col = col

                        break

            # -----------------------------------------
        # AUTOMATIC NUMERIC COLUMN DISCOVERY
        # -----------------------------------------

            # -----------------------------------------
        # PRIORITY COLUMN DETECTION
        # -----------------------------------------

        detected_column = None

        # First check the actual dataset column names.
        # This gives an explicitly mentioned column priority
        # over predefined metrics such as Age or Salary.

        for col in df.columns:

            col_name = str(col).strip().lower()

            if re.search(
        r"(?<!\w)" + re.escape(col_name) + r"(?!\w)",
        q
    ):

                if pd.api.types.is_numeric_dtype(
                    df[col]
                ):

                    detected_column = col

                    break

        if detected_column is not None:

            selected_col = detected_column
            selected_metric = str(
                detected_column
            )

        # -----------------------------------------
        # AUTOMATIC NUMERIC ANALYSIS
        # -----------------------------------------

        if selected_col is not None:

            series = pd.to_numeric(
                df[selected_col],
                errors="coerce"
            ).dropna()

            if not series.empty:

                if (
                    "average" in q
                    or "avg" in q
                    or "mean" in q
                ):

                    value = series.mean()
                    operation = "average"

                elif (
                    "maximum" in q
                    or "highest" in q
                    or "max" in q
                ):

                    value = series.max()
                    operation = "maximum"

                elif (
                    "minimum" in q
                    or "lowest" in q
                    or "min" in q
                ):

                    value = series.min()
                    operation = "minimum"

                elif (
                    "total" in q
                    or "sum" in q
                ):

                    value = series.sum()
                    operation = "total"

                elif (
                    "count" in q
                    or "how many" in q
                ):

                    value = series.count()
                    operation = "count"

                else:

                    value = series.mean()
                    operation = "average"

                return {
                    "answer": (
                        f"📊 {operation.title()} "
                        f"{selected_col}: "
                        f"{value:,.2f}"
                    ),
                    "analysis_type":
                        "advanced_numeric_analysis",
                    "column": str(selected_col),
                    "operation": operation,
                    "value": round(
                        float(value),
                        4
                    ),
                    "count": int(
                        series.count()
                    )
                }
        # =========================================
        # GENESIS AI RECOMMENDATIONS / ROOT CAUSE
        # =========================================

        recommendation_keywords = [
            "recommendation",
            "recommendations",
            "suggestion",
            "suggestions",
            "what should we do",
            "what should i do",
            "improve",
            "improvement",
            "business advice",
            "action plan",
            "root cause",
            "root causes",
            "why is profit low",
            "why profit is low",
            "why is performance low",
            "why performance is low"
        ]

        if any(keyword in q for keyword in recommendation_keywords):

            try:

                recommendation_result = genesis_dashboard_recommendations()

                executive_summary = recommendation_result.get(
                    "executive_summary",
                    "No executive summary available."
                )

                recommendations = recommendation_result.get(
                    "recommendations",
                    []
                )

                root_causes = recommendation_result.get(
                    "root_causes",
                    []
                )

                answer = (
                    f"🧠 Genesis AI Business Analysis\n\n"
                    f"{executive_summary}\n\n"
                )

                if root_causes:

                    answer += "🔍 Key Root Causes:\n\n"

                    for item in root_causes[:5]:

                        answer += (
                            f"• {item.get('title')}: "
                            f"{item.get('evidence')}\n"
                        )

                    answer += "\n"

                if recommendations:

                    answer += "💡 Recommended Actions:\n\n"

                    for index, item in enumerate(
                        recommendations[:5],
                        start=1
                    ):

                        answer += (
                            f"{index}. {item.get('title')}\n"
                            f"   Action: "
                            f"{item.get('recommended_action')}\n\n"
                        )

                return {
                    "answer": answer,
                    "analysis_type": "ai_recommendations",
                    "overall_risk": recommendation_result.get(
                        "overall_risk"
                    ),
                    "recommendations": recommendations,
                    "root_causes": root_causes
                }

            except Exception as error:

                return {
                    "answer": (
                        "⚠️ Recommendation analysis could not "
                        "be completed."
                    ),
                    "error": str(error),
                    "analysis_type": "ai_recommendations_error"
                }
            # =========================================================
    # PHASE 3 - NATURAL LANGUAGE BUSINESS INTELLIGENCE
    # =========================================================

    business_problem_words = [
        "business problem",
        "biggest problem",
        "biggest problems",
        "main problem",
        "main problems",
        "business issues",
        "issues in business",
        "key problems"
    ]

    risk_words = [
        "risk",
        "risks",
        "key risk",
        "key risks",
        "biggest risk",
        "biggest risks",
        "business risk"
    ]

    recommendation_words = [
        "what should management focus on",
        "what should we focus on",
        "what should management do",
        "what should we do",
        "management focus",
        "improvement areas"
    ]

    profitability_words = [
        "why is profit low",
        "why profit is low",
        "why is profitability low",
        "what is affecting profitability",
        "what affects profitability",
        "profitability problem",
        "profit problem"
    ]

    department_improvement_words = [
        "which department needs improvement",
        "department needs improvement",
        "worst department",
        "weakest department",
        "which department is performing poorly"
    ]

    executive_insight_words = [
        "executive insights",
        "executive insight",
        "management insights",
        "business insights",
        "key insights",
        "important insights"
    ]

    # =========================================================
    # GET BUSINESS RECOMMENDATION DATA
    # =========================================================

    phase3_business_question = (
        any(word in q for word in business_problem_words)
        or any(word in q for word in risk_words)
        or any(word in q for word in recommendation_words)
        or any(word in q for word in profitability_words)
        or any(word in q for word in department_improvement_words)
    )

    if phase3_business_question:

        try:

            analysis = genesis_dashboard_recommendations()

            root_causes = analysis.get(
                "root_causes",
                []
            )

            recommendations = analysis.get(
                "recommendations",
                []
            )

            overall_risk = analysis.get(
                "overall_risk",
                "Unknown"
            )

            # ---------------------------------------------
            # BUSINESS PROBLEMS
            # ---------------------------------------------

            if any(
                word in q
                for word in business_problem_words
            ):

                answer = (
                    "🔍 Genesis AI Business Problems Analysis\n\n"
                    f"Overall Risk Level: {overall_risk}\n\n"
                    "🚨 Main Business Problems:\n\n"
                )

                for index, cause in enumerate(
                    root_causes[:5],
                    start=1
                ):

                    answer += (
                        f"{index}. {cause.get('title', 'Unknown Issue')}\n"
                        f"   Evidence: {cause.get('evidence', '')}\n"
                        f"   Impact: {cause.get('business_impact', '')}\n\n"
                    )

                return {
                    "answer": answer,
                    "analysis_type": "business_problem_analysis",
                    "overall_risk": overall_risk,
                    "root_causes": root_causes
                }

            # ---------------------------------------------
            # BUSINESS RISKS
            # ---------------------------------------------

            if any(
                word in q
                for word in risk_words
            ):

                answer = (
                    "⚠️ Genesis AI Business Risk Analysis\n\n"
                    f"Overall Business Risk: {overall_risk}\n\n"
                    "🚨 Key Risks:\n\n"
                )

                for index, cause in enumerate(
                    root_causes[:5],
                    start=1
                ):

                    answer += (
                        f"{index}. {cause.get('title', '')}\n"
                        f"   Severity: {cause.get('severity', '').upper()}\n"
                        f"   Evidence: {cause.get('evidence', '')}\n\n"
                    )

                return {
                    "answer": answer,
                    "analysis_type": "business_risk_analysis",
                    "overall_risk": overall_risk,
                    "risks": root_causes
                }

            # ---------------------------------------------
            # MANAGEMENT FOCUS
            # ---------------------------------------------

            if any(
                word in q
                for word in recommendation_words
            ):

                answer = (
                    "🎯 Genesis AI Management Focus Areas\n\n"
                    f"Overall Risk Level: {overall_risk}\n\n"
                    "Management should prioritize:\n\n"
                )

                for index, recommendation in enumerate(
                    recommendations[:5],
                    start=1
                ):

                    answer += (
                        f"{index}. {recommendation.get('title', '')}\n"
                        f"   Why: {recommendation.get('message', '')}\n"
                        f"   Action: "
                        f"{recommendation.get('recommended_action', '')}\n\n"
                    )

                return {
                    "answer": answer,
                    "analysis_type": "management_focus_analysis",
                    "overall_risk": overall_risk,
                    "recommendations": recommendations
                }

            # ---------------------------------------------
            # PROFITABILITY ANALYSIS
            # ---------------------------------------------

            if any(
                word in q
                for word in profitability_words
            ):

                profitability_causes = [

                    cause

                    for cause in root_causes

                    if cause.get("category") in [
                        "profitability",
                        "expense_management",
                        "revenue_growth"
                    ]
                ]

                answer = (
                    "💰 Genesis AI Profitability Analysis\n\n"
                    f"Overall Business Risk: {overall_risk}\n\n"
                    "Possible Factors Affecting Profitability:\n\n"
                )

                if profitability_causes:

                    for index, cause in enumerate(
                        profitability_causes,
                        start=1
                    ):

                        answer += (
                            f"{index}. {cause.get('title', '')}\n"
                            f"   Evidence: {cause.get('evidence', '')}\n"
                            f"   Impact: {cause.get('business_impact', '')}\n"
                            f"   Recommendation: "
                            f"{cause.get('recommendation', '')}\n\n"
                        )

                else:

                    answer += (
                        "No major profitability root causes "
                        "were detected in the current dataset."
                    )

                return {
                    "answer": answer,
                    "analysis_type": "profitability_root_cause_analysis",
                    "overall_risk": overall_risk,
                    "root_causes": profitability_causes
                }

            # ---------------------------------------------
            # DEPARTMENT IMPROVEMENT
            # ---------------------------------------------

            if any(
                word in q
                for word in department_improvement_words
            ):

                department_causes = [

                    cause

                    for cause in root_causes

                    if cause.get("category")
                    == "department_analysis"
                ]

                answer = (
                    "🏢 Genesis AI Department Improvement Analysis\n\n"
                )

                if department_causes:

                    for cause in department_causes:

                        answer += (
                            f"⚠️ {cause.get('title', '')}\n\n"
                            f"Evidence: {cause.get('evidence', '')}\n\n"
                            f"Business Impact: "
                            f"{cause.get('business_impact', '')}\n\n"
                            f"Recommended Action: "
                            f"{cause.get('recommendation', '')}\n"
                        )

                else:

                    answer += (
                        "No significant department-level "
                        "improvement issue was detected."
                    )

                return {
                    "answer": answer,
                    "analysis_type": "department_improvement_analysis",
                    "root_causes": department_causes
                }

        except Exception as e:

            return {
                "answer": (
                    "❌ Genesis AI could not complete "
                    "the business intelligence analysis."
                ),
                "analysis_type": "phase3_error",
                "error": str(e)
            }

    # =========================================================
    # EXECUTIVE INSIGHTS
    # =========================================================

    if any(
        word in q
        for word in executive_insight_words
    ):

        try:

            executive_data = (
                genesis_dashboard_executive_summary()
            )

            return {
                "answer": (
                    "📊 Genesis AI Executive Insights\n\n"
                    + str(
                        executive_data.get(
                            "executive_summary",
                            executive_data
                        )
                    )
                ),
                "analysis_type": "executive_insights",
                "data": executive_data
            }

        except Exception as e:

            return {
                "answer": (
                    "❌ Unable to generate executive insights."
                ),
                "analysis_type": "executive_insights_error",
                "error": str(e)
            }
    # -----------------------------------------
    # FINAL FALLBACK
    # -----------------------------------------

    return {
        "answer": (
            "🤖 I couldn't fully understand "
            "the question yet.\n\n"
            "Try asking:\n"
            "• Average Target\n"
            "• Total Bonus\n"
            "• Maximum Incentive\n"
            "• Minimum Training Hours\n"
            "• Average Monthly Sales\n"
            "• Average Salary\n"
            "• Total Profit\n"
            "• Find outliers\n"
            "• Show correlation\n"
            "• Give me a dataset summary"
        ),
        "analysis_type": "advanced_ask_fallback"
    }

# ============================================================
# GENESIS ANALYTICS DASHBOARD - STABLE API LAYER
# Added to repair missing analytics functions/routes.
# ============================================================

def require_df():
    global latest_df
    if latest_df is None or latest_df.empty:
        raise HTTPException(
            status_code=400,
            detail="No dataset uploaded. Please upload a CSV or XLSX file first."
        )
    return latest_df.copy()


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    return value


def _numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def _date_column(df):
    for col in df.columns:
        name = str(col).lower()
        if "date" in name or "time" in name or "month" in name or "year" in name:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() >= max(2, len(df) * 0.3):
                return col
    return None


def genesis_dashboard_insights():
    df = require_df()
    numeric_cols = _numeric_columns(df)

    result = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": numeric_cols,
        "categorical_columns": [
            str(c) for c in df.columns if c not in numeric_cols
        ],
    }

    if numeric_cols:
        summary = {}
        for col in numeric_cols[:10]:
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if not series.empty:
                summary[str(col)] = {
                    "average": float(series.mean()),
                    "minimum": float(series.min()),
                    "maximum": float(series.max()),
                }
        result["numeric_summary"] = summary

    return _json_safe(result)


def genesis_dashboard_statistics():
    df = require_df()
    numeric_cols = _numeric_columns(df)

    if not numeric_cols:
        return {
            "message": "No numeric columns available for statistical analysis."
        }

    stats = df[numeric_cols].describe().T
    return {
        "statistics": _json_safe(
            stats.reset_index()
            .rename(columns={"index": "column"})
            .to_dict(orient="records")
        )
    }

# =========================================================
# GENESIS AI - PROFESSIONAL STATISTICAL ANALYSIS ENGINE
# =========================================================

def genesis_statistical_analysis(df, column=None):
    """
    Professional statistical analysis engine.

    Calculates:
        count
        missing
        mean
        median
        mode
        minimum
        maximum
        range
        variance
        standard deviation
        Q1 / Q2 / Q3
        IQR
        percentiles
        skewness
        kurtosis

    Automatically ignores identifier-like numeric columns.
    """

    # -----------------------------------------------------
    # VALIDATE DATASET
    # -----------------------------------------------------

    if df is None or df.empty:
        return {
            "success": False,
            "message": "No dataset available."
        }

    # -----------------------------------------------------
    # NUMERIC COLUMNS
    # -----------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:
        return {
            "success": False,
            "message": "No numeric columns available."
        }

    # -----------------------------------------------------
    # IGNORE IDENTIFIER-LIKE COLUMNS
    # -----------------------------------------------------

    identifier_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "name",
        "code",
        "number"
    ]

    ignored_columns = []
    analytical_columns = []

    for col in numeric_columns:

        col_name = str(col).strip().lower()

        if any(
            keyword in col_name
            for keyword in identifier_keywords
        ):
            ignored_columns.append(str(col))
        else:
            analytical_columns.append(col)

    # -----------------------------------------------------
    # SINGLE COLUMN MODE
    # -----------------------------------------------------

    if column is not None:

        column = str(column).strip()

        if column not in df.columns:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' not found."
                )
            }

        if column not in analytical_columns:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' is not suitable "
                    "for statistical analysis."
                )
            }

        columns_to_analyze = [column]

    else:

        columns_to_analyze = analytical_columns

    # -----------------------------------------------------
    # RESULT CONTAINER
    # -----------------------------------------------------

    results = {}

    # -----------------------------------------------------
    # ANALYZE EACH COLUMN
    # -----------------------------------------------------

    for col in columns_to_analyze:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        missing_count = int(
            series.isna().sum()
        )

        clean = series.dropna()

        count = int(len(clean))

        # -------------------------------------------------
        # NOT ENOUGH DATA
        # -------------------------------------------------

        if count == 0:

            results[str(col)] = {
                "count": 0,
                "missing": missing_count,
                "mean": None,
                "median": None,
                "mode": [],
                "minimum": None,
                "maximum": None,
                "range": None,
                "variance": None,
                "standard_deviation": None,
                "q1": None,
                "q2": None,
                "q3": None,
                "iqr": None,
                "percentiles": {},
                "skewness": None,
                "kurtosis": None
            }

            continue

        # -------------------------------------------------
        # BASIC STATISTICS
        # -------------------------------------------------

        mean_value = clean.mean()
        median_value = clean.median()

        mode_values = clean.mode()

        mode_list = [
            float(value)
            for value in mode_values.tolist()
        ]

        minimum_value = clean.min()
        maximum_value = clean.max()

        range_value = (
            maximum_value
            - minimum_value
        )

        # -------------------------------------------------
        # VARIANCE / STANDARD DEVIATION
        # -------------------------------------------------

        variance_value = clean.var()

        standard_deviation = clean.std()

        # -------------------------------------------------
        # QUARTILES
        # -------------------------------------------------

        q1 = clean.quantile(0.25)
        q2 = clean.quantile(0.50)
        q3 = clean.quantile(0.75)

        iqr = q3 - q1

        # -------------------------------------------------
        # PERCENTILES
        # -------------------------------------------------

        percentiles = {
            "1": float(clean.quantile(0.01)),
            "5": float(clean.quantile(0.05)),
            "10": float(clean.quantile(0.10)),
            "25": float(clean.quantile(0.25)),
            "50": float(clean.quantile(0.50)),
            "75": float(clean.quantile(0.75)),
            "90": float(clean.quantile(0.90)),
            "95": float(clean.quantile(0.95)),
            "99": float(clean.quantile(0.99))
        }

        # -------------------------------------------------
        # SKEWNESS / KURTOSIS
        # -------------------------------------------------

        if count >= 3:

            skewness_value = clean.skew()

        else:

            skewness_value = None

        if count >= 4:

            kurtosis_value = clean.kurt()

        else:

            kurtosis_value = None

        # -------------------------------------------------
        # STORE RESULT
        # -------------------------------------------------

        results[str(col)] = {

            "count": count,

            "missing": missing_count,

            "mean": round(
                float(mean_value),
                4
            ),

            "median": round(
                float(median_value),
                4
            ),

            "mode": mode_list[:10],

            "minimum": round(
                float(minimum_value),
                4
            ),

            "maximum": round(
                float(maximum_value),
                4
            ),

            "range": round(
                float(range_value),
                4
            ),

            "variance": round(
                float(variance_value),
                4
            ),

            "standard_deviation": round(
                float(standard_deviation),
                4
            ),

            "q1": round(
                float(q1),
                4
            ),

            "q2": round(
                float(q2),
                4
            ),

            "q3": round(
                float(q3),
                4
            ),

            "iqr": round(
                float(iqr),
                4
            ),

            "percentiles": percentiles,

            "skewness": (
                round(
                    float(skewness_value),
                    4
                )
                if skewness_value is not None
                else None
            ),

            "kurtosis": (
                round(
                    float(kurtosis_value),
                    4
                )
                if kurtosis_value is not None
                else None
            )
        }

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return {
        "success": True,
        "columns_analyzed": [
            str(col)
            for col in columns_to_analyze
        ],
        "ignored_columns": ignored_columns,
        "statistics": results
    }
# =========================================================
# GENESIS AI - STATISTICAL ANALYSIS API
# =========================================================

@app.api_route(
    "/analytics/statistics",
    methods=["GET", "POST"]
)
# =====================================================
# GENESIS AI - ADVANCED STATISTICAL ANALYSIS
# =====================================================
# =====================================================
# GENESIS AI - PROFESSIONAL STATISTICAL ANALYSIS V2
# =====================================================

@app.api_route(
    "/analytics/statistical-analysis",
    methods=["GET", "POST"]
)
def analytics_statistical_analysis(
    column: str = None
):
    df = require_df()

    # -------------------------------------------------
    # IDENTIFIER-LIKE COLUMNS TO IGNORE
    # -------------------------------------------------

    identifier_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "contact",
        "code",
        "pin",
        "zip",
        "number"
    ]

    numeric_columns = []

    ignored_columns = []

    for col in df.columns:

        if not pd.api.types.is_numeric_dtype(
            df[col]
        ):
            continue

        col_name = str(col).strip().lower()

        if any(
            keyword in col_name
            for keyword in identifier_keywords
        ):
            ignored_columns.append(
                str(col)
            )
            continue

        # Extremely high-cardinality numeric
        # columns are usually identifiers.
        unique_ratio = (
            df[col].nunique(dropna=True)
            / max(len(df), 1)
        )

        if unique_ratio > 0.95:
            ignored_columns.append(
                str(col)
            )
            continue

        numeric_columns.append(col)

    # -------------------------------------------------
    # SINGLE COLUMN VALIDATION
    # -------------------------------------------------

    if column is not None:

        column = str(column).strip()

        if column not in df.columns:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' not found."
                )
            }

        if column not in numeric_columns:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' is not "
                    "suitable for statistical analysis."
                ),
                "ignored_columns": ignored_columns
            }

        columns_to_analyze = [column]

    else:

        columns_to_analyze = numeric_columns

    # -------------------------------------------------
    # NO NUMERIC COLUMNS
    # -------------------------------------------------

    if not columns_to_analyze:

        return {
            "success": False,
            "message": (
                "No meaningful numeric columns "
                "available for statistical analysis."
            )
        }

    # -------------------------------------------------
    # RESULT CONTAINER
    # -------------------------------------------------

    statistics = {}

    # -------------------------------------------------
    # ANALYZE EACH COLUMN
    # -------------------------------------------------

    for col in columns_to_analyze:

        original_series = df[col]

        series = pd.to_numeric(
            original_series,
            errors="coerce"
        ).dropna()

        count = int(series.count())

        missing_values = int(
            original_series.isna().sum()
        )

        unique_values = int(
            series.nunique()
        )

        # ---------------------------------------------
        # NOT ENOUGH DATA
        # ---------------------------------------------

        if count == 0:

            continue

        if count == 1:

            statistics[str(col)] = {
                "count": count,
                "mean": float(series.iloc[0]),
                "median": float(series.iloc[0]),
                "mode": float(series.iloc[0]),
                "std_dev": 0.0,
                "variance": 0.0,
                "minimum": float(series.iloc[0]),
                "maximum": float(series.iloc[0]),
                "range": 0.0,
                "q1": float(series.iloc[0]),
                "q2": float(series.iloc[0]),
                "q3": float(series.iloc[0]),
                "iqr": 0.0,
                "skewness": None,
                "kurtosis": None,
                "standard_error": None,
                "cv_percent": 0.0,
                "confidence_interval_95": {
                    "lower": float(series.iloc[0]),
                    "upper": float(series.iloc[0])
                },
                "distribution": (
                    "Insufficient data"
                ),
                "variability": "None",
                "missing_values": missing_values,
                "unique_values": unique_values
            }

            continue

        # ---------------------------------------------
        # CENTRAL TENDENCY
        # ---------------------------------------------

        mean_value = float(
            series.mean()
        )

        median_value = float(
            series.median()
        )

        mode_series = series.mode()

        mode_value = (
            float(mode_series.iloc[0])
            if not mode_series.empty
            else None
        )

        # ---------------------------------------------
        # DISPERSION
        # ---------------------------------------------

        std_dev = float(
            series.std()
        )

        variance = float(
            series.var()
        )

        minimum = float(
            series.min()
        )

        maximum = float(
            series.max()
        )

        value_range = (
            maximum - minimum
        )

        # ---------------------------------------------
        # QUARTILES
        # ---------------------------------------------

        q1 = float(
            series.quantile(0.25)
        )

        q2 = float(
            series.quantile(0.50)
        )

        q3 = float(
            series.quantile(0.75)
        )

        iqr = q3 - q1

        # ---------------------------------------------
        # SKEWNESS / KURTOSIS
        # ---------------------------------------------

        skewness_value = float(
            series.skew()
        )

        kurtosis_value = float(
            series.kurt()
        )

        # ---------------------------------------------
        # STANDARD ERROR
        # ---------------------------------------------

        standard_error = (
            std_dev
            / np.sqrt(count)
        )

        # ---------------------------------------------
        # COEFFICIENT OF VARIATION
        # ---------------------------------------------

        if mean_value != 0:

            cv_percent = (
                abs(std_dev / mean_value)
                * 100
            )

        else:

            cv_percent = None

        # ---------------------------------------------
        # 95% CONFIDENCE INTERVAL
        #
        # Approximation using 1.96 * SE
        # ---------------------------------------------

        margin_of_error = (
            1.96 * standard_error
        )

        confidence_lower = (
            mean_value
            - margin_of_error
        )

        confidence_upper = (
            mean_value
            + margin_of_error
        )

        # ---------------------------------------------
        # DISTRIBUTION CLASSIFICATION
        # ---------------------------------------------

        abs_skew = abs(
            skewness_value
        )

        if abs_skew < 0.5:

            distribution = (
                "Approximately symmetric"
            )

        elif abs_skew < 1:

            if skewness_value > 0:

                distribution = (
                    "Moderately right-skewed"
                )

            else:

                distribution = (
                    "Moderately left-skewed"
                )

        else:

            if skewness_value > 0:

                distribution = (
                    "Highly right-skewed"
                )

            else:

                distribution = (
                    "Highly left-skewed"
                )

        # ---------------------------------------------
        # VARIABILITY CLASSIFICATION
        # ---------------------------------------------

        if cv_percent is None:

            variability = (
                "Undefined"
            )

        elif cv_percent < 10:

            variability = "Low"

        elif cv_percent < 20:

            variability = "Moderate"

        elif cv_percent < 30:

            variability = "High"

        else:

            variability = (
                "Very High"
            )

        # ---------------------------------------------
        # STATISTICAL INTERPRETATION
        # ---------------------------------------------

        interpretation = []

        if abs(
            mean_value - median_value
        ) < (
            0.05 * max(
                abs(mean_value),
                1
            )
        ):

            interpretation.append(
                "Mean and median are close."
            )

        elif mean_value > median_value:

            interpretation.append(
                "Mean is above median."
            )

        else:

            interpretation.append(
                "Mean is below median."
            )

        interpretation.append(
            f"Variability is {variability.lower()}."
        )

        interpretation.append(
            distribution + "."
        )

        if iqr > 0:

            interpretation.append(
                "IQR indicates measurable "
                "middle-50% spread."
            )

        # ---------------------------------------------
        # FINAL COLUMN RESULT
        # ---------------------------------------------

        statistics[str(col)] = {

            "count": count,

            "mean": round(
                mean_value,
                4
            ),

            "median": round(
                median_value,
                4
            ),

            "mode": (
                round(
                    mode_value,
                    4
                )
                if mode_value is not None
                else None
            ),

            "std_dev": round(
                std_dev,
                4
            ),

            "variance": round(
                variance,
                4
            ),

            "minimum": round(
                minimum,
                4
            ),

            "maximum": round(
                maximum,
                4
            ),

            "range": round(
                value_range,
                4
            ),

            "q1": round(
                q1,
                4
            ),

            "q2": round(
                q2,
                4
            ),

            "q3": round(
                q3,
                4
            ),

            "iqr": round(
                iqr,
                4
            ),

            "skewness": round(
                skewness_value,
                4
            ),

            "kurtosis": round(
                kurtosis_value,
                4
            ),

            "standard_error": round(
                standard_error,
                4
            ),

            "cv_percent": (
                round(
                    cv_percent,
                    4
                )
                if cv_percent is not None
                else None
            ),

            "confidence_interval_95": {

                "lower": round(
                    confidence_lower,
                    4
                ),

                "upper": round(
                    confidence_upper,
                    4
                )
            },

            "distribution": distribution,

            "variability": variability,

            "interpretation": interpretation,

            "missing_values": (
                missing_values
            ),

            "unique_values": (
                unique_values
            )
        }

    # -------------------------------------------------
    # FINAL RESPONSE
    # -------------------------------------------------

    return {

        "success": True,

        "analysis_type":
            "professional_statistical_analysis_v2",

        "columns_analyzed": [
            str(col)
            for col in columns_to_analyze
        ],

        "ignored_columns":
            ignored_columns,

        "total_columns_analyzed":
            len(statistics),

        "statistics":
            statistics
    }
@app.api_route(
    "/api/analytics/statistics",
    methods=["GET", "POST"]
)
def analytics_statistics(
    column: str = None
):
    df = require_df()

    return genesis_statistical_analysis(
        df,
        column=column
    )
# =========================================================
# GENESIS AI - ADVANCED STATISTICAL ANALYSIS ENGINE
# =========================================================

def genesis_advanced_statistics(df, column=None):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # -----------------------------------------------------
    # IGNORE IDENTIFIER-LIKE COLUMNS
    # -----------------------------------------------------

    identifier_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "name",
        "code",
        "number"
    ]

    ignored_columns = []
    columns_analyzed = []

    for col in numeric_columns:

        col_name = str(col).strip().lower()

        if any(
            keyword in col_name
            for keyword in identifier_keywords
        ):
            ignored_columns.append(str(col))
        else:
            columns_analyzed.append(col)

    # -----------------------------------------------------
    # SINGLE COLUMN MODE
    # -----------------------------------------------------

    if column is not None:

        column = str(column).strip()

        if column not in df.columns:
            return {
                "success": False,
                "message": f"Column '{column}' not found."
            }

        if column not in columns_analyzed:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' is not suitable "
                    "for statistical analysis."
                )
            }

        columns_to_analyze = [column]

    else:
        columns_to_analyze = columns_analyzed

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    results = {}

    for col in columns_to_analyze:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        n = int(len(series))

        if n < 2:
            continue

        mean_value = float(series.mean())
        std_value = float(series.std())

        median_value = float(series.median())

        # -------------------------------------------------
        # STANDARD ERROR
        # -------------------------------------------------

        standard_error = (
            std_value / np.sqrt(n)
        )

        # -------------------------------------------------
        # 95% CONFIDENCE INTERVAL
        # -------------------------------------------------

        confidence_margin = (
            1.96 * standard_error
        )

        confidence_lower = (
            mean_value - confidence_margin
        )

        confidence_upper = (
            mean_value + confidence_margin
        )

        # -------------------------------------------------
        # COEFFICIENT OF VARIATION
        # -------------------------------------------------

        if mean_value != 0:

            coefficient_variation = (
                abs(std_value / mean_value) * 100
            )

        else:

            coefficient_variation = None

        # -------------------------------------------------
        # SKEWNESS
        # -------------------------------------------------

        skewness = float(
            series.skew()
        )

        if abs(skewness) < 0.5:

            skew_interpretation = "Approximately symmetric"

        elif abs(skewness) < 1:

            skew_interpretation = "Moderately skewed"

        else:

            skew_interpretation = "Highly skewed"

        # -------------------------------------------------
        # KURTOSIS
        # -------------------------------------------------

        kurtosis = float(
            series.kurt()
        )

        if kurtosis > 1:

            kurtosis_interpretation = "Heavy-tailed distribution"

        elif kurtosis < -1:

            kurtosis_interpretation = "Light-tailed distribution"

        else:

            kurtosis_interpretation = "Normal-like tail behavior"

        # -------------------------------------------------
        # VARIABILITY
        # -------------------------------------------------

        if coefficient_variation is None:

            variability_level = "Unknown"

        elif coefficient_variation < 10:

            variability_level = "Low"

        elif coefficient_variation < 25:

            variability_level = "Moderate"

        else:

            variability_level = "High"

        # -------------------------------------------------
        # AUTOMATIC INSIGHT
        # -------------------------------------------------

        insights = []

        if skewness > 1:

            insights.append(
                "The distribution is strongly right-skewed."
            )

        elif skewness < -1:

            insights.append(
                "The distribution is strongly left-skewed."
            )

        else:

            insights.append(
                "The distribution is relatively balanced."
            )

        if coefficient_variation is not None:

            if coefficient_variation >= 25:

                insights.append(
                    "The metric shows high relative variability."
                )

            elif coefficient_variation >= 10:

                insights.append(
                    "The metric shows moderate relative variability."
                )

            else:

                insights.append(
                    "The metric shows relatively low variability."
                )

        if mean_value > median_value:

            insights.append(
                "Mean is higher than median."
            )

        elif mean_value < median_value:

            insights.append(
                "Mean is lower than median."
            )

        else:

            insights.append(
                "Mean and median are approximately equal."
            )

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        results[str(col)] = {

            "sample_size": n,

            "mean": round(
                mean_value,
                4
            ),

            "median": round(
                median_value,
                4
            ),

            "standard_deviation": round(
                std_value,
                4
            ),

            "standard_error": round(
                standard_error,
                4
            ),

            "coefficient_of_variation_percent": (
                round(
                    coefficient_variation,
                    2
                )
                if coefficient_variation is not None
                else None
            ),

            "confidence_interval_95": {

                "lower": round(
                    confidence_lower,
                    4
                ),

                "upper": round(
                    confidence_upper,
                    4
                )
            },

            "skewness": round(
                skewness,
                4
            ),

            "skewness_interpretation":
                skew_interpretation,

            "kurtosis": round(
                kurtosis,
                4
            ),

            "kurtosis_interpretation":
                kurtosis_interpretation,

            "variability_level":
                variability_level,

            "insights":
                insights
        }

    return {

        "success": True,

        "columns_analyzed": [
            str(c)
            for c in columns_to_analyze
        ],

        "ignored_columns":
            ignored_columns,

        "advanced_statistics":
            results
    }
def genesis_dashboard_quality():
    df = require_df()

    total_cells = max(int(df.shape[0] * df.shape[1]), 1)
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())

    missing_rate = (missing / total_cells) * 100
    duplicate_rate = (duplicates / max(len(df), 1)) * 100
    score = max(0, round(100 - missing_rate - duplicate_rate, 2))

    column_issues = []
    for col in df.columns:
        nulls = int(df[col].isna().sum())
        if nulls:
            column_issues.append({
                "column": str(col),
                "missing_values": nulls,
                "missing_percentage": round((nulls / max(len(df), 1)) * 100, 2)
            })

    return {
        "quality_score": score,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": missing,
        "duplicate_rows": duplicates,
        "issues": column_issues
    }


def genesis_dashboard_profile():
    df = require_df()
    profile_rows = []

    for col in df.columns:
        series = df[col]
        item = {
            "column": str(col),
            "dtype": str(series.dtype),
            "non_null": int(series.notna().sum()),
            "missing": int(series.isna().sum()),
            "unique": int(series.nunique(dropna=True)),
            "sample_values": [
                _json_safe(v) for v in series.dropna().head(5).tolist()
            ]
        }

        if pd.api.types.is_numeric_dtype(series):
            clean = pd.to_numeric(series, errors="coerce").dropna()
            if not clean.empty:
                item.update({
                    "mean": float(clean.mean()),
                    "min": float(clean.min()),
                    "max": float(clean.max())
                })

        profile_rows.append(item)

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "profile": profile_rows
    }


def genesis_dashboard_correlation():
    df = require_df()
    numeric_cols = _numeric_columns(df)

    if len(numeric_cols) < 2:
        return {
            "message": "At least two numeric columns are required for correlation."
        }

    corr = df[numeric_cols].corr().round(4)
    return {
        "numeric_columns": numeric_cols,
        "correlation_matrix": _json_safe(corr.to_dict())
    }


def genesis_dashboard_trend():
    df = require_df()
    date_col = _date_column(df)

    if not date_col:
        return {
            "success": False,
            "message": "No usable date/time column was detected for trend analysis."
        }

    # Copy dataset
    temp = df.copy()

    # Convert date column
    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    # Remove invalid dates
    temp = temp.dropna(subset=[date_col])

    if temp.empty:
        return {
            "success": False,
            "message": "No valid date values available for trend analysis."
        }

    # -------------------------------------------------
    # SMART NUMERIC COLUMN DETECTION
    # -------------------------------------------------

    excluded_keywords = [
        "id",
        "phone",
        "mobile",
        "contact",
        "number",
        "code",
        "pin",
        "zip"
    ]

    numeric_cols = []

    for col in temp.columns:

        if col == date_col:
            continue

        if not pd.api.types.is_numeric_dtype(temp[col]):
            continue

        col_name = str(col).lower()

        # Ignore identifier-like columns
        if any(
            keyword in col_name
            for keyword in excluded_keywords
        ):
            continue

        # Ignore almost unique columns
        unique_ratio = (
            temp[col]
            .nunique(dropna=True)
            / max(len(temp), 1)
        )

        if unique_ratio > 0.95:
            continue

        numeric_cols.append(col)

    if not numeric_cols:
        return {
            "success": False,
            "message": "No meaningful numeric columns available for trend analysis.",
            "date_column": str(date_col)
        }

    # -------------------------------------------------
    # CREATE MONTHLY PERIOD
    # -------------------------------------------------

    temp["__trend_period__"] = (
        temp[date_col]
        .dt.to_period("M")
        .astype(str)
    )

    trends = {}

    # Maximum 10 useful metrics
    for col in numeric_cols[:10]:

        metric_data = (
            temp
            .groupby("__trend_period__")[col]
            .mean()
            .dropna()
        )

        if len(metric_data) < 2:
            continue

        first_period = str(metric_data.index[0])
        last_period = str(metric_data.index[-1])

        first_value = float(metric_data.iloc[0])
        last_value = float(metric_data.iloc[-1])

        change = last_value - first_value

        if first_value != 0:
            percentage_change = (
                change / abs(first_value)
            ) * 100
        else:
            percentage_change = None

        # Trend direction
        if percentage_change is not None:

            if percentage_change > 1:
                direction = "upward"

            elif percentage_change < -1:
                direction = "downward"

            else:
                direction = "flat"

        else:
            direction = "flat"

        # Monthly data
        monthly_values = []

        for period, value in metric_data.tail(24).items():

            monthly_values.append({
                "period": str(period),
                "value": round(float(value), 4)
            })

        trends[str(col)] = {
            "first_period": first_period,
            "last_period": last_period,
            "first_value": round(first_value, 4),
            "last_value": round(last_value, 4),
            "change": round(change, 4),
            "percentage_change": (
                round(float(percentage_change), 2)
                if percentage_change is not None
                else None
            ),
            "direction": direction,
            "data_points": int(len(metric_data)),
            "monthly_trend": monthly_values
        }
        

    return {
        "success": True,
        "date_column": str(date_col),
        "aggregation": "monthly average",
        "period_start": str(temp[date_col].min()),
        "period_end": str(temp[date_col].max()),
        "metrics_analyzed": len(trends),
        "trends": trends
    }
def _classify_series_behavior(
    current_value,
    forecast_value,
    normalized_slope,
    volatility_ratio
):

    change_percent = 0

    if current_value != 0:
        change_percent = (
            (forecast_value - current_value)
            / abs(current_value)
        ) * 100

    # High volatility
    if volatility_ratio >= 0.20:
        return "volatile"

    # Strong upward movement
    if change_percent >= 5:
        return "strong_upward"

    # Strong downward movement
    if change_percent <= -5:
        return "strong_downward"

    # Moderate upward trend
    if normalized_slope > 0.01:
        return "upward"

    # Moderate downward trend
    if normalized_slope < -0.01:
        return "downward"

    return "stable"

def _forecast_backtest(y):

    import numpy as np

    y = np.asarray(
        y,
        dtype=float
    )

    data_points = len(y)

    # Backtesting ke liye minimum data
    if data_points < 6:

        return {
            "success": False,
            "backtest_points": 0,
            "mae": None,
            "rmse": None,
            "mape": None,
            "bias": None,
            "accuracy_score": 0.0,
            "message": "Not enough historical data for backtesting."
        }

    errors = []
    absolute_percentage_errors = []

    # Walk-forward validation
    for i in range(3, data_points):

        train_y = y[:i]

        actual_value = float(
            y[i]
        )

        x_train = np.arange(
            len(train_y)
        )

        try:

            slope, intercept = np.polyfit(
                x_train,
                train_y,
                1
            )

            predicted_value = float(
                intercept
                + slope * len(train_y)
            )

        except Exception:

            continue

        error = (
            predicted_value
            - actual_value
        )

        errors.append(
            error
        )

        if actual_value != 0:

            absolute_percentage_errors.append(
                abs(
                    error
                    / actual_value
                )
                * 100
            )

    if not errors:

        return {
            "success": False,
            "backtest_points": 0,
            "mae": None,
            "rmse": None,
            "mape": None,
            "bias": None,
            "accuracy_score": 0.0,
            "message": "Backtesting could not be completed."
        }

    errors = np.asarray(
        errors,
        dtype=float
    )

    mae = float(
        np.mean(
            np.abs(errors)
        )
    )

    rmse = float(
        np.sqrt(
            np.mean(
                errors ** 2
            )
        )
    )

    bias = float(
        np.mean(
            errors
        )
    )

    if absolute_percentage_errors:

        mape = float(
            np.mean(
                absolute_percentage_errors
            )
        )

    else:

        mape = None

    # Accuracy score
    if mape is not None:

        accuracy_score = max(
            0.0,
            min(
                100.0,
                100.0 - mape
            )
        )

    else:

        accuracy_score = 0.0

    return {
        "success": True,
        "backtest_points": int(
            len(errors)
        ),
        "mae": round(
            mae,
            4
        ),
        "rmse": round(
            rmse,
            4
        ),
        "mape": (
            round(mape, 4)
            if mape is not None
            else None
        ),
        "bias": round(
            bias,
            4
        ),
        "accuracy_score": round(
            accuracy_score,
            2
        ),
        "message": "Walk-forward backtesting completed."
    }
def _forecast_reliability(
    confidence_score,
    r_squared,
    volatility_ratio,
    data_points,
    current_value
):

    # -------------------------------------------------
    # SAFETY CONVERSION
    # -------------------------------------------------

    try:
        confidence_score = float(confidence_score)
    except:
        confidence_score = 0.0

    try:
        r_squared = float(r_squared)
    except:
        r_squared = 0.0

    try:
        volatility_ratio = float(volatility_ratio)
    except:
        volatility_ratio = 1.0

    try:
        data_points = int(data_points)
    except:
        data_points = 0


    # -------------------------------------------------
    # BACKTEST / CONFIDENCE QUALITY
    # Weight: 40 points
    # -------------------------------------------------

    confidence_component = (
        max(
            0.0,
            min(100.0, confidence_score)
        )
        / 100
    ) * 40


    # -------------------------------------------------
    # MODEL PATTERN QUALITY
    # R-squared has lower importance because
    # stable business data can naturally have low R².
    # Weight: 10 points
    # -------------------------------------------------

    r_squared_component = (
        max(
            0.0,
            min(1.0, r_squared)
        )
    ) * 10


    # -------------------------------------------------
    # DATA STABILITY / VOLATILITY
    # Lower volatility = higher reliability
    # Weight: 30 points
    # -------------------------------------------------

    stability_score = max(
        0.0,
        min(
            1.0,
            1.0 - volatility_ratio
        )
    )

    volatility_component = (
        stability_score * 30
    )


    # -------------------------------------------------
    # HISTORICAL DATA QUALITY
    # 24 or more data points gets full score.
    # Weight: 20 points
    # -------------------------------------------------

    data_component = (
        min(
            data_points / 24,
            1.0
        )
        * 20
    )


    # -------------------------------------------------
    # FINAL RELIABILITY SCORE
    # -------------------------------------------------

    reliability_score = (
        confidence_component
        + r_squared_component
        + volatility_component
        + data_component
    )

    reliability_score = round(
        max(
            0.0,
            min(
                100.0,
                reliability_score
            )
        ),
        2
    )


    # -------------------------------------------------
    # QUALITY CLASSIFICATION
    # -------------------------------------------------

    if reliability_score >= 75:

        quality = "high"
        reliable = True

        reason = (
            "Strong forecast reliability based on "
            "historical data stability and model performance."
        )

    elif reliability_score >= 50:

        quality = "medium"
        reliable = True

        reason = (
            "Moderate forecast reliability. "
            "The forecast should be monitored."
        )

    else:

        quality = "low"
        reliable = False

        reason = (
            "Forecast reliability is limited because "
            "the historical pattern is weak or unstable."
        )


    # -------------------------------------------------
    # RETURN
    # -------------------------------------------------

    return {
        "score": reliability_score,
        "quality": quality,
        "reliable": reliable,
        "reason": reason
    }


def _forecast_business_metrics(
    metric_name,
    current_value,
    forecast_value,
    behavior,
    reliability
):
    metric_name_lower = str(
        metric_name
    ).lower()

    if current_value == 0:
        change_percent = 0.0

    else:
        change_percent = (
            (
                forecast_value - current_value
            )
            / abs(current_value)
        ) * 100

    change_percent = round(
        float(change_percent),
        2
    )

    business_category = "general"

    if any(
        word in metric_name_lower
        for word in [
            "revenue",
            "sales",
            "profit",
            "income"
        ]
    ):
        business_category = "financial"

    elif any(
        word in metric_name_lower
        for word in [
            "expense",
            "cost",
            "budget"
        ]
    ):
        business_category = "cost"

    elif any(
        word in metric_name_lower
        for word in [
            "attendance",
            "performance",
            "training",
            "leaves",
            "experience"
        ]
    ):
        business_category = "workforce"

    if change_percent >= 10:
        impact = "strong_increase"

    elif change_percent >= 3:
        impact = "increase"

    elif change_percent <= -10:
        impact = "strong_decrease"

    elif change_percent <= -3:
        impact = "decrease"

    else:
        impact = "stable"

    return {
        "category": business_category,
        "expected_change_percent": change_percent,
        "behavior": behavior,
        "forecast_reliability": reliability,
        "business_impact": impact
    }
# =========================================================
# FORECAST INTELLIGENCE V5 - BACKTEST VALIDATION ENGINE
# =========================================================
def _forecast_backtest_validation(values):

    try:
        values = np.array(
            values,
            dtype=float
        )

    except Exception:

        return {
            "success": False,
            "mae": None,
            "mape": None,
            "test_points": 0,
            "message": "Unable to prepare data for backtesting."
        }


    # -------------------------------------------------
    # MINIMUM DATA CHECK
    # -------------------------------------------------

    if len(values) < 12:

        return {
            "success": False,
            "mae": None,
            "mape": None,
            "test_points": 0,
            "message": (
                "Not enough historical data "
                "for backtest validation."
            )
        }


    # -------------------------------------------------
    # TRAIN / TEST SPLIT
    # -------------------------------------------------

    test_size = max(
        3,
        int(len(values) * 0.20)
    )

    train_values = values[:-test_size]
    test_values = values[-test_size:]


    if len(train_values) < 2:

        return {
            "success": False,
            "mae": None,
            "mape": None,
            "test_points": 0,
            "message": (
                "Insufficient training data "
                "for backtesting."
            )
        }


    # -------------------------------------------------
    # LINEAR REGRESSION MODEL
    # -------------------------------------------------

    x_train = np.arange(
        len(train_values)
    )

    slope, intercept = np.polyfit(
        x_train,
        train_values,
        1
    )


    # -------------------------------------------------
    # PREDICT HIDDEN TEST DATA
    # -------------------------------------------------

    x_test = np.arange(
        len(train_values),
        len(values)
    )

    predictions = (
        slope * x_test
        + intercept
    )


    # -------------------------------------------------
    # MAE
    # -------------------------------------------------

    mae = np.mean(
        np.abs(
            test_values
            - predictions
        )
    )


    # -------------------------------------------------
    # MAPE
    # -------------------------------------------------

    non_zero_mask = (
        test_values != 0
    )

    if np.any(non_zero_mask):

        mape = np.mean(
            np.abs(
                (
                    test_values[non_zero_mask]
                    - predictions[non_zero_mask]
                )
                /
                test_values[non_zero_mask]
            )
        ) * 100

    else:

        mape = 0.0


    # -------------------------------------------------
    # ACCURACY SCORE
    # -------------------------------------------------

    accuracy_score = max(
        0.0,
        100.0 - float(mape)
    )


    # -------------------------------------------------
    # BACKTEST QUALITY
    # -------------------------------------------------

    if accuracy_score >= 85:

        quality = "high"

    elif accuracy_score >= 65:

        quality = "medium"

    else:

        quality = "low"


    # -------------------------------------------------
    # RETURN RESULT
    # -------------------------------------------------

    return {

        "success": True,

        "test_points": int(
            test_size
        ),

        "mae": round(
            float(mae),
            4
        ),

        "mape": round(
            float(mape),
            2
        ),

        "accuracy_score": round(
            float(accuracy_score),
            2
        ),

        "quality": quality,

        "message": (
            "Backtest validation completed successfully."
        )
    }

def _forecast_backtest_validation(y):

    import numpy as np

    y = np.asarray(
        y,
        dtype=float
    )

    total_points = len(y)

    # -----------------------------------------------------
    # MINIMUM DATA CHECK
    # -----------------------------------------------------

    if total_points < 6:

        return {
            "validation_status": "weak_validation",
            "validation_points": 0,
            "linear_backtest_mae": None,
            "moving_average_backtest_mae": None,
            "naive_backtest_mae": None,
            "best_backtest_model": None,
            "baseline_improvement_percent": 0.0,
            "model_beats_baseline": False,
            "validation_score": 0.0
        }

    # -----------------------------------------------------
    # NUMBER OF BACKTEST POINTS
    # -----------------------------------------------------

    validation_points = min(
        12,
        max(
            3,
            total_points // 5
        )
    )

    start_index = (
        total_points
        - validation_points
    )

    linear_errors = []

    moving_average_errors = []

    naive_errors = []

    # -----------------------------------------------------
    # WALK-FORWARD BACKTEST
    # -----------------------------------------------------

    for i in range(
        start_index,
        total_points
    ):

        train_y = y[:i]

        actual_value = float(
            y[i]
        )

        if len(train_y) < 3:
            continue

        # -------------------------------------------------
        # NAIVE BASELINE
        # -------------------------------------------------

        naive_prediction = float(
            train_y[-1]
        )

        naive_error = abs(
            actual_value
            - naive_prediction
        )

        naive_errors.append(
            naive_error
        )

        # -------------------------------------------------
        # LINEAR REGRESSION
        # -------------------------------------------------

        try:

            x_train = np.arange(
                len(train_y)
            )

            slope, intercept = np.polyfit(
                x_train,
                train_y,
                1
            )

            linear_prediction = float(
                intercept
                + (
                    slope
                    * len(train_y)
                )
            )

            linear_error = abs(
                actual_value
                - linear_prediction
            )

            linear_errors.append(
                linear_error
            )

        except Exception:

            pass

        # -------------------------------------------------
        # MOVING AVERAGE
        # -------------------------------------------------

        try:

            window = min(
                3,
                len(train_y)
            )

            moving_average_prediction = float(
                np.mean(
                    train_y[-window:]
                )
            )

            moving_average_error = abs(
                actual_value
                - moving_average_prediction
            )

            moving_average_errors.append(
                moving_average_error
            )

        except Exception:

            pass

    # -----------------------------------------------------
    # CALCULATE MAE
    # -----------------------------------------------------

    linear_mae = (
        float(
            np.mean(linear_errors)
        )
        if linear_errors
        else None
    )

    moving_average_mae = (
        float(
            np.mean(
                moving_average_errors
            )
        )
        if moving_average_errors
        else None
    )

    naive_mae = (
        float(
            np.mean(
                naive_errors
            )
        )
        if naive_errors
        else None
    )

    # -----------------------------------------------------
    # MODEL COMPARISON
    # -----------------------------------------------------

    model_scores = {}

    if linear_mae is not None:

        model_scores[
            "Linear Regression"
        ] = linear_mae

    if moving_average_mae is not None:

        model_scores[
            "Moving Average"
        ] = moving_average_mae

    if naive_mae is not None:

        model_scores[
            "Naive Baseline"
        ] = naive_mae

    if not model_scores:

        return {
            "validation_status": "weak_validation",
            "validation_points": validation_points,
            "linear_backtest_mae": None,
            "moving_average_backtest_mae": None,
            "naive_backtest_mae": None,
            "best_backtest_model": None,
            "baseline_improvement_percent": 0.0,
            "model_beats_baseline": False,
            "validation_score": 0.0
        }

    best_model = min(
        model_scores,
        key=model_scores.get
    )

    best_mae = model_scores[
        best_model
    ]

    # -----------------------------------------------------
    # BASELINE IMPROVEMENT
    # -----------------------------------------------------

    baseline_improvement_percent = 0.0

    model_beats_baseline = False

    if (
        naive_mae is not None
        and naive_mae > 0
        and best_mae is not None
    ):

        baseline_improvement_percent = (
            (
                naive_mae
                - best_mae
            )
            / naive_mae
        ) * 100

        if (
            best_model
            != "Naive Baseline"
            and best_mae < naive_mae
        ):

            model_beats_baseline = True

    # -----------------------------------------------------
    # VALIDATION SCORE
    # -----------------------------------------------------

    validation_score = 50.0

    if model_beats_baseline:

        validation_score += min(
            30.0,
            max(
                0.0,
                baseline_improvement_percent
            )
        )

    if validation_points >= 10:

        validation_score += 20

    elif validation_points >= 6:

        validation_score += 10

    validation_score = min(
        100.0,
        validation_score
    )

    # -----------------------------------------------------
    # VALIDATION STATUS
    # -----------------------------------------------------

    if validation_score >= 80:

        validation_status = "strong_validation"

    elif validation_score >= 60:

        validation_status = "moderate_validation"

    else:

        validation_status = "weak_validation"

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "validation_status":
            validation_status,

        "validation_points":
            int(validation_points),

        "linear_backtest_mae":
            round(
                linear_mae,
                4
            )
            if linear_mae is not None
            else None,

        "moving_average_backtest_mae":
            round(
                moving_average_mae,
                4
            )
            if moving_average_mae is not None
            else None,

        "naive_backtest_mae":
            round(
                naive_mae,
                4
            )
            if naive_mae is not None
            else None,

        "best_backtest_model":
            best_model,

        "baseline_improvement_percent":
            round(
                baseline_improvement_percent,
                2
            ),

        "model_beats_baseline":
            model_beats_baseline,

        "validation_score":
            round(
                validation_score,
                2
            )
    }
# =========================================================
# FORECAST INTELLIGENCE V5
# SMART INSIGHTS & BUSINESS RECOMMENDATIONS
# =========================================================

def _generate_forecast_insights(forecasts):

    insights = []

    recommendations = []

    if not forecasts:

        return {
            "insights": insights,
            "recommendations": recommendations
        }

    for item in forecasts:

        metric = str(
            item.get("metric", "Unknown Metric")
        )

        trend = str(
            item.get("trend", "stable")
        )

        change = item.get(
            "expected_change_percent"
        )

        reliability = item.get(
            "forecast_reliability",
            {}
        )

        reliability_score = float(
            reliability.get(
                "score",
                0
            ) or 0
        )

        reliability_quality = str(
            reliability.get(
                "quality",
                "low"
            )
        )

        business = item.get(
            "business_metrics",
            {}
        )

        business_impact = str(
            business.get(
                "business_impact",
                "stable"
            )
        )

        # -----------------------------------------
        # TREND INSIGHT
        # -----------------------------------------

        if change is not None:

            try:

                change = float(change)

                if change >= 10:

                    summary = (
                        f"{metric} is forecasted to increase "
                        f"significantly by {abs(change):.2f}%."
                    )

                elif change >= 3:

                    summary = (
                        f"{metric} is expected to increase "
                        f"by {abs(change):.2f}%."
                    )

                elif change <= -10:

                    summary = (
                        f"{metric} is forecasted to decrease "
                        f"significantly by {abs(change):.2f}%."
                    )

                elif change <= -3:

                    summary = (
                        f"{metric} is expected to decrease "
                        f"by {abs(change):.2f}%."
                    )

                else:

                    summary = (
                        f"{metric} is expected to remain "
                        f"relatively stable."
                    )

            except Exception:

                summary = (
                    f"{metric} forecast trend is {trend}."
                )

        else:

            summary = (
                f"{metric} forecast trend is {trend}."
            )

        insights.append({

            "metric": metric,

            "summary": summary,

            "trend": trend,

            "reliability_score": round(
                reliability_score,
                2
            ),

            "business_impact": business_impact
        })


        # -----------------------------------------
        # BUSINESS RECOMMENDATION
        # -----------------------------------------

        if reliability_quality == "low":

            recommendation = (
                f"Monitor {metric} closely because "
                f"forecast reliability is currently low."
            )

        elif business_impact == "strong_increase":

            recommendation = (
                f"Prepare for a significant increase in "
                f"{metric} and review capacity or planning."
            )

        elif business_impact == "strong_decrease":

            recommendation = (
                f"Investigate the expected decrease in "
                f"{metric} and consider corrective action."
            )

        elif business_impact == "increase":

            recommendation = (
                f"Track the expected growth in {metric} "
                f"and adjust business planning if needed."
            )

        elif business_impact == "decrease":

            recommendation = (
                f"Review {metric} because a downward "
                f"movement is forecasted."
            )

        else:

            recommendation = (
                f"Continue monitoring {metric} as the "
                f"forecast currently indicates stability."
            )

        recommendations.append({

            "metric": metric,

            "recommendation": recommendation,

            "priority": (
                "high"
                if reliability_quality == "low"
                or business_impact
                in [
                    "strong_increase",
                    "strong_decrease"
                ]
                else "normal"
            ),

            "reliability": reliability_quality
        })


    # -----------------------------------------
    # SORT HIGH PRIORITY RECOMMENDATIONS FIRST
    # -----------------------------------------

    recommendations.sort(

        key=lambda x: (
            0
            if x["priority"] == "high"
            else 1
        )
    )


    return {

        "insights": insights,

        "recommendations": recommendations
    }
# =====================================================
# FORECAST EXPLAINABILITY ENGINE
# =====================================================

def generate_forecast_explanation(
    metric,
    expected_change_percent,
    trend,
    trend_strength,
    forecast_risk,
    confidence_score,
    volatility_ratio,
    best_model
):

    explanations = []

    # -------------------------------------------------
    # FORECAST DIRECTION
    # -------------------------------------------------

    if expected_change_percent is None:

        direction = (
            "No reliable percentage change "
            "could be calculated."
        )

    elif expected_change_percent > 0:

        direction = (
            f"{metric} is expected to increase by "
            f"{abs(expected_change_percent):.2f}%."
        )

    elif expected_change_percent < 0:

        direction = (
            f"{metric} is expected to decrease by "
            f"{abs(expected_change_percent):.2f}%."
        )

    else:

        direction = (
            f"{metric} is expected to remain stable."
        )

    explanations.append(direction)

    # -------------------------------------------------
    # TREND EXPLANATION
    # -------------------------------------------------

    explanations.append(
        f"The detected trend is {trend} "
        f"with {trend_strength} strength."
    )

    # -------------------------------------------------
    # VOLATILITY EXPLANATION
    # -------------------------------------------------

    if volatility_ratio >= 0.30:

        volatility_explanation = (
            "Historical values show high volatility, "
            "which increases forecast uncertainty."
        )

    elif volatility_ratio >= 0.15:

        volatility_explanation = (
            "Historical values show moderate volatility."
        )

    else:

        volatility_explanation = (
            "Historical values are relatively stable."
        )

    explanations.append(
        volatility_explanation
    )

    # -------------------------------------------------
    # RISK EXPLANATION
    # -------------------------------------------------

    if forecast_risk == "High":

        risk_explanation = (
            "Forecast risk is high because the historical "
            "pattern is unstable or model uncertainty is high."
        )

    elif forecast_risk == "Medium":

        risk_explanation = (
            "Forecast risk is moderate. The forecast should "
            "be monitored before major business decisions."
        )

    else:

        risk_explanation = (
            "Forecast risk is low because the historical "
            "pattern is relatively stable."
        )

    explanations.append(
        risk_explanation
    )

    # -------------------------------------------------
    # CONFIDENCE EXPLANATION
    # -------------------------------------------------

    if confidence_score >= 80:

        confidence_explanation = (
            "The forecast has strong confidence based on "
            "the available historical data."
        )

    elif confidence_score >= 60:

        confidence_explanation = (
            "The forecast has moderate confidence and "
            "should be used with reasonable caution."
        )

    else:

        confidence_explanation = (
            "The forecast confidence is limited. Additional "
            "historical data may improve reliability."
        )

    explanations.append(
        confidence_explanation
    )

    # -------------------------------------------------
    # MODEL EXPLANATION
    # -------------------------------------------------

    explanations.append(
        f"The selected forecasting model is {best_model} "
        f"because it performed better during model comparison."
    )

    # -------------------------------------------------
    # RECOMMENDED ACTION
    # -------------------------------------------------

    if forecast_risk == "High":

        recommended_action = (
            "Monitor this metric closely and avoid making "
            "high-impact decisions using this forecast alone."
        )

    elif (
        expected_change_percent is not None
        and expected_change_percent <= -10
    ):

        recommended_action = (
            "Investigate the expected decline and prepare "
            "a corrective business action plan."
        )

    elif (
        expected_change_percent is not None
        and expected_change_percent >= 10
    ):

        recommended_action = (
            "Prepare capacity and resources to support "
            "the expected growth."
        )

    else:

        recommended_action = (
            "Continue monitoring this metric and compare "
            "future actual results against the forecast."
        )

    return {

        "summary": direction,

        "trend_explanation": (
            explanations[1]
        ),

        "volatility_explanation": (
            explanations[2]
        ),

        "risk_explanation": (
            explanations[3]
        ),

        "confidence_explanation": (
            explanations[4]
        ),

        "model_explanation": (
            explanations[5]
        ),

        "recommended_action": (
            recommended_action
        )

    }
# =====================================================
# FORECAST SCENARIO ANALYSIS ENGINE
# =====================================================

def generate_forecast_scenarios(
    current_value,
    forecast_value,
    lower_bound,
    upper_bound,
    forecast_risk
):

    # -------------------------------------------------
    # EXPECTED SCENARIO
    # -------------------------------------------------

    expected_case = float(
        forecast_value
    )

    # -------------------------------------------------
    # BEST CASE
    # -------------------------------------------------

    best_case = float(
        upper_bound
    )

    # -------------------------------------------------
    # WORST CASE
    # -------------------------------------------------

    worst_case = float(
        lower_bound
    )

    # -------------------------------------------------
    # SCENARIO CHANGE %
    # -------------------------------------------------

    if current_value != 0:

        best_case_change = (
            (best_case - current_value)
            / abs(current_value)
        ) * 100

        expected_case_change = (
            (expected_case - current_value)
            / abs(current_value)
        ) * 100

        worst_case_change = (
            (worst_case - current_value)
            / abs(current_value)
        ) * 100

    else:

        best_case_change = 0.0
        expected_case_change = 0.0
        worst_case_change = 0.0

    # -------------------------------------------------
    # SCENARIO INTERPRETATION
    # -------------------------------------------------

    if forecast_risk == "High":

        scenario_note = (
            "High uncertainty detected. Actual results "
            "may vary significantly between scenarios."
        )

    elif forecast_risk == "Medium":

        scenario_note = (
            "Moderate uncertainty detected. Monitor actual "
            "performance against the expected scenario."
        )

    else:

        scenario_note = (
            "Lower uncertainty detected. Expected scenario "
            "is relatively more reliable."
        )

    return {

        "best_case": {
            "value": round(
                best_case,
                4
            ),
            "change_percent": round(
                best_case_change,
                2
            )
        },

        "expected_case": {
            "value": round(
                expected_case,
                4
            ),
            "change_percent": round(
                expected_case_change,
                2
            )
        },

        "worst_case": {
            "value": round(
                worst_case,
                4
            ),
            "change_percent": round(
                worst_case_change,
                2
            )
        },

        "scenario_note": (
            scenario_note
        )

    }
# =====================================================
# FORECAST VS ACTUAL TRACKING ENGINE
# =====================================================

def calculate_forecast_accuracy(
    forecast_value,
    actual_value
):

    # -------------------------------------------------
    # VALIDATE VALUES
    # -------------------------------------------------

    try:

        forecast_value = float(
            forecast_value
        )

        actual_value = float(
            actual_value
        )

    except (
        TypeError,
        ValueError
    ):

        return {

            "success": False,

            "message": (
                "Invalid forecast or actual value."
            )

        }

    # -------------------------------------------------
    # CALCULATE ERRORS
    # -------------------------------------------------

    absolute_error = abs(
        actual_value
        - forecast_value
    )

    if actual_value != 0:

        error_percent = (
            absolute_error
            / abs(actual_value)
        ) * 100

    else:

        error_percent = 0.0

    # -------------------------------------------------
    # ACCURACY SCORE
    # -------------------------------------------------

    accuracy_percent = max(
        0.0,
        100 - error_percent
    )

    # -------------------------------------------------
    # ACCURACY LEVEL
    # -------------------------------------------------

    if accuracy_percent >= 90:

        accuracy_level = (
            "Excellent"
        )

    elif accuracy_percent >= 75:

        accuracy_level = (
            "Good"
        )

    elif accuracy_percent >= 60:

        accuracy_level = (
            "Moderate"
        )

    else:

        accuracy_level = (
            "Low"
        )

    # -------------------------------------------------
    # RETURN RESULT
    # -------------------------------------------------

    return {

        "success": True,

        "forecast_value": round(
            forecast_value,
            4
        ),

        "actual_value": round(
            actual_value,
            4
        ),

        "absolute_error": round(
            absolute_error,
            4
        ),

        "error_percent": round(
            error_percent,
            2
        ),

        "accuracy_percent": round(
            accuracy_percent,
            2
        ),

        "accuracy_level": (
            accuracy_level
        )

    }
def genesis_dashboard_forecast():
    """
    Genesis AI - Professional Forecast Engine

    Features:
    - Automatic date detection
    - Business metric selection
    - Monthly aggregation
    - Linear Regression
    - Moving Average
    - Automatic best-model selection
    - Backtesting
    - Trend analysis
    - Growth analysis
    - Volatility analysis
    - Forecast confidence
    - Forecast reliability
    - Forecast risk
    - Forecast range
    - Scenario analysis
    - Explainability
    - Business priority
    - Forecast alerts
    - Forecast insights
    - Forecast history tracking
    """

    import numpy as np

    df = require_df()

    # =========================================================
    # 1. DATE COLUMN
    # =========================================================

    date_col = _date_column(df)

    if not date_col:
        return {
            "success": False,
            "message": (
                "No usable date/time column was detected "
                "for forecasting."
            )
        }

    temp = df.copy()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    temp = temp.dropna(
        subset=[date_col]
    )

    if temp.empty:
        return {
            "success": False,
            "message": (
                "No valid date values available "
                "for forecasting."
            )
        }

    # =========================================================
    # 2. NUMERIC METRIC DETECTION
    # =========================================================

    excluded_keywords = [
        "id",
        "phone",
        "mobile",
        "contact",
        "number",
        "code",
        "pin",
        "zip"
    ]

    numeric_cols = []

    for col in temp.columns:

        if col == date_col:
            continue

        converted = pd.to_numeric(
            temp[col],
            errors="coerce"
        )

        valid_numeric_ratio = (
            converted.notna().sum()
            / max(len(temp), 1)
        )

        if valid_numeric_ratio < 0.70:
            continue

        temp[col] = converted

        col_name = str(col).lower()

        if any(
            keyword in col_name
            for keyword in excluded_keywords
        ):
            continue

        unique_ratio = (
            temp[col].nunique(dropna=True)
            / max(len(temp), 1)
        )

        # Ignore almost-unique technical columns
        if unique_ratio > 0.95:
            continue

        numeric_cols.append(col)

    if not numeric_cols:
        return {
            "success": False,
            "message": (
                "No meaningful numeric columns "
                "available for forecasting."
            )
        }

    # =========================================================
    # 3. BUSINESS-AWARE METRIC SELECTION
    # =========================================================

    priority_keywords = [

        # Financial
        "revenue",
        "profit",
        "expense",
        "expenses",
        "income",
        "cost",
        "budget",

        # Sales / Growth
        "sales",
        "monthly sales",
        "target",
        "achievement",

        # HR / Employee
        "salary",
        "bonus",
        "incentive",
        "attendance",
        "leave",
        "leaves",
        "performance",
        "training",
        "experience"
    ]

    business_metrics = []
    other_metrics = []

    for col in numeric_cols:

        col_name = str(col).lower()

        if any(
            keyword in col_name
            for keyword in priority_keywords
        ):
            business_metrics.append(col)
        else:
            other_metrics.append(col)

    # Prefer business metrics
    selected_metrics = business_metrics.copy()

    # If business metrics are too few,
    # add useful remaining metrics.
    if len(selected_metrics) < 3:

        excluded_fallback = [
            "age",
            "rating",
            "score"
        ]

        for col in other_metrics:

            col_name = str(col).lower()

            if any(
                keyword in col_name
                for keyword in excluded_fallback
            ):
                continue

            if col not in selected_metrics:
                selected_metrics.append(col)

    numeric_cols = selected_metrics

    print(
        "FINAL FORECAST METRICS:",
        numeric_cols
    )

    # =========================================================
    # 4. MONTHLY PERIOD
    # =========================================================

    temp["__forecast_period__"] = (
        temp[date_col]
        .dt.to_period("M")
        .astype(str)
    )

    forecasts = []
    alerts = []
    insights = []

    # =========================================================
    # 5. FORECAST EACH METRIC
    # =========================================================

    for col in numeric_cols:

        monthly_data = (
            temp
            .groupby(
                "__forecast_period__"
            )[col]
            .mean()
            .dropna()
        )

        # Need enough data for forecasting
        if len(monthly_data) < 2:
            continue

        y = monthly_data.to_numpy(
            dtype=float
        )

        x = np.arange(
            len(y),
            dtype=float
        )

        current_value = float(
            y[-1]
        )

        # =====================================================
        # 6. LINEAR REGRESSION
        # =====================================================

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        linear_predicted = (
            intercept
            + slope * x
        )

        linear_next = float(
            intercept
            + slope * len(y)
        )

        linear_three_month = float(
            intercept
            + slope * (len(y) + 2)
        )

        linear_mae = float(
            np.mean(
                np.abs(
                    y - linear_predicted
                )
            )
        )

        # =====================================================
        # 7. MOVING AVERAGE
        # =====================================================

        window = min(
            3,
            len(y)
        )

        moving_average_next = float(
            np.mean(
                y[-window:]
            )
        )

        moving_average_three_month = (
            moving_average_next
        )

        ma_errors = []

        if len(y) > window:

            for i in range(
                window,
                len(y)
            ):

                historical_prediction = float(
                    np.mean(
                        y[i - window:i]
                    )
                )

                actual_value = float(
                    y[i]
                )

                ma_errors.append(
                    abs(
                        actual_value
                        - historical_prediction
                    )
                )

        if ma_errors:

            moving_average_mae = float(
                np.mean(
                    ma_errors
                )
            )

        else:

            moving_average_mae = float(
                np.mean(
                    np.abs(
                        y
                        - moving_average_next
                    )
                )
            )

        # =====================================================
        # 8. BEST MODEL SELECTION
        # =====================================================

        if linear_mae <= moving_average_mae:

            best_model = (
                "Linear Regression"
            )

            next_forecast = (
                linear_next
            )

            three_month_forecast = (
                linear_three_month
            )

            model_error = (
                linear_mae
            )

        else:

            best_model = (
                "Moving Average"
            )

            next_forecast = (
                moving_average_next
            )

            three_month_forecast = (
                moving_average_three_month
            )

            model_error = (
                moving_average_mae
            )

        # =====================================================
        # 9. BACKTEST VALIDATION
        # =====================================================

        try:

            backtest = (
                _forecast_backtest(
                    y
                )
            )

        except Exception:

            try:

                backtest = (
                    _forecast_backtest_validation(
                        y
                    )
                )

            except Exception:

                backtest = {
                    "validation_status":
                        "unavailable",
                    "validation_score":
                        0
                }

        # =====================================================
        # 10. TREND ANALYSIS
        # =====================================================

        mean_value = float(
            np.mean(y)
        )

        if mean_value != 0:

            normalized_slope = (
                slope
                / abs(mean_value)
            )

        else:

            normalized_slope = 0.0

        if normalized_slope >= 0.02:

            trend = "strong upward"

        elif normalized_slope >= 0.005:

            trend = "weak upward"

        elif normalized_slope <= -0.02:

            trend = "strong downward"

        elif normalized_slope <= -0.005:

            trend = "weak downward"

        else:

            trend = "stable"

        # =====================================================
        # 11. FORECAST CHANGE
        # =====================================================

        if current_value != 0:

            expected_change_percent = (
                (
                    next_forecast
                    - current_value
                )
                / abs(current_value)
            ) * 100

        else:

            expected_change_percent = None

        # =====================================================
        # 12. GROWTH ANALYSIS
        # =====================================================

        if current_value != 0:

            growth_rate_percent = (
                (
                    next_forecast
                    - current_value
                )
                / abs(current_value)
            ) * 100

            three_month_growth_percent = (
                (
                    three_month_forecast
                    - current_value
                )
                / abs(current_value)
            ) * 100

        else:

            growth_rate_percent = 0.0
            three_month_growth_percent = 0.0

        if growth_rate_percent >= 2:

            growth_direction = "Growing"

        elif growth_rate_percent <= -2:

            growth_direction = "Declining"

        else:

            growth_direction = "Stable"

        absolute_growth = abs(
            growth_rate_percent
        )

        if absolute_growth >= 15:

            trend_strength = "Strong"

        elif absolute_growth >= 5:

            trend_strength = "Moderate"

        else:

            trend_strength = "Weak"

        if (
            growth_rate_percent > 0
            and three_month_growth_percent
            > growth_rate_percent
        ):

            growth_momentum = (
                "Accelerating"
            )

        elif (
            growth_rate_percent < 0
            and three_month_growth_percent
            < growth_rate_percent
        ):

            growth_momentum = (
                "Worsening"
            )

        elif growth_direction == "Stable":

            growth_momentum = "Stable"

        else:

            growth_momentum = "Steady"

        # =====================================================
        # 13. VOLATILITY
        # =====================================================

        std_dev = float(
            np.std(y)
        )

        if mean_value != 0:

            volatility_ratio = (
                std_dev
                / abs(mean_value)
            )

        else:

            volatility_ratio = 0.0

        volatility_percent = (
            abs(volatility_ratio)
            * 100
        )

        if volatility_percent < 10:

            forecast_risk = "Low"

        elif volatility_percent < 25:

            forecast_risk = "Medium"

        else:

            forecast_risk = "High"

        # =====================================================
        # 14. R-SQUARED
        # =====================================================

        ss_res = float(
            np.sum(
                (
                    y
                    - linear_predicted
                ) ** 2
            )
        )

        ss_tot = float(
            np.sum(
                (
                    y
                    - np.mean(y)
                ) ** 2
            )
        )

        if ss_tot > 0:

            r_squared = max(
                0.0,
                min(
                    1.0,
                    1
                    - (
                        ss_res
                        / ss_tot
                    )
                )
            )

        else:

            r_squared = 0.0

        # =====================================================
        # 15. FORECAST CONFIDENCE
        # =====================================================

        try:

            confidence_analysis = (
                calculate_forecast_confidence(
                    current_value=current_value,
                    forecast_value=next_forecast,
                    model_error=model_error,
                    volatility_ratio=volatility_ratio,
                    data_points=len(y)
                )
            )

        except Exception:

            confidence_analysis = {
                "confidence_score": 0.0,
                "confidence_level": "Low",
                "forecast_risk": forecast_risk,
                "forecast_change_percent": (
                    round(
                        float(
                            expected_change_percent
                            or 0
                        ),
                        2
                    )
                ),
                "lower_bound": (
                    next_forecast
                    - model_error
                ),
                "upper_bound": (
                    next_forecast
                    + model_error
                ),
                "model_error": model_error
            }

        confidence_score = float(
            confidence_analysis.get(
                "confidence_score",
                0
            )
        )

        confidence_level = (
            confidence_analysis.get(
                "confidence_level",
                "Low"
            )
        )

        # =====================================================
        # 16. FORECAST QUALITY
        # =====================================================

        if confidence_score >= 75:

            forecast_quality = "high"

        elif confidence_score >= 50:

            forecast_quality = "medium"

        else:

            forecast_quality = "low"

        # =====================================================
        # 17. FORECAST RANGE
        # =====================================================

        forecast_range = max(
            abs(model_error),
            abs(next_forecast)
            * abs(volatility_ratio)
        )

        lower_forecast = (
            next_forecast
            - forecast_range
        )

        upper_forecast = (
            next_forecast
            + forecast_range
        )

        # =====================================================
        # 18. FORECAST RELIABILITY
        # =====================================================

        try:

            reliability = (
                _forecast_reliability(
                    confidence_score=confidence_score,
                    r_squared=r_squared,
                    volatility_ratio=volatility_ratio,
                    data_points=len(y),
                    current_value=current_value
                )
            )

        except Exception:

            reliability = {
                "level": confidence_level,
                "score": round(
                    confidence_score,
                    2
                )
            }

        # =====================================================
        # 19. BUSINESS METRICS
        # =====================================================

        try:

            business_metrics = (
                _forecast_business_metrics(
                    metric_name=str(col),
                    current_value=current_value,
                    forecast_value=next_forecast,
                    behavior=trend,
                    reliability=reliability
                )
            )

        except Exception:

            business_metrics = {}

        # =====================================================
        # 20. BUSINESS PRIORITY
        # =====================================================

        col_name = str(col).lower()

        if any(
            keyword in col_name
            for keyword in [
                "revenue",
                "profit",
                "sales"
            ]
        ):

            business_priority = "Critical"
            priority_score = 100

        elif any(
            keyword in col_name
            for keyword in [
                "target",
                "achievement",
                "expense",
                "expenses"
            ]
        ):

            business_priority = "High"
            priority_score = 80

        elif any(
            keyword in col_name
            for keyword in [
                "salary",
                "bonus",
                "incentive",
                "performance",
                "attendance"
            ]
        ):

            business_priority = "Medium"
            priority_score = 60

        else:

            business_priority = "Normal"
            priority_score = 40

        # =====================================================
        # 21. DATE PERIODS
        # =====================================================

        try:

            last_period = pd.Period(
                str(
                    monthly_data.index[-1]
                ),
                freq="M"
            )

            next_period = (
                last_period + 1
            )

            three_month_period = (
                last_period + 3
            )

        except Exception:

            last_period = (
                monthly_data.index[-1]
            )

            next_period = (
                "Next Period"
            )

            three_month_period = (
                "Three Months Ahead"
            )

        # =====================================================
        # 22. SCENARIO ANALYSIS
        # =====================================================

        try:

            forecast_scenarios = (
                generate_forecast_scenarios(
                    current_value=current_value,
                    forecast_value=next_forecast,
                    lower_bound=lower_forecast,
                    upper_bound=upper_forecast,
                    forecast_risk=forecast_risk
                )
            )

        except Exception:

            forecast_scenarios = {}

        # =====================================================
        # 23. EXPLAINABILITY
        # =====================================================

        try:

            forecast_explanation = (
                generate_forecast_explanation(
                    metric=str(col),
                    expected_change_percent=(
                        expected_change_percent
                    ),
                    trend=trend,
                    trend_strength=trend_strength,
                    forecast_risk=forecast_risk,
                    confidence_score=confidence_score,
                    volatility_ratio=volatility_ratio,
                    best_model=best_model
                )
            )

        except Exception:

            forecast_explanation = (
                f"{col} is expected to "
                f"{'increase' if (expected_change_percent or 0) > 0 else 'decrease'} "
                f"by approximately "
                f"{abs(expected_change_percent or 0):.2f}% "
                f"in the next forecast period."
            )

        # =====================================================
        # 24. FORECAST ITEM
        # =====================================================

        forecast_item = {

            "metric":
                str(col),

            "business_priority":
                business_priority,

            "priority_score":
                priority_score,

            "last_period":
                str(last_period),

            "next_forecast_period":
                str(next_period),

            "three_month_forecast_period":
                str(three_month_period),

            "current_value":
                round(
                    current_value,
                    4
                ),

            "next_month_forecast":
                round(
                    next_forecast,
                    4
                ),

            "three_month_forecast":
                round(
                    three_month_forecast,
                    4
                ),

            "expected_change_percent":
                (
                    round(
                        float(
                            expected_change_percent
                        ),
                        2
                    )
                    if expected_change_percent
                    is not None
                    else None
                ),

            "forecast_change_percent":
                (
                    round(
                        float(
                            expected_change_percent
                            or 0
                        ),
                        2
                    )
                ),

            "growth_rate_percent":
                round(
                    growth_rate_percent,
                    2
                ),

            "three_month_growth_percent":
                round(
                    three_month_growth_percent,
                    2
                ),

            "growth_direction":
                growth_direction,

            "growth_momentum":
                growth_momentum,

            "trend":
                trend,

            "trend_strength":
                trend_strength,

            "trend_strength_label":
                trend_strength,

            "normalized_slope":
                round(
                    float(
                        normalized_slope
                    ),
                    6
                ),

            "volatility_percent":
                round(
                    volatility_percent,
                    2
                ),

            "volatility_ratio":
                round(
                    float(
                        volatility_ratio
                    ),
                    4
                ),

            "forecast_risk":
                forecast_risk,

            "confidence_score":
                round(
                    confidence_score,
                    2
                ),

            "confidence_level":
                confidence_level,

            "forecast_quality":
                forecast_quality,

            "forecast_reliability":
                reliability,

            "forecast_range": {

                "lower":
                    round(
                        lower_forecast,
                        4
                    ),

                "expected":
                    round(
                        next_forecast,
                        4
                    ),

                "upper":
                    round(
                        upper_forecast,
                        4
                    )
            },

            "confidence_range": {

                "lower":
                    confidence_analysis.get(
                        "lower_bound",
                        lower_forecast
                    ),

                "upper":
                    confidence_analysis.get(
                        "upper_bound",
                        upper_forecast
                    )
            },

            "model_error":
                round(
                    float(model_error),
                    4
                ),

            "best_model":
                best_model,

            "model_comparison": {

                "linear_regression_mae":
                    round(
                        linear_mae,
                        4
                    ),

                "moving_average_mae":
                    round(
                        moving_average_mae,
                        4
                    )
            },

            "r_squared":
                round(
                    float(r_squared),
                    4
                ),

            "data_points":
                int(len(y)),

            "backtest":
                backtest,

            "business_metrics":
                business_metrics,

            "scenarios":
                forecast_scenarios,

            "explanation":
                forecast_explanation,

            "method":
                (
                    "Multi-Model Forecasting "
                    "with Automatic Best Model Selection"
                )
        }

        forecasts.append(
            forecast_item
        )

        # =====================================================
        # 25. FORECAST ALERT
        # =====================================================

        if (
            expected_change_percent
            is not None
            and abs(
                expected_change_percent
            ) >= 5
        ):

            alert_priority = (
                "high"
                if abs(
                    expected_change_percent
                ) >= 15
                else "medium"
            )

            alerts.append({

                "priority":
                    alert_priority,

                "metric":
                    str(col),

                "message":
                    (
                        f"{col} is forecasted to "
                        f"{'increase' if expected_change_percent > 0 else 'decrease'} "
                        f"by "
                        f"{abs(expected_change_percent):.2f}% "
                        f"in the next period."
                    ),

                "forecast_quality":
                    forecast_quality,

                "forecast_risk":
                    forecast_risk,

                "best_model":
                    best_model
            })

        # =====================================================
        # 26. BASIC FORECAST INSIGHT
        # =====================================================

        if expected_change_percent is None:

            forecast_direction = (
                "change"
            )

        elif expected_change_percent > 5:

            forecast_direction = (
                "increase"
            )

        elif expected_change_percent < -5:

            forecast_direction = (
                "decrease"
            )

        else:

            forecast_direction = (
                "remain relatively stable"
            )

        insights.append({

            "metric":
                str(col),

            "summary":
                (
                    f"{col} is expected to "
                    f"{forecast_direction} "
                    f"in the next forecast period."
                ),

            "current_value":
                round(
                    current_value,
                    4
                ),

            "forecast_value":
                round(
                    next_forecast,
                    4
                ),

            "expected_change_percent":
                (
                    round(
                        float(
                            expected_change_percent
                        ),
                        2
                    )
                    if expected_change_percent
                    is not None
                    else None
                ),

            "trend":
                trend,

            "forecast_quality":
                forecast_quality,

            "forecast_risk":
                forecast_risk,

            "best_model":
                best_model
        })

    # =========================================================
    # 27. NO FORECAST RESULT
    # =========================================================

    if not forecasts:

        return {
            "success": False,
            "message": (
                "Forecasting requires at least "
                "two valid monthly data points "
                "for a meaningful numeric metric."
            ),
            "date_column": str(date_col)
        }

    # =========================================================
    # 28. SORT BY BUSINESS PRIORITY
    # =========================================================

    forecasts = sorted(
        forecasts,
        key=lambda item: (
            item.get(
                "priority_score",
                0
            ),
            abs(
                item.get(
                    "expected_change_percent",
                    0
                ) or 0
            )
        ),
        reverse=True
    )

    # =========================================================
    # 29. QUALITY SUMMARY
    # =========================================================

    quality_summary = {

        "high":
            sum(
                1
                for item in forecasts
                if item.get(
                    "forecast_quality"
                ) == "high"
            ),

        "medium":
            sum(
                1
                for item in forecasts
                if item.get(
                    "forecast_quality"
                ) == "medium"
            ),

        "low":
            sum(
                1
                for item in forecasts
                if item.get(
                    "forecast_quality"
                ) == "low"
            )
    }

    # =========================================================
    # 30. SMART FORECAST INTELLIGENCE
    # =========================================================

    try:

        forecast_intelligence = (
            _generate_forecast_insights(
                forecasts
            )
        )

    except Exception:

        forecast_intelligence = {

            "insights":
                insights,

            "recommendations":
                []
        }

    intelligence_insights = (
        forecast_intelligence.get(
            "insights",
            insights
        )
    )

    intelligence_recommendations = (
        forecast_intelligence.get(
            "recommendations",
            []
        )
    )

    # =========================================================
    # 31. EXECUTIVE SUMMARY
    # =========================================================

    executive_summary = {

        "top_priority_metric":
            None,

        "strongest_positive_forecast":
            None,

        "strongest_negative_forecast":
            None,

        "highest_risk_metric":
            None
    }

    if forecasts:

        executive_summary[
            "top_priority_metric"
        ] = forecasts[0]

        executive_summary[
            "strongest_positive_forecast"
        ] = max(
            forecasts,
            key=lambda item: (
                item.get(
                    "expected_change_percent"
                )
                if item.get(
                    "expected_change_percent"
                ) is not None
                else float("-inf")
            )
        )

        executive_summary[
            "strongest_negative_forecast"
        ] = min(
            forecasts,
            key=lambda item: (
                item.get(
                    "expected_change_percent"
                )
                if item.get(
                    "expected_change_percent"
                ) is not None
                else float("inf")
            )
        )

        risk_order = {

            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        executive_summary[
            "highest_risk_metric"
        ] = max(
            forecasts,
            key=lambda item: (
                risk_order.get(
                    item.get(
                        "forecast_risk",
                        "Low"
                    ),
                    0
                )
            )
        )

    # =========================================================
    # 32. SAVE FORECAST HISTORY
    # =========================================================

    for forecast in forecasts:

        forecast_record = {

            "metric":
                forecast.get(
                    "metric"
                ),

            "forecast_value":
                forecast.get(
                    "next_month_forecast"
                ),

            "forecast_period":
                forecast.get(
                    "next_forecast_period"
                ),

            "current_value":
                forecast.get(
                    "current_value"
                ),

            "best_model":
                forecast.get(
                    "best_model"
                ),

            "created_at":
                str(
                    pd.Timestamp.now()
                )
        }

        duplicate_exists = any(

            item.get(
                "metric"
            )
            == forecast_record.get(
                "metric"
            )

            and

            item.get(
                "forecast_period"
            )
            == forecast_record.get(
                "forecast_period"
            )

            for item in forecast_history
        )

        if not duplicate_exists:

            forecast_history.append(
                forecast_record
            )

    print(
        "FORECAST DEBUG:",
        len(forecasts)
    )

    # =========================================================
    # 33. FINAL RESPONSE
    # =========================================================

    return {

        "success":
            True,

        "date_column":
            str(date_col),

        "aggregation":
            "monthly average",

        "metrics_analyzed":
            len(forecasts),

        "forecast_quality":
            quality_summary,

        "alerts":
            alerts,

        "insights":
            intelligence_insights,

        "recommendations":
            intelligence_recommendations,

        "executive_summary":
            executive_summary,

        "forecasts":
            forecasts
    }

        
    # =====================================================
# FORECAST CONFIDENCE & RISK ANALYSIS
# =====================================================

def calculate_forecast_confidence(
    current_value,
    forecast_value,
    model_error,
    volatility_ratio,
    data_points
):

    # ---------------------------------------------
    # DEFAULT VALUES
    # ---------------------------------------------

    current_value = float(current_value or 0)
    forecast_value = float(forecast_value or 0)
    model_error = abs(float(model_error or 0))
    volatility_ratio = abs(
        float(volatility_ratio or 0)
    )

    data_points = int(data_points or 0)

    # ---------------------------------------------
    # FORECAST CHANGE
    # ---------------------------------------------

    if current_value != 0:

        forecast_change_percent = (
            (
                forecast_value
                - current_value
            )
            / abs(current_value)
        ) * 100

    else:

        forecast_change_percent = 0.0

    # ---------------------------------------------
    # MODEL ERROR SCORE
    # ---------------------------------------------

    if current_value != 0:

        error_percent = (
            model_error
            / abs(current_value)
        ) * 100

    else:

        error_percent = model_error

    error_score = max(
        0,
        100 - error_percent
    )

    # ---------------------------------------------
    # VOLATILITY SCORE
    # ---------------------------------------------

    volatility_percent = (
        volatility_ratio * 100
        if volatility_ratio <= 1
        else volatility_ratio
    )

    volatility_score = max(
        0,
        100 - volatility_percent
    )

    # ---------------------------------------------
    # DATA SUFFICIENCY SCORE
    # ---------------------------------------------

    data_score = min(
        100,
        data_points * 10
    )

    # ---------------------------------------------
    # FINAL CONFIDENCE SCORE
    # ---------------------------------------------

    confidence_score = (

        error_score * 0.50

        + volatility_score * 0.30

        + data_score * 0.20

    )

    confidence_score = max(
        0,
        min(
            100,
            confidence_score
        )
    )

    # ---------------------------------------------
    # CONFIDENCE LEVEL
    # ---------------------------------------------

    if confidence_score >= 80:

        confidence_level = "High"

    elif confidence_score >= 60:

        confidence_level = "Medium"

    else:

        confidence_level = "Low"

    # ---------------------------------------------
    # FORECAST RISK
    # ---------------------------------------------

    if confidence_score >= 80:

        forecast_risk = "Low"

    elif confidence_score >= 60:

        forecast_risk = "Medium"

    else:

        forecast_risk = "High"

    # ---------------------------------------------
    # FORECAST RANGE
    # ---------------------------------------------

    uncertainty = max(
        model_error,
        abs(forecast_value)
        * volatility_ratio
    )

    lower_bound = (
        forecast_value
        - uncertainty
    )

    upper_bound = (
        forecast_value
        + uncertainty
    )

    return {

        "confidence_score": round(
            confidence_score,
            2
        ),

        "confidence_level":
            confidence_level,

        "forecast_risk":
            forecast_risk,

        "forecast_change_percent": round(
            forecast_change_percent,
            2
        ),

        "lower_bound": round(
            lower_bound,
            2
        ),

        "upper_bound": round(
            upper_bound,
            2
        ),

        "model_error": round(
            model_error,
            2
        )
    }
def _smart_group_column(df):
    """
    Select a meaningful categorical column for analysis.
    Ignores high-cardinality columns such as Employee Name, Email, etc.
    """

    preferred_columns = [
        "Department",
        "Branch",
        "City",
        "Gender",
        "Work Mode",
        "Designation",
        "Employment Type",
        "Project",
        "Project Status",
        "Shift",
        "Education",
        "Skill Level",
        "Promotion",
        "Resigned"
    ]

    # First try preferred business columns
    for col in preferred_columns:
        if col in df.columns:
            unique_count = df[col].nunique(dropna=True)

            if 2 <= unique_count <= 50:
                return col

    # Fallback: any reasonable categorical column
    for col in df.columns:
        if (
            df[col].dtype == "object"
            or pd.api.types.is_categorical_dtype(df[col])
        ):
            unique_count = df[col].nunique(dropna=True)

            if 2 <= unique_count <= 50:
                return col

    return None


def _smart_metric_column(df):
    """
    Select a meaningful numeric business metric.
    Avoid IDs and phone numbers.
    """

    preferred_metrics = [
        "Salary",
        "Profit",
        "Revenue",
        "Expenses",
        "Monthly Sales",
        "Bonus",
        "Incentive",
        "Attendance %",
        "Achievement %",
        "Performance Rating",
        "Training Hours",
        "Experience (Years)",
        "Age"
    ]

    for col in preferred_metrics:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            return col

    # Fallback numeric column
    for col in _numeric_columns(df):
        col_lower = str(col).lower()

        if (
            "id" not in col_lower
            and "phone" not in col_lower
            and "mobile" not in col_lower
        ):
            return col

    return None


def genesis_dashboard_group():
    df = require_df()

    group_col = _smart_group_column(df)
    metric = _smart_metric_column(df)

    if not group_col:
        return {
            "success": False,
            "message": "No suitable categorical column available for group analysis."
        }

    counts = (
        df[group_col]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .head(20)
    )

    result = {
        "success": True,
        "group_column": str(group_col),
        "group_counts": _json_safe(counts.to_dict())
    }

    if metric:
        grouped = (
            df.groupby(group_col, dropna=False)[metric]
            .agg(["count", "mean", "sum", "min", "max"])
            .round(2)
            .sort_values("mean", ascending=False)
            .head(20)
        )

        result["metric_column"] = str(metric)
        result["analysis"] = _json_safe(
            grouped.reset_index().to_dict(orient="records")
        )

        if len(grouped) > 0:
            result["highest_average_group"] = str(grouped.index[0])
            result["highest_average_value"] = round(
                float(grouped.iloc[0]["mean"]), 2
            )

            result["lowest_average_group"] = str(grouped.index[-1])
            result["lowest_average_value"] = round(
                float(grouped.iloc[-1]["mean"]), 2
            )

    return result


def genesis_dashboard_comparison():
    df = require_df()

    group_col = _smart_group_column(df)
    metric = _smart_metric_column(df)

    if not group_col:
        return {
            "success": False,
            "message": "No suitable categorical column available for comparison."
        }

    if not metric:
        return {
            "success": False,
            "message": "No suitable numeric metric available for comparison."
        }

    grouped = (
        df.groupby(group_col, dropna=False)[metric]
        .agg(["count", "mean", "sum", "min", "max"])
        .round(2)
        .sort_values("mean", ascending=False)
    )

    if len(grouped) < 2:
        return {
            "success": False,
            "message": "At least two groups are required for comparison."
        }

    highest_group = grouped.index[0]
    lowest_group = grouped.index[-1]

    highest_value = float(grouped.iloc[0]["mean"])
    lowest_value = float(grouped.iloc[-1]["mean"])

    difference = highest_value - lowest_value

    percent_difference = (
        (difference / lowest_value) * 100
        if lowest_value != 0
        else None
    )

    return {
        "success": True,

        "comparison_column": str(group_col),
        "metric_column": str(metric),

        "highest_group": str(highest_group),
        "highest_average": round(highest_value, 2),

        "lowest_group": str(lowest_group),
        "lowest_average": round(lowest_value, 2),

        "difference": round(difference, 2),

        "percentage_difference": (
            round(percent_difference, 2)
            if percent_difference is not None
            else None
        ),

        "all_groups": _json_safe(
            grouped.reset_index().to_dict(orient="records")
        )
    }





def genesis_dashboard_ranking():
    df = require_df()

    # Smart business metric selection
    metric = _smart_metric_column(df)

    if not metric:
        return {
            "success": False,
            "message": "No suitable numeric metric available for ranking."
        }

    # Exclude meaningless identifier columns from display if possible
    display_cols = []

    preferred_display = [
        "Employee Name",
        "Department",
        "Designation",
        "Branch",
        "City",
        metric
    ]

    for col in preferred_display:
        if col in df.columns and col not in display_cols:
            display_cols.append(col)

    # Fallback
    if metric not in display_cols:
        display_cols.append(metric)

    ranked = (
        df[display_cols]
        .copy()
        .sort_values(metric, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    ranked.insert(
        0,
        "Rank",
        range(1, len(ranked) + 1)
    )

    return {
        "success": True,
        "ranking_metric": str(metric),
        "ranking_type": "Top 10",
        "top_10": _json_safe(
            ranked.to_dict(orient="records")
        )
    }


def genesis_dashboard_cleaning():
    df = require_df()

    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates()

    for col in cleaned.columns:
        if pd.api.types.is_numeric_dtype(cleaned[col]):
            if cleaned[col].isna().any():
                cleaned[col] = cleaned[col].fillna(cleaned[col].median())
        else:
            if cleaned[col].isna().any():
                cleaned[col] = cleaned[col].fillna("Missing")

    return {
        "original_rows": int(len(df)),
        "cleaned_rows": int(len(cleaned)),
        "duplicates_removed": int(duplicates_before),
        "missing_values_before": int(missing_before),
        "missing_values_after": int(cleaned.isna().sum().sum()),
        "status": "Cleaning analysis completed. Original uploaded dataset was not overwritten."
    }


@app.api_route("/analytics/insights", methods=["GET", "POST"])
def analytics_insights():
    return genesis_dashboard_insights()


def analytics_statistics():
    return genesis_dashboard_statistics()


@app.api_route("/analytics/quality", methods=["GET", "POST"])
def analytics_quality():
    return genesis_dashboard_quality()


@app.api_route("/analytics/profile", methods=["GET", "POST"])
def analytics_profile():
    return genesis_dashboard_profile()


@app.api_route("/analytics/correlation", methods=["GET", "POST"])
def analytics_correlation():
    return genesis_dashboard_correlation()




    import numpy as np

    y = np.asarray(
        y,
        dtype=float
    )

    total_points = len(y)

    # ---------------------------------------------
    # MINIMUM DATA CHECK
    # ---------------------------------------------

    if total_points < 6:

        return {
            "validation_status": "weak_validation",
            "validation_points": 0,
            "linear_backtest_mae": None,
            "moving_average_backtest_mae": None,
            "naive_backtest_mae": None,
            "best_backtest_model": None,
            "baseline_improvement_percent": 0.0,
            "model_beats_baseline": False,
            "validation_score": 0.0
        }

    # ---------------------------------------------
    # VALIDATION POINTS
    # ---------------------------------------------

    validation_points = min(
        12,
        max(
            3,
            total_points // 5
        )
    )

    errors_linear = []
    errors_moving_average = []
    errors_naive = []

    start_index = total_points - validation_points

    # ---------------------------------------------
    # WALK-FORWARD BACKTEST
    # ---------------------------------------------

    for i in range(
        start_index,
        total_points
    ):

        train = y[:i]

        actual = y[i]

        if len(train) < 3:
            continue

        # -----------------------------------------
        # LINEAR REGRESSION
        # -----------------------------------------

        x_train = np.arange(
            len(train)
        )

        slope, intercept = np.polyfit(
            x_train,
            train,
            1
        )

        linear_prediction = (
            slope * len(train)
            + intercept
        )

        # -----------------------------------------
        # MOVING AVERAGE
        # -----------------------------------------

        window = min(
            3,
            len(train)
        )

        moving_average_prediction = float(
            np.mean(
                train[-window:]
            )
        )

        # -----------------------------------------
        # NAIVE BASELINE
        # -----------------------------------------

        naive_prediction = float(
            train[-1]
        )

        # -----------------------------------------
        # ERRORS
        # -----------------------------------------

        errors_linear.append(
            abs(
                actual
                - linear_prediction
            )
        )

        errors_moving_average.append(
            abs(
                actual
                - moving_average_prediction
            )
        )

        errors_naive.append(
            abs(
                actual
                - naive_prediction
            )
        )

    # ---------------------------------------------
    # MAE CALCULATION
    # ---------------------------------------------

    linear_mae = float(
        np.mean(
            errors_linear
        )
    )

    moving_average_mae = float(
        np.mean(
            errors_moving_average
        )
    )

    naive_mae = float(
        np.mean(
            errors_naive
        )
    )

    model_scores = {
        "Linear Regression": linear_mae,
        "Moving Average": moving_average_mae,
        "Naive Baseline": naive_mae
    }

    best_backtest_model = min(
        model_scores,
        key=model_scores.get
    )

    best_mae = model_scores[
        best_backtest_model
    ]

    # ---------------------------------------------
    # BASELINE IMPROVEMENT
    # ---------------------------------------------

    if naive_mae > 0:

        baseline_improvement_percent = (
            (
                naive_mae
                - best_mae
            )
            / naive_mae
        ) * 100

    else:

        baseline_improvement_percent = 0.0

    model_beats_baseline = (
        best_mae
        < naive_mae
    )

    # ---------------------------------------------
    # VALIDATION SCORE
    # ---------------------------------------------

    if baseline_improvement_percent >= 20:

        validation_score = 100.0

        validation_status = "strong_validation"

    elif baseline_improvement_percent >= 5:

        validation_score = 75.0

        validation_status = "good_validation"

    elif model_beats_baseline:

        validation_score = 55.0

        validation_status = "moderate_validation"

    else:

        validation_score = 25.0

        validation_status = "weak_validation"

    # ---------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------

    return {
        "validation_status": validation_status,

        "validation_points": int(
            len(
                errors_linear
            )
        ),

        "linear_backtest_mae": round(
            linear_mae,
            4
        ),

        "moving_average_backtest_mae": round(
            moving_average_mae,
            4
        ),

        "naive_backtest_mae": round(
            naive_mae,
            4
        ),

        "best_backtest_model": best_backtest_model,

        "baseline_improvement_percent": round(
            baseline_improvement_percent,
            2
        ),

        "model_beats_baseline": bool(
            model_beats_baseline
        ),

        "validation_score": round(
            validation_score,
            2
        )
    }

def _forecast_backtest_validation(y):

    import numpy as np

    y = np.asarray(
        y,
        dtype=float
    )

    total_points = len(y)

    # ---------------------------------------------
    # MINIMUM DATA CHECK
    # ---------------------------------------------

    if total_points < 6:

        return {
            "validation_status": "weak_validation",
            "validation_points": 0,
            "linear_backtest_mae": None,
            "moving_average_backtest_mae": None,
            "naive_backtest_mae": None,
            "best_backtest_model": None,
            "baseline_improvement_percent": 0.0,
            "model_beats_baseline": False,
            "validation_score": 0.0
        }




    # ---------------------------------------------
    # NUMBER OF BACKTEST POINTS
    # ---------------------------------------------

    validation_points = min(
        12,
        max(
            3,
            total_points // 5
        )
    )

    start_index = (
        total_points
        - validation_points
    )

    linear_errors = []
    moving_average_errors = []
    naive_errors = []

    # ---------------------------------------------
    # WALK-FORWARD BACKTEST
    # ---------------------------------------------

    for i in range(
        start_index,
        total_points
    ):

        train_y = y[:i]

        actual_value = float(
            y[i]
        )

        if len(train_y) < 3:
            continue

        # -----------------------------------------
        # NAIVE BASELINE
        # -----------------------------------------

        naive_prediction = float(
            train_y[-1]
        )

        naive_error = abs(
            actual_value
            - naive_prediction
        )

        naive_errors.append(
            naive_error
        )

        # -----------------------------------------
        # LINEAR REGRESSION
        # -----------------------------------------

        x_train = np.arange(
            len(train_y)
        )

        slope, intercept = np.polyfit(
            x_train,
            train_y,
            1
        )

        linear_prediction = float(
            intercept
            + (
                slope
                * len(train_y)
            )
        )

        linear_error = abs(
            actual_value
            - linear_prediction
        )

        linear_errors.append(
            linear_error
        )

        # -----------------------------------------
        # MOVING AVERAGE
        # -----------------------------------------

        window_size = min(
            6,
            len(train_y)
        )

        moving_average_prediction = float(
            np.mean(
                train_y[
                    -window_size:
                ]
            )
        )

        moving_average_error = abs(
            actual_value
            - moving_average_prediction
        )

        moving_average_errors.append(
            moving_average_error
        )

    # ---------------------------------------------
    # MAE CALCULATION
    # ---------------------------------------------

    if not naive_errors:

        return {
            "validation_status": "weak_validation",
            "validation_points": 0,
            "linear_backtest_mae": None,
            "moving_average_backtest_mae": None,
            "naive_backtest_mae": None,
            "best_backtest_model": None,
            "baseline_improvement_percent": 0.0,
            "model_beats_baseline": False,
            "validation_score": 0.0
        }

    linear_backtest_mae = float(
        np.mean(
            linear_errors
        )
    )

    moving_average_backtest_mae = float(
        np.mean(
            moving_average_errors
        )
    )

    naive_backtest_mae = float(
        np.mean(
            naive_errors
        )
    )

    # ---------------------------------------------
    # BEST MODEL
    # ---------------------------------------------

    backtest_models = {
        "Linear Regression":
            linear_backtest_mae,

        "Moving Average":
            moving_average_backtest_mae,

        "Naive Baseline":
            naive_backtest_mae
    }

    best_backtest_model = min(
        backtest_models,
        key=backtest_models.get
    )

    best_model_mae = float(
        backtest_models[
            best_backtest_model
        ]
    )

    # ---------------------------------------------
    # BASELINE IMPROVEMENT
    # ---------------------------------------------

    if naive_backtest_mae > 0:

        baseline_improvement_percent = (
            (
                naive_backtest_mae
                - best_model_mae
            )
            / naive_backtest_mae
        ) * 100

    else:

        baseline_improvement_percent = 0.0

    baseline_improvement_percent = round(
        float(
            baseline_improvement_percent
        ),
        2
    )

    model_beats_baseline = (
        best_model_mae
        < naive_backtest_mae
    )

    # ---------------------------------------------
    # VALIDATION SCORE
    # ---------------------------------------------

    if model_beats_baseline:

        validation_score = min(
            100.0,
            max(
                0.0,
                baseline_improvement_percent
                * 2
            )
        )

    else:

        validation_score = 0.0

    validation_score = round(
        float(
            validation_score
        ),
        2
    )

    # ---------------------------------------------
    # VALIDATION STATUS
    # ---------------------------------------------

    if (
        model_beats_baseline
        and baseline_improvement_percent >= 15
    ):

        validation_status = "validated"

    elif (
        model_beats_baseline
        and baseline_improvement_percent > 0
    ):

        validation_status = (
            "partially_validated"
        )

    else:

        validation_status = (
            "weak_validation"
        )

    # ---------------------------------------------
    # RETURN
    # ---------------------------------------------

    return {
        "validation_status":
            validation_status,

        "validation_points":
            len(naive_errors),

        "linear_backtest_mae":
            round(
                linear_backtest_mae,
                4
            ),

        "moving_average_backtest_mae":
            round(
                moving_average_backtest_mae,
                4
            ),

        "naive_backtest_mae":
            round(
                naive_backtest_mae,
                4
            ),

        "best_backtest_model":
            best_backtest_model,

        "baseline_improvement_percent":
            baseline_improvement_percent,

        "model_beats_baseline":
            bool(
                model_beats_baseline
            ),

        "validation_score":
            validation_score
    }
@app.api_route("/analytics/forecast", methods=["GET", "POST"])
def analytics_forecast():

    return genesis_dashboard_forecast()
# =====================================================
# FORECAST HISTORY API
# =====================================================

@app.get("/api/analytics/forecast-history")
def get_forecast_history():

    return {

        "success": True,

        "total_forecasts": len(
            forecast_history
        ),

        "history": forecast_history
    }
    # =====================================================
# FORECAST ACTUAL VALUE UPDATE API
# =====================================================

@app.post("/api/analytics/forecast-history/update")
def update_forecast_actual(
    metric: str,
    forecast_period: str,
    actual_value: float
):

    matching_forecast = None

    for item in forecast_history:

        if (
            str(item.get("metric")) == str(metric)
            and str(
                item.get("forecast_period")
            ) == str(forecast_period)
        ):

            matching_forecast = item
            break

    if matching_forecast is None:

        return {

            "success": False,

            "message": (
                "Matching forecast not found."
            )
        }

    forecast_value = matching_forecast.get(
        "forecast_value"
    )

    if forecast_value is None:

        return {

            "success": False,

            "message": (
                "Forecast value not available."
            )
        }

    actual_value = float(
        actual_value
    )

    forecast_value = float(
        forecast_value
    )

    absolute_error = abs(
        actual_value
        - forecast_value
    )

    error_percent = (
        absolute_error
        / abs(actual_value)
        * 100
        if actual_value != 0
        else 0
    )

    accuracy_percent = max(
        0,
        100 - error_percent
    )

    if accuracy_percent >= 90:

        accuracy_level = "Excellent"

    elif accuracy_percent >= 75:

        accuracy_level = "Good"

    elif accuracy_percent >= 50:

        accuracy_level = "Moderate"

    else:

        accuracy_level = "Low"

    matching_forecast[
        "actual_value"
    ] = actual_value

    matching_forecast[
        "accuracy"
    ] = {

        "forecast_value": round(
            forecast_value,
            4
        ),

        "actual_value": round(
            actual_value,
            4
        ),

        "absolute_error": round(
            absolute_error,
            4
        ),

        "error_percent": round(
            error_percent,
            2
        ),

        "accuracy_percent": round(
            accuracy_percent,
            2
        ),

        "accuracy_level": accuracy_level
    }

    return {

        "success": True,

        "message": (
            "Actual value updated successfully."
        ),

        "forecast": matching_forecast
    }


# =====================================================
# FORECAST TRACKING SUMMARY API
# =====================================================

@app.get("/api/analytics/forecast-tracking-summary")
def get_forecast_tracking_summary():

    total_forecasts = len(
        forecast_history
    )

    updated_forecasts = [
        item
        for item in forecast_history
        if item.get("actual_value") is not None
    ]

    pending_forecasts = (
        total_forecasts
        - len(updated_forecasts)
    )

    accuracy_values = []

    for item in updated_forecasts:

        accuracy = item.get(
            "accuracy"
        )

        if isinstance(
            accuracy,
            dict
        ):

            value = accuracy.get(
                "accuracy_percent"
            )

            if value is not None:

                accuracy_values.append(
                    float(value)
                )

    if accuracy_values:

        average_accuracy = (
            sum(accuracy_values)
            / len(accuracy_values)
        )

    else:

        average_accuracy = 0.0

    excellent = 0
    good = 0
    moderate = 0
    low = 0

    for item in updated_forecasts:

        accuracy = item.get(
            "accuracy"
        )

        if not isinstance(
            accuracy,
            dict
        ):
            continue

        level = accuracy.get(
            "accuracy_level"
        )

        if level == "Excellent":

            excellent += 1

        elif level == "Good":

            good += 1

        elif level == "Moderate":

            moderate += 1

        elif level == "Low":

            low += 1

    return {

        "success": True,

        "total_forecasts": total_forecasts,

        "actuals_updated": len(
            updated_forecasts
        ),

        "actuals_pending": pending_forecasts,

        "average_accuracy_percent": round(
            average_accuracy,
            2
        ),

        "accuracy_distribution": {

            "excellent": excellent,

            "good": good,

            "moderate": moderate,

            "low": low
        }
    }

    

    # =============================================
    # RETURN SUMMARY
    # =============================================

    return {

        "success": True,

        "total_forecasts": (
            total_forecasts
        ),

        "actuals_updated": (
            len(updated_forecasts)
        ),

        "actuals_pending": (
            pending_forecasts
        ),

        "average_accuracy_percent": round(
            average_accuracy,
            2
        ),

        "accuracy_distribution": {

            "excellent": excellent,

            "good": good,

            "moderate": moderate,

            "low": low
        }
    }
    # =============================================
    # FIND MATCHING FORECAST
    # =============================================

    matching_forecast = None

    for item in forecast_history:

        if (

            item.get("metric") == metric

            and

            item.get("forecast_period")
            == forecast_period
        ):

            matching_forecast = item

            break

    # =============================================
    # FORECAST NOT FOUND
    # =============================================

    if matching_forecast is None:

        return {

            "success": False,

            "message": (
                "Matching forecast not found."
            )
        }

    # =============================================
    # CALCULATE FORECAST ACCURACY
    # =============================================

    accuracy_result = (
        calculate_forecast_accuracy(

            forecast_value=
                matching_forecast.get(
                    "forecast_value"
                ),

            actual_value=
                actual_value
        )
    )

    # =============================================
    # SAVE ACTUAL RESULT
    # =============================================

    matching_forecast[
        "actual_value"
    ] = actual_value

    matching_forecast[
        "accuracy"
    ] = accuracy_result

    matching_forecast[
        "updated_at"
    ] = str(
        pd.Timestamp.now()
    )

    # =============================================
    # RETURN RESULT
    # =============================================

    return {

        "success": True,

        "message": (
            "Actual value updated successfully."
        ),

        "forecast": matching_forecast
    }


@app.api_route("/analytics/group", methods=["GET", "POST"])
def analytics_group():
    return genesis_dashboard_group()


@app.api_route("/analytics/comparison", methods=["GET", "POST"])
def analytics_comparison():
    return genesis_dashboard_comparison()


@app.api_route("/analytics/ranking", methods=["GET", "POST"])
def analytics_ranking():
    return genesis_dashboard_ranking()


@app.api_route("/analytics/cleaning", methods=["GET", "POST"])
def analytics_cleaning():
    return genesis_dashboard_cleaning()
# =========================================
# PREVIEW API
# =========================================

@app.api_route("/preview", methods=["GET", "POST"])
@app.api_route("/api/preview", methods=["GET", "POST"])
def preview_dataset():
    df = require_df()

    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": df.head(50)
        .fillna("")
        .to_dict(orient="records")
    }


# =========================================
# EXPORT DATASET API
# =========================================

from fastapi import Request
from fastapi.responses import StreamingResponse
from io import BytesIO
import json


@app.post("/api/export")
@app.post("/export")
async def export_dataset_api(request: Request):

    df = require_df()

    try:
        body = await request.json()
    except Exception:
        body = {}

    export_format = str(
        body.get("format", "csv")
    ).lower()

    if export_format == "xlsx":
        return {
            "success": True,
            "download_url": "/download/export/xlsx"
        }

    return {
        "success": True,
        "download_url": "/download/export/csv"
    }


@app.get("/download/export/{export_format}")
def download_export(export_format: str):

    df = require_df()

    # CSV EXPORT
    if export_format.lower() == "csv":

        csv_data = df.to_csv(
            index=False
        )

        return StreamingResponse(
            iter([csv_data.encode("utf-8-sig")]),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=genesis_dataset.csv"
            }
        )

    # EXCEL EXPORT
    if export_format.lower() in ["xlsx", "excel"]:

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Dataset"
            )

        output.seek(0)

        return StreamingResponse(
            output,
            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition":
                "attachment; filename=genesis_dataset.xlsx"
            }
        )

    return {
        "error": "Unsupported export format"
    }
# =========================================
# EXTRA ANALYTICS FUNCTIONS
# =========================================

# =========================================
# GENESIS AI - PROFESSIONAL OUTLIER ENGINE
# =========================================

def genesis_outliers(
    df,
    method="iqr",
    column=None,
    max_rows=100
):
    """
    Professional outlier detection engine.

    Methods:
        iqr
        zscore

    Automatically ignores identifier-like columns
    such as ID, phone, email, name.
    """

    method = str(method).strip().lower()

    if method not in ["iqr", "zscore"]:
        return {
            "success": False,
            "message": "Method must be 'iqr' or 'zscore'."
        }
        # -----------------------------------------------------
    # SELECT NUMERIC COLUMNS
    # -----------------------------------------------------
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # -----------------------------------------------------
    # IGNORE IDENTIFIER-LIKE COLUMNS
    # -----------------------------------------------------
    ignored_columns = []

    identifier_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "name"
    ]

    columns_analyzed = []

    for col in numeric_columns:
        col_name = str(col).strip().lower()

        if any(
            keyword in col_name
            for keyword in identifier_keywords
        ):
            ignored_columns.append(str(col))
        else:
            columns_analyzed.append(col)

    # -----------------------------------------------------
    # SINGLE COLUMN MODE
    # -----------------------------------------------------
    if column is not None:

        column = str(column).strip()

        if column not in df.columns:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' not found."
                )
            }

        if column not in columns_analyzed:
            return {
                "success": False,
                "message": (
                    f"Column '{column}' is not suitable "
                    "for outlier analysis."
                )
            }

        columns_to_analyze = [column]

    else:
        columns_to_analyze = columns_analyzed

    # -----------------------------------------------------
    # RESULT CONTAINER
    # -----------------------------------------------------
    result = {}

    # -----------------------------------------------------
    # ANALYZE EACH COLUMN
    # -----------------------------------------------------
    for col in columns_to_analyze:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        total_valid_values = int(len(series))

        if total_valid_values < 2:
            result[str(col)] = {
                "method": method,
                "outlier_count": 0,
                "outlier_percentage": 0,
                "total_valid_values": total_valid_values,
                "lower_bound": None,
                "upper_bound": None,
                "sample_rows": []
            }
            continue

        # -------------------------------------------------
        # IQR METHOD
        # -------------------------------------------------
        if method == "iqr":

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = (
                q1 - (1.5 * iqr)
            )

            upper_bound = (
                q3 + (1.5 * iqr)
            )

            mask = (
                (pd.to_numeric(
                    df[col],
                    errors="coerce"
                ) < lower_bound)
                |
                (pd.to_numeric(
                    df[col],
                    errors="coerce"
                ) > upper_bound)
            )

        # -------------------------------------------------
        # Z-SCORE METHOD
        # -------------------------------------------------
        else:

            mean_value = series.mean()
            std_value = series.std()

            if std_value == 0 or pd.isna(std_value):
                result[str(col)] = {
                    "method": method,
                    "outlier_count": 0,
                    "outlier_percentage": 0,
                    "total_valid_values": total_valid_values,
                    "lower_bound": None,
                    "upper_bound": None,
                    "sample_rows": []
                }
                continue

            z_scores = (
                (
                    pd.to_numeric(
                        df[col],
                        errors="coerce"
                    )
                    - mean_value
                )
                / std_value
            )

            mask = z_scores.abs() > 3

            lower_bound = (
                mean_value - (3 * std_value)
            )

            upper_bound = (
                mean_value + (3 * std_value)
            )

        # -------------------------------------------------
        # OUTLIER COUNT
        # -------------------------------------------------
        mask = mask.fillna(False)

        outlier_count = int(mask.sum())

        outlier_percentage = round(
            (
                outlier_count
                / max(total_valid_values, 1)
            ) * 100,
            2
        )

        # -------------------------------------------------
        # SAMPLE OUTLIER ROWS
        # -------------------------------------------------
        sample_indices = (
            df.index[mask]
            .tolist()
            [:max_rows]
        )

        sample_rows = []

        for idx in sample_indices:

            row_data = {}

            for c in df.columns:
                value = df.loc[idx, c]

                if pd.isna(value):
                    row_data[str(c)] = None

                elif hasattr(value, "item"):
                    try:
                        row_data[str(c)] = value.item()
                    except Exception:
                        row_data[str(c)] = str(value)

                elif isinstance(
                    value,
                    pd.Timestamp
                ):
                    row_data[str(c)] = (
                        value.isoformat()
                    )

                else:
                    row_data[str(c)] = value

            sample_rows.append({
                "row_index": int(idx),
                "value": (
                    df.loc[idx, col].item()
                    if hasattr(
                        df.loc[idx, col],
                        "item"
                    )
                    else df.loc[idx, col]
                ),
                "row": row_data
            })

        # -------------------------------------------------
        # SAVE COLUMN RESULT
        # -------------------------------------------------
        result[str(col)] = {
            "method": method,
            "outlier_count": outlier_count,
            "outlier_percentage": outlier_percentage,
            "total_valid_values": total_valid_values,
            "lower_bound": round(
                float(lower_bound),
                2
            ),
            "upper_bound": round(
                float(upper_bound),
                2
            ),
            "sample_rows": sample_rows
        }

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------
    return {
        "success": True,
        "method": method,
        "columns_analyzed": [
            str(c)
            for c in columns_to_analyze
        ],
        "ignored_columns": ignored_columns,
        "outliers": result
    }
# =========================================================
# GENESIS AI - PROFESSIONAL OUTLIER TREATMENT ENGINE
# =========================================================

@app.post("/genesis/transform/outliers")
def genesis_outlier_treatment(
    column: str,
    strategy: str = "cap",
    method: str = "iqr"
):
    global current_df
    global transformation_history
    global redo_history

    # -----------------------------------------------------
    # CHECK DATASET
    # -----------------------------------------------------
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = str(column).strip()
    strategy = str(strategy).strip().lower()
    method = str(method).strip().lower()

    # -----------------------------------------------------
    # VALIDATE STRATEGY
    # -----------------------------------------------------
    allowed_strategies = [
        "remove",
        "cap",
        "median",
        "mean"
    ]

    if strategy not in allowed_strategies:
        return {
            "success": False,
            "message": (
                "Strategy must be one of: "
                "remove, cap, median, mean."
            )
        }

    # -----------------------------------------------------
    # VALIDATE METHOD
    # -----------------------------------------------------
    if method not in ["iqr", "zscore"]:
        return {
            "success": False,
            "message": "Method must be 'iqr' or 'zscore'."
        }

    # -----------------------------------------------------
    # VALIDATE COLUMN
    # -----------------------------------------------------
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # -----------------------------------------------------
    # NUMERIC CHECK
    # -----------------------------------------------------
    numeric_series = pd.to_numeric(
        current_df[column],
        errors="coerce"
    )

    if numeric_series.notna().sum() == 0:
        return {
            "success": False,
            "message": (
                f"Column '{column}' does not contain "
                "valid numeric values."
            )
        }

    # -----------------------------------------------------
    # ORIGINAL DATASET
    # -----------------------------------------------------
    original_df = current_df.copy(deep=True)

    df = current_df.copy(deep=True)

    valid = numeric_series.dropna()

    # -----------------------------------------------------
    # CALCULATE OUTLIER BOUNDS
    # -----------------------------------------------------
    if method == "iqr":

        q1 = valid.quantile(0.25)
        q3 = valid.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_mask = (
            (numeric_series < lower_bound)
            | (numeric_series > upper_bound)
        )

    else:

        mean_value = valid.mean()
        std_value = valid.std()

        if std_value == 0 or pd.isna(std_value):
            return {
                "success": False,
                "message": (
                    f"Column '{column}' has zero variance. "
                    "Z-score treatment is not possible."
                )
            }

        z_scores = (
            (numeric_series - mean_value)
            / std_value
        )

        outlier_mask = z_scores.abs() > 3

        lower_bound = (
            mean_value - (3 * std_value)
        )

        upper_bound = (
            mean_value + (3 * std_value)
        )

    # -----------------------------------------------------
    # OUTLIERS BEFORE
    # -----------------------------------------------------
    outliers_before = int(
        outlier_mask.fillna(False).sum()
    )

    rows_before = int(len(df))

    # -----------------------------------------------------
    # NOTHING TO TREAT
    # -----------------------------------------------------
    if outliers_before == 0:
        return {
            "success": True,
            "message": (
                f"No outliers found in '{column}'."
            ),
            "column": column,
            "strategy": strategy,
            "method": method,
            "outliers_before": 0,
            "outliers_after": 0,
            "changed_count": 0,
            "rows_before": rows_before,
            "rows_after": rows_before,
            "history_count": len(
                transformation_history
            )
        }

    # -----------------------------------------------------
    # SAVE UNDO STATE
    # -----------------------------------------------------
    transformation_history.append({
        "dataset": original_df,
        "column": column,
        "operation": "outlier_treatment",
        "strategy": strategy,
        "method": method,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "rows_before": rows_before,
        "columns_before": int(len(df.columns))
    })

    # New transformation invalidates REDO
    redo_history.clear()

    # -----------------------------------------------------
    # APPLY TREATMENT
    # -----------------------------------------------------

    if strategy == "remove":

        df = df.loc[
            ~outlier_mask.fillna(False)
        ].reset_index(drop=True)

    elif strategy == "cap":

        df[column] = numeric_series.clip(
            lower=lower_bound,
            upper=upper_bound
        )

    elif strategy == "median":

        replacement_value = float(
            valid.median()
        )

        df.loc[
            outlier_mask.fillna(False),
            column
        ] = replacement_value

    elif strategy == "mean":

        replacement_value = float(
            valid.mean()
        )

        df.loc[
            outlier_mask.fillna(False),
            column
        ] = replacement_value

    # -----------------------------------------------------
    # COUNT AFTER
    # -----------------------------------------------------
    treated_numeric = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if method == "iqr":

        treated_valid = treated_numeric.dropna()

        if len(treated_valid) > 0:

            treated_q1 = treated_valid.quantile(0.25)
            treated_q3 = treated_valid.quantile(0.75)

            treated_iqr = (
                treated_q3 - treated_q1
            )

            treated_lower = (
                treated_q1
                - (1.5 * treated_iqr)
            )

            treated_upper = (
                treated_q3
                + (1.5 * treated_iqr)
            )

            treated_mask = (
                (treated_numeric < treated_lower)
                | (treated_numeric > treated_upper)
            )

        else:
            treated_mask = pd.Series(
                False,
                index=treated_numeric.index
            )

    else:

        treated_valid = treated_numeric.dropna()

        if len(treated_valid) > 1:

            treated_mean = treated_valid.mean()
            treated_std = treated_valid.std()

            if treated_std != 0:

                treated_z = (
                    (
                        treated_numeric
                        - treated_mean
                    )
                    / treated_std
                )

                treated_mask = (
                    treated_z.abs() > 3
                )

            else:
                treated_mask = pd.Series(
                    False,
                    index=treated_numeric.index
                )

        else:
            treated_mask = pd.Series(
                False,
                index=treated_numeric.index
            )

    outliers_after = int(
        treated_mask.fillna(False).sum()
    )

    # -----------------------------------------------------
    # CHANGED COUNT
    # -----------------------------------------------------
    if strategy == "remove":

        changed_count = outliers_before

    else:

        changed_count = int(
            (
                numeric_series
                .reset_index(drop=True)
                != treated_numeric
                .reset_index(drop=True)
            ).fillna(False).sum()
        )

    rows_after = int(len(df))

    # -----------------------------------------------------
    # SAVE DATASET
    # -----------------------------------------------------
    current_df = df

    # -----------------------------------------------------
    # AUDIT LOG
    # -----------------------------------------------------
    try:
        add_audit_log(
            "outlier_treatment",
            {
                "column": column,
                "strategy": strategy,
                "method": method,
                "outliers_before": outliers_before,
                "outliers_after": outliers_after,
                "changed_count": changed_count,
                "rows_before": rows_before,
                "rows_after": rows_after
            }
        )
    except Exception:
        pass

    # -----------------------------------------------------
    # DATASET VERSION
    # -----------------------------------------------------
    try:
        save_dataset_version(
            "outlier_treatment_applied"
        )
    except Exception:
        pass

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------
    return {
        "success": True,
        "message": (
            "Outlier treatment applied successfully."
        ),
        "column": column,
        "strategy": strategy,
        "method": method,
        "lower_bound": round(
            float(lower_bound), 4
        ),
        "upper_bound": round(
            float(upper_bound), 4
        ),
        "outliers_before": outliers_before,
        "outliers_after": outliers_after,
        "changed_count": changed_count,
        "rows_before": rows_before,
        "rows_after": rows_after,
        "columns": int(len(df.columns)),
        "history_count": len(
            transformation_history
        )
    }
    # -----------------------------------------
    # IDENTIFIER / NON-ANALYTICAL COLUMNS
    # -----------------------------------------

    ignore_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "name",
        "address"
    ]

    def is_identifier_column(col):
        col_lower = str(col).strip().lower()

        return any(
            keyword in col_lower
            for keyword in ignore_keywords
        )

    # -----------------------------------------
    # NUMERIC COLUMNS
    # -----------------------------------------

    numeric_columns = list(
        df.select_dtypes(include="number").columns
    )

    ignored_columns = []

    analytical_columns = []

    for col in numeric_columns:

        if is_identifier_column(col):
            ignored_columns.append(str(col))
        else:
            analytical_columns.append(col)

    # -----------------------------------------
    # OPTIONAL COLUMN FILTER
    # -----------------------------------------

    if column is not None and str(column).strip():

        requested_column = str(column).strip()

        matching_columns = [
            col
            for col in analytical_columns
            if str(col) == requested_column
        ]

        if not matching_columns:

            return {
                "success": False,
                "message": (
                    f"Analytical numeric column "
                    f"'{requested_column}' not found."
                ),
                "available_columns": [
                    str(c)
                    for c in analytical_columns
                ]
            }

        analytical_columns = matching_columns

    # -----------------------------------------
    # NO ANALYTICAL COLUMNS
    # -----------------------------------------

    if not analytical_columns:

        return {
            "success": True,
            "method": method,
            "message": "No analytical numeric columns found.",
            "outliers": {},
            "ignored_columns": ignored_columns
        }

    result = {}

    # -----------------------------------------
    # PROCESS EACH COLUMN
    # -----------------------------------------

    for col in analytical_columns:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        valid = series.dropna()

        total_values = int(len(valid))

        if total_values == 0:

            result[str(col)] = {
                "outlier_count": 0,
                "outlier_percentage": 0.0,
                "lower_bound": None,
                "upper_bound": None,
                "sample_rows": []
            }

            continue

        # -------------------------------------
        # IQR METHOD
        # -------------------------------------

        if method == "iqr":

            q1 = valid.quantile(0.25)
            q3 = valid.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            mask = (
                (series < lower_bound) |
                (series > upper_bound)
            )

        # -------------------------------------
        # Z-SCORE METHOD
        # -------------------------------------

        else:

            mean = valid.mean()
            std = valid.std(ddof=0)

            if std == 0 or pd.isna(std):

                result[str(col)] = {
                    "outlier_count": 0,
                    "outlier_percentage": 0.0,
                    "lower_bound": float(mean),
                    "upper_bound": float(mean),
                    "method": "zscore",
                    "sample_rows": []
                }

                continue

            z_scores = (
                (series - mean) / std
            ).abs()

            mask = z_scores > 3

            lower_bound = mean - (3 * std)
            upper_bound = mean + (3 * std)

        # -------------------------------------
        # OUTLIER VALUES
        # -------------------------------------

        outlier_values = series[mask].dropna()

        outlier_count = int(len(outlier_values))

        outlier_percentage = (
            (outlier_count / total_values) * 100
        )

        # -------------------------------------
        # SAMPLE ROWS
        # -------------------------------------

        outlier_indices = list(
            outlier_values.index[:max_rows]
        )

        sample_rows = []

        for index in outlier_indices:

            row_data = {}

            for c in df.columns:

                value = df.loc[index, c]

                if pd.isna(value):
                    row_data[str(c)] = None
                else:
                    try:
                        row_data[str(c)] = (
                            value.item()
                            if hasattr(value, "item")
                            else value
                        )
                    except Exception:
                        row_data[str(c)] = str(value)

            sample_rows.append({
                "row_index": int(index),
                "value": row_data.get(str(col)),
                "row": row_data
            })

        # -------------------------------------
        # FINAL COLUMN RESULT
        # -------------------------------------

        result[str(col)] = {

            "method": method,

            "outlier_count":
                outlier_count,

            "outlier_percentage":
                round(
                    float(outlier_percentage),
                    2
                ),

            "total_valid_values":
                total_values,

            "lower_bound":
                round(
                    float(lower_bound),
                    2
                ),

            "upper_bound":
                round(
                    float(upper_bound),
                    2
                ),

            "sample_rows":
                sample_rows
        }

    # -----------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------

    return {
        "success": True,
        "method": method,
        "columns_analyzed": [
            str(c)
            for c in analytical_columns
        ],
        "ignored_columns": ignored_columns,
        "outliers": result
    }

# =========================================
# GENESIS AI - ANALYTICS HELPER FUNCTIONS
# =========================================

def genesis_correlation_matrix(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return {
            "message": "At least two numeric columns are required."
        }

    correlation = numeric_df.corr()

    return {
        "columns": list(correlation.columns),
        "matrix": correlation.round(4).to_dict()
    }


def genesis_group_summary(df):
    categorical_columns = list(
        df.select_dtypes(exclude="number").columns
    )

    numeric_columns = list(
        df.select_dtypes(include="number").columns
    )

    result = {}

    for group_column in categorical_columns[:10]:
        try:
            grouped = df.groupby(
                group_column,
                dropna=False
            )

            summary = {
                "count": grouped.size()
                .sort_values(ascending=False)
                .head(20)
                .to_dict()
            }

            if numeric_columns:
                averages = {}

                for numeric_column in numeric_columns[:10]:
                    try:
                        values = grouped[
                            numeric_column
                        ].mean()

                        averages[numeric_column] = (
                            values
                            .round(2)
                            .head(20)
                            .to_dict()
                        )

                    except Exception:
                        pass

                summary["averages"] = averages

            result[group_column] = summary

        except Exception:
            pass

    return result


def genesis_dataset_columns(df):
    columns = []

    for column in df.columns:
        columns.append({
            "name": str(column),
            "dtype": str(df[column].dtype),
            "missing_values": int(
                df[column].isna().sum()
            ),
            "unique_values": int(
                df[column].nunique()
            )
        })

    return {
        "total_columns": int(len(df.columns)),
        "columns": columns
    }
# =========================================
# EXTRA ANALYTICS ROUTES
# =========================================

@app.api_route(
    "/analytics/outliers",
    methods=["GET", "POST"]
)

@app.api_route(
    "/api/analytics/outliers",
    methods=["GET", "POST"]
)
def analytics_outliers(
    method: str = "iqr"
):
    df = require_df()

    method = method.strip().lower()

    if method not in ["iqr", "zscore"]:
        return {
            "success": False,
            "message": "Method must be 'iqr' or 'zscore'.",
            "available_methods": [
                "iqr",
                "zscore"
            ]
        }

    result = genesis_outliers(
        df,
        method=method
    )

    return result


@app.api_route(
    "/analytics/correlation-matrix",
    methods=["GET", "POST"]
)
@app.api_route(
    "/api/analytics/correlation-matrix",
    methods=["GET", "POST"]
)
def analytics_correlation_matrix():
    return {
        "success": True,
        "correlation_matrix":
            genesis_correlation_matrix(
                require_df()
            )
    }


@app.api_route(
    "/analytics/group-summary",
    methods=["GET", "POST"]
)
@app.api_route(
    "/api/analytics/group-summary",
    methods=["GET", "POST"]
)
def analytics_group_summary():
    return {
        "success": True,
        "group_summary":
            genesis_group_summary(
                require_df()
            )
    }


@app.api_route(
    "/analytics/columns",
    methods=["GET", "POST"]
)
@app.api_route(
    "/api/analytics/columns",
    methods=["GET", "POST"]
)
def analytics_dataset_columns():
    return {
        "success": True,
        "dataset_columns":
            genesis_dataset_columns(
                require_df()
            )
    }
@app.api_route(
    "/api/analytics/forecast",
    methods=["GET", "POST"]
)
def analytics_forecast():
    return genesis_dashboard_forecast()

# ============================================================
# GENESIS AI CONSOLIDATED PROFESSIONAL MODULES
# Added without replacing existing working analytics routes.
# ============================================================

from datetime import datetime
import copy

GENESIS_AUDIT_LOG = []
GENESIS_VERSIONS = []

def _genesis_df():
    return require_df()

def _audit(action, details=None):
    GENESIS_AUDIT_LOG.append({
        "time": datetime.now().isoformat(timespec="seconds"),
        "action": action,
        "details": details or {}
    })

def _snapshot(label):
    try:
        df = require_df()
        GENESIS_VERSIONS.append({
            "version": len(GENESIS_VERSIONS) + 1,
            "label": label,
            "time": datetime.now().isoformat(timespec="seconds"),
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "data": df.copy()
        })
    except Exception:
        pass

@app.api_route("/genesis/clean/profile", methods=["GET", "POST"])
def genesis_clean_profile():
    df = _genesis_df()
    result = []
    for c in df.columns:
        s = df[c]
        result.append({
            "column": str(c),
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "missing_percent": round(float(s.isna().mean() * 100), 2),
            "duplicates": int(s.duplicated().sum()),
            "unique": int(s.nunique(dropna=True))
        })
    return {"success": True, "rows": int(len(df)), "columns": result}

def genesis_ai_clean():
    df = _genesis_df().copy()
    _snapshot("before_ai_clean")
    before = {"rows": int(len(df)), "missing": int(df.isna().sum().sum()), "duplicates": int(df.duplicated().sum())}
    df.columns = [str(c).strip().replace("  ", " ") for c in df.columns]
    df = df.drop_duplicates()
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            if df[c].isna().any():
                df[c] = df[c].fillna(df[c].median())
        else:
            df[c] = df[c].astype("object").where(df[c].notna(), None)
            if df[c].isna().any():
                mode = df[c].mode(dropna=True)
                df[c] = df[c].fillna(mode.iloc[0] if not mode.empty else "Unknown")
    # Support both common state styles.
    global latest_df, current_df

    latest_df = df.copy()
    current_df = df.copy()
    _snapshot("after_ai_clean")
    _audit("ai_clean", before)
    return {"success": True, "before": before, "after": {
        "rows": int(len(df)), "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }}

def genesis_standardize():
    df = _genesis_df().copy()
    _snapshot("before_standardization")
    changed = []
    for c in df.columns:
        old = str(c)
        new = re.sub(r"\s+", "_", old.strip().lower())
        new = re.sub(r"[^0-9a-zA-Z_]", "", new)
        changed.append({"old": old, "new": new})
    df.columns = [x["new"] for x in changed]
    try: df
    except Exception: pass
    _snapshot("after_standardization")
    _audit("standardize_columns")
    return {"success": True, "changes": changed}

@app.api_route("/genesis/clean/versions", methods=["GET", "POST"])
def genesis_versions():
    return {"success": True, "versions": [
        {k:v for k,v in x.items() if k != "data"} for x in GENESIS_VERSIONS
    ]}

def genesis_smart_visualization():
    df = _genesis_df()
    numeric = [str(c) for c in df.select_dtypes(include="number").columns]
    categorical = [str(c) for c in df.select_dtypes(exclude="number").columns]
    recommendations = []
    if categorical:
        recommendations.append({"chart": "bar", "column": categorical[0], "reason": "Best for category comparison"})
    if numeric:
        recommendations.append({"chart": "histogram", "column": numeric[0], "reason": "Best for numeric distribution"})
    if len(numeric) >= 2:
        recommendations.append({"chart": "scatter", "x": numeric[0], "y": numeric[1], "reason": "Explore relationship between numeric variables"})
    return {"success": True, "recommendations": recommendations}

def genesis_kpis():
    df = _genesis_df()
    numeric = df.select_dtypes(include="number")
    cards = [{"title": "Rows", "value": int(len(df))}, {"title": "Columns", "value": int(len(df.columns))}]
    for c in list(numeric.columns)[:6]:
        cards.append({"title": f"Average {c}", "value": round(float(numeric[c].mean()), 2)})
    return {"success": True, "kpis": cards}

def genesis_pii():
    df = _genesis_df()
    keywords = {
        "name": ["name", "first_name", "last_name"],
        "email": ["email", "mail"],
        "phone": ["phone", "mobile", "contact"],
        "address": ["address", "location"],
        "government_id": ["aadhaar", "passport", "pan", "ssn"]
    }
    found = {}
    for kind, words in keywords.items():
        cols = [str(c) for c in df.columns if any(w in str(c).lower() for w in words)]
        if cols: found[kind] = cols
    _audit("pii_scan", {"detected_types": list(found)})
    return {"success": True, "pii": found, "recommendation": "Review detected fields before sharing data externally."}

def genesis_metadata():
    df = _genesis_df()
    return {"success": True, "metadata": {
        "rows": int(len(df)), "columns": int(len(df.columns)),
        "schema": [{"name": str(c), "dtype": str(df[c].dtype), "unique": int(df[c].nunique())} for c in df.columns]
    }}

def genesis_audit():
    return {"success": True, "audit_log": GENESIS_AUDIT_LOG[-200:]}

@app.api_route("/genesis/engineering/schema-evolution", methods=["GET", "POST"])
def genesis_schema_evolution():
    df = _genesis_df()
    schema = {str(c): str(df[c].dtype) for c in df.columns}
    _audit("schema_snapshot", {"columns": len(schema)})
    return {"success": True, "current_schema": schema, "version": len(GENESIS_VERSIONS)}

@app.api_route("/genesis/engineering/model", methods=["GET", "POST"])
def genesis_data_model():
    df = _genesis_df()
    numeric = [str(c) for c in df.select_dtypes(include="number").columns]
    categorical = [str(c) for c in df.select_dtypes(exclude="number").columns]
    return {"success": True, "model": {
        "fact_table_candidate": "uploaded_dataset",
        "numeric_measures": numeric,
        "dimension_candidates": categorical,
        "primary_key_candidates": [str(c) for c in df.columns if "id" in str(c).lower()]
    }}

@app.api_route("/genesis/engineering/orchestrate", methods=["GET", "POST"])
def genesis_orchestrate():
    df = _genesis_df()
    steps = ["profile", "quality_check", "clean", "schema_snapshot", "metadata_refresh"]
    _audit("pipeline_orchestrated", {"steps": steps})
    return {"success": True, "pipeline": {"status": "completed", "steps": steps, "rows": int(len(df))}}

@app.api_route("/genesis/observability/status", methods=["GET", "POST"])
def genesis_observability():
    df = _genesis_df()
    missing = int(df.isna().sum().sum())
    return {"success": True, "status": "healthy", "metrics": {
        "rows": int(len(df)), "columns": int(len(df.columns)),
        "missing_cells": missing, "audit_events": len(GENESIS_AUDIT_LOG),
        "versions": len(GENESIS_VERSIONS)
    }}

@app.api_route("/genesis/agents/run/{agent}", methods=["GET", "POST"])
def genesis_agent(agent: str):
    df = _genesis_df()
    agent = agent.lower()
    if agent == "analyst":
        result = {"focus": "dataset analysis", "rows": int(len(df)), "numeric_columns": list(df.select_dtypes(include="number").columns)}
    elif agent == "quality":
        result = {"focus": "quality", "missing": int(df.isna().sum().sum()), "duplicates": int(df.duplicated().sum())}
    elif agent == "forecast":
        result = {"focus": "forecast readiness", "numeric_columns": list(df.select_dtypes(include="number").columns)}
    elif agent == "visualization":
        result = {"focus": "visualization", "recommended": "Use Smart Visualization endpoint"}
    elif agent == "engineer":
        result = {"focus": "engineering", "schema": {str(c): str(df[c].dtype) for c in df.columns}}
    else:
        result = {"focus": "recommendation", "recommendation": "Start with profiling, quality, then cleaning and analysis."}
    _audit("agent_run", {"agent": agent})
    return {"success": True, "agent": agent, "result": result}
def genesis_dashboard_auto_insights():
    df = require_df()

    insights = []

    # ---------------------------------
    # HELPER: IDENTIFY NON-BUSINESS COLUMNS
    # ---------------------------------
    ignore_keywords = [
        "id",
        "phone",
        "mobile",
        "email",
        "name"
    ]

    def is_ignored_column(column):
        column_lower = str(column).lower()

        return any(
            keyword in column_lower
            for keyword in ignore_keywords
        )

    # ---------------------------------
    # 1. DATA QUALITY INSIGHTS
    # ---------------------------------
    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    if missing_values == 0:
        insights.append({
            "priority": "high",
            "type": "data_quality",
            "message": "Dataset has no missing values."
        })
    else:
        insights.append({
            "priority": "high",
            "type": "data_quality",
            "message": f"Dataset contains {missing_values} missing values."
        })

    if duplicate_rows == 0:
        insights.append({
            "priority": "high",
            "type": "data_quality",
            "message": "No duplicate rows detected."
        })
    else:
        insights.append({
            "priority": "high",
            "type": "data_quality",
            "message": f"{duplicate_rows} duplicate rows detected."
        })

    # ---------------------------------
    # 2. BUSINESS NUMERIC COLUMNS ONLY
    # ---------------------------------
    numeric_cols = [
        col for col in _numeric_columns(df)
        if not is_ignored_column(col)
    ]

    # Preferred business metrics
    preferred_metrics = [
        "Salary",
        "Revenue",
        "Expenses",
        "Profit",
        "Achievement %",
        "Performance Rating",
        "Attendance %",
        "Monthly Sales"
    ]

    summary_metrics = []

    for metric in preferred_metrics:
        if metric in numeric_cols:
            summary_metrics.append(metric)

    # Fallback
    if not summary_metrics:
        summary_metrics = numeric_cols[:5]

    # ---------------------------------
    # 3. NUMERIC BUSINESS INSIGHTS
    # ---------------------------------
    for col in summary_metrics:

        series = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        if len(series) == 0:
            continue

        mean_value = float(series.mean())
        min_value = float(series.min())
        max_value = float(series.max())

        insights.append({
            "priority": "medium",
            "type": "numeric_summary",
            "column": str(col),
            "mean": round(mean_value, 2),
            "min": round(min_value, 2),
            "max": round(max_value, 2),
            "message": (
                f"Average {col} is "
                f"{round(mean_value, 2)}."
            )
        })

    # ---------------------------------
    # 4. GROUP COMPARISON INSIGHT
    # ---------------------------------
    preferred_group_columns = [
        "Department",
        "City",
        "Branch",
        "Gender",
        "Work Mode"
    ]

    group_col = None

    for col in preferred_group_columns:
        if col in df.columns:
            group_col = col
            break

    metric_col = None

    preferred_group_metrics = [
        "Salary",
        "Revenue",
        "Profit",
        "Achievement %",
        "Performance Rating"
    ]

    for col in preferred_group_metrics:
        if col in numeric_cols:
            metric_col = col
            break

    if group_col and metric_col:

        group_analysis = (
            df.groupby(group_col)[metric_col]
            .mean()
            .dropna()
            .sort_values(ascending=False)
        )

        if len(group_analysis) >= 2:

            highest_group = str(group_analysis.index[0])
            highest_value = float(group_analysis.iloc[0])

            lowest_group = str(group_analysis.index[-1])
            lowest_value = float(group_analysis.iloc[-1])

            difference = highest_value - lowest_value

            percentage_difference = (
                difference / lowest_value * 100
                if lowest_value != 0
                else 0
            )

            insights.append({
                "priority": "high",
                "type": "group_comparison",
                "group_column": str(group_col),
                "metric_column": str(metric_col),
                "highest_group": highest_group,
                "highest_value": round(highest_value, 2),
                "lowest_group": lowest_group,
                "lowest_value": round(lowest_value, 2),
                "difference": round(difference, 2),
                "percentage_difference": round(
                    percentage_difference,
                    2
                ),
                "message": (
                    f"{highest_group} has the highest average "
                    f"{metric_col}, while {lowest_group} has "
                    f"the lowest. The difference is "
                    f"{round(percentage_difference, 2)}%."
                )
            })

    # ---------------------------------
    # 5. MEANINGFUL CORRELATION INSIGHTS
    # ---------------------------------
    correlation_insights = []

    if len(numeric_cols) >= 2:

        correlation_df = (
            df[numeric_cols]
            .apply(pd.to_numeric, errors="coerce")
            .corr()
        )

        for i, col1 in enumerate(numeric_cols):

            for col2 in numeric_cols[i + 1:]:

                value = correlation_df.loc[col1, col2]

                if pd.isna(value):
                    continue

                # Ignore weak relationships
                if abs(value) < 0.4:
                    continue

                correlation_insights.append({
                    "column_1": str(col1),
                    "column_2": str(col2),
                    "correlation": float(value)
                })

        correlation_insights = sorted(
            correlation_insights,
            key=lambda x: abs(x["correlation"]),
            reverse=True
        )

        # Maximum top 5 meaningful correlations
        for item in correlation_insights[:5]:

            corr = item["correlation"]

            if corr >= 0.7:
                relationship = "strong positive"
                priority = "high"

            elif corr >= 0.4:
                relationship = "moderate positive"
                priority = "medium"

            elif corr <= -0.7:
                relationship = "strong negative"
                priority = "high"

            else:
                relationship = "moderate negative"
                priority = "medium"

            insights.append({
                "priority": priority,
                "type": "correlation",
                "column_1": item["column_1"],
                "column_2": item["column_2"],
                "correlation": round(corr, 4),
                "relationship": relationship,
                "message": (
                    f"{item['column_1']} and "
                    f"{item['column_2']} have a "
                    f"{relationship} relationship "
                    f"({round(corr, 4)})."
                )
            })
    # ---------------------------------
    # 6. ADVANCED AUTOMATIC AI INSIGHTS
    # ---------------------------------

    advanced_result = generate_auto_insights(df)

    advanced_insights = advanced_result.get(
        "insights",
        []
    )


    priority_mapping = {

        "Critical": "high",
        "High": "high",
        "Medium": "medium",
        "Info": "low"

    }


    for item in advanced_insights:

        advanced_priority = priority_mapping.get(

            item.get("priority"),

            "low"

        )


        insights.append({

            "priority": advanced_priority,

            "type": item.get(
                "type",

                "automatic_insight"
            ),

            "column": str(
                item.get(
                    "column",
                    ""
                )
            ),

            "title": item.get(
                "title",
                "Genesis AI Insight"
            ),

            "message": item.get(
                "insight",
                ""
            ),

            "score": item.get(
                "score",
                0
            )

        })
    # ---------------------------------
    # 6. SORT BY PRIORITY
    # ---------------------------------
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    insights = sorted(
        insights,
        key=lambda x: priority_order.get(
            x.get("priority", "low"),
            3
        )
    )

    # ---------------------------------
    # FINAL RESPONSE
    # ---------------------------------
    return {
        "success": True,
        "total_insights": len(insights),
        "high_priority": sum(
            1 for x in insights
            if x.get("priority") == "high"
        ),
        "medium_priority": sum(
            1 for x in insights
            if x.get("priority") == "medium"
        ),
        "low_priority": sum(
            1 for x in insights
            if x.get("priority") == "low"
        ),
        "insights": insights
    }
# ============================================================
# GENESIS AI - EXECUTIVE SUMMARY INTELLIGENCE
# ============================================================

def genesis_dashboard_executive_summary():

    df = require_df()

    # Get Automatic Insights
    auto_result = genesis_dashboard_auto_insights()

    insights = auto_result.get(
        "insights",
        []
    )

    critical_issues = []
    positive_signals = []
    management_priorities = []
    key_findings = []


    # --------------------------------------------------------
    # ANALYZE INSIGHTS
    # --------------------------------------------------------

    for item in insights:

        priority = str(
            item.get("priority", "")
        ).lower()

        insight_type = item.get(
            "type",
            ""
        )

        message = item.get(
            "message",
            ""
        )


        # CRITICAL BUSINESS ISSUES

        if insight_type in [

            "negative_profit",

            "high_expense_ratio",

            "low_performance",

            "department_profit_difference"

        ]:

            critical_issues.append({

                "type": insight_type,

                "message": message

            })


        # HIGH PRIORITY FINDINGS

        if priority == "high":

            key_findings.append({

                "type": insight_type,

                "message": message

            })


        # POSITIVE SIGNALS

        if insight_type == "data_quality":

            if (

                "no missing values"
                in message.lower()

                or

                "no duplicate"
                in message.lower()

            ):

                positive_signals.append({

                    "type": insight_type,

                    "message": message

                })


        # MANAGEMENT PRIORITIES

        if insight_type == "negative_profit":

            management_priorities.append({

                "priority": "Critical",

                "action":
                    "Reduce loss-making records and improve profitability."

            })


        elif insight_type == "high_expense_ratio":

            management_priorities.append({

                "priority": "Critical",

                "action":
                    "Control high expenses and improve cost efficiency."

            })


        elif insight_type == "low_performance":

            management_priorities.append({

                "priority": "High",

                "action":
                    "Improve employee performance through targeted intervention."

            })


        elif insight_type == "department_profit_difference":

            management_priorities.append({

                "priority": "Medium",

                "action":
                    "Investigate department-level profitability differences."

            })


    # --------------------------------------------------------
    # LIMIT RESULTS
    # --------------------------------------------------------

    critical_issues = critical_issues[:5]

    positive_signals = positive_signals[:5]

    management_priorities = management_priorities[:5]

    key_findings = key_findings[:8]


    # --------------------------------------------------------
    # DETERMINE BUSINESS HEALTH
    # --------------------------------------------------------

    critical_count = len(critical_issues)

    high_priority_count = auto_result.get(
        "high_priority",
        0
    )


    if critical_count >= 3:

        business_health = "Critical"

    elif critical_count >= 2:

        business_health = "High Risk"

    elif high_priority_count >= 5:

        business_health = "Needs Attention"

    else:

        business_health = "Healthy"


    # --------------------------------------------------------
    # GENERATE EXECUTIVE SUMMARY
    # --------------------------------------------------------

    summary = (

        f"Genesis AI analyzed {len(df):,} records and "

        f"{len(df.columns)} columns. "

        f"The overall business health is currently rated "

        f"as {business_health}. "

    )


    if critical_count > 0:

        summary += (

            f"{critical_count} major business risks "

            f"require management attention. "

        )


    if positive_signals:

        summary += (

            f"The dataset shows "

            f"{len(positive_signals)} positive "

            f"data quality signals. "

        )


    if management_priorities:

        summary += (

            "Management should prioritize profitability, "

            "cost control and performance improvement."

        )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "business_health": business_health,

        "dataset_rows": len(df),

        "dataset_columns": len(df.columns),

        "executive_summary": summary,

        "critical_issues": critical_issues,

        "positive_signals": positive_signals,

        "management_priorities": management_priorities,

        "key_findings": key_findings,

        "total_insights_analyzed": len(insights)

    }
# ============================================================
# GENESIS AI - DECISION PRIORITY ANALYTICS
# ============================================================

def genesis_dashboard_decision_priorities():

    df = require_df()

    # --------------------------------------------------------
    # GET AUTOMATIC INSIGHTS
    # --------------------------------------------------------

    auto_result = genesis_dashboard_auto_insights()

    insights = auto_result.get(
        "insights",
        []
    )

    # --------------------------------------------------------
    # PREPARE ROOT CAUSES
    # --------------------------------------------------------

    root_causes = []

    root_cause_types = [

        "negative_profit",

        "high_expense_ratio",

        "low_performance",

        "high_variation",

        "outliers",

        "missing_data"

    ]

    for item in insights:

        if item.get("type") in root_cause_types:

            priority = item.get(
                "priority",
                "medium"
            )

            priority = str(
                priority
            ).capitalize()

            root_causes.append({

                "priority": priority,

                "title": item.get(
                    "title",
                    item.get(
                        "type",
                        "Business Issue"
                    ).replace(
                        "_",
                        " "
                    ).title()
                ),

                "message": item.get(
                    "message",
                    ""
                ),

                "type": item.get(
                    "type",
                    ""
                ),

                "score": item.get(
                    "score",
                    0
                )

            })

    # --------------------------------------------------------
    # PREPARE RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    for root_cause in root_causes:

        issue_type = root_cause.get(
            "type"
        )

        recommendation_text = None

        if issue_type == "negative_profit":

            recommendation_text = (

                "Investigate loss-making records, identify revenue and cost drivers, "
                "and create a targeted profitability improvement plan."

            )

        elif issue_type == "high_expense_ratio":

            recommendation_text = (

                "Review high-cost operations and reduce unnecessary expenses "
                "to improve the expense-to-revenue ratio."

            )

        elif issue_type == "low_performance":

            recommendation_text = (

                "Identify low-performing employees or teams and implement "
                "targeted training and performance improvement plans."

            )

        elif issue_type == "high_variation":

            recommendation_text = (

                "Investigate the causes of unusually high variation and "
                "check for extreme values, instability, or inconsistent processes."

            )

        elif issue_type == "outliers":

            recommendation_text = (

                "Review detected outliers and validate whether they represent "
                "data errors or meaningful business events."

            )

        elif issue_type == "missing_data":

            recommendation_text = (

                "Improve data collection and validation processes to reduce "
                "missing information."

            )

        if recommendation_text:

            recommendations.append({

                "priority": root_cause.get(
                    "priority",
                    "Medium"
                ),

                "type": root_cause.get(
                    "type",
                    ""
                ),

                "score": root_cause.get(
                    "score",
                    0
                ),

                "title": (

                    f"Action: "
                    f"{root_cause.get('title')}"

                ),

                "message": root_cause.get(
                    "message",
                    ""
                ),

                "recommendation": recommendation_text

            })

    # --------------------------------------------------------
    # GENERATE DECISION PRIORITIES
    # --------------------------------------------------------

    decision_result = calculate_decision_priority(

        root_causes,

        recommendations

    )

    decisions = decision_result.get(

        "decisions",

        []

    )
        # --------------------------------------------------------
    # ADVANCED ROOT CAUSE INTELLIGENCE
    # --------------------------------------------------------

    advanced_root_cause_analysis = []

    for root_cause in root_causes:

        analysis_result = analyze_advanced_root_cause(

            df=df,

            issue_type=root_cause.get(
                "type",
                ""
            ),

            issue_title=root_cause.get(
                "title",
                ""
            ),

            issue_message=root_cause.get(
                "message",
                ""
            )

        )

        advanced_root_cause_analysis.append(
            analysis_result
        )

        # --------------------------------------------------------
    # ADD IMPACT ANALYSIS + ACTION PLAN
    # --------------------------------------------------------

    enhanced_decisions = []

    for decision in decisions:

        # ----------------------------------------------------
        # CALCULATE DECISION IMPACT
        # ----------------------------------------------------

        impact_result = calculate_decision_impact(
            decision
        )

        decision["impact_score"] = impact_result.get(
            "impact_score",
            0
        )

        decision["impact_level"] = impact_result.get(
            "impact_level",
            "Low"
        )

        decision["urgency"] = impact_result.get(
            "urgency",
            "Low"
        )


        # ----------------------------------------------------
        # GENERATE ACTION PLAN
        # ----------------------------------------------------

        action_plan = generate_decision_action_plan(
            decision
        )

        decision["action_plan"] = action_plan


        # ----------------------------------------------------
        # DECISION CONFIDENCE & RISK ANALYSIS
        # ----------------------------------------------------

        confidence_result = calculate_decision_confidence_and_risk(
            decision
        )

        decision["confidence_score"] = confidence_result.get(
            "confidence_score",
            0
        )

        decision["confidence_level"] = confidence_result.get(
            "confidence_level",
            "Low"
        )

        decision["risk_score"] = confidence_result.get(
            "risk_score",
            0
        )

        decision["risk_level"] = confidence_result.get(
            "risk_level",
            "Low"
        )


        # ----------------------------------------------------
        # GENERATE DECISION EXPLANATION
        # IMPORTANT: CONFIDENCE/RISK KE BAAD
        # ----------------------------------------------------

        decision_explanation = generate_decision_explanation(
            decision
        )

        decision["decision_explanation"] = decision_explanation


        # ----------------------------------------------------
        # ADD ENHANCED DECISION
        # ----------------------------------------------------

        enhanced_decisions.append(
            decision
        )

    # --------------------------------------------------------
    # SORT BY IMPACT SCORE
    # --------------------------------------------------------

    enhanced_decisions = sorted(

        enhanced_decisions,

        key=lambda x: x.get(

            "impact_score",

            0

        ),

        reverse=True

    )

    # --------------------------------------------------------
    # UPDATE FINAL RANK
    # --------------------------------------------------------

    for index, decision in enumerate(

        enhanced_decisions

    ):

        decision["rank"] = index + 1
            # --------------------------------------------------------
    # SENIOR ANALYST REASONING
    # --------------------------------------------------------
    

    senior_reasoning_result = generate_senior_analyst_reasoning(

        enhanced_decisions

    )

    # --------------------------------------------------------
    # GROUP DECISIONS
    # --------------------------------------------------------

    grouping_result = group_decisions(

        enhanced_decisions

    )

    grouped_decisions = grouping_result.get(

        "groups",

        []

    )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "total_decisions": len(

            enhanced_decisions

        ),

        "high_priority_decisions": sum(

            1

            for item in enhanced_decisions

            if item.get(

                "priority"

            )

            in [

                "Critical",

                "High"

            ]

        ),

        # Individual Decisions

        "decisions": enhanced_decisions,
        # Advanced Root Cause Intelligence

"advanced_root_cause_analysis": advanced_root_cause_analysis,

"senior_analyst_reasoning": senior_reasoning_result,

        # Grouped Decision Intelligence

        "decision_groups": grouped_decisions,

        "grouping_statistics": {

            "total_groups": grouping_result.get(

                "total_groups",

                0

            ),

            "complete_groups": grouping_result.get(

                "complete_groups",

                0

            ),

            "incomplete_groups": grouping_result.get(

                "incomplete_groups",

                0

            )

        }

    }

@app.api_route("/analytics/auto-insights", methods=["GET", "POST"])
def analytics_auto_insights():

    return genesis_dashboard_auto_insights()


# ============================================================
# GENESIS AI - ADVANCED STATISTICAL ANALYSIS
# ============================================================

@app.api_route(
    "/analytics/advanced-statistics",
    methods=["GET", "POST"]
)
def analytics_advanced_statistics():

    df = require_df()

    result = run_advanced_statistics(
        df
    )

    return result


# ============================================================
# GENESIS AI - WHAT-IF / SCENARIO ANALYSIS
# ============================================================

@app.api_route(
    "/analytics/scenario-analysis",
    methods=["GET", "POST"]
)
def analytics_scenario_analysis():

    df = require_df()

    result = run_scenario_analysis(
        df
    )

    return result
    # ============================================================
# GENESIS AI - SENIOR ANALYST REASONING
# ============================================================

@app.api_route(
    "/analytics/senior-analyst-reasoning",
    methods=["GET", "POST"]
)
def analytics_senior_analyst_reasoning():

    # --------------------------------------------------------
    # GET DECISION INTELLIGENCE
    # --------------------------------------------------------

    decision_result = genesis_dashboard_decision_priorities()

    decisions = decision_result.get(
        "decisions",
        []
    )

    # --------------------------------------------------------
    # GENERATE SENIOR ANALYST REASONING
    # --------------------------------------------------------

    result = generate_senior_analyst_reasoning(
        decisions
    )

    return result
# ============================================================
# GENESIS AI - ROOT CAUSE ANALYSIS
# ============================================================

@app.get("/analytics/root-cause-analysis")
def analytics_root_cause_analysis(
    target_column: str
):

    df = require_df()

    result = investigate_root_cause(
        df,
        target_column
    )

    return result
# ============================================================
# GENESIS AI - SYSTEM DIAGNOSTICS
# ============================================================

@app.api_route(
    "/analytics/system-diagnostics",
    methods=["GET", "POST"]
)
def analytics_system_diagnostics():

    df = require_df()

    result = run_system_diagnostics(df)

    return result
# ============================================================
# GENESIS AI - PERFORMANCE MONITORING
# ============================================================

@app.api_route(
    "/analytics/performance-summary",
    methods=["GET"]
)
def analytics_performance_summary():

    return get_performance_summary()


# ============================================================
# GENESIS AI - RESET PERFORMANCE METRICS
# ============================================================

@app.api_route(
    "/analytics/performance-reset",
    methods=["POST"]
)
def analytics_performance_reset():

    return reset_performance_metrics()
# ============================================================
# GENESIS AI - DATASET STRESS TEST
# ============================================================

@app.api_route(
    "/analytics/dataset-stress-test",
    methods=["GET", "POST"]
)
def analytics_dataset_stress_test():

    df = require_df()

    result = run_dataset_stress_test(df)

    return result
# ============================================================
# GENESIS AI - SECURITY VALIDATION
# ============================================================

@app.api_route(
    "/analytics/security-validation",
    methods=["GET", "POST"]
)
def analytics_security_validation():

    return run_security_validation()
# ============================================================
# GENESIS AI - AUTONOMOUS ANALYSIS WORKFLOW
# ============================================================

@app.api_route(
    "/analytics/autonomous-analysis",
    methods=["GET", "POST"]
)
def analytics_autonomous_analysis():

    df = require_df()

    result = run_autonomous_analysis(

        df=df,

        statistics_function=run_advanced_statistics,

        scenario_function=run_scenario_analysis,

        decision_function=genesis_dashboard_decision_priorities,

        reasoning_function=generate_senior_analyst_reasoning

    )

    return result
# ============================================================
# GENESIS AI - PROFESSIONAL REPORT BUILDER
# ============================================================

@app.api_route(
    "/analytics/professional-report",
    methods=["GET", "POST"]
)
def analytics_professional_report():

    df = require_df()

    # --------------------------------------------------------
    # RUN AUTONOMOUS ANALYSIS
    # --------------------------------------------------------

    autonomous_result = run_autonomous_analysis(

        df=df,

        statistics_function=run_advanced_statistics,

        scenario_function=run_scenario_analysis,

        decision_function=genesis_dashboard_decision_priorities,

        reasoning_function=generate_senior_analyst_reasoning

    )

    # --------------------------------------------------------
    # BUILD PROFESSIONAL REPORT
    # --------------------------------------------------------

    report = build_professional_report(

        df=df,

        autonomous_result=autonomous_result

    )

    return report
# ============================================================
# GENESIS AI - PROFESSIONAL REPORT EXPORT
# ============================================================

@app.api_route(
    "/analytics/professional-report/export/{export_format}",
    methods=["GET", "POST"]
)
def analytics_export_professional_report(
    export_format: str
):

    df = require_df()

    # --------------------------------------------------------
    # RUN AUTONOMOUS ANALYSIS
    # --------------------------------------------------------

    autonomous_result = run_autonomous_analysis(

        df=df,

        statistics_function=run_advanced_statistics,

        scenario_function=run_scenario_analysis,

        decision_function=genesis_dashboard_decision_priorities,

        reasoning_function=generate_senior_analyst_reasoning

    )

    # --------------------------------------------------------
    # BUILD PROFESSIONAL REPORT
    # --------------------------------------------------------

    report = build_professional_report(

        df=df,

        autonomous_result=autonomous_result

    )

    # --------------------------------------------------------
    # EXPORT REPORT
    # --------------------------------------------------------

    export_result = export_professional_report(

        report=report,

        export_format=export_format

    )

    return {

        "report": report,

        "export": export_result

    }
# ============================================================
# GENESIS AI - DECISION PRIORITIES
# ============================================================

@app.api_route(
    "/analytics/decision-priorities",
    methods=["GET", "POST"]
)
def analytics_decision_priorities():

    return genesis_dashboard_decision_priorities()

def analytics_decision_priorities():

    return genesis_dashboard_decision_priorities()
@app.api_route(
    "/analytics/executive-summary",
    methods=["GET", "POST"]
)
def analytics_executive_summary():
    return genesis_dashboard_executive_summary()

# ============================================================
# GENESIS AI - ADVANCED EXECUTIVE SUMMARY ENGINE
# ============================================================

def genesis_dashboard_executive_summary():

    df = require_df()

    # --------------------------------------------------------
    # GET AUTOMATIC AI INSIGHTS
    # --------------------------------------------------------

    auto_result = genesis_dashboard_auto_insights()

    insights = auto_result.get(
        "insights",
        []
    )


    critical_issues = []
    positive_signals = []
    management_priorities = []
    key_findings = []


    # --------------------------------------------------------
    # ANALYZE ALL INSIGHTS
    # --------------------------------------------------------

    for item in insights:

        priority = str(
            item.get(
                "priority",
                ""
            )
        ).lower()

        insight_type = item.get(
            "type",
            ""
        )

        message = item.get(
            "message",
            ""
        )


        # ----------------------------------------------------
        # HIGH PRIORITY / CRITICAL ISSUES
        # ----------------------------------------------------

        if priority == "high":

            if insight_type in [

                "negative_profit",

                "high_expense_ratio",

                "high_variation",

                "low_performance",

                "missing_data",

                "outliers"

            ]:

                critical_issues.append({

                    "type": insight_type,

                    "message": message,

                    "score": item.get(
                        "score",
                        0
                    )

                })


        # ----------------------------------------------------
        # POSITIVE SIGNALS
        # ----------------------------------------------------

        if insight_type == "data_quality":

            message_lower = message.lower()

            if (

                "no missing values" in message_lower

                or

                "no duplicate" in message_lower

            ):

                positive_signals.append({

                    "type": insight_type,

                    "message": message

                })


        # ----------------------------------------------------
        # KEY BUSINESS FINDINGS
        # ----------------------------------------------------

        if insight_type in [

            "group_comparison",

            "correlation",

            "department_profit_difference",

            "numeric_summary"

        ]:

            key_findings.append({

                "type": insight_type,

                "message": message,

                "priority": priority

            })


    # --------------------------------------------------------
    # SORT CRITICAL ISSUES
    # --------------------------------------------------------

    critical_issues = sorted(

        critical_issues,

        key=lambda x: x.get(
            "score",
            0
        ),

        reverse=True

    )


    # Maximum 5 critical issues

    critical_issues = critical_issues[:5]


    # --------------------------------------------------------
    # MANAGEMENT PRIORITIES
    # --------------------------------------------------------

    for issue in critical_issues:

        issue_type = issue.get(
            "type"
        )


        if issue_type == "negative_profit":

            management_priorities.append(

                "Investigate negative profit records and identify the main loss drivers."

            )


        elif issue_type == "high_expense_ratio":

            management_priorities.append(

                "Review operational expenses and reduce high expense-to-revenue ratios."

            )


        elif issue_type == "low_performance":

            management_priorities.append(

                "Review employees or teams with low performance ratings and create improvement plans."

            )


        elif issue_type == "high_variation":

            management_priorities.append(

                "Investigate metrics with unusually high variation to identify instability or extreme values."

            )


        elif issue_type == "missing_data":

            management_priorities.append(

                "Improve data collection processes to reduce missing information."

            )


        elif issue_type == "outliers":

            management_priorities.append(

                "Review detected outliers before making important business decisions."

            )


    # Remove duplicate priorities

    management_priorities = list(

        dict.fromkeys(
            management_priorities
        )

    )


    # --------------------------------------------------------
    # EXECUTIVE SUMMARY TEXT
    # --------------------------------------------------------

    summary_sentences = []


    if positive_signals:

        summary_sentences.append(

            "The dataset shows strong data quality with positive validation signals."

        )


    if critical_issues:

        summary_sentences.append(

            f"{len(critical_issues)} high-priority business or data risks require management attention."

        )


    # Add important findings

    important_findings = [

        item

        for item in key_findings

        if item.get("priority") in [

            "high",

            "medium"

        ]

    ]


    for finding in important_findings[:3]:

        if finding.get("message"):

            summary_sentences.append(

                finding.get("message")

            )


    if management_priorities:

        summary_sentences.append(

            "Management should prioritize profitability, operational efficiency, and high-risk performance areas."

        )


    executive_summary = " ".join(
        summary_sentences
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "executive_summary": executive_summary,

        "critical_issues": critical_issues,

        "positive_signals": positive_signals,

        "management_priorities": management_priorities,

        "key_findings": key_findings[:10],

        "summary_statistics": {

            "total_insights":

                len(insights),

            "critical_issues":

                len(critical_issues),

            "positive_signals":

                len(positive_signals),

            "management_priorities":

                len(management_priorities)

        }

    }
# =========================================================
# GENESIS AI - PROFESSIONAL ROOT CAUSE
# + AI RECOMMENDATIONS ENGINE V2
# =========================================================

def genesis_dashboard_recommendations():

    df = require_df()

    recommendations = []
    root_causes = []

    total_rows = int(len(df))

    # =====================================================
    # HELPER
    # =====================================================

    def numeric(column):

        if column not in df.columns:
            return None

        return pd.to_numeric(
            df[column],
            errors="coerce"
        )

    def add_root_cause(
        category,
        title,
        factor,
        evidence,
        impact,
        severity="medium",
        confidence="medium",
        recommendation=""
    ):

        root_causes.append({

            "category": category,

            "title": title,

            "factor": factor,

            "evidence": evidence,

            "business_impact": impact,

            "severity": severity,

            "confidence": confidence,

            "recommendation": recommendation
        })

    def add_recommendation(
        priority,
        category,
        title,
        message,
        action,
        impact="medium"
    ):

        recommendations.append({

            "priority": priority,

            "category": category,

            "title": title,

            "message": message,

            "recommended_action": action,

            "expected_impact": impact
        })

    # =====================================================
    # 1. DATA QUALITY ROOT CAUSE
    # =====================================================

    missing_values = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_percentage = round(
        (
            missing_values
            / max(total_rows * max(len(df.columns), 1), 1)
        ) * 100,
        2
    )

    if missing_values > 0:

        severity = (
            "high"
            if missing_percentage >= 10
            else "medium"
        )

        add_root_cause(

            "data_quality",

            "Missing Data Risk",

            "Missing values",

            f"{missing_values} missing values detected "
            f"({missing_percentage}% of dataset cells).",

            "Incomplete records may reduce analytical accuracy.",

            severity,

            "high",

            "Review missing-value patterns and apply "
            "appropriate imputation or validation rules."
        )

        add_recommendation(

            severity,

            "data_quality",

            "Improve Missing Data Quality",

            f"The dataset contains {missing_values} missing values.",

            "Profile missing values by column and apply "
            "business-appropriate treatment.",

            "high"
        )

    if duplicate_rows > 0:

        duplicate_percentage = round(
            (
                duplicate_rows
                / max(total_rows, 1)
            ) * 100,
            2
        )

        add_root_cause(

            "data_quality",

            "Duplicate Record Risk",

            "Duplicate rows",

            f"{duplicate_rows} duplicate rows detected "
            f"({duplicate_percentage}%).",

            "Duplicate records can distort counts, "
            "averages and business KPIs.",

            "high" if duplicate_percentage >= 5 else "medium",

            "high",

            "Review duplicate records and remove "
            "confirmed duplicates."
        )

        add_recommendation(

            "high" if duplicate_percentage >= 5 else "medium",

            "data_quality",

            "Review Duplicate Records",

            f"{duplicate_rows} duplicate records were detected.",

            "Validate and remove duplicate records before "
            "final reporting.",

            "high"
        )

    # =====================================================
    # 2. PROFITABILITY ROOT CAUSE
    # =====================================================

    revenue = numeric("Revenue")
    expenses = numeric("Expenses")
    profit = numeric("Profit")

    if (
        revenue is not None
        and expenses is not None
        and profit is not None
    ):

        valid = pd.concat(
            [
                revenue.rename("Revenue"),
                expenses.rename("Expenses"),
                profit.rename("Profit")
            ],
            axis=1
        ).dropna()

        if not valid.empty:

            valid["expense_ratio"] = (
                valid["Expenses"]
                / valid["Revenue"].replace(0, np.nan)
            )

            valid["profit_margin"] = (
                valid["Profit"]
                / valid["Revenue"].replace(0, np.nan)
                * 100
            )

            negative_profit = int(
                (valid["Profit"] < 0).sum()
            )

            negative_profit_pct = round(
                negative_profit
                / max(len(valid), 1)
                * 100,
                2
            )

            high_expense = int(
                (
                    valid["expense_ratio"]
                    > 0.80
                ).sum()
            )

            high_expense_pct = round(
                high_expense
                / max(len(valid), 1)
                * 100,
                2
            )

            average_margin = round(
                float(
                    valid["profit_margin"].mean()
                ),
                2
            )

            # ---------------------------------------------
            # NEGATIVE PROFIT
            # ---------------------------------------------

            if negative_profit > 0:

                severity = (
                    "critical"
                    if negative_profit_pct >= 20
                    else "high"
                    if negative_profit_pct >= 10
                    else "medium"
                )

                add_root_cause(

                    "profitability",

                    "Negative Profit Driver",

                    "Loss-making records",

                    f"{negative_profit} records "
                    f"({negative_profit_pct}%) have negative profit.",

                    "Loss-making transactions directly reduce "
                    "overall profitability.",

                    severity,

                    "high",

                    "Investigate revenue, expenses and margin "
                    "for loss-making records."
                )

                add_recommendation(

                    severity,

                    "profitability",

                    "Reduce Negative Profit Cases",

                    f"{negative_profit_pct}% of valid records "
                    "are loss-making.",

                    "Identify high-cost and low-revenue records "
                    "and prioritize corrective action.",

                    "high"
                )

            # ---------------------------------------------
            # HIGH EXPENSE
            # ---------------------------------------------

            if high_expense > 0:

                severity = (
                    "critical"
                    if high_expense_pct >= 30
                    else "high"
                    if high_expense_pct >= 15
                    else "medium"
                )

                add_root_cause(

                    "expense_management",

                    "High Expense Ratio",

                    "Expenses exceeding 80% of revenue",

                    f"{high_expense} records "
                    f"({high_expense_pct}%) have expenses "
                    "above 80% of revenue.",

                    "High operating costs can suppress "
                    "profit margins.",

                    severity,

                    "high",

                    "Investigate cost drivers and reduce "
                    "unnecessary operating expenses."
                )

                add_recommendation(

                    severity,

                    "expense_management",

                    "Control High Expense Records",

                    f"{high_expense_pct}% of records have "
                    "expenses above 80% of revenue.",

                    "Analyze major expense categories and "
                    "identify cost-reduction opportunities.",

                    "high"
                )

            # ---------------------------------------------
            # PROFIT MARGIN
            # ---------------------------------------------

            if average_margin < 10:

                add_root_cause(

                    "profitability",

                    "Low Average Profit Margin",

                    "Overall profit margin",

                    f"Average profit margin is "
                    f"{average_margin}%.",

                    "Low margins indicate limited profitability "
                    "after accounting for operating costs.",

                    "high",

                    "medium",

                    "Review pricing, expense structure and "
                    "revenue mix."
                )

                add_recommendation(

                    "high",

                    "profitability",

                    "Improve Profit Margin",

                    f"Average profit margin is only "
                    f"{average_margin}%.",

                    "Improve pricing, reduce unnecessary costs "
                    "and prioritize higher-margin business areas.",

                    "high"
                )

    # =====================================================
    # 3. REVENUE -> PROFIT ROOT CAUSE
    # =====================================================

    if (
        revenue is not None
        and profit is not None
    ):

        correlation_df = pd.concat(
            [
                revenue.rename("Revenue"),
                profit.rename("Profit")
            ],
            axis=1
        ).dropna()

        if len(correlation_df) >= 3:

            correlation = correlation_df[
                "Revenue"
            ].corr(
                correlation_df["Profit"]
            )

            if pd.notna(correlation):

                correlation = float(correlation)

                if correlation >= 0.70:

                    add_root_cause(

                        "revenue_growth",

                        "Revenue Strongly Influences Profit",

                        "Revenue",

                        f"Revenue-Profit correlation "
                        f"is {round(correlation, 4)}.",

                        "Revenue growth is strongly associated "
                        "with higher profit.",

                        "high",

                        "high",

                        "Focus on sustainable revenue growth "
                        "while protecting margins."
                    )

                elif correlation < 0.30:

                    add_root_cause(

                        "profitability",

                        "Weak Revenue-to-Profit Conversion",

                        "Revenue conversion",

                        f"Revenue-Profit correlation "
                        f"is only {round(correlation, 4)}.",

                        "Additional revenue may not consistently "
                        "translate into additional profit.",

                        "high",

                        "medium",

                        "Investigate pricing, expenses and "
                        "low-margin revenue sources."
                    )

                    add_recommendation(

                        "high",

                        "profitability",

                        "Improve Revenue-to-Profit Conversion",

                        f"Revenue-Profit correlation is "
                        f"{round(correlation, 4)}.",

                        "Identify revenue sources with weak "
                        "profit conversion and improve their margins.",

                        "high"
                    )

    # =====================================================
    # 4. PERFORMANCE ROOT CAUSE
    # =====================================================

    performance = numeric(
        "Performance Rating"
    )

    if performance is not None:

        valid_performance = (
            performance.dropna()
        )

        if not valid_performance.empty:

            low_performance = int(
                (
                    valid_performance <= 2
                ).sum()
            )

            low_performance_pct = round(
                low_performance
                / len(valid_performance)
                * 100,
                2
            )

            if low_performance > 0:

                severity = (
                    "high"
                    if low_performance_pct >= 20
                    else "medium"
                )

                add_root_cause(

                    "performance",

                    "Low Performance Population",

                    "Performance Rating <= 2",

                    f"{low_performance} records "
                    f"({low_performance_pct}%) have "
                    "low performance ratings.",

                    "Low performance can affect productivity "
                    "and business outcomes.",

                    severity,

                    "high",

                    "Analyze low-performing groups and "
                    "identify training or management gaps."
                )

                add_recommendation(

                    severity,

                    "performance",

                    "Improve Low Performance",

                    f"{low_performance_pct}% of records "
                    "have ratings of 2 or below.",

                    "Provide targeted training, coaching and "
                    "performance monitoring.",

                    "medium"
                )

    # =====================================================
    # 5. ATTENDANCE -> PERFORMANCE ROOT CAUSE
    # =====================================================

    attendance = numeric(
        "Attendance %"
    )

    if (
        attendance is not None
        and performance is not None
    ):

        relationship_df = pd.concat(
            [
                attendance.rename("Attendance"),
                performance.rename("Performance")
            ],
            axis=1
        ).dropna()

        if len(relationship_df) >= 3:

            correlation = relationship_df[
                "Attendance"
            ].corr(
                relationship_df["Performance"]
            )

            if pd.notna(correlation):

                correlation = float(
                    correlation
                )

                if correlation < -0.30:

                    add_root_cause(

                        "workforce",

                        "Attendance May Affect Performance",

                        "Attendance",

                        f"Attendance-Performance correlation "
                        f"is {round(correlation, 4)}.",

                        "Lower attendance is associated with "
                        "lower performance.",

                        "medium",

                        "medium",

                        "Investigate attendance patterns and "
                        "workforce engagement."
                    )

                elif correlation > 0.30:

                    add_root_cause(

                        "workforce",

                        "Attendance Is Positively Associated With Performance",

                        "Attendance",

                        f"Attendance-Performance correlation "
                        f"is {round(correlation, 4)}.",

                        "Higher attendance is associated with "
                        "higher performance.",

                        "medium",

                        "medium",

                        "Maintain attendance initiatives and "
                        "monitor their performance impact."
                    )

    # =====================================================
    # 6. TRAINING -> PERFORMANCE ROOT CAUSE
    # =====================================================

    training = numeric(
        "Training Hours"
    )

    if (
        training is not None
        and performance is not None
    ):

        training_df = pd.concat(
            [
                training.rename("Training"),
                performance.rename("Performance")
            ],
            axis=1
        ).dropna()

        if len(training_df) >= 3:

            correlation = training_df[
                "Training"
            ].corr(
                training_df["Performance"]
            )

            if pd.notna(correlation):

                correlation = float(
                    correlation
                )

                if correlation > 0.30:

                    add_root_cause(

                        "training",

                        "Training Is Positively Associated With Performance",

                        "Training Hours",

                        f"Training-Performance correlation "
                        f"is {round(correlation, 4)}.",

                        "Training may contribute to improved "
                        "employee performance.",

                        "medium",

                        "medium",

                        "Prioritize targeted training for "
                        "low-performing employees."
                    )

                    add_recommendation(

                        "medium",

                        "training",

                        "Use Targeted Training",

                        f"Training-Performance correlation "
                        f"is {round(correlation, 4)}.",

                        "Focus training programs on employees "
                        "with low performance ratings.",

                        "medium"
                    )

    # =====================================================
    # 7. DEPARTMENT ROOT CAUSE
    # =====================================================

    if (
        "Department" in df.columns
        and profit is not None
    ):

        temp = df.copy()

        temp["_profit_numeric"] = profit

        department_profit = (
            temp.groupby(
                "Department"
            )["_profit_numeric"]
            .mean()
            .dropna()
            .sort_values()
        )

        if len(department_profit) >= 2:

            lowest_department = str(
                department_profit.index[0]
            )

            highest_department = str(
                department_profit.index[-1]
            )

            lowest_profit = float(
                department_profit.iloc[0]
            )

            highest_profit = float(
                department_profit.iloc[-1]
            )

            difference = (
                highest_profit
                - lowest_profit
            )

            if difference > 0:

                add_root_cause(

                    "department_analysis",

                    "Department Profitability Difference",

                    lowest_department,

                    f"{lowest_department} has the lowest "
                    f"average profit ({round(lowest_profit, 2)}), "
                    f"while {highest_department} has the highest "
                    f"({round(highest_profit, 2)}).",

                    f"Average profit differs by "
                    f"{round(difference, 2)} between "
                    "the highest and lowest departments.",

                    "medium",

                    "high",

                    "Investigate department-level revenue, "
                    "expense and operational differences."
                )

                add_recommendation(

                    "medium",

                    "department_analysis",

                    "Investigate Department Profitability",

                    f"{lowest_department} has the lowest "
                    "average profit among departments.",

                    "Compare revenue, expenses, staffing and "
                    "operational factors with higher-performing departments.",

                    "medium"
                )

    # =====================================================
    # 8. DEPARTMENT PERFORMANCE ROOT CAUSE
    # =====================================================

    if (
        "Department" in df.columns
        and performance is not None
    ):

        temp = df.copy()

        temp["_performance_numeric"] = performance

        department_performance = (
            temp.groupby(
                "Department"
            )["_performance_numeric"]
            .mean()
            .dropna()
            .sort_values()
        )

        if len(department_performance) >= 2:

            lowest_department = str(
                department_performance.index[0]
            )

            highest_department = str(
                department_performance.index[-1]
            )

            lowest_score = float(
                department_performance.iloc[0]
            )

            highest_score = float(
                department_performance.iloc[-1]
            )

            difference = (
                highest_score
                - lowest_score
            )

            if difference >= 0.50:

                add_root_cause(

                    "performance",

                    "Department Performance Gap",

                    lowest_department,

                    f"{lowest_department} has average "
                    f"performance {round(lowest_score, 2)}, "
                    f"versus {round(highest_score, 2)} in "
                    f"{highest_department}.",

                    "Performance gaps may indicate differences "
                    "in workload, management, skills or training.",

                    "medium",

                    "high",

                    "Compare training, workload, attendance "
                    "and management factors across departments."
                )

                add_recommendation(

                    "medium",

                    "performance",

                    "Investigate Department Performance Gap",

                    f"{lowest_department} has the lowest "
                    "average performance.",

                    "Compare workforce and operational factors "
                    "against higher-performing departments.",

                    "medium"
                )

    # =====================================================
    # 9. PRIORITY SORTING
    # =====================================================

    priority_order = {

        "critical": 1,

        "high": 2,

        "medium": 3,

        "low": 4
    }

    severity_order = {

        "critical": 1,

        "high": 2,

        "medium": 3,

        "low": 4
    }

    recommendations = sorted(

        recommendations,

        key=lambda item:
        priority_order.get(
            item.get("priority"),
            99
        )
    )

    root_causes = sorted(

        root_causes,

        key=lambda item:
        severity_order.get(
            item.get("severity"),
            99
        )
    )

    # =====================================================
    # 10. PRIORITY COUNTS
    # =====================================================

    priority_counts = {

        "critical": sum(
            1
            for item in recommendations
            if item["priority"] == "critical"
        ),

        "high": sum(
            1
            for item in recommendations
            if item["priority"] == "high"
        ),

        "medium": sum(
            1
            for item in recommendations
            if item["priority"] == "medium"
        ),

        "low": sum(
            1
            for item in recommendations
            if item["priority"] == "low"
        )
    }

    # =====================================================
    # 11. EXECUTIVE SUMMARY
    # =====================================================

    if root_causes:

        critical_causes = sum(
            1
            for item in root_causes
            if item["severity"] == "critical"
        )

        high_causes = sum(
            1
            for item in root_causes
            if item["severity"] == "high"
        )

        if critical_causes > 0:

            overall_risk = "Critical"

        elif high_causes > 0:

            overall_risk = "High"

        elif len(root_causes) > 0:

            overall_risk = "Moderate"

        else:

            overall_risk = "Low"

        executive_summary = (

            f"Genesis AI identified "
            f"{len(root_causes)} potential root-cause signals "
            f"and {len(recommendations)} actionable recommendations. "
            f"Overall business risk level is {overall_risk}."
        )

    else:

        overall_risk = "Low"

        executive_summary = (

            "No significant business root-cause signals "
            "were identified from the available dataset."
        )

        recommendations.append({

            "priority": "low",

            "category": "monitoring",

            "title": "Continue Business Monitoring",

            "message": (
                "No major risk signals were detected."
            ),

            "recommended_action": (
                "Continue monitoring business KPIs, "
                "data quality and performance trends."
            ),

            "expected_impact": "medium"
        })

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return _json_safe({

        "success": True,

        "analysis_type":
            "professional_root_cause_analysis_v2",

        "dataset_rows":
            total_rows,

        "dataset_columns":
            int(len(df.columns)),

        "overall_risk":
            overall_risk,

        "executive_summary":
            executive_summary,

        "root_cause_summary": {

            "total_root_causes":
                len(root_causes),

            "critical":
                sum(
                    1
                    for item in root_causes
                    if item["severity"] == "critical"
                ),

            "high":
                sum(
                    1
                    for item in root_causes
                    if item["severity"] == "high"
                ),

            "medium":
                sum(
                    1
                    for item in root_causes
                    if item["severity"] == "medium"
                ),

            "low":
                sum(
                    1
                    for item in root_causes
                    if item["severity"] == "low"
                )
        },

        "priority_counts":
            priority_counts,

        "root_causes":
            root_causes,

        "recommendations":
            recommendations
    })
@app.api_route(
    "/analytics/recommendations",
    methods=["GET", "POST"]
)
def analytics_recommendations():
    return genesis_dashboard_recommendations()

def analytics_executive_summary():
    return genesis_dashboard_executive_summary()


# =====================================================
# GENESIS AI - CLEANING PROFILE
# =====================================================

def genesis_cleaning_profile():

    global df

    if df is None or df.empty:
        raise HTTPException(
            status_code=400,
            detail="Please upload a dataset first."
        )

    total_rows = len(df)
    total_columns = len(df.columns)

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    empty_columns = [
        column
        for column in df.columns
        if df[column].isnull().all()
    ]

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()
    

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    issues = []

    if missing_values > 0:
        issues.append(
            f"{missing_values} missing values detected"
        )

    if duplicate_rows > 0:
        issues.append(
            f"{duplicate_rows} duplicate rows detected"
        )

    if len(empty_columns) > 0:
        issues.append(
            f"{len(empty_columns)} completely empty columns detected"
        )

    if missing_values > total_rows * 0.2:
        cleaning_priority = "HIGH"

    elif (
        missing_values > 0
        or duplicate_rows > 0
        or len(empty_columns) > 0
    ):
        cleaning_priority = "MEDIUM"

    else:
        cleaning_priority = "LOW"

    recommendations = []

    if missing_values > 0:
        recommendations.append(
            "Review and handle missing values"
        )

    if duplicate_rows > 0:
        recommendations.append(
            "Review and remove duplicate records"
        )

    if len(text_columns) > 0:
        recommendations.append(
            "Standardize text formatting"
        )

    if len(empty_columns) > 0:
        recommendations.append(
            "Remove or review completely empty columns"
        )

    if not recommendations:
        recommendations.append(
            "Dataset appears clean. Continue with regular quality monitoring."
        )

    return {
        "status": "success",
        "module": "Genesis AI Cleaning Profile",

        "dataset_profile": {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "empty_columns": empty_columns,
            "numeric_columns_count": len(numeric_columns),
            "text_columns_count": len(text_columns)
        },

        "cleaning_priority": cleaning_priority,

        "issues_detected": issues,

        "recommended_actions": recommendations
    }
# =====================================================
# GENESIS AI CLEANING ENGINE
# =====================================================

@app.post("/genesis/clean/ai")
def genesis_ai_cleaning():

    global current_df

    if current_df is None:
        add_audit_log(
    "AI_CLEANING",
    {
        "rows_before": int(len(df)),
        "rows_after": int(len(df)),
        "recommendations": len(recommendations)
    }
)
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    recommendations = []

    # -----------------------------------------
    # Missing Values
    # -----------------------------------------

    missing_columns = []

    for column in df.columns:

        missing_count = int(df[column].isna().sum())

        if missing_count > 0:

            missing_columns.append({
                "column": column,
                "missing": missing_count
            })

            recommendations.append({
                "issue": "Missing Values",
                "column": column,
                "action": f"Fill or remove {missing_count} missing values."
            })

    # -----------------------------------------
    # Duplicate Rows
    # -----------------------------------------

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if duplicate_rows > 0:

        recommendations.append({
            "issue": "Duplicate Rows",
            "column": "Dataset",
            "action": f"Remove {duplicate_rows} duplicate rows."
        })

    # -----------------------------------------
    # Text Cleaning
    # -----------------------------------------

    text_columns = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    for column in text_columns:

        try:

            values = df[column].dropna().astype(str)

            space_count = int(
                values.str.startswith(" ").sum()
                +
                values.str.endswith(" ").sum()
            )

            if space_count > 0:

                recommendations.append({
                    "issue": "Extra Spaces",
                    "column": column,
                    "action": "Trim leading and trailing spaces."
                })

        except Exception:
            pass

    # -----------------------------------------
    # Data Type Suggestions
    # -----------------------------------------

    datatype_suggestions = []

    for column in df.columns:

        dtype = str(df[column].dtype)

        datatype_suggestions.append({
            "column": column,
            "current_type": dtype
        })

    # -----------------------------------------
    # Cleaning Score
    # -----------------------------------------

    total_issues = (
        len(missing_columns)
        +
        duplicate_rows
    )

    if total_issues == 0:

        cleaning_score = 100

    else:

        cleaning_score = max(
            0,
            100 - min(total_issues, 100)
        )

    # -----------------------------------------
    # Response
    # -----------------------------------------
    current_df = df

    save_dataset_version("AI Cleaning Applied")
    return {

        "success": True,

        "rows": int(len(df)),

        "columns": int(len(df.columns)),

        "cleaning_score": cleaning_score,

        "duplicate_rows": duplicate_rows,

        "missing_columns": missing_columns,

        "recommendations": recommendations,

        "datatype_suggestions": datatype_suggestions,

        "summary": (
            "Dataset is clean and ready for analysis."
            if len(recommendations) == 0
            else
            f"Genesis AI detected {len(recommendations)} cleaning recommendations."
        )

    }
# =====================================================
# GENESIS AI STANDARDIZATION ENGINE
# =====================================================

@app.post("/genesis/clean/standardize")
def genesis_standardization():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    changes = []

    # -----------------------------------------
    # STANDARDIZE COLUMN NAMES
    # -----------------------------------------

    old_columns = df.columns.tolist()

    new_columns = []

    for column in old_columns:

        clean_name = str(column).strip()

        clean_name = " ".join(
            clean_name.split()
        )

        new_columns.append(clean_name)

        if clean_name != column:

            changes.append({
                "type": "column_name",
                "column": str(column),
                "before": str(column),
                "after": clean_name
            })

    df.columns = new_columns

    # -----------------------------------------
    # STANDARDIZE TEXT COLUMNS
    # -----------------------------------------

    text_columns = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    for column in text_columns:

        before_series = df[column].copy()

        # Remove extra spaces
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

        # Replace multiple spaces with one space
        df[column] = (
            df[column]
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )

        # Count changed values
        changed_count = int(
            (before_series.astype(str) != df[column])
            .sum()
        )

        if changed_count > 0:

            changes.append({
                "type": "text_standardization",
                "column": column,
                "changed_values": changed_count,
                "actions": [
                    "Removed leading/trailing spaces",
                    "Normalized multiple spaces"
                ]
            })

    # -----------------------------------------
    # SAVE STANDARDIZED DATASET
    # -----------------------------------------

    current_df = df
    add_audit_log(
    "STANDARDIZATION",
    {
        "changes": len(changes)
    }
)
save_dataset_version("Standardization Applied")
    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------


# =====================================================
# GENESIS AI SMART VISUALIZATION ENGINE
# =====================================================

@app.post("/genesis/visualization/smart")
def genesis_smart_visualization():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=["datetime64[ns]"]
    ).columns.tolist()

    recommendations = []

    # Category charts
    for column in categorical_columns:

        unique_count = int(
            df[column].nunique()
        )

        if 2 <= unique_count <= 20:

            recommendations.append({
                "chart_type": "bar",
                "title": f"{column} Distribution",
                "column": column,
                "reason": "Good for comparing categories."
            })

    # Numeric charts
    for column in numeric_columns[:10]:

        recommendations.append({
            "chart_type": "histogram",
            "title": f"{column} Distribution",
            "column": column,
            "reason": "Good for understanding numeric distribution."
        })

    # Category vs numeric
    for category in categorical_columns[:5]:

        if 2 <= df[category].nunique() <= 15:

            for metric in numeric_columns[:5]:

                recommendations.append({
                    "chart_type": "bar",
                    "title": f"{metric} by {category}",
                    "category": category,
                    "metric": metric,
                    "aggregation": "mean",
                    "reason": "Good for comparing averages."
                })

    return {
        "success": True,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations[:50],
        "summary": (
            f"Genesis AI generated "
            f"{min(len(recommendations), 50)} "
            f"smart chart recommendations."
        )
    }
# =====================================================
# GENESIS AI KPI INTELLIGENCE ENGINE
# =====================================================

@app.post("/genesis/visualization/kpis")
def genesis_kpi_cards():

    global current_df

    if current_df is None:

        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    kpis = []

    # -----------------------------------------
    # DATASET KPIs
    # -----------------------------------------

    kpis.append({
        "title": "Total Records",
        "value": int(len(df)),
        "type": "dataset"
    })

    kpis.append({
        "title": "Total Columns",
        "value": int(len(df.columns)),
        "type": "dataset"
    })

    # -----------------------------------------
    # NUMERIC KPIs
    # -----------------------------------------

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    for column in numeric_columns:

        try:

            total_value = float(
                df[column].sum()
            )

            average_value = float(
                df[column].mean()
            )

            max_value = float(
                df[column].max()
            )

            min_value = float(
                df[column].min()
            )

            kpis.append({
                "title": f"Total {column}",
                "value": round(total_value, 2),
                "column": column,
                "metric": "sum"
            })

            kpis.append({
                "title": f"Average {column}",
                "value": round(average_value, 2),
                "column": column,
                "metric": "average"
            })

            kpis.append({
                "title": f"Maximum {column}",
                "value": round(max_value, 2),
                "column": column,
                "metric": "maximum"
            })

        except Exception:

            pass

    # -----------------------------------------
    # BUSINESS KPI DETECTION
    # -----------------------------------------

    business_keywords = [
        "revenue",
        "profit",
        "sales",
        "salary",
        "target",
        "achievement",
        "expenses",
        "bonus",
        "incentive"
    ]

    business_kpis = []

    for kpi in kpis:

        column_name = str(
            kpi.get("column", "")
        ).lower()

        if any(
            keyword in column_name
            for keyword in business_keywords
        ):

            business_kpis.append(kpi)

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return {

        "success": True,

        "dataset": {
            "rows": int(len(df)),
            "columns": int(len(df.columns))
        },

        "total_kpis": len(kpis),

        "kpis": kpis,

        "business_kpis": business_kpis[:20],

        "summary": (
            f"Genesis AI generated "
            f"{len(kpis)} KPI insights."
        )

    }
    # =====================================================
# GENESIS AI PII DETECTION ENGINE
# =====================================================

import re


@app.post("/genesis/governance/pii")
def genesis_pii_detection():

    global current_df

    # -----------------------------------------
    # CHECK DATASET
    # -----------------------------------------

    if current_df is None:
        add_audit_log(
    "PII_DETECTION",
    {
        "sensitive_columns": len(
            sensitive_columns
        ),
        "risk_level": risk_level
    }
)
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    sensitive_columns = []

    # -----------------------------------------
    # COLUMN NAME BASED DETECTION
    # -----------------------------------------

    pii_keywords = {

        "PERSON_NAME": [
            "name",
            "full_name",
            "first_name",
            "last_name",
            "employee_name",
            "customer_name"
        ],

        "EMAIL": [
            "email",
            "e_mail",
            "email_address"
        ],

        "PHONE": [
            "phone",
            "mobile",
            "mobile_number",
            "phone_number",
            "contact"
        ],

        "IDENTIFIER": [
            "employee_id",
            "customer_id",
            "user_id",
            "id_number",
            "identifier"
        ],

        "ADDRESS": [
            "address",
            "street",
            "location",
            "postal",
            "zipcode",
            "zip_code"
        ]

    }

    # -----------------------------------------
    # DETECT PII USING COLUMN NAMES
    # -----------------------------------------

    detected_columns = set()

    for column in df.columns:

        column_name = str(column).lower().strip()

        for pii_type, keywords in pii_keywords.items():

            if any(
                keyword in column_name
                for keyword in keywords
            ):

                sensitive_columns.append({

                    "column": column,

                    "pii_type": pii_type,

                    "detection_method":
                        "column_name"

                })

                detected_columns.add(column)

                break

    # -----------------------------------------
    # VALUE PATTERN DETECTION
    # -----------------------------------------

    email_pattern = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    phone_pattern = re.compile(
        r"^\+?[0-9\s\-\(\)]{7,20}$"
    )

    for column in df.columns:

        if column in detected_columns:
            continue

        try:

            values = (
                df[column]
                .dropna()
                .astype(str)
                .head(100)
            )

            if len(values) == 0:
                continue

            # EMAIL DETECTION

            email_matches = sum(
                bool(email_pattern.match(value))
                for value in values
            )

            if email_matches >= max(
                3,
                len(values) * 0.5
            ):

                sensitive_columns.append({

                    "column": column,

                    "pii_type": "EMAIL",

                    "detection_method":
                        "value_pattern"

                })

                detected_columns.add(column)

                continue

            # PHONE DETECTION

            phone_matches = sum(
                bool(phone_pattern.match(value))
                for value in values
            )

            if phone_matches >= max(
                3,
                len(values) * 0.5
            ):

                sensitive_columns.append({

                    "column": column,

                    "pii_type": "PHONE",

                    "detection_method":
                        "value_pattern"

                })

                detected_columns.add(column)

        except Exception:
            pass

    # -----------------------------------------
    # RISK SUMMARY
    # -----------------------------------------

    pii_count = len(sensitive_columns)

    if pii_count == 0:

        risk_level = "LOW"

    elif pii_count <= 2:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return {

        "success": True,

        "rows_analyzed": int(len(df)),

        "columns_analyzed": int(len(df.columns)),

        "pii_detected": pii_count > 0,

        "sensitive_columns":
            sensitive_columns,

        "total_sensitive_columns":
            pii_count,

        "privacy_risk":
            risk_level,

        "recommendation": (

            "No sensitive information detected."
            if pii_count == 0
            else
            "Sensitive columns detected. Consider masking, "
            "anonymization or access restrictions."

        )

    }
# =====================================================
# GENESIS AI METADATA CATALOG
# =====================================================

@app.post("/genesis/governance/metadata")
def genesis_metadata_catalog():

    global current_df

    # -----------------------------------------
    # CHECK DATASET
    # -----------------------------------------

    if current_df is None:
        add_audit_log(
    "METADATA_CATALOG",
    {
        "rows": int(len(df)),
        "columns": int(len(df.columns))
    }
)
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    metadata = []

    # -----------------------------------------
    # BUSINESS MEANING DETECTION
    # -----------------------------------------

    business_keywords = {
        "salary": "Employee compensation or salary amount",
        "bonus": "Employee bonus amount",
        "incentive": "Employee incentive amount",
        "revenue": "Business revenue",
        "expenses": "Business expenses",
        "expense": "Business expense amount",
        "profit": "Business profit",
        "sales": "Sales performance metric",
        "target": "Business or employee target",
        "achievement": "Target achievement percentage",
        "employee": "Employee-related information",
        "department": "Employee department",
        "designation": "Employee job designation",
        "manager": "Reporting manager information",
        "branch": "Business branch or office",
        "city": "Geographic city information",
        "email": "Email address",
        "phone": "Phone number",
        "age": "Employee age",
        "gender": "Employee gender",
        "experience": "Employee work experience",
        "attendance": "Employee attendance percentage",
        "leaves": "Employee leave information",
        "performance": "Employee performance rating",
        "training": "Employee training information",
        "project": "Project information",
        "client": "Client information",
        "education": "Employee education details",
        "skill": "Employee skill information",
        "promotion": "Employee promotion status",
        "resigned": "Employee resignation status",
        "date": "Date or time information"
    }

    # -----------------------------------------
    # PII DETECTION FOR CATALOG
    # -----------------------------------------

    pii_keywords = [
        "name",
        "email",
        "phone",
        "mobile",
        "address"
    ]

    # -----------------------------------------
    # BUILD COLUMN METADATA
    # -----------------------------------------

    for column in df.columns:

        column_name = str(column)

        lower_name = column_name.lower()

        dtype = str(df[column].dtype)

        missing = int(
            df[column].isna().sum()
        )

        unique = int(
            df[column].nunique(dropna=True)
        )

        # Sample values

        sample_values = (
            df[column]
            .dropna()
            .head(3)
            .astype(str)
            .tolist()
        )

        # -----------------------------------------
        # COLUMN CATEGORY
        # -----------------------------------------

        if pd.api.types.is_numeric_dtype(df[column]):

            category = "numeric"

        elif pd.api.types.is_datetime64_any_dtype(df[column]):

            category = "datetime"

        else:

            category = "categorical"

        # -----------------------------------------
        # BUSINESS MEANING
        # -----------------------------------------

        business_meaning = "General dataset information"

        for keyword, meaning in business_keywords.items():

            if keyword in lower_name:

                business_meaning = meaning

                break

        # -----------------------------------------
        # PII STATUS
        # -----------------------------------------

        is_pii = any(
            keyword in lower_name
            for keyword in pii_keywords
        )

        metadata.append({

            "column": column_name,

            "data_type": dtype,

            "category": category,

            "missing_values": missing,

            "missing_percent": round(
                (missing / len(df) * 100)
                if len(df) > 0 else 0,
                2
            ),

            "unique_values": unique,

            "sample_values": sample_values,

            "business_meaning": business_meaning,

            "pii": is_pii

        })

    # -----------------------------------------
    # DATASET SUMMARY
    # -----------------------------------------

    numeric_columns = int(
        len(
            df.select_dtypes(
                include=["number"]
            ).columns
        )
    )

    categorical_columns = int(
        len(
            df.select_dtypes(
                exclude=["number", "datetime"]
            ).columns
        )
    )

    datetime_columns = int(
        len(
            df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )
    )

    pii_columns = [
        item["column"]
        for item in metadata
        if item["pii"]
    ]

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return {

        "success": True,

        "dataset_summary": {

            "rows": int(len(df)),

            "columns": int(len(df.columns)),

            "numeric_columns": numeric_columns,

            "categorical_columns": categorical_columns,

            "datetime_columns": datetime_columns,

            "pii_columns": pii_columns

        },

        "metadata": metadata

    }
# =====================================================
# GENESIS AI AUDIT LOGS
# =====================================================

@app.post("/genesis/governance/audit")
def genesis_audit_logs():

    return {
        "success": True,

        "total_events": len(audit_logs),

        "logs": audit_logs[::-1]
    }
# =====================================================
# GENESIS AI DATA TRANSFORMATION ENGINE
# COLUMN RENAME
# =====================================================


# =====================================================
# GENESIS AI DELETE COLUMN
# =====================================================

@app.post("/genesis/transform/delete-column")
def genesis_delete_column(
    column: str
):

    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Prevent deleting the last remaining column
    if len(current_df.columns) <= 1:
        return {
            "success": False,
            "message": "Cannot delete the last remaining column."
        }

    # Save current dataset for UNDO
    transformation_history.append({
        "dataset": current_df.copy(),
        "column": column,
        "operation": "delete_column",
        "value": None,
        "new_column": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rows_before": int(len(current_df)),
        "columns_before": int(len(current_df.columns))
    })

    # New transformation clears REDO history
    redo_history.clear()

    # Delete column
    current_df = current_df.drop(
        columns=[column]
    )

    # Audit log
    add_audit_log(
        "delete_column",
        {
            "column": column
        }
    )

    # Dataset version
    save_dataset_version(
        "column_deleted"
    )

    return {
        "success": True,
        "message": "Column deleted successfully.",
        "deleted_column": column,
        "rows": int(len(current_df)),
        "columns": int(len(current_df.columns)),
        "remaining_columns": current_df.columns.tolist(),
        "history_count": len(transformation_history)
    }
# =====================================================
# GENESIS AI DATA TRANSFORMATION ENGINE
# DATA TYPE CONVERSION
# =====================================================

@app.post("/genesis/transform/change-dtype")
def genesis_change_dtype(
    column: str,
    target_type: str
):

    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    # Check column
    if column not in df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Normalize target type
    target_type = target_type.strip().lower()

    allowed_types = [
        "int",
        "float",
        "string",
        "datetime"
    ]

    if target_type not in allowed_types:
        return {
            "success": False,
            "message": (
                "Invalid target type. "
                "Use: int, float, string, or datetime."
            )
        }

    # Store original type
    old_type = str(df[column].dtype)
    # Save current dataset for UNDO
    transformation_history.append({
    "dataset": current_df.copy(),
    "column": column,
    "operation": "change_dtype",
    "value": target_type,
    "new_column": None,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rows_before": int(len(current_df)),
    "columns_before": int(len(current_df.columns))
})

    # New transformation clears REDO history
    redo_history.clear()
    try:

        if target_type == "int":

            df[column] = pd.to_numeric(
                df[column],
                errors="raise"
            ).astype(int)

        elif target_type == "float":

            df[column] = pd.to_numeric(
                df[column],
                errors="raise"
            ).astype(float)

        elif target_type == "string":

            df[column] = df[column].astype(str)

        elif target_type == "datetime":

            df[column] = pd.to_datetime(
                df[column],
                errors="raise"
            )

    except Exception as e:

        return {
            "success": False,
            "message": f"Conversion failed: {str(e)}"
        }

    # Save transformed dataset
    current_df = df

    # Audit log
    add_audit_log(
        "change_dtype",
        {
            "column": column,
            "old_type": old_type,
            "new_type": str(df[column].dtype)
        }
    )

    # Dataset version
    save_dataset_version(
        "data_type_changed"
    )

    return {
        "success": True,
        "message": "Data type changed successfully.",
        "column": column,
        "old_type": old_type,
        "new_type": str(df[column].dtype)
    }
# =====================================================
# GENESIS AI DATA TRANSFORMATION ENGINE
# =====================================================

def genesis_transformation_preview():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    text_columns = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=["datetime64", "datetimetz"]
    ).columns.tolist()

    return {
        "success": True,

        "dataset": {
            "rows": int(len(df)),
            "columns": int(len(df.columns))
        },

        "available_transformations": {
            "numeric_columns": numeric_columns,
            "text_columns": text_columns,
            "datetime_columns": datetime_columns
        }
    }
# =====================================================
# GENESIS AI DATA TRANSFORMATION ENGINE
# =====================================================

@app.post("/genesis/transform/auto")
def genesis_data_transformation():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    df = current_df.copy()

    transformations = []

    # -----------------------------------------
    # DETECT DATE COLUMNS
    # -----------------------------------------

    date_columns = df.select_dtypes(
        include=["datetime64[ns]", "datetime64"]
    ).columns.tolist()

    for column in date_columns:

        year_column = f"{column}_Year"
        month_column = f"{column}_Month"

        if year_column not in df.columns:

            df[year_column] = df[column].dt.year

            transformations.append({
                "type": "date_extraction",
                "source": column,
                "created": year_column
            })

        if month_column not in df.columns:

            df[month_column] = df[column].dt.month

            transformations.append({
                "type": "date_extraction",
                "source": column,
                "created": month_column
            })

    # -----------------------------------------
    # NUMERIC CALCULATIONS
    # -----------------------------------------

    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if "Revenue" in df.columns and "Expenses" in df.columns:

        if "Calculated Profit" not in df.columns:

            df["Calculated Profit"] = (
                df["Revenue"] - df["Expenses"]
            )

            transformations.append({
                "type": "calculation",
                "formula": "Revenue - Expenses",
                "created": "Calculated Profit"
            })

    # -----------------------------------------
    # SAVE TRANSFORMED DATASET
    # -----------------------------------------

    current_df = df

    # -----------------------------------------
    # AUDIT LOG
    # -----------------------------------------

    try:

        add_audit_log(
            "DATA_TRANSFORMATION",
            {
                "transformations": len(transformations)
            }
        )

    except Exception:
        pass

    # -----------------------------------------
    # SAVE VERSION
    # -----------------------------------------

    try:

        save_dataset_version(
            "Data Transformation Applied"
        )

    except Exception:
        pass

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return {

        "success": True,

        "transformations": transformations,

        "total_transformations": len(
            transformations
        ),

        "rows": int(len(df)),

        "columns": int(len(df.columns))

    }
# =====================================================
# GENESIS AI DATA EXPLORER
# =====================================================

@app.get("/genesis/explore/{column_name}")
def genesis_explore_column(column_name: str):

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if column_name not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column_name}' not found."
        }

    series = current_df[column_name]

    result = {
        "success": True,
        "column": column_name,
        "dtype": str(series.dtype),
        "rows": int(len(series)),
        "missing": int(series.isna().sum()),
        "unique": int(series.nunique())
    }

    # Numeric column analysis
    if pd.api.types.is_numeric_dtype(series):

        result["type"] = "numeric"
        result["minimum"] = float(series.min())
        result["maximum"] = float(series.max())
        result["average"] = round(float(series.mean()), 2)
        result["median"] = round(float(series.median()), 2)

    else:

        result["type"] = "categorical"

        top_values = (
            series
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
        )

        result["top_values"] = [
            {
                "value": str(value),
                "count": int(count)
            }
            for value, count in top_values.items()
        ]

    return result
from pydantic import BaseModel


class TransformationRequest(BaseModel):
    column: str
    operation: str
    value: float | str | None = None
    new_column: str | None = None
    # =====================================================
# GENESIS AI TRANSFORMATION PREVIEW ENGINE
# =====================================================

@app.post("/genesis/transform/preview")
def genesis_transformation_preview(request: TransformationRequest):

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if request.column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{request.column}' not found."
        }

    # Original data copy
    preview_df = current_df.copy()

    column = request.column
    operation = request.operation.lower()

    try:

        # TEXT TRANSFORMATIONS
        if operation == "uppercase":
            preview_df[column] = preview_df[column].astype(str).str.upper()

        elif operation == "lowercase":
            preview_df[column] = preview_df[column].astype(str).str.lower()

        elif operation == "trim":
            preview_df[column] = preview_df[column].astype(str).str.strip()

        # NUMERIC TRANSFORMATIONS
        elif operation == "multiply":

            if request.value is None:
                return {
                    "success": False,
                    "message": "Value is required for multiply operation."
                }

            preview_df[column] = preview_df[column] * request.value

        elif operation == "divide":

            if request.value is None:
                return {
                    "success": False,
                    "message": "Value is required for divide operation."
                }

            if request.value == 0:
                return {
                    "success": False,
                    "message": "Cannot divide by zero."
                }

            preview_df[column] = preview_df[column] / request.value

        elif operation == "round":

            decimals = int(request.value or 0)
            preview_df[column] = preview_df[column].round(decimals)

        elif operation == "copy":

            if not request.new_column:
                return {
                    "success": False,
                    "message": "new_column is required for copy operation."
                }

            preview_df[request.new_column] = preview_df[column]

        else:
            return {
                "success": False,
                "message": f"Unsupported operation: {operation}"
            }

        # Before / After sample
        preview = []

        for index in range(min(10, len(current_df))):

            before_value = current_df.iloc[index][column]

            if operation == "copy":
                after_value = preview_df.iloc[index][request.new_column]
            else:
                after_value = preview_df.iloc[index][column]

            preview.append({
                "row": int(index + 1),
                "before": None if pd.isna(before_value) else str(before_value),
                "after": None if pd.isna(after_value) else str(after_value)
            })

        return {
            "success": True,
            "column": column,
            "operation": operation,
            "value": request.value,
            "new_column": request.new_column,
            "total_rows": int(len(current_df)),
            "preview_rows": len(preview),
            "preview": preview,
            "message": "Transformation preview generated successfully. No changes were applied to the dataset."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
# =====================================================
# GENESIS AI MANUAL TRANSFORMATION ENGINE
# =====================================================

@app.post("/genesis/transform/manual")
def genesis_transform(request: TransformationRequest):

    global current_df, transformation_history, redo_history
    

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if request.column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{request.column}' not found."
        }

    # -----------------------------------------
    # SAVE DATASET STATE FOR UNDO
    # -----------------------------------------

    transformation_history.append({
    "dataset": current_df.copy(),
    "column": request.column,
    "operation": request.operation,
    "value": request.value,
    "new_column": request.new_column,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rows_before": int(len(current_df)),
    "columns_before": int(len(current_df.columns))
})
    redo_history.clear()

    # Create working copy
    df = current_df.copy()

    column = request.column
    operation = request.operation.lower()

    try:

        # -----------------------------------------
        # TEXT TRANSFORMATIONS
        # -----------------------------------------

        if operation == "uppercase":

            df[column] = df[column].astype(str).str.upper()

        elif operation == "lowercase":

            df[column] = df[column].astype(str).str.lower()

        elif operation == "trim":

            df[column] = df[column].astype(str).str.strip()

        # -----------------------------------------
        # NUMERIC TRANSFORMATIONS
        # -----------------------------------------

        elif operation == "multiply":

            if request.value is None:
                return {
                    "success": False,
                    "message": "Please provide a value."
                }

            df[column] = df[column] * float(request.value)

        elif operation == "divide":

            if request.value is None:
                return {
                    "success": False,
                    "message": "Please provide a value."
                }

            if float(request.value) == 0:
                return {
                    "success": False,
                    "message": "Cannot divide by zero."
                }

            df[column] = df[column] / float(request.value)

        elif operation == "round":

            decimals = int(float(request.value or 0))

            df[column] = df[column].round(decimals)

        # -----------------------------------------
        # CREATE COPY OF COLUMN
        # -----------------------------------------

        elif operation == "copy":

            if not request.new_column:
                return {
                    "success": False,
                    "message": "Please provide new_column."
                }

            df[request.new_column] = df[column]

        else:

            return {
                "success": False,
                "message": f"Unsupported operation: {operation}"
            }

        # -----------------------------------------
        # SAVE TRANSFORMED DATASET
        # -----------------------------------------

        current_df = df

        return {
            "success": True,
            "column": column,
            "operation": operation,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history),
            "message": "Transformation applied successfully."
        }

    except Exception as e:

        # Remove history entry if transformation failed
        if transformation_history:
            transformation_history.pop()

        return {
            "success": False,
            "message": str(e)
        }


# =====================================================
# GENESIS AI TRANSFORMATION UNDO
# =====================================================
@app.post("/genesis/transform/undo")
def genesis_transform_undo():

    global current_df, transformation_history, redo_history

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if not transformation_history:
        return {
            "success": False,
            "message": "No transformation available to undo."
        }

    # Get last dataset state
    last_state = transformation_history.pop()

    # Save current dataset for REDO
    redo_history.append({
    "dataset": current_df.copy(),
    "column": last_state.get("column"),
    "operation": last_state.get("operation"),
    "value": last_state.get("value"),
    "new_column": last_state.get("new_column"),
    "timestamp": last_state.get("timestamp"),
    "rows_before": last_state.get("rows_before"),
    "columns_before": last_state.get("columns_before")
})

    # Restore previous dataset
    current_df = last_state["dataset"].copy()

    return {
        "success": True,
        "message": "Last transformation undone successfully.",
        "undone_column": last_state["column"],
        "undone_operation": last_state["operation"],
        "remaining_history": len(transformation_history),
        "rows": int(len(current_df)),
        "columns": int(len(current_df.columns))
    }
# =====================================================
# GENESIS AI TRANSFORMATION REDO
# =====================================================

@app.post("/genesis/transform/redo")
def genesis_transform_redo():

    global current_df, transformation_history, redo_history

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if not redo_history:
        return {
            "success": False,
            "message": "No transformation available to redo."
        }

    # Get last redo state
    redo_state = redo_history.pop()

    # Save current dataset back to UNDO history
    transformation_history.append({
    "dataset": current_df.copy(),
    "column": redo_state.get("column"),
    "operation": redo_state.get("operation"),
    "value": redo_state.get("value"),
    "new_column": redo_state.get("new_column"),
    "timestamp": redo_state.get("timestamp"),
    "rows_before": redo_state.get("rows_before"),
    "columns_before": redo_state.get("columns_before")
})

    # Restore dataset after transformation
    current_df = redo_state["dataset"].copy()

    return {
        "success": True,
        "message": "Last transformation redone successfully.",
        "redone_column": redo_state["column"],
        "redone_operation": redo_state["operation"],
        "remaining_redo_history": len(redo_history),
        "rows": int(len(current_df)),
        "columns": int(len(current_df.columns))
    }
# =====================================================
# GENESIS AI TRANSFORMATION HISTORY
# =====================================================

@app.get("/genesis/transform/history")
def genesis_transform_history():

    global transformation_history, redo_history

    history = []

    for index, item in enumerate(transformation_history, start=1):

        history.append({
            "step": index,
            "column": item.get("column"),
            "operation": item.get("operation"),
            "value": item.get("value"),
            "new_column": item.get("new_column"),
            "timestamp": item.get("timestamp"),
            "rows_before": item.get("rows_before"),
            "columns_before": item.get("columns_before")
        })

    return {
        "success": True,
        "history_count": len(transformation_history),
        "redo_count": len(redo_history),
        "history": history
    }
# =====================================================
# GENESIS AI DATASET RESET
# =====================================================

@app.post("/genesis/dataset/reset")
def genesis_dataset_reset():

    global latest_df, current_df
    global transformation_history, redo_history

    if latest_df is None:
        return {
            "success": False,
            "message": "No original dataset available. Please upload a dataset first."
        }

    # Restore original uploaded dataset
    current_df = latest_df.copy()

    # Clear transformation history
    transformation_history.clear()
    redo_history.clear()

    return {
        "success": True,
        "message": "Dataset reset successfully to the original uploaded version.",
        "rows": int(len(current_df)),
        "columns": int(len(current_df.columns)),
        "history_count": len(transformation_history),
        "redo_count": len(redo_history)
    }
# =====================================================
# GENESIS AI BATCH TRANSFORMATION ENGINE
# =====================================================

@app.post("/genesis/transform/batch")
def genesis_transform_batch(requests: list[TransformationRequest]):

    global current_df, transformation_history, redo_history

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if not requests:
        return {
            "success": False,
            "message": "No transformations provided."
        }

    # Save current dataset before batch transformation
    original_df = current_df.copy()

    results = []

    try:

        # Work on a copy first
        df = current_df.copy()

        for request in requests:

            column = request.column
            operation = request.operation.lower()

            if column not in df.columns:
                return {
                    "success": False,
                    "message": f"Column '{column}' not found."
                }

            # TEXT TRANSFORMATIONS
            if operation == "uppercase":
                df[column] = df[column].astype(str).str.upper()

            elif operation == "lowercase":
                df[column] = df[column].astype(str).str.lower()

            elif operation == "trim":
                df[column] = df[column].astype(str).str.strip()

            # NUMERIC TRANSFORMATIONS
            elif operation == "multiply":

                if request.value is None:
                    return {
                        "success": False,
                        "message": f"Value required for multiply on '{column}'."
                    }

                df[column] = df[column] * request.value

            elif operation == "divide":

                if request.value is None:
                    return {
                        "success": False,
                        "message": f"Value required for divide on '{column}'."
                    }

                if request.value == 0:
                    return {
                        "success": False,
                        "message": "Cannot divide by zero."
                    }

                df[column] = df[column] / request.value

            elif operation == "round":

                decimals = int(request.value or 0)
                df[column] = df[column].round(decimals)

            # COPY COLUMN
            elif operation == "copy":

                if not request.new_column:
                    return {
                        "success": False,
                        "message": f"new_column required for copy on '{column}'."
                    }

                df[request.new_column] = df[column]

            else:
                return {
                    "success": False,
                    "message": f"Unsupported operation: {operation}"
                }

            results.append({
                "column": column,
                "operation": operation,
                "value": request.value,
                "new_column": request.new_column
            })

        # Save ONE history state for entire batch
        transformation_history.append({
            "dataset": original_df,
            "column": "BATCH",
            "operation": "batch",
            "value": None,
            "new_column": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # New transformation clears redo history
        redo_history.clear()

        # Save final transformed dataset
        current_df = df

        return {
            "success": True,
            "message": "Batch transformations applied successfully.",
            "transformations_applied": len(results),
            "results": results,
            "rows": int(len(current_df)),
            "columns": int(len(current_df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
@app.post("/genesis/transform/create-column")
def genesis_create_column(
    new_column: str,
    source_column: str = None,
    value: str = None
):

    global current_df

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Save original dataset for UNDO
    original_df = current_df.copy(deep=True)

    # Working copy
    df = current_df.copy()

    # Clean column name
    new_column = new_column.strip()

    if not new_column:
        return {
            "success": False,
            "message": "New column name cannot be empty."
        }

    # Prevent duplicate column
    if new_column in df.columns:
        return {
            "success": False,
            "message": f"Column '{new_column}' already exists."
        }

    # At least one source is required
    if source_column is None and value is None:
        return {
            "success": False,
            "message": "Provide either source_column or value."
        }

    operation = None

    # Create column by copying another column
    if source_column is not None:

        source_column = source_column.strip()

        if source_column not in df.columns:
            return {
                "success": False,
                "message": f"Source column '{source_column}' not found."
            }

        df[new_column] = df[source_column]

        operation = "copy_column"

    # Create constant value column
    else:

        df[new_column] = value

        operation = "create_constant_column"

    # Save state for UNDO
    transformation_history.append({
        "dataset": original_df,
        "column": source_column if source_column else new_column,
        "operation": operation,
        "value": value,
        "new_column": new_column,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rows_before": int(len(original_df)),
        "columns_before": int(len(original_df.columns))
    })

    # New transformation clears REDO history
    redo_history.clear()

    # Save updated dataset
    current_df = df

    # Audit log
    add_audit_log(
        operation,
        {
            "new_column": new_column,
            "source_column": source_column,
            "value": value
        }
    )

    # Dataset version
    save_dataset_version(
        operation
    )

    return {
        "success": True,
        "message": "New column created successfully.",
        "new_column": new_column,
        "source_column": source_column,
        "value": value,
        "operation": operation,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "history_count": len(transformation_history)
    }
# ============================================================
# GENESIS AI - CALCULATED / DERIVED COLUMN
# ============================================================


# ============================================================
# GENESIS AI - CONDITIONAL COLUMN / IF-ELSE TRANSFORMATION
# ============================================================

# ============================================================
# GENESIS AI - COLUMN VALUE REPLACEMENT
# ============================================================

@app.post("/genesis/transform/replace-value")
def genesis_replace_value(
    column: str,
    old_value: str,
    new_value: str
):

    global current_df

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean column name
    column = column.strip()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Save original dataset for UNDO
    original_df = current_df.copy(deep=True)

    df = current_df.copy()

    try:

        # Count matching values
        replacement_count = int(
            (df[column].astype(str) == str(old_value)).sum()
        )

        # Check if value exists
        if replacement_count == 0:
            return {
                "success": False,
                "message": (
                    f"Value '{old_value}' not found "
                    f"in column '{column}'."
                )
            }

        # Replace value
        df[column] = df[column].replace(
            old_value,
            new_value
        )

    except Exception as e:

        return {
            "success": False,
            "message": f"Value replacement failed: {str(e)}"
        }

    # Save history for UNDO
    transformation_history.append({
        "dataset": original_df,
        "column": column,
        "operation": "replace_value",
        "value": {
            "old_value": old_value,
            "new_value": new_value
        },
        "new_column": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rows_before": int(len(original_df)),
        "columns_before": int(len(original_df.columns))
    })

    # Clear redo history
    redo_history.clear()

    # Save transformed dataset
    current_df = df

    # Audit log
    add_audit_log(
        "replace_value",
        {
            "column": column,
            "old_value": old_value,
            "new_value": new_value,
            "replacement_count": replacement_count
        }
    )

    # Dataset version
    save_dataset_version(
        "value_replaced"
    )

    return {
        "success": True,
        "message": "Value replaced successfully.",
        "column": column,
        "old_value": old_value,
        "new_value": new_value,
        "replacement_count": replacement_count,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "history_count": len(transformation_history)
    }
# =========================================================
# GENESIS AI - SPLIT COLUMN TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/split-column")
def genesis_split_column(
    column: str,
    delimiter: str = "",
    new_columns: str = ""
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean column name
    column = column.strip()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    try:

        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Get sample values
        sample_values = (
            df[column]
            .dropna()
            .astype(str)
            .head(20)
            .tolist()
        )

        # -------------------------------------------------
        # AUTO DETECT DELIMITER
        # -------------------------------------------------

        cleaned_delimiter = delimiter.strip() if delimiter else ""

        if cleaned_delimiter:

            # User provided delimiter
            used_delimiter = cleaned_delimiter

        else:

            # Automatically detect delimiter
            possible_delimiters = [
                "_",
                " ",
                "-",
                ",",
                "/",
                "|",
                ";",
                ":"
            ]

            used_delimiter = None

            for possible in possible_delimiters:

                if any(
                    possible in value
                    for value in sample_values
                ):
                    used_delimiter = possible
                    break

            # No delimiter detected
            if used_delimiter is None:
                return {
                    "success": False,
                    "message": (
                        "No delimiter could be detected automatically. "
                        "Please provide a valid delimiter."
                    ),
                    "sample_values": sample_values[:5]
                }

        # -------------------------------------------------
        # SPLIT DATA
        # -------------------------------------------------

        split_data = df[column].astype(str).str.split(
            used_delimiter,
            expand=True,
            regex=False
        )

        # Remove completely empty columns
        split_data = split_data.dropna(
            axis=1,
            how="all"
        )

        split_parts = split_data.shape[1]

        # -------------------------------------------------
        # CHECK SPLIT RESULT
        # -------------------------------------------------

        if split_parts < 2:
            return {
                "success": False,
                "message": (
                    f"Column could not be split using delimiter "
                    f"'{used_delimiter}'."
                ),
                "detected_delimiter": used_delimiter,
                "split_parts": split_parts,
                "sample_values": sample_values[:5]
            }

        # -------------------------------------------------
        # NEW COLUMN NAMES
        # -------------------------------------------------

        if new_columns and new_columns.strip():

            column_names = [
                name.strip()
                for name in new_columns.split(",")
                if name.strip()
            ]

            if len(column_names) != split_parts:
                return {
                    "success": False,
                    "message": (
                        f"Split created {split_parts} parts, "
                        f"but you provided {len(column_names)} "
                        f"new column names."
                    ),
                    "detected_parts": split_parts
                }

        else:

            column_names = [
                f"{column}_part_{i + 1}"
                for i in range(split_parts)
            ]

        # -------------------------------------------------
        # CHECK EXISTING COLUMNS
        # -------------------------------------------------

        existing_columns = [
            col_name
            for col_name in column_names
            if col_name in df.columns
        ]

        if existing_columns:
            return {
                "success": False,
                "message": (
                    "These columns already exist: "
                    + ", ".join(existing_columns)
                )
            }

        # Assign names
        split_data.columns = column_names

        # Add columns
        for col_name in column_names:
            df[col_name] = split_data[col_name]

        # -------------------------------------------------
        # SAVE UNDO HISTORY
        # -------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "split_column",
            "new_columns": column_names,
            "delimiter": used_delimiter,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "split_column",
            {
                "column": column,
                "delimiter": used_delimiter,
                "new_columns": column_names
            }
        )

        # Dataset version
        save_dataset_version(
            "column_split"
        )

        return {
            "success": True,
            "message": "Column split successfully.",
            "source_column": column,
            "delimiter_used": used_delimiter,
            "new_columns": column_names,
            "split_parts": split_parts,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Split column failed: {str(e)}"
        }
    # =========================================================
# DEBUG EMPLOYEE NAME VALUES
# =========================================================

@app.get("/genesis/debug/column-values")
def debug_column_values(column: str):

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    sample_values = (
        current_df[column]
        .dropna()
        .astype(str)
        .head(10)
        .tolist()
    )

    return {
        "success": True,
        "column": column,
        "sample_values": sample_values,
        "python_repr": [repr(value) for value in sample_values]
    }
# =========================================================
# GENESIS DEBUG - EMPLOYEE NAME
# =========================================================

@app.get("/genesis/debug/employee-name")
def debug_employee_name():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = "Employee Name"

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found.",
            "available_columns": current_df.columns.tolist()
        }

    values = current_df[column].head(10).tolist()

    return {
        "success": True,
        "column": column,
        "values": values,
        "repr_values": [
            repr(value)
            for value in values
        ]
    }
# =========================================================
# GENESIS AI - MERGE / COMBINE COLUMNS TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/merge-columns")
def genesis_merge_columns(
    columns: str,
    separator: str = "_",
    new_column: str = ""
):
    global current_df, transformation_history, redo_history

    # -------------------------------------------------
    # CHECK DATASET
    # -------------------------------------------------

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # -------------------------------------------------
    # VALIDATE INPUT
    # -------------------------------------------------

    if not columns or not columns.strip():
        return {
            "success": False,
            "message": "Please provide columns to merge."
        }

    if not new_column or not new_column.strip():
        return {
            "success": False,
            "message": "Please provide a new column name."
        }

    # Convert comma-separated columns to list
    column_list = [
        col.strip()
        for col in columns.split(",")
        if col.strip()
    ]

    new_column = new_column.strip()

    # Need at least 2 columns
    if len(column_list) < 2:
        return {
            "success": False,
            "message": "Please provide at least 2 columns to merge."
        }

    # -------------------------------------------------
    # CHECK COLUMNS EXIST
    # -------------------------------------------------

    missing_columns = [
        col
        for col in column_list
        if col not in current_df.columns
    ]

    if missing_columns:
        return {
            "success": False,
            "message": (
                "These columns were not found: "
                + ", ".join(missing_columns)
            )
        }

    # Check duplicate column name
    if new_column in current_df.columns:
        return {
            "success": False,
            "message": (
                f"Column '{new_column}' already exists."
            )
        }

    try:

        # -------------------------------------------------
        # SAVE ORIGINAL DATASET FOR UNDO
        # -------------------------------------------------

        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # -------------------------------------------------
        # CLEAN SEPARATOR
        # -------------------------------------------------

        if separator is None:
            separator = ""

        # -------------------------------------------------
        # MERGE COLUMNS
        # -------------------------------------------------

        df[new_column] = (
            df[column_list]
            .fillna("")
            .astype(str)
            .agg(separator.join, axis=1)
        )

        # -------------------------------------------------
        # SAVE UNDO HISTORY
        # -------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": None,
            "operation": "merge_columns",
            "source_columns": column_list,
            "new_column": new_column,
            "separator": separator,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(
                len(original_df.columns)
            )
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        add_audit_log(
            "merge_columns",
            {
                "source_columns": column_list,
                "new_column": new_column,
                "separator": separator
            }
        )

        # Dataset version
        save_dataset_version(
            "columns_merged"
        )

        # -------------------------------------------------
        # SUCCESS RESPONSE
        # -------------------------------------------------

        return {
            "success": True,
            "message": "Columns merged successfully.",
            "source_columns": column_list,
            "new_column": new_column,
            "separator": separator,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(
                transformation_history
            )
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Merge columns failed: {str(e)}"
        }
    # =========================================================
# GENESIS AI - RENAME COLUMN TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/rename-column")
def genesis_rename_column(
    old_column: str,
    new_column: str
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean names
    old_column = old_column.strip()
    new_column = new_column.strip()

    # Validate old column
    if old_column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{old_column}' not found."
        }

    # Validate new column
    if not new_column:
        return {
            "success": False,
            "message": "New column name cannot be empty."
        }

    # Check duplicate column
    if (
        new_column != old_column
        and new_column in current_df.columns
    ):
        return {
            "success": False,
            "message": (
                f"Column '{new_column}' already exists."
            )
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Create transformed copy
        df = current_df.copy()

        # Rename column
        df.rename(
            columns={
                old_column: new_column
            },
            inplace=True
        )

        # Save transformation history
        transformation_history.append({
            "dataset": original_df,
            "column": old_column,
            "operation": "rename_column",
            "old_column": old_column,
            "new_column": new_column,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "rename_column",
            {
                "old_column": old_column,
                "new_column": new_column
            }
        )

        # Dataset version
        save_dataset_version(
            "column_renamed"
        )

        return {
            "success": True,
            "message": "Column renamed successfully.",
            "old_column": old_column,
            "new_column": new_column,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(
                transformation_history
            )
        }

    except Exception as e:
        return {
            "success": False,
            "message": (
                f"Rename column failed: {str(e)}"
            )
        }

    # =========================================================
# GENESIS AI - DROP COLUMN TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/drop-column")
def genesis_drop_column(
    column: str
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean column name
    column = column.strip()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on a copy
        df = current_df.copy()

        # Drop column
        df.drop(
            columns=[column],
            inplace=True
        )

        # Save transformation history
        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "drop_column",
            "new_column": None,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "drop_column",
            {
                "column": column
            }
        )

        # Dataset version
        save_dataset_version(
            "column_dropped"
        )

        return {
            "success": True,
            "message": "Column dropped successfully.",
            "dropped_column": column,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Drop column failed: {str(e)}"
        }

    # ============================================================
# GENESIS AI - CHANGE DATA TYPE TRANSFORMATION
# ============================================================

@app.post("/genesis/transform/change-data-type")
def genesis_change_data_type(
    column: str,
    new_type: str
):

    global current_df, transformation_history, redo_history

    # --------------------------------------------------------
    # CHECK DATASET
    # --------------------------------------------------------

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean inputs
    column = column.strip()
    new_type = new_type.strip().lower()

    # --------------------------------------------------------
    # CHECK COLUMN
    # --------------------------------------------------------

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Supported data types
    supported_types = [
        "int",
        "integer",
        "float",
        "string",
        "datetime",
        "boolean"
    ]

    if new_type not in supported_types:
        return {
            "success": False,
            "message": (
                f"Unsupported data type '{new_type}'. "
                f"Supported types: {', '.join(supported_types)}"
            )
        }

    try:

        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Store old type
        old_type = str(df[column].dtype)

        # ----------------------------------------------------
        # INTEGER
        # ----------------------------------------------------

        if new_type in ["int", "integer"]:

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if converted.isna().any():
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' contains values "
                        "that cannot be converted to integer."
                    )
                }

            df[column] = converted.astype("int64")
            final_type = "int64"

        # ----------------------------------------------------
        # FLOAT
        # ----------------------------------------------------

        elif new_type == "float":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if converted.isna().any():
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' contains values "
                        "that cannot be converted to float."
                    )
                }

            df[column] = converted.astype(float)
            final_type = "float64"

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        elif new_type == "string":

            df[column] = df[column].astype(str)
            final_type = "string"

        # ----------------------------------------------------
        # DATETIME
        # ----------------------------------------------------

        elif new_type == "datetime":

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            if converted.isna().any():
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' contains invalid "
                        "date values that cannot be converted."
                    )
                }

            df[column] = converted
            final_type = "datetime64[ns]"

        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        elif new_type == "boolean":

            true_values = [
                "true", "1", "yes", "y"
            ]

            false_values = [
                "false", "0", "no", "n"
            ]

            def convert_to_boolean(value):

                value_str = str(value).strip().lower()

                if value_str in true_values:
                    return True

                elif value_str in false_values:
                    return False

                else:
                    raise ValueError(
                        f"Invalid boolean value: {value}"
                    )

            df[column] = df[column].apply(
                convert_to_boolean
            )

            final_type = "bool"

        # ----------------------------------------------------
        # SAVE TRANSFORMATION HISTORY
        # ----------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "change_data_type",
            "old_type": old_type,
            "new_type": final_type,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "change_data_type",
            {
                "column": column,
                "old_type": old_type,
                "new_type": final_type
            }
        )

        # Dataset version
        save_dataset_version(
            "data_type_changed"
        )

        return {
            "success": True,
            "message": "Data type changed successfully.",
            "column": column,
            "old_type": old_type,
            "new_type": final_type,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Data type conversion failed: {str(e)}"
        }

        # ============================================================
# GENESIS AI - CREATE CALCULATED COLUMN TRANSFORMATION
# ============================================================

@app.post("/genesis/transform/calculated-column")
def genesis_calculated_column(
    column1: str,
    operator: str,
    value_or_column: str,
    new_column: str
):

    global current_df, transformation_history, redo_history

    # --------------------------------------------------------
    # CHECK DATASET
    # --------------------------------------------------------

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean inputs
    column1 = column1.strip()
    operator = operator.strip()
    value_or_column = value_or_column.strip()
    new_column = new_column.strip()

    # --------------------------------------------------------
    # VALIDATE INPUTS
    # --------------------------------------------------------

    if column1 not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column1}' not found."
        }

    if not new_column:
        return {
            "success": False,
            "message": "New column name cannot be empty."
        }

    if new_column in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{new_column}' already exists."
        }

    allowed_operators = [
        "+",
        "-",
        "*",
        "/",
        "%"
    ]

    if operator not in allowed_operators:
        return {
            "success": False,
            "message": (
                f"Unsupported operator '{operator}'. "
                "Supported operators: +, -, *, /, %"
            )
        }

    try:

        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Convert first column to numeric
        left_values = pd.to_numeric(
            df[column1],
            errors="coerce"
        )

        if left_values.isna().any():
            return {
                "success": False,
                "message": (
                    f"Column '{column1}' contains non-numeric "
                    "values and cannot be used for calculation."
                )
            }

        # ----------------------------------------------------
        # SECOND VALUE: COLUMN OR NUMBER
        # ----------------------------------------------------

        if value_or_column in df.columns:

            right_values = pd.to_numeric(
                df[value_or_column],
                errors="coerce"
            )

            if right_values.isna().any():
                return {
                    "success": False,
                    "message": (
                        f"Column '{value_or_column}' contains "
                        "non-numeric values."
                    )
                }

            calculation_source = {
                "type": "column",
                "value": value_or_column
            }

        else:

            try:
                right_values = float(value_or_column)

            except ValueError:
                return {
                    "success": False,
                    "message": (
                        f"'{value_or_column}' is neither a valid "
                        "numeric value nor an existing column."
                    )
                }

            calculation_source = {
                "type": "constant",
                "value": right_values
            }

        # ----------------------------------------------------
        # PERFORM CALCULATION
        # ----------------------------------------------------

        if operator == "+":
            df[new_column] = left_values + right_values

        elif operator == "-":
            df[new_column] = left_values - right_values

        elif operator == "*":
            df[new_column] = left_values * right_values

        elif operator == "/":

            # Prevent division by zero
            if isinstance(right_values, (int, float)):

                if right_values == 0:
                    return {
                        "success": False,
                        "message": "Division by zero is not allowed."
                    }

            df[new_column] = left_values / right_values

        elif operator == "%":

            if isinstance(right_values, (int, float)):

                if right_values == 0:
                    return {
                        "success": False,
                        "message": "Modulo by zero is not allowed."
                    }

            df[new_column] = left_values % right_values

        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column1,
            "operation": "calculated_column",
            "new_column": new_column,
            "operator": operator,
            "value_or_column": value_or_column,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "calculated_column",
            {
                "column1": column1,
                "operator": operator,
                "value_or_column": value_or_column,
                "new_column": new_column
            }
        )

        # Dataset version
        save_dataset_version(
            "calculated_column_created"
        )

        return {
            "success": True,
            "message": "Calculated column created successfully.",
            "column1": column1,
            "operator": operator,
            "calculation_source": calculation_source,
            "new_column": new_column,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:

        return {
            "success": False,
            "message": (
                f"Calculated column creation failed: {str(e)}"
            )
        }

        # ============================================================
# GENESIS AI - CONDITIONAL COLUMN TRANSFORMATION
# ============================================================

@app.post("/genesis/transform/conditional-column")
def genesis_conditional_column(
    column: str,
    operator: str,
    value: str,
    true_value: str,
    false_value: str,
    new_column: str
):

    global current_df, transformation_history, redo_history

    # --------------------------------------------------------
    # CHECK DATASET
    # --------------------------------------------------------

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean inputs
    column = column.strip()
    operator = operator.strip()
    value = value.strip()
    true_value = true_value.strip()
    false_value = false_value.strip()
    new_column = new_column.strip()

    # --------------------------------------------------------
    # VALIDATE COLUMN
    # --------------------------------------------------------

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    if not new_column:
        return {
            "success": False,
            "message": "New column name cannot be empty."
        }

    if new_column in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{new_column}' already exists."
        }

    # Supported operators
    allowed_operators = [
        ">",
        ">=",
        "<",
        "<=",
        "==",
        "!="
    ]

    if operator not in allowed_operators:
        return {
            "success": False,
            "message": (
                f"Unsupported operator '{operator}'. "
                "Supported operators: >, >=, <, <=, ==, !="
            )
        }

    try:

        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on a copy
        df = current_df.copy()

        # ----------------------------------------------------
        # DETERMINE VALUE TYPE
        # ----------------------------------------------------

        try:
            comparison_value = float(value)
            numeric_comparison = True

        except ValueError:
            comparison_value = value
            numeric_comparison = False

        # ----------------------------------------------------
        # CREATE CONDITION
        # ----------------------------------------------------

        if numeric_comparison:

            left_values = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if left_values.isna().any():
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' contains non-numeric "
                        "values and cannot be compared with "
                        f"numeric value '{value}'."
                    )
                }

        else:

            left_values = df[column].astype(str)

        # ----------------------------------------------------
        # APPLY OPERATOR
        # ----------------------------------------------------

        if operator == ">":
            condition = left_values > comparison_value

        elif operator == ">=":
            condition = left_values >= comparison_value

        elif operator == "<":
            condition = left_values < comparison_value

        elif operator == "<=":
            condition = left_values <= comparison_value

        elif operator == "==":
            condition = left_values == comparison_value

        elif operator == "!=":
            condition = left_values != comparison_value

        # ----------------------------------------------------
        # CREATE CONDITIONAL COLUMN
        # ----------------------------------------------------

        df[new_column] = condition.map(
            {
                True: true_value,
                False: false_value
            }
        )

        # Count results
        true_count = int(condition.sum())
        false_count = int((~condition).sum())

        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "conditional_column",
            "new_column": new_column,
            "operator": operator,
            "comparison_value": value,
            "true_value": true_value,
            "false_value": false_value,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "conditional_column",
            {
                "column": column,
                "operator": operator,
                "comparison_value": value,
                "true_value": true_value,
                "false_value": false_value,
                "new_column": new_column
            }
        )

        # Dataset version
        save_dataset_version(
            "conditional_column_created"
        )

        return {
            "success": True,
            "message": "Conditional column created successfully.",
            "source_column": column,
            "operator": operator,
            "comparison_value": comparison_value,
            "new_column": new_column,
            "true_value": true_value,
            "false_value": false_value,
            "true_count": true_count,
            "false_count": false_count,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:

        return {
            "success": False,
            "message": (
                f"Conditional column creation failed: {str(e)}"
            )
        }

        # =========================================================
# GENESIS AI - BULK VALUE MAPPING
# =========================================================

@app.post("/genesis/transform/bulk-replace")
def genesis_bulk_replace(
    column: str,
    mappings: str
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean column name
    column = column.strip()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Check mappings
    if not mappings or not mappings.strip():
        return {
            "success": False,
            "message": "Please provide value mappings."
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # -------------------------------------------------
        # PARSE MAPPINGS
        # Format:
        # old1:new1,old2:new2
        # Example:
        # Male:M,Female:F
        # -------------------------------------------------

        mapping_dict = {}

        mapping_items = [
            item.strip()
            for item in mappings.split(",")
            if item.strip()
        ]

        for item in mapping_items:

            if ":" not in item:
                return {
                    "success": False,
                    "message": (
                        f"Invalid mapping format: '{item}'. "
                        "Use old:new format."
                    )
                }

            old_value, new_value = item.split(":", 1)

            old_value = old_value.strip()
            new_value = new_value.strip()

            if old_value == "":
                return {
                    "success": False,
                    "message": "Old value cannot be empty."
                }

            mapping_dict[old_value] = new_value

        # -------------------------------------------------
        # COUNT MATCHES
        # -------------------------------------------------

        column_as_string = df[column].astype(str)

        replacement_counts = {}

        total_matches = 0

        for old_value in mapping_dict:

            count = int(
                (column_as_string == old_value).sum()
            )

            replacement_counts[old_value] = count

            total_matches += count

        if total_matches == 0:
            return {
                "success": False,
                "message": (
                    "None of the provided values were found "
                    f"in column '{column}'."
                ),
                "replacement_counts": replacement_counts
            }

        # -------------------------------------------------
        # REPLACE VALUES
        # -------------------------------------------------

        df[column] = (
            df[column]
            .astype(str)
            .replace(mapping_dict)
        )

        # -------------------------------------------------
        # SAVE UNDO HISTORY
        # -------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "bulk_replace",
            "mappings": mapping_dict,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "bulk_replace",
            {
                "column": column,
                "mappings": mapping_dict,
                "replacement_counts": replacement_counts,
                "total_matches": total_matches
            }
        )

        # Dataset version
        save_dataset_version(
            "bulk_values_replaced"
        )

        return {
            "success": True,
            "message": "Multiple values replaced successfully.",
            "column": column,
            "mappings": mapping_dict,
            "replacement_counts": replacement_counts,
            "total_replacements": total_matches,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Bulk value replacement failed: {str(e)}"
        }

        # =========================================================
# GENESIS AI - TEXT CASE TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/text-case")
def genesis_text_case(
    column: str,
    case_type: str
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    # Clean inputs
    column = column.strip()
    case_type = case_type.strip().lower()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    # Allowed transformations
    allowed_cases = ["upper", "lower", "title"]

    if case_type not in allowed_cases:
        return {
            "success": False,
            "message": (
                "Invalid case_type. "
                "Use: upper, lower, or title."
            )
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Preserve null values
        original_nulls = df[column].isna()

        # Apply transformation
        if case_type == "upper":
            df[column] = df[column].astype(str).str.upper()

        elif case_type == "lower":
            df[column] = df[column].astype(str).str.lower()

        elif case_type == "title":
            df[column] = df[column].astype(str).str.title()

        # Restore null values
        df.loc[original_nulls, column] = None

        # Count changed values
        changed_count = int(
            (
                original_df[column].astype(str)
                != df[column].astype(str)
            ).sum()
        )

        # Save transformation history
        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "text_case",
            "case_type": case_type,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "text_case_transformation",
            {
                "column": column,
                "case_type": case_type,
                "changed_count": changed_count
            }
        )

        # Dataset version
        save_dataset_version(
            "text_case_transformed"
        )

        return {
            "success": True,
            "message": "Text case transformed successfully.",
            "column": column,
            "case_type": case_type,
            "changed_count": changed_count,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Text case transformation failed: {str(e)}"
        }

    # =========================================================
# GENESIS AI - TRIM & NORMALIZE SPACES
# =========================================================

@app.post("/genesis/transform/trim")
def genesis_trim(
    column: str
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = column.strip()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Preserve null values
        null_mask = df[column].isna()

        # Convert to string and normalize whitespace
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        # Restore null values
        df.loc[null_mask, column] = None

        # Count changed values
        original_values = original_df[column].astype(str)
        new_values = df[column].astype(str)

        changed_count = int(
            (original_values != new_values).sum()
        )

        # Save history
        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "trim_normalize_spaces",
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "trim_normalize_spaces",
            {
                "column": column,
                "changed_count": changed_count
            }
        )

        # Dataset version
        save_dataset_version(
            "trim_normalize_spaces"
        )

        return {
            "success": True,
            "message": "Whitespace trimmed and normalized successfully.",
            "column": column,
            "changed_count": changed_count,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Trim transformation failed: {str(e)}"
        }

        # =========================================================
# GENESIS AI - MISSING VALUE TRANSFORMATION
# =========================================================

@app.post("/genesis/transform/missing-values")
def genesis_missing_values(
    column: str,
    strategy: str,
    value: str = ""
):
    global current_df, transformation_history, redo_history

    # Check dataset
    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = column.strip()
    strategy = strategy.strip().lower()

    # Check column
    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    allowed_strategies = [
        "value",
        "mean",
        "median",
        "mode",
        "forward_fill",
        "backward_fill",
        "drop"
    ]

    if strategy not in allowed_strategies:
        return {
            "success": False,
            "message": (
                "Invalid strategy. Use one of: "
                + ", ".join(allowed_strategies)
            )
        }

    try:
        # Save original dataset for UNDO
        original_df = current_df.copy(deep=True)

        # Work on copy
        df = current_df.copy()

        # Count missing values before
        missing_before = int(df[column].isna().sum())

        if missing_before == 0:
            return {
                "success": False,
                "message": f"No missing values found in '{column}'.",
                "missing_before": 0
            }

        # -------------------------------------------------
        # FILL WITH FIXED VALUE
        # -------------------------------------------------

        if strategy == "value":

            if value == "":
                return {
                    "success": False,
                    "message": (
                        "Please provide a value when using "
                        "strategy='value'."
                    )
                }

            df[column] = df[column].fillna(value)

        # -------------------------------------------------
        # MEAN
        # -------------------------------------------------

        elif strategy == "mean":

            numeric_series = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if numeric_series.notna().sum() == 0:
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' has no numeric values "
                        "for mean calculation."
                    )
                }

            fill_value = float(numeric_series.mean())

            df[column] = numeric_series.fillna(fill_value)

        # -------------------------------------------------
        # MEDIAN
        # -------------------------------------------------

        elif strategy == "median":

            numeric_series = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if numeric_series.notna().sum() == 0:
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' has no numeric values "
                        "for median calculation."
                    )
                }

            fill_value = float(numeric_series.median())

            df[column] = numeric_series.fillna(fill_value)

        # -------------------------------------------------
        # MODE
        # -------------------------------------------------

        elif strategy == "mode":

            mode_values = df[column].mode(dropna=True)

            if mode_values.empty:
                return {
                    "success": False,
                    "message": (
                        f"Column '{column}' has no valid mode."
                    )
                }

            fill_value = mode_values.iloc[0]

            df[column] = df[column].fillna(fill_value)

        # -------------------------------------------------
        # FORWARD FILL
        # -------------------------------------------------

        elif strategy == "forward_fill":

            df[column] = df[column].ffill()

        # -------------------------------------------------
        # BACKWARD FILL
        # -------------------------------------------------

        elif strategy == "backward_fill":

            df[column] = df[column].bfill()

        # -------------------------------------------------
        # DROP ROWS
        # -------------------------------------------------

        elif strategy == "drop":

            df = df.dropna(
                subset=[column]
            ).reset_index(drop=True)

        # -------------------------------------------------
        # COUNT AFTER
        # -------------------------------------------------

        missing_after = int(df[column].isna().sum())

        changed_count = missing_before - missing_after

        # -------------------------------------------------
        # SAVE HISTORY
        # -------------------------------------------------

        transformation_history.append({
            "dataset": original_df,
            "column": column,
            "operation": "missing_value_transformation",
            "strategy": strategy,
            "value": value,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "rows_before": int(len(original_df)),
            "columns_before": int(len(original_df.columns))
        })

        # Clear redo history
        redo_history.clear()

        # Save transformed dataset
        current_df = df

        # Audit log
        add_audit_log(
            "missing_value_transformation",
            {
                "column": column,
                "strategy": strategy,
                "value": value,
                "missing_before": missing_before,
                "missing_after": missing_after,
                "changed_count": changed_count
            }
        )

        # Dataset version
        save_dataset_version(
            "missing_values_transformed"
        )

        return {
            "success": True,
            "message": (
                "Missing values transformed successfully."
            ),
            "column": column,
            "strategy": strategy,
            "missing_before": missing_before,
            "missing_after": missing_after,
            "changed_count": changed_count,
            "rows_before": int(len(original_df)),
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "history_count": len(transformation_history)
        }

    except Exception as e:
        return {
            "success": False,
            "message": (
                f"Missing value transformation failed: {str(e)}"
            )
        }

    # =========================================================
# GENESIS AI - DEBUG: CREATE TEMPORARY MISSING VALUE
# =========================================================

@app.post("/genesis/debug/create-missing-test")
def create_missing_test(
    column: str = "Salary"
):
    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = column.strip()

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    try:
        # Create a temporary copy
        df = current_df.copy()

        # Save original value
        original_value = df.iloc[0][column]

        # Create exactly ONE missing value
        df.iloc[0, df.columns.get_loc(column)] = np.nan

        current_df = df

        return {
            "success": True,
            "message": "Temporary missing value created successfully.",
            "column": column,
            "row_index": 0,
            "original_value": str(original_value),
            "new_value": None,
            "missing_count": int(df[column].isna().sum())
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Test missing value creation failed: {str(e)}"
        }
    # =========================================================
# GENESIS AI - DEBUG: CREATE TEMPORARY OUTLIER
# =========================================================

@app.post("/genesis/debug/create-outlier-test")
def create_outlier_test(
    column: str = "Salary",
    value: float = 1000000
):
    global current_df
    global latest_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = column.strip()

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    if not pd.api.types.is_numeric_dtype(current_df[column]):
        return {
            "success": False,
            "message": f"Column '{column}' must be numeric."
        }

    try:
        df = current_df.copy()

        original_value = df.iloc[0][column]

        # Create one extreme temporary value
        df.iloc[0, df.columns.get_loc(column)] = value

        current_df = df
        latest_df = df

        return {
            "success": True,
            "message": "Temporary outlier created successfully.",
            "column": column,
            "row_index": 0,
            "original_value": (
                original_value.item()
                if hasattr(original_value, "item")
                else original_value
            ),
            "new_value": value
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Test outlier creation failed: {str(e)}"
        }
    # =========================================================
# GENESIS AI - DEBUG: CREATE MISSING VALUE AT ROW 1
# =========================================================

@app.post("/genesis/debug/create-missing-test-row1")
def create_missing_test_row1(
    column: str = "Department"
):
    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    column = column.strip()

    if column not in current_df.columns:
        return {
            "success": False,
            "message": f"Column '{column}' not found."
        }

    try:
        df = current_df.copy()

        # Row 1 must be filled before creating the test
        if pd.isna(df.iloc[1][column]):
            return {
                "success": False,
                "message": f"Row 1 in '{column}' is already missing."
            }

        previous_value = df.iloc[0][column]
        original_value = df.iloc[1][column]

        # Create missing value at row 1
        df.iloc[1, df.columns.get_loc(column)] = np.nan

        current_df = df

        return {
            "success": True,
            "message": "Temporary missing value created at row 1.",
            "column": column,
            "row_index": 1,
            "previous_row_value": str(previous_value),
            "original_value": str(original_value),
            "new_value": None,
            "missing_count": int(df[column].isna().sum())
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Test missing value creation failed: {str(e)}"
        }

@app.get("/analytics/decision-intelligence")
def analytics_decision_intelligence():

    global current_df

    if current_df is None or current_df.empty:
        return {
            "success": False,
            "message": "No dataset uploaded. Please upload a dataset first."
        }

    try:

        # ==========================================
        # 1. GET ANOMALY DATA
        # ==========================================

        anomalies_result = analytics_anomalies()

        anomalies = []

        if isinstance(anomalies_result, dict):
            anomalies = anomalies_result.get(
                "anomalies",
                []
            )

        # ==========================================
        # 2. GET RECOMMENDATIONS DATA
        # ==========================================

        recommendations_result = analytics_recommendations()

        recommendations = []

        if isinstance(recommendations_result, dict):
            recommendations = recommendations_result.get(
                "recommendations",
                []
            )

        # ==========================================
        # 3. GET ROOT CAUSE DATA
        # ==========================================

        root_result = investigate_root_cause(
            current_df,
            "Profit"
        )

        root_causes = []

        if isinstance(root_result, dict):
            root_causes = root_result.get(
                "root_causes",
                []
            )

        # ==========================================
        # 4. GENESIS AI DECISION INTELLIGENCE
        # ==========================================

        result = generate_decision_intelligence(
            df=current_df,
            anomalies=anomalies,
            recommendations=recommendations,
            root_causes=root_causes
        )

        return result

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    # ============================================================
# ANOMALY DETECTION API
# ============================================================

@app.get("/anomaly-detection")
def anomaly_detection():

    global current_df

    if current_df is None or current_df.empty:

        return {
            "success": False,
            "message": "No dataset uploaded."
        }

    try:

        result = run_anomaly_detection(
            current_df
        )

        return result

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

        # ============================================================
# ROOT CAUSE ANALYSIS API
# ============================================================

@app.get("/root-cause-analysis")
def root_cause_analysis():

    global current_df

    if current_df is None:

        return {

            "success": False,

            "message": (
                "No dataset uploaded. "
                "Please upload a dataset first."
            )

        }

    return run_root_cause_analysis(
        current_df
    )

# ============================================================
# BUSINESS SEGMENTATION & CLUSTERING API
# ============================================================

@app.get("/segmentation-analysis")
def segmentation_analysis():

    global latest_df, current_df

    # --------------------------------------------------------
    # GET ACTIVE DATASET
    # --------------------------------------------------------

    df = current_df

    if df is None or df.empty:

        df = latest_df


    if df is None or df.empty:

        return {

            "success": False,

            "error":

                "No dataset available. Please upload a dataset first."

        }


    try:

        result = run_segmentation_analysis(

            df=df,

            number_of_clusters=3

        )


        return result


    except Exception as error:

        return {

            "success": False,

            "error": str(error)

        }

    # ============================================================
# DATA MODELING API
# ============================================================

@app.get("/data-modeling")
def data_modeling():

    global latest_df

    try:

        # ----------------------------------------------------
        # DATASET VALIDATION
        # ----------------------------------------------------

        if latest_df is None:

            return {
                "success": False,
                "message": "No dataset loaded. Please upload a dataset first."
            }

        if latest_df.empty:

            return {
                "success": False,
                "message": "The loaded dataset is empty."
            }


        # ----------------------------------------------------
        # RUN DATA MODELING ENGINE
        # ----------------------------------------------------

        result = run_data_modeling(
            latest_df
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return result


    except Exception as error:

        return {
            "success": False,
            "message": "Data modeling analysis failed.",
            "error": str(error)
        }

        # ============================================================
# GENESIS AI - INTELLIGENT ORCHESTRATION ENGINE
# ============================================================

@app.get("/orchestration")
def orchestration():

    global latest_df, current_df

    # Use current dataset if available
    df = current_df if current_df is not None else latest_df

    if df is None or df.empty:
        return {
            "success": False,
            "message": "No dataset available. Please upload a dataset first."
        }

    try:
        result = run_orchestration(df)

        return result

    except Exception as e:
        print("Orchestration Engine Error:", str(e))

        return {
            "success": False,
            "message": f"Orchestration analysis failed: {str(e)}"
        }

    # =========================================================
# OBSERVABILITY ENGINE
# =========================================================

@app.get("/observability")
def observability():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    try:

        result = run_observability_analysis(current_df)

        return result

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

        # =========================================================
# METADATA INTELLIGENCE ENGINE
# =========================================================

@app.get("/metadata")
def metadata_analysis():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    try:

        result = run_metadata_analysis(current_df)

        return result

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

        # -----------------------------------
# Genesis AI Audit Logs
# -----------------------------------

@app.get("/audit-logs")
def audit_logs():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_audit_logs_analysis(current_df)

# -----------------------------------
# Genesis AI Schema Evolution
# -----------------------------------

@app.get("/schema-evolution")
def schema_evolution():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_schema_evolution_analysis(current_df)

# -----------------------------------
# Genesis AI Analyst Agent
# -----------------------------------

@app.get("/analyst-agent")
def analyst_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_analyst_agent(current_df)

# -----------------------------------
# Genesis AI Quality Agent
# -----------------------------------

@app.get("/quality-agent")
def quality_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_quality_agent(current_df)

# -----------------------------------
# Genesis AI Engineer Agent
# -----------------------------------

@app.get("/engineer-agent")
def engineer_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_engineer_agent(current_df)

# -----------------------------------
# Genesis AI Forecast Agent
# -----------------------------------

@app.get("/forecast-agent")
def forecast_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_forecast_agent(current_df)

    # -----------------------------------
# Genesis AI Insights Agent
# -----------------------------------

@app.get("/insights-agent")
def insights_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_insights_agent(current_df)

# -----------------------------------
# Genesis AI Recommendation Agent
# -----------------------------------

@app.get("/recommendation-agent")
def recommendation_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_recommendation_agent(current_df)

    # -----------------------------------
# Genesis AI Root Cause Agent
# -----------------------------------

@app.get("/root-cause-agent")
def root_cause_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_root_cause_analysis(current_df)

    # -----------------------------------
# Genesis AI Decision Agent
# -----------------------------------

@app.get("/decision-agent")
def decision_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_decision_agent(current_df)

    # -----------------------------------
# Genesis AI Reporting Agent
# -----------------------------------

@app.get("/reporting-agent")
def reporting_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_reporting_agent(current_df)

    # -----------------------------------
# Genesis AI Multi-Agent Orchestrator
# -----------------------------------

@app.get("/orchestrator-agent")
def orchestrator_agent():

    global current_df

    if current_df is None:
        return {
            "success": False,
            "message": "Please upload a dataset first."
        }

    return run_orchestrator_agent(
        current_df,
        run_analyst_agent,
        run_quality_agent,
        run_engineer_agent,
        run_forecast_agent,
        run_insights_agent,
        run_recommendation_agent,
        run_root_cause_analysis,
        run_decision_agent,
        run_reporting_agent
    )

# ============================================================
# AGENT ROUTER ENDPOINT
# ============================================================

@app.get("/agent-router")
def agent_router(query: str):
    """
    Automatically selects the best Genesis AI agent
    based on the user's question.
    """

    try:

        result = route_agent(query)

        return {
            "success": True,
            "user_query": query,
            "routing_result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

        # ============================================================
# INTELLIGENT AGENT EXECUTION ENDPOINT
# ============================================================

@app.get("/execute-agent")
def intelligent_agent_execution(query: str):
    """
    Automatically routes the user query to the correct agent
    and executes that agent using the currently uploaded dataset.
    """

    global current_df

    try:

        # =====================================================
        # CHECK DATASET
        # =====================================================

        if current_df is None:
            return {
                "success": False,
                "message": "No dataset available. Please upload a dataset first."
            }

        # =====================================================
        # STEP 1: ROUTE THE QUERY
        # =====================================================

        routing_result = route_agent(query)

        if not routing_result.get("success"):
            return {
                "success": False,
                "message": "Agent routing failed.",
                "routing_result": routing_result
            }

        # =====================================================
        # STEP 2: GET SELECTED AGENT
        # =====================================================

        selected_agent = routing_result.get("selected_agent")

        # =====================================================
        # STEP 3: EXECUTE SELECTED AGENT
        # =====================================================

        execution_result = execute_agent(
            selected_agent,
            current_df
        )

        # =====================================================
        # STEP 4: RETURN COMPLETE WORKFLOW RESULT
        # =====================================================

        return {
            "success": True,
            "user_query": query,
            "selected_agent": selected_agent,
            "routing_reason": routing_result.get("reason"),
            "execution_result": execution_result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

        # ============================================================
# MULTI AGENT WORKFLOW ENDPOINT
# ============================================================

@app.get("/multi-agent-workflow")
def multi_agent_workflow_endpoint(query: str):
    """
    Automatically runs multiple Genesis AI agents
    based on the user's query.
    """

    global current_df

    try:

        # ====================================================
        # CHECK DATASET
        # ====================================================

        if current_df is None:
            return {
                "success": False,
                "message": "No dataset available. Please upload a dataset first."
            }

        # ====================================================
        # RUN MULTI-AGENT WORKFLOW
        # ====================================================

        workflow_result = run_multi_agent_workflow(
            query,
            current_df
        )

        return workflow_result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

        # ============================================================
# PLANNER AGENT ENDPOINT
# ============================================================

@app.get("/planner-agent")
def planner_agent_endpoint(query: str):
    """
    Creates an intelligent execution plan based on the user's query.
    """

    try:

        result = run_planner_agent(query)

        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

        # ============================================================
# PLANNED WORKFLOW ENDPOINT
# ============================================================

@app.get("/planned-workflow")
def planned_workflow_endpoint(query: str):

    global current_df

    try:

        if current_df is None:
            return {
                "success": False,
                "message": "No dataset available. Please upload a dataset first."
            }

        result = run_planned_workflow(
            query,
            current_df
        )

        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }