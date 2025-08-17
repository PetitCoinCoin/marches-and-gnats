ALPHABET = "abcdefghijklmnopqrstuvwxyzäöõü-"

def build_rules() -> set:
    rules = set()
    for char in ALPHABET:
        if char != "-":
            rules.add(f"INIT {char} FWD {char} R")
        rules.add(f"FWD {char} BACK_{char} # L")
        for other_char in ALPHABET:
            rules.add(f"BACK_{char} {other_char} BACK_{char} {other_char} L")
        rules.add(f"BACK_{char} # BACK_{char} # L")
        rules.add(f"BACK_{char} _ ID {char} R")
        rules.add(f"ID {char} ID {char} R")
    rules.add("ID # FWD # R")
    rules.add("FWD # FWD # R")
    rules.add("FWD _ CLEAR _ L")
    rules.add("CLEAR # CLEAR _ L")
    for char in ALPHABET:
        if char != "-":
            rules.add(f"CLEAR {char} HALT {char} R")
    return rules


if __name__ == "__main__":
    print("\n".join(build_rules()))
