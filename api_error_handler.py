# ============================================================
# GENESIS AI - API ERROR HANDLER
# ============================================================

import logging
from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("genesis_api_errors")


# ============================================================
# SAFE ERROR RESPONSE
# ============================================================

def create_safe_error_response(
    error,
    status_code=500
):

    error_id = datetime.now().strftime(
        "ERR_%Y%m%d_%H%M%S"
    )

    # Log full error internally
    logger.exception(
        "Error ID: %s | Error: %s",
        error_id,
        str(error)
    )

    return JSONResponse(

        status_code=status_code,

        content={

            "success": False,

            "error_id": error_id,

            "message": (
                "An internal error occurred. "
                "Please try again later."
            )

        }

    )


# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

async def global_exception_handler(
    request: Request,
    exc: Exception
):

    error_id = datetime.now().strftime(
        "ERR_%Y%m%d_%H%M%S"
    )

    logger.exception(

        "Unhandled API Error | "
        "Error ID: %s | "
        "Path: %s | "
        "Error: %s",

        error_id,

        request.url.path,

        str(exc)

    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "error_id": error_id,

            "message": (
                "An unexpected server error occurred. "
                "The error has been logged."
            )

        }

    )