# ============================================================
# GENESIS AI - ADVANCED INTENT ENGINE
# ============================================================


def detect_advanced_intent(question):

    # --------------------------------------------------------
    # NORMALIZE QUESTION
    # --------------------------------------------------------

    q = str(question).lower().strip()


    # --------------------------------------------------------
    # INTENT DEFINITIONS
    # --------------------------------------------------------

    intents = {

        "poor_performance": [

            "performing poorly",
            "poor performance",
            "low performance",
            "worst performing",
            "underperforming",
            "needs improvement"

        ],

        "business_risk": [

            "business risks",
            "biggest risk",
            "biggest risks",
            "risk areas",
            "risks",
            "potential risk"

        ],

        "management_focus": [

            "management focus",
            "where should management focus",
            "where to focus",
            "focus area",
            "priority area"

        ],

        "employee_attention": [

            "employees need attention",
            "employee needs attention",
            "employees at risk",
            "which employees",
            "employee attention"

        ],

        "best_performer": [

            "best performer",
            "top performer",
            "highest performing",
            "performing best"

        ],

        "comparison": [

            "compare",
            "comparison",
            "difference between",
            "versus",
            "vs"

        ]

    }


    # --------------------------------------------------------
    # DETECT INTENT
    # --------------------------------------------------------

    for intent, keywords in intents.items():

        for keyword in keywords:

            if keyword in q:

                return {

                    "intent": intent,

                    "confidence": "High",

                    "matched_keyword": keyword

                }


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return {

        "intent": "general_analysis",

        "confidence": "Low",

        "matched_keyword": None

    } 