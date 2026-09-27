import pandas as pd
from typing import Dict, Any, List

from services import engine_registry


class OrchestrationEngine:
    """
    Genesis AI Orchestration Engine

    This engine intelligently decides which analytics engines
    should run based on the uploaded dataset.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze_dataset(self) -> Dict[str, Any]:
        """
        Analyze dataset structure and determine the recommended
        execution workflow.
        """

        if self.df is None or self.df.empty:
            return {
                "success": False,
                "message": "No dataset available for orchestration."
            }

        total_rows = len(self.df)
        total_columns = len(self.df.columns)

        numeric_columns = self.df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = self.df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        missing_values = int(self.df.isnull().sum().sum())

        duplicate_rows = int(self.df.duplicated().sum())

        workflow = self._build_workflow(
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            missing_values=missing_values,
            duplicate_rows=duplicate_rows
        )

        execution_results = self._execute_workflow(workflow)

        return {
            "success": True,
            "analysis_type": "Genesis AI Intelligent Orchestration",
            "dataset_summary": {
                "total_rows": total_rows,
                "total_columns": total_columns,
                "numeric_columns": len(numeric_columns),
                "categorical_columns": len(categorical_columns),
                "missing_values": missing_values,
                "duplicate_rows": duplicate_rows
            },
            "recommended_workflow": workflow,
            "total_recommended_steps": len(workflow),
            "execution_results": execution_results,
            "message": "Intelligent analytics workflow generated successfully."
        }

    def _execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute currently integrated canonical analytics engines."""

        execution_results: Dict[str, Any] = {}

        for step in workflow:
            if step["engine"] == "Correlation Analysis Engine":
                correlation_engine = engine_registry.resolve_engine("correlation")
                execution_results["correlation"] = correlation_engine(self.df)

            if step["engine"] == "Segmentation Engine":
                segmentation_engine = engine_registry.resolve_engine("segmentation")
                execution_results["segmentation"] = segmentation_engine(self.df)

        return execution_results

    def _build_workflow(
        self,
        numeric_columns: List[str],
        categorical_columns: List[str],
        missing_values: int,
        duplicate_rows: int
    ) -> List[Dict[str, Any]]:

        workflow = []

        # Step 1
        workflow.append({
            "step": 1,
            "engine": "Data Quality Engine",
            "priority": "Critical",
            "reason": "Dataset should always be checked for quality issues first."
        })

        # Step 2
        if missing_values > 0 or duplicate_rows > 0:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Data Cleaning Engine",
                "priority": "Critical",
                "reason": (
                    f"Detected {missing_values} missing values and "
                    f"{duplicate_rows} duplicate rows."
                )
            })

        # Step 3
        workflow.append({
            "step": len(workflow) + 1,
            "engine": "Data Profiling Engine",
            "priority": "High",
            "reason": "Understand dataset structure, distributions and column characteristics."
        })

        # Step 4
        if len(numeric_columns) >= 2:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Correlation Analysis Engine",
                "priority": "High",
                "reason": "Multiple numeric columns available for relationship analysis."
            })

        # Step 5
        if len(numeric_columns) >= 1:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Anomaly Detection Engine",
                "priority": "High",
                "reason": "Numeric data available for anomaly and outlier detection."
            })

        # Step 6
        if len(numeric_columns) >= 2:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Root Cause Analysis Engine",
                "priority": "High",
                "reason": "Dataset contains enough numeric information for root cause investigation."
            })

        # Step 7
        if len(categorical_columns) >= 1 and len(numeric_columns) >= 1:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Segmentation Engine",
                "priority": "Medium",
                "reason": "Categorical and numeric features available for segmentation."
            })

        # Step 8
        if len(numeric_columns) >= 2:
            workflow.append({
                "step": len(workflow) + 1,
                "engine": "Data Modeling Engine",
                "priority": "Medium",
                "reason": "Dataset structure supports advanced data modeling analysis."
            })

        # Step 9
        workflow.append({
            "step": len(workflow) + 1,
            "engine": "AI Recommendation Engine",
            "priority": "High",
            "reason": "Generate business recommendations after analytics execution."
        })

        return workflow


def run_orchestration(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Main function used by FastAPI.
    """

    engine = OrchestrationEngine(df)

    return engine.analyze_dataset()

