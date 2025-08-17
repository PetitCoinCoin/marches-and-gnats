ALPHABET = "abcdefghijklmnopqrstuvwxyzäöõü-"

def build_rules() -> set:
    rules = set()
    rules.add("INIT _ HALT | R")
    rules.add("INIT + COUNT | R")
    for char in ALPHABET:
        rules.add(f"INIT {char} INIT _ R")
        rules.add(f"COUNT {char} BACK | L")
    rules.add("BACK | BACK | L")
    rules.add("BACK _ CLEAR _ R")
    rules.add("CLEAR | COUNT _ R")
    rules.add("COUNT | COUNT | R")
    rules.add("COUNT + COUNT | R")
    rules.add("COUNT _ HALT | R")
    return rules


if __name__ == "__main__":
    print("\n".join(build_rules()))
