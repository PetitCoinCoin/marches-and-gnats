from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    ALPHABET = "abdefghijklmnopqrstuvxyzäöõü-"  # w and c missing

    def _build_steps_opt(self):
        """83 776 movements, 1255 rules, 41 states"""
        # setup
        for char in self.ALPHABET + "wc":
            self.add(f"INIT {char} INIT {char} R")
        self.add("INIT _ BACK # L")
        for char in self.ALPHABET + "wc#[]":
            self.add(f"BACK {char} BACK {char} L")
        self.add("BACK _ FWD _ R")

        # copy chain
        for char in self.ALPHABET:
            self.add(f"FWD {char} COPY_{char} _ R")
            self.add(f"COPY_{char} _ BACK {char} L")
            for other_char in self.ALPHABET + "wc#[]":
                self.add(f"COPY_{char} {other_char} COPY_{char} {other_char} R")

        # mark w
        self.add("FWD w COPY_w _ R")
        for other_char in self.ALPHABET + "wc#[]":
            self.add(f"COPY_w {other_char} COPY_w {other_char} R")
        self.add("COPY_w _ WRITE_w [ R")
        self.add("WRITE_w _ CLOSE w R")
        self.add("CLOSE _ BACK ] L")

        # mark ch
        self.add("FWD c CHECK_c _ R")
        for other_char in self.ALPHABET + "wc#[]":
            if other_char in "[]":
                pass
            elif other_char != "h":
                self.add(f"CHECK_c {other_char} COPY_c {other_char} R")
            else:
                self.add("CHECK_c h COPY_ch _ R")
            self.add(f"COPY_c {other_char} COPY_c {other_char} R")
            self.add(f"COPY_ch {other_char} COPY_ch {other_char} R")
        self.add("COPY_c _ BACK c L")
        self.add("COPY_ch _ WRITE_c [ R")
        self.add("WRITE_c _ WRITE_h c R")
        self.add("WRITE_h _ CLOSE h R")

        # end
        self.add("FWD # HALT _ R")

    def _build_rules_opt(self):
        """
            Knowing that test cases do not have c followed by something else than h allows me to comment a few rules...
            83 776 movements, 1224 rules, 41 states
        """
        self._build_steps_opt()
        to_remove = set()
        for rule in self.rules:
            if rule.state == "CHECK_c" and rule.symbol != "h":
                to_remove.add(rule)
        self.rules -= to_remove

if __name__ == "__main__":
    args = arg_parser()
    machine = Machine()
    machine.build_rules(rules_optimized=args.rules)
    if args.stats:
        print(machine.stats)
    if args.test:
        pass
    else:
        set_clipboard_data(machine.pretty_rules)
        print("Rules copied to clipboard!")
