from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    ALPHABET = "abcdefghijklmnopqrstuvwxyzäöõü-"

    def _build_steps_opt(self):
        """64 952 movements, 1149 rules, 36 states"""
        for char in self.ALPHABET:
            if char != "-":
                self.add(f"INIT {char} FWD {char} R")
            self.add(f"FWD {char} BACK_{char} # L")
            for other_char in self.ALPHABET:
                self.add(f"BACK_{char} {other_char} BACK_{char} {other_char} L")
            self.add(f"BACK_{char} # BACK_{char} # L")
            self.add(f"BACK_{char} _ ID {char} R")
            self.add(f"ID {char} ID {char} R")
        self.add("ID # FWD # R")
        self.add("FWD # FWD # R")
        self.add("FWD _ CLEAR _ L")
        self.add("CLEAR # CLEAR _ L")
        for char in self.ALPHABET:
            if char != "-":
                self.add(f"CLEAR {char} HALT {char} R")


if __name__ == "__main__":
    args = arg_parser()
    machine = Machine()
    machine.build_rules(rules_optimized=args.rules)
    if args.stats:
        print(machine.stats)
    if args.test:
        machine.play(args.test)
    else:
        set_clipboard_data(machine.pretty_rules)
        print("Rules copied to clipboard!")
