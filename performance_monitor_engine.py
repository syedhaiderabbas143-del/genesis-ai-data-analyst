# ============================================================
# GENESIS AI - PERFORMANCE MONITORING ENGINE
# ============================================================

import time
from datetime import datetime


# ============================================================
# PERFORMANCE STORAGE
# ============================================================

performance_metrics = {

    "total_requests": 0,

    "slow_requests": 0,

    "total_execution_time": 0.0,

    "last_execution_time": 0.0,

    "last_updated": None

}


# ============================================================
# RECORD PERFORMANCE
# ============================================================

def record_performance(
    execution_time,
    slow_threshold=2.0
):

    global performance_metrics

    performance_metrics[
        "total_requests"
    ] += 1

    performance_metrics[
        "total_execution_time"
    ] += execution_time

    performance_metrics[
        "last_execution_time"
    ] = round(
        execution_time,
        4
    )

    performance_metrics[
        "last_updated"
    ] = datetime.now().isoformat()

    # --------------------------------------------------------
    # SLOW REQUEST DETECTION
    # --------------------------------------------------------

    if execution_time > slow_threshold:

        performance_metrics[
            "slow_requests"
        ] += 1


# ============================================================
# PERFORMANCE TIMER
# ============================================================

class PerformanceTimer:

    def __init__(self):

        self.start_time = None


    def start(self):

        self.start_time = time.time()


    def stop(self):

        if self.start_time is None:

            return 0.0

        execution_time = (
            time.time()
            - self.start_time
        )

        record_performance(
            execution_time
        )

        return round(
            execution_time,
            4
        )


# ============================================================
# GET PERFORMANCE SUMMARY
# ============================================================

def get_performance_summary():

    total_requests = performance_metrics[
        "total_requests"
    ]

    total_execution_time = performance_metrics[
        "total_execution_time"
    ]

    # --------------------------------------------------------
    # AVERAGE EXECUTION TIME
    # --------------------------------------------------------

    if total_requests > 0:

        average_execution_time = round(

            total_execution_time
            / total_requests,

            4

        )

    else:

        average_execution_time = 0.0


    # --------------------------------------------------------
    # PERFORMANCE STATUS
    # --------------------------------------------------------

    if average_execution_time < 1:

        performance_status = "Excellent"

    elif average_execution_time < 2:

        performance_status = "Healthy"

    elif average_execution_time < 5:

        performance_status = "Warning"

    else:

        performance_status = "Critical"


    return {

        "success": True,

        "performance_status": performance_status,

        "total_requests": total_requests,

        "slow_requests": performance_metrics[
            "slow_requests"
        ],

        "average_execution_time_seconds": (
            average_execution_time
        ),

        "last_execution_time_seconds": performance_metrics[
            "last_execution_time"
        ],

        "last_updated": performance_metrics[
            "last_updated"
        ]

    }


# ============================================================
# RESET PERFORMANCE METRICS
# ============================================================

def reset_performance_metrics():

    global performance_metrics

    performance_metrics = {

        "total_requests": 0,

        "slow_requests": 0,

        "total_execution_time": 0.0,

        "last_execution_time": 0.0,

        "last_updated": datetime.now().isoformat()

    }


    return {

        "success": True,

        "message": (
            "Performance metrics "
            "successfully reset."
        )

    }