def build_rules() -> set:
    rules = set()
    rules.add("INIT 1 INIT 1 R")
    rules.add("INIT 0 INIT 0 R")
    rules.add("INIT _ ADD _ L")
    rules.add("ADD 1 ADD 0 L")
    rules.add("ADD 0 HALT 1 L")
    rules.add("ADD _ HALT 1 R")
    return rules

if __name__ == "__main__":
    print("\n".join(build_rules()))
