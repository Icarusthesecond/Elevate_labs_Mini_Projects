def detect_sqli(input_data):

    patterns = [
        "' OR '1'='1",
        "' OR 1=1",
        "--",
        ";",
        "/*",
        "*/",
        "DROP",
        "UNION",
        "SELECT"
    ]

    input_upper = input_data.upper()

    for p in patterns:
        if p in input_upper:
            return True

    return False
