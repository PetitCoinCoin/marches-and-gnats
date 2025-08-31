def build_rules() -> set:
    rules = set()
    rules.add("INIT | ODD _ R")
    rules.add("ODD | INIT _ R")
    rules.add("INIT _ HALT E R")
    rules.add("ODD _ HALT O R")
    return rules

if __name__ == "__main__":
    print("\n".join(build_rules()))
