import os
import uuid
import re
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ==========================================================
# COLUMN ALIASES
# ==========================================================

COLUMN_ALIASES = {

    "Employee Name": [
        "employee",
        "employees",
        "employee name",
        "name",
        "staff",
        "person"
    ],

    "Age": [
        "age",
        "ages"
    ],

    "Department": [
        "department",
        "departments",
        "dept",
        "team"
    ],

    "Salary": [
        "salary",
        "salaries",
        "income",
        "pay",
        "ctc",
        "package",
        "wage"
    ],

    "Experience": [
        "experience",
        "exp",
        "years"
    ],

    "City": [
        "city",
        "cities",
        "location"
    ],

    "Branch": [
        "branch",
        "branches"
    ],

    "Gender": [
        "gender",
        "male",
        "female"
    ],

    "Bonus": [
        "bonus"
    ],

    "Work Mode": [
        "work mode",
        "remote",
        "office",
        "hybrid"
    ]
}


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text):

    return str(text).lower().strip()


# ==========================================================
# FIND ALL COLUMNS IN QUESTION
# ==========================================================

def find_columns(df, question):

    q = normalize_text(question)

    words = re.findall(r"\b\w+\b", q)

    found = []

    # Actual column names
    for column in df.columns:

        col_lower = column.lower()

        if col_lower in q:
            found.append(column)

    # Aliases
    for column, aliases in COLUMN_ALIASES.items():

        if column not in df.columns:
            continue

        for alias in aliases:

            alias_lower = alias.lower()

            if " " in alias_lower:

                if alias_lower in q:
                    found.append(column)
                    break

            else:

                if alias_lower in words:
                    found.append(column)
                    break

    # Remove duplicates
    result = []

    for column in found:

        if column not in result:
            result.append(column)

    return result


# ==========================================================
# FIND SINGLE COLUMN
# ==========================================================

def find_column(df, text):

    columns = find_columns(df, text)

    if columns:
        return columns[0]

    return None


# ==========================================================
# DETECT INTENT
# ==========================================================

def detect_intent(question):

    q = normalize_text(question)

    if "top" in q:
        return "top"

    if "bottom" in q:
        return "bottom"

    if "average" in q or "avg" in q or "mean" in q:
        return "average"

    if (
        "maximum" in q
        or "highest" in q
        or "max" in q
    ):
        return "maximum"

    if (
        "minimum" in q
        or "lowest" in q
        or "min" in q
    ):
        return "minimum"

    if "sum" in q or "total salary" in q or "total bonus" in q:
        return "sum"

    if "count rows" in q or "total rows" in q:
        return "count_rows"

    if "count columns" in q or "total columns" in q:
        return "count_columns"

    if (
        "count" in q
        or "how many" in q
        or "kitne" in q
        or "kitni" in q
    ):
        return "count"

    return "unknown"


# ==========================================================
# TOP N
# ==========================================================

def extract_top_n(question):

    q = normalize_text(question)

    match = re.search(
        r"\b(?:top|bottom|lowest|highest)\s+(\d+)",
        q
    )

    if match:
        return int(match.group(1))

    return 10


# ==========================================================
# APPLY TEXT FILTERS
# ==========================================================

def apply_text_filters(df, question):

    q = normalize_text(question)

    filtered_df = df.copy()

    for column in df.columns:

        # Text / categorical columns only
        if (
            pd.api.types.is_object_dtype(df[column])
            or pd.api.types.is_string_dtype(df[column])
            or isinstance(df[column].dtype, pd.CategoricalDtype)
        ):

            values = (
                df[column]
                .dropna()
                .astype(str)
                .unique()
            )

            # Longer values first
            values = sorted(
                values,
                key=lambda x: len(str(x)),
                reverse=True
            )

            for value in values:

                value_lower = normalize_text(value)

                pattern = (
                    r"(?<!\w)"
                    + re.escape(value_lower)
                    + r"(?!\w)"
                )

                if re.search(pattern, q):

                    # IMPORTANT:
                    # Apply every new filter to filtered_df
                    mask = (
                        filtered_df[column]
                        .astype(str)
                        .str.lower()
                        .str.strip()
                        == value_lower
                    )

                    filtered_df = filtered_df.loc[mask].copy()

                    print(
                        f"TEXT FILTER: "
                        f"{column} = {value} | "
                        f"Rows remaining: {len(filtered_df)}"
                    )

                    break

    return filtered_df


