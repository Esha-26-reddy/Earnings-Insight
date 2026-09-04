import re


# ============================================================
# EARNINGS DOCUMENT VALIDATION
# ============================================================

def validate_earnings_document(text):

    if not text or len(text.strip()) < 200:
        return False, "The uploaded file does not contain enough readable text."

    text_lower = text.lower()

    # --------------------------------------------------------
    # Earnings-related keywords
    # --------------------------------------------------------

    earnings_keywords = [
        "earnings",
        "revenue",
        "quarter",
        "fiscal",
        "financial results",
        "financial highlights",
        "operating income",
        "net income",
        "earnings per share",
        "eps",
        "guidance",
        "outlook",
        "profit",
        "loss",
        "cash flow",
        "balance sheet",
        "income statement",
        "year over year",
        "yoy",
        "q1",
        "q2",
        "q3",
        "q4"
    ]

    # --------------------------------------------------------
    # Earnings call keywords
    # --------------------------------------------------------

    call_keywords = [
        "prepared remarks",
        "operator",
        "question-and-answer",
        "question and answer",
        "q&a",
        "analyst",
        "chief executive officer",
        "ceo",
        "chief financial officer",
        "cfo",
        "management commentary"
    ]

    earnings_matches = sum(
        1
        for keyword in earnings_keywords
        if keyword in text_lower
    )

    call_matches = sum(
        1
        for keyword in call_keywords
        if keyword in text_lower
    )

    # --------------------------------------------------------
    # Basic financial number detection
    # --------------------------------------------------------

    has_financial_numbers = bool(
        re.search(
            r"\$\s?\d+(?:\.\d+)?\s?(?:billion|million|bn|m)?",
            text_lower
        )
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if earnings_matches >= 3:
        return True, "Earnings-related document detected."

    if earnings_matches >= 2 and (
        call_matches >= 1 or has_financial_numbers
    ):
        return True, "Earnings-related document detected."

    return False, (
        "This file does not appear to be an earnings report "
        "or earnings call transcript. Please upload a relevant "
        "earnings document."
    )