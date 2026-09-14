# ============================================================
# GENESIS AI - SECURITY VALIDATION ENGINE
# ============================================================

import os
import re


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_FILE_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls"
}


# ============================================================
# MAXIMUM FILE SIZE
# ============================================================

MAX_FILE_SIZE_MB = 100

MAX_FILE_SIZE_BYTES = (
    MAX_FILE_SIZE_MB
    * 1024
    * 1024
)


# ============================================================
# VALIDATE FILE EXTENSION
# ============================================================

def validate_file_extension(filename):

    if not filename:

        return False, "Filename is missing."

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in ALLOWED_FILE_EXTENSIONS:

        return (
            False,
            f"File type '{extension}' is not allowed."
        )

    return True, "File type is allowed."


# ============================================================
# VALIDATE FILE SIZE
# ============================================================

def validate_file_size(file_size):

    if file_size is None:

        return False, "File size is missing."

    if file_size > MAX_FILE_SIZE_BYTES:

        return (
            False,
            f"File size exceeds the maximum limit of "
            f"{MAX_FILE_SIZE_MB} MB."
        )

    return True, "File size is allowed."
# ============================================================
# VALIDATE FILE CONTENT
# ============================================================

def validate_file_content(
    filename,
    file_content
):

    if not filename:

        return False, "Filename is missing."


    if not file_content:

        return False, "Uploaded file is empty."


    extension = os.path.splitext(
        filename
    )[1].lower()


    # --------------------------------------------------------
    # CSV VALIDATION
    # --------------------------------------------------------

    if extension == ".csv":

        try:

            file_content.decode(
                "utf-8"
            )

            return True, "CSV file content is valid."

        except UnicodeDecodeError:

            return False, (
                "Invalid CSV file content."
            )


    # --------------------------------------------------------
    # EXCEL VALIDATION
    # --------------------------------------------------------

    elif extension in [".xlsx", ".xls"]:

        # Basic validation:
        # Excel files should not be empty

        if len(file_content) < 10:

            return False, (
                "Invalid or corrupted Excel file."
            )

        return True, (
            "Excel file content passed basic validation."
        )


    return False, (
        "Unsupported file format."
    )

# ============================================================
# SUSPICIOUS INPUT DETECTION
# ============================================================

def detect_suspicious_input(value):

    if value is None:

        return False, None

    text = str(value).lower()

    suspicious_patterns = [

        r"<script",
        r"javascript:",
        r"../",
        r"..\\",
        r"\bselect\b.*\bfrom\b",
        r"\bdrop\b.*\btable\b",
        r"\bdelete\b.*\bfrom\b",
        r"\binsert\b.*\binto\b",
        r"\bunion\b.*\bselect\b"

    ]

    for pattern in suspicious_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            return True, pattern

    return False, None


# ============================================================
# VALIDATE USER INPUT
# ============================================================

def validate_user_input(value):

    is_suspicious, pattern = (
        detect_suspicious_input(value)
    )

    if is_suspicious:

        return {

            "safe": False,

            "message": (
                "Potentially unsafe input detected."
            ),

            "detected_pattern": pattern

        }

    return {

        "safe": True,

        "message": "Input is safe.",

        "detected_pattern": None

    }


# ============================================================
# COMPLETE SECURITY VALIDATION
# ============================================================

def run_security_validation(
    filename=None,
    file_size=None,
    user_input=None
):

    results = {

        "file_validation": None,

        "input_validation": None

    }


    security_status = "Secure"


    # --------------------------------------------------------
    # FILE VALIDATION
    # --------------------------------------------------------

    if filename:

        extension_valid, extension_message = (
            validate_file_extension(filename)
        )

        size_valid = True

        size_message = (
            "File size was not provided."
        )

        if file_size is not None:

            size_valid, size_message = (
                validate_file_size(file_size)
            )

        results["file_validation"] = {

            "filename": filename,

            "extension_valid": extension_valid,

            "extension_message": extension_message,

            "size_valid": size_valid,

            "size_message": size_message

        }

        if not extension_valid or not size_valid:

            security_status = "Warning"


    # --------------------------------------------------------
    # USER INPUT VALIDATION
    # --------------------------------------------------------

    if user_input is not None:

        input_result = validate_user_input(
            user_input
        )

        results["input_validation"] = input_result

        if not input_result["safe"]:

            security_status = "Warning"


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "success": True,

        "security_status": security_status,

        "allowed_file_extensions": sorted(
            list(ALLOWED_FILE_EXTENSIONS)
        ),

        "maximum_file_size_mb": MAX_FILE_SIZE_MB,

        "validation_results": results

    }