# ==========================================================
# NUMERIC CONDITIONS
# ==========================================================

def extract_numeric_conditions(df, question):

    q = normalize_text(question)

    conditions = []

    numeric_columns = [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    for column in numeric_columns:

        aliases = [column.lower()]

        if column in COLUMN_ALIASES:
            aliases.extend(
                alias.lower()
                for alias in COLUMN_ALIASES[column]
            )

        aliases = sorted(
            set(aliases),
            key=len,
            reverse=True
        )

        condition_found = False

        for alias in aliases:

            escaped = re.escape(alias)

            # ------------------------------------------
            # 1. Symbol format
            # salary > 50000
            # age <= 30
            # ------------------------------------------

            pattern = (
                rf"\b{escaped}\b\s*"
                rf"(>=|<=|>|<|=)\s*"
                rf"(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                conditions.append(
                    (
                        column,
                        match.group(1),
                        float(match.group(2))
                    )
                )

                condition_found = True
                break

            # ------------------------------------------
            # 2. Roman English
            # salary 50000 se zyada
            # age 30 se zyada
            # ------------------------------------------

            pattern = (
                rf"\b{escaped}\b"
                rf".{{0,15}}?"
                rf"(\d+(?:\.\d+)?)"
                rf"\s*(?:se\s*)?"
                rf"(zyada|jyada|jiyada)"
            )

            match = re.search(pattern, q)

            if match:

                conditions.append(
                    (
                        column,
                        ">",
                        float(match.group(1))
                    )
                )

                condition_found = True
                break

            # ------------------------------------------
            # 3. Roman English LESS THAN
            # salary 100000 se kam
            # age 40 se kam
            # ------------------------------------------

            pattern = (
                rf"\b{escaped}\b"
                rf".{{0,15}}?"
                rf"(\d+(?:\.\d+)?)"
                rf"\s*(?:se\s*)?"
                rf"(kam|less)"
            )

            match = re.search(pattern, q)

            if match:

                conditions.append(
                    (
                        column,
                        "<",
                        float(match.group(1))
                    )
                )

                condition_found = True
                break

            # ------------------------------------------
            # 4. English MORE THAN
            # salary more than 50000
            # age greater than 30
            # ------------------------------------------

            pattern = (
                rf"\b{escaped}\b"
                rf".{{0,15}}?"
                rf"(?:more\s+than|greater\s+than|above|over)"
                rf"\s*(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                conditions.append(
                    (
                        column,
                        ">",
                        float(match.group(1))
                    )
                )

                condition_found = True
                break

            # ------------------------------------------
            # 5. English LESS THAN
            # salary less than 100000
            # age below 30
            # ------------------------------------------

            pattern = (
                rf"\b{escaped}\b"
                rf".{{0,15}}?"
                rf"(?:less\s+than|below|under)"
                rf"\s*(\d+(?:\.\d+)?)"
            )

            match = re.search(pattern, q)

            if match:

                conditions.append(
                    (
                        column,
                        "<",
                        float(match.group(1))
                    )
                )

                condition_found = True
                break

        if condition_found:
            continue

    print("Detected Numeric Conditions:", conditions)

    return conditions


# ==========================================================
# APPLY NUMERIC CONDITION
# ==========================================================

def apply_condition(df, column, operator, value):

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if operator == ">":
        return df[series > value]

    if operator == "<":
        return df[series < value]

    if operator == ">=":
        return df[series >= value]

    if operator == "<=":
        return df[series <= value]

    if operator == "=":
        return df[series == value]

    return df


# ==========================================================
# DETECT GROUP BY COLUMN
# ==========================================================

def detect_groupby_column(df, question):

    q = normalize_text(question)

    group_words = [
        "wise",
        "by",
        "group by",
        "according to",
        "per"
    ]

    if not any(word in q for word in group_words):
        return None

    columns = find_columns(df, question)

    # Prefer categorical columns
    for column in columns:

        if (
            pd.api.types.is_object_dtype(df[column])
            or pd.api.types.is_string_dtype(df[column])
        ):
            return column

    return None


# ==========================================================
# DETECT TARGET NUMERIC COLUMN
# ==========================================================

def detect_target_column(df, question, group_column=None):

    q = normalize_text(question)
    words = re.findall(r"\b\w+\b", q)

    # 1. First priority:
    # Numeric column explicitly mentioned in question
    for column in df.columns:

        if column == group_column:
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            continue

        column_lower = column.lower()

        if " " in column_lower:
            if column_lower in q:
                return column
        else:
            if column_lower in words:
                return column

    # 2. Second priority:
    # Numeric aliases explicitly mentioned
    for column, aliases in COLUMN_ALIASES.items():

        if column not in df.columns:
            continue

        if column == group_column:
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            continue

        for alias in aliases:

            alias_lower = alias.lower()

            if " " in alias_lower:

                if alias_lower in q:
                    return column

            else:

                if alias_lower in words:
                    return column

    return None


# ==========================================================
# CREATE CHART
# ==========================================================

def create_chart(
    data,
    title="Genesis AI Chart",
    chart_type="bar"
):

    os.makedirs(
        "charts",
        exist_ok=True
    )

    filename = f"{uuid.uuid4()}.png"

    filepath = os.path.join(
        "charts",
        filename
    )

    plt.figure(figsize=(9, 5))

    if chart_type == "pie":

        data.plot(
            kind="pie",
            autopct="%1.1f%%"
        )

        plt.ylabel("")

    else:

        data.plot(kind="bar")

        plt.xticks(rotation=30)

    plt.title(title)

    plt.tight_layout()

    plt.savefig(filepath)

    plt.close()

    return f"/charts/{filename}"


# ==========================================================
# GROUP BY ANALYSIS
# ==========================================================

def groupby_analysis(
    df,
    group_column,
    target_column,
    intent
):

    if intent == "count":

        if target_column:

            result = (
                df.groupby(group_column)[target_column]
                .count()
            )

        else:

            result = (
                df.groupby(group_column)
                .size()
            )

        return result

    if target_column is None:
        return None

    if not pd.api.types.is_numeric_dtype(
        df[target_column]
    ):
        return None

    grouped = df.groupby(group_column)[target_column]

    if intent == "average":
        return grouped.mean()

    if intent == "sum":
        return grouped.sum()

    if intent == "maximum":
        return grouped.max()

    if intent == "minimum":
        return grouped.min()

    return None


# ==========================================================
# FORMAT GROUP RESULT
# ==========================================================

def format_group_result(
    result,
    group_column,
    target_column,
    intent
):

    title_target = (
        target_column
        if target_column
        else "Employees"
    )

    answer = (
        f"📊 {group_column}-wise "
        f"{intent.title()} {title_target}\n\n"
    )

    for name, value in result.items():

        if isinstance(value, float):
            value = round(value, 2)

        answer += f"{name}: {value}\n"

    return answer


# ==========================================================
# MAIN GENESIS AI ENGINE
# ==========================================================

def analyze_question(df, question):

    if df is None or df.empty:

        return {
            "answer": "❌ Dataset is empty."
        }

    q = normalize_text(question)

    intent = detect_intent(question)

    print("=" * 60)
    print("GENESIS AI V4")
    print("Question:", question)
    print("Intent:", intent)

    # ------------------------------------------------------
    # FILTER DATA
    # ------------------------------------------------------

    filtered_df = apply_text_filters(
        df.copy(),
        question
    )

    numeric_conditions = extract_numeric_conditions(
        df,
        question
    )

    for column, operator, value in numeric_conditions:

        filtered_df = apply_condition(
            filtered_df,
            column,
            operator,
            value
        )

        print(
            "NUMERIC FILTER:",
            column,
            operator,
            value
        )

    print(
        "Rows after filters:",
        len(filtered_df)
    )

    # ------------------------------------------------------
    # EMPTY RESULT
    # ------------------------------------------------------

    if filtered_df.empty:

        return {
            "answer":
            "❌ No records matched your filters."
        }

    # ------------------------------------------------------
    # BASIC COUNTS
    # ------------------------------------------------------

    if intent == "count_rows":

        return {
            "answer":
            f"📄 Total Rows: {len(filtered_df)}"
        }

    if intent == "count_columns":

        return {
            "answer":
            f"📋 Total Columns: {len(df.columns)}"
        }

    # ------------------------------------------------------
    # COLUMN UNDERSTANDING
    # ------------------------------------------------------

    group_column = detect_groupby_column(
        df,
        question
    )

    target_column = detect_target_column(
        df,
        question,
        group_column
    )

    print("Group Column:", group_column)
    print("Target Column:", target_column)

    # ------------------------------------------------------
    # GROUP BY
    # ------------------------------------------------------

    if (
        group_column is not None
        and intent in [
            "average",
            "sum",
            "maximum",
            "minimum",
            "count"
        ]
    ):

        result = groupby_analysis(
            filtered_df,
            group_column,
            target_column,
            intent
        )

        if result is not None:

            answer = format_group_result(
                result,
                group_column,
                target_column,
                intent
            )

            response = {
                "answer": answer
            }

            if (
                "chart" in q
                or "graph" in q
                or "plot" in q
            ):

                chart = create_chart(
                    result,
                    title=(
                        f"{group_column}-wise "
                        f"{intent.title()} "
                        f"{target_column or 'Employees'}"
                    )
                )

                response["chart_file"] = chart
                response["chart"] = chart

            return response

    # ------------------------------------------------------
    # TOP / BOTTOM
    # ------------------------------------------------------

    if intent in ["top", "bottom"]:

        top_n = extract_top_n(question)

        if target_column is None:

            if "Salary" in filtered_df.columns:
                target_column = "Salary"

        if target_column is None:

            return {
                "answer":
                "❌ Please specify a numeric column."
            }

        if not pd.api.types.is_numeric_dtype(
            filtered_df[target_column]
        ):

            return {
                "answer":
                f"❌ '{target_column}' is not numeric."
            }

        if intent == "top":

            result_df = filtered_df.nlargest(
                top_n,
                target_column
            )

            heading = "Top"

        else:

            result_df = filtered_df.nsmallest(
                top_n,
                target_column
            )

            heading = "Bottom"

        answer = (
            f"📊 {heading} {top_n} "
            f"by {target_column}\n\n"
        )

        for i, (_, row) in enumerate(
            result_df.iterrows(),
            start=1
        ):

            answer += f"{i}. "

            if "Employee Name" in result_df.columns:

                answer += (
                    f"{row['Employee Name']} | "
                )

            answer += (
                f"{target_column}: "
                f"{row[target_column]}"
            )

            if "Department" in result_df.columns:

                answer += (
                    f" | {row['Department']}"
                )

            answer += "\n"

        return {
            "answer": answer
        }

    # ------------------------------------------------------
    # SHOW / LIST FILTERED DATA
    # ------------------------------------------------------

    show_words = [
        "show",
        "list",
        "display",
        "dikhao"
    ]

    if any(word in q for word in show_words):

        if len(filtered_df) != len(df):

            return {
                "answer":
                filtered_df.head(100).to_string(
                    index=False
                )
            }

    # ------------------------------------------------------
    # SINGLE NUMERIC ANALYSIS
    # ------------------------------------------------------

    if intent in [
        "average",
        "sum",
        "maximum",
        "minimum"
    ]:

        if target_column is None:

            return {
                "answer":
                "❌ I couldn't identify the numeric column."
            }

        series = pd.to_numeric(
            filtered_df[target_column],
            errors="coerce"
        )

        if intent == "average":

            value = series.mean()

            return {
                "answer":
                f"📊 Average {target_column}: "
                f"{round(value, 2)}"
            }

        if intent == "sum":

            value = series.sum()

            return {
                "answer":
                f"💰 Sum of {target_column}: "
                f"{round(value, 2)}"
            }

        if intent == "maximum":

            value = series.max()

            return {
                "answer":
                f"📈 Maximum {target_column}: "
                f"{value}"
            }

        if intent == "minimum":

            value = series.min()

            return {
                "answer":
                f"📉 Minimum {target_column}: "
                f"{value}"
            }

    # ------------------------------------------------------
    # COUNT
    # ------------------------------------------------------

    if intent == "count":

        return {
            "answer":
            f"👥 Count: {len(filtered_df)}"
        }

    # ------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------

    return {
        "answer":
        "❌ Sorry, I couldn't understand your question."
    }


# ==========================================================
# HELPERS
# ==========================================================

def available_numeric_columns(df):

    return [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]


def available_columns(df):

    return list(df.columns)