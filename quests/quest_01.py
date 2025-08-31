def build_rules() -> set:
    rules = set()
    rules.add("INIT | FIND | R")
    rules.add("FIND | FIND | R")
    rules.add("FIND + HALT | R")
    return rules

if __name__ == "__main__":
    print("\n".join(build_rules()))
