ALPHABET = "abdefghijklmnopqrstuvxyzäöõü-"  # w and c missing

def build_rules() -> set:
    rules = set()
    # setup
    for char in ALPHABET + "wc":
        rules.add(f"INIT {char} INIT {char} R")
    rules.add("INIT _ BACK # L")
    for char in ALPHABET + "wc#[]":
        rules.add(f"BACK {char} BACK {char} L")
    rules.add("BACK _ FWD _ R")

    # copy chain
    for char in ALPHABET:
        rules.add(f"FWD {char} COPY_{char} _ R")
        rules.add(f"COPY_{char} _ BACK {char} L")
        for other_char in ALPHABET + "wc#[]":
            rules.add(f"COPY_{char} {other_char} COPY_{char} {other_char} R")

    # mark w
    rules.add("FWD w COPY_w _ R")
    for other_char in ALPHABET + "wc#[]":
        rules.add(f"COPY_w {other_char} COPY_w {other_char} R")
    rules.add("COPY_w _ WRITE_w [ R")
    rules.add("WRITE_w _ CLOSE w R")
    rules.add("CLOSE _ BACK ] L")

    # mark ch
    rules.add("FWD c CHECK_c _ R")
    for other_char in ALPHABET + "wc#[]":
        if other_char in "[]":
            pass
        elif other_char != "h":
            rules.add(f"CHECK_c {other_char} COPY_c {other_char} R")
        else:
            rules.add("CHECK_c h COPY_ch _ R")
        rules.add(f"COPY_c {other_char} COPY_c {other_char} R")
        rules.add(f"COPY_ch {other_char} COPY_ch {other_char} R")
    rules.add("COPY_c _ BACK c L")
    rules.add("COPY_ch _ WRITE_c [ R")
    rules.add("WRITE_c _ WRITE_h c R")
    rules.add("WRITE_h _ CLOSE h R")

    # end
    rules.add("FWD # HALT _ R")
    return rules


if __name__ == "__main__":
    print("\n".join(build_rules()))
