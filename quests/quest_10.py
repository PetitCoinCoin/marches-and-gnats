from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):
    ALPHABET = "abcdefghijklmnopqrstuvwxyzäöõü-"

    def _build_steps_opt(self):
        """803 939 movements, 70 rules, 5 states"""
        self.add("INIT _ HALT | R")
        self.add("INIT + COUNT | R")
        for char in self.ALPHABET:
            self.add(f"INIT {char} INIT _ R")
            self.add(f"COUNT {char} BACK | L")
        self.add("BACK | BACK | L")
        self.add("BACK _ CLEAR _ R")
        self.add("CLEAR | COUNT _ R")
        self.add("COUNT | COUNT | R")
        self.add("COUNT + COUNT | R")
        self.add("COUNT _ HALT | R")


if __name__ == "__main__":
    args = arg_parser()
    machine = Machine()
    machine.build_rules(rules_optimized=args.rules)
    if args.stats:
        print(machine.stats)
    if args.test:
        machine.play(args.test, verbose=args.verbose)
    else:
        set_clipboard_data(machine.pretty_rules)
        print(f"{Colors.GREEN}Rules copied to clipboard!")
