DIGITS = "0123456789"

def build_rules() -> set:
    rules = set()
    for digit in DIGITS:
        rules.add(f"INIT {digit} FILL {digit} L")
        rules.add(f"FWD {digit} FWD {digit} R")
        rules.add(f"RFWD {digit} RFWD {digit} R")
    # Add leading zero for carryover
    rules.add("FILL _ SEP 0 L")
    rules.add("SEP _ FWD # R")
    rules.add("FWD + RFWD + R")
    rules.add("FWD _ FWD _ R")
    rules.add("RFWD _ SCAN _ L")
    for digit in DIGITS:
        rules.add(f"SCAN {digit} OP_{digit} _ L")
        rules.add(f"OP_{digit} + LOP_{digit} + L")
        rules.add(f"LOP_{digit} _ LOP_{digit} _ L")
        rules.add(f"LOP_{digit} # LDONE_{digit} # L")
        for other_digit in DIGITS:
            rules.add(f"OP_{digit} {other_digit} OP_{digit} {other_digit} L")
            result = int(digit) + int(other_digit)
            if result >= 10:
                rules.add(f"LOP_{digit} {other_digit} SUM+_{result - 10} _ L")
            else:
                rules.add(f"LOP_{digit} {other_digit} SUM_{result} _ L")
        for other_digit in DIGITS:
            if digit != "9":  # max digit here is 8 because 9+9=18
                result = int(other_digit) + 1
                if result >= 10:
                    rules.add(f"SUM+_{digit} {other_digit} SUM+_{digit} {result - 10} L")
                else:
                    rules.add(f"SUM+_{digit} {other_digit} SUM_{digit} {result} L")
            rules.add(f"SUM_{digit} {other_digit} SUM_{digit} {other_digit} L")
        rules.add(f"SUM_{digit} # RES_{digit} # L")
        for other_digit in DIGITS:
            rules.add(f"RES_{digit} {other_digit}  RES_{digit} {other_digit} L")
        rules.add(f"RES_{digit} _ FWD {digit} R")

    rules.add("SUM+_0 # MORE # R")
    rules.add("MORE _ SUM_0 1 L")
    rules.add("FWD # FWD # R")
    rules.add("SCAN + RDONE _ L")
    rules.add("RDONE _ RDONE _ L")
    rules.add("RDONE # HALT _ R")

    for digit in DIGITS:
        rules.add(f"RDONE {digit} RDONE_{digit} _ L")
        if digit != "0":
            rules.add(f"RDONE_{digit} # RDONE_{digit} # L")
        for other_digit in DIGITS:
            rules.add(f"RDONE_{digit} {other_digit} RDONE_{digit} {other_digit} L")
            rules.add(f"LDONE_{digit} {other_digit} LDONE_{digit} {other_digit} L")
        rules.add(f"RDONE_{digit} _ FWD_RDONE {digit} R")
        rules.add(f"LDONE_{digit} _ FWD {digit} R")
        rules.add(f"FWD_RDONE {digit} FWD_RDONE {digit} R")
    # check if the 0 carried is the leading 0
    rules.add("RDONE_0 # CHECK # R")
    rules.add("CHECK _ DONE _ L")
    rules.add("CHECK 1 STILL 1 L")
    rules.add("CHECK 0 STILL 0 L")
    rules.add("STILL # RDONE_0 # L")
    rules.add("DONE # HALT _ L")

    rules.add("FWD_RDONE # FWD_RDONE # R")
    rules.add("FWD_RDONE _ RDONE _ L")
    return rules


if __name__ == "__main__":
    print("\n".join(build_rules()))
