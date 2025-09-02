from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):

    def _build_steps_opt(self):
        """247 170 movements, 24 rules, 10 states"""
        self.add("INIT | SETUP _ R")
        # Count left
        self.add("SETUP | ID _ R")
        self.add("SETUP * CLEAN _ R")
        self.add("ID | ID | R")
        self.add("ID * MUL * R")
        self.add("BACK_COUNT | BACK_COUNT | L")
        self.add("BACK_COUNT _ SETUP _ R")
        # Add once
        self.add("MUL | COPY_FROM_1 X R")
        self.add("MUL 0 COPY_FROM_0 X R")
        self.add("MUL X MUL X R")
        for state in "|0X":
            self.add(f"COPY_FROM_1 {state} COPY_FROM_1 {state} R")
        self.add("COPY_FROM_1 _ BACK_COPY 0 L")
        self.add("COPY_FROM_0 0 COPY_FROM_0 | R")
        self.add("COPY_FROM_0 _ BACK_COPY 0 L")
        self.add("BACK_COPY | COPY_FROM_1 X R")
        self.add("BACK_COPY 0 BACK_COPY 0 L")
        self.add("BACK_COPY X BACK_COPY X L")
        self.add("BACK_COPY * BACK_COUNT * L")
        # End
        self.add("CLEAN X CLEAN | R")
        self.add("CLEAN 0 CLEAN | R")
        self.add("CLEAN | HALT | R")
        self.add("CLEAN _ HALT _ R")

    def _build_rules_opt(self):
        """
            First viable solution: 1 341 179 movements, 21 rules, 10 states
            Improved to: 1 258 165 movements, 18 rules, 8 states
        """
        self.add("INIT | SETUP _ R")
        self.add("SETUP | ID _ R")
        # Count left
        self.add("ID | ID | R")  # Common
        self.add("ID * MUL * R")
        # Add once
        self.add("MUL | ID X R")
        self.add("ID 0 ID 0 R")
        self.add("ID _ BACK_COPY 0 L")
        self.add("BACK_COPY X MUL | R")
        self.add("BACK_COPY | BACK_COPY | L")
        self.add("BACK_COPY 0 BACK_COPY 0 L")
        # Iteration done
        self.add("MUL 0 BACK 0 L")
        self.add("BACK | BACK | L")
        self.add("BACK * BACK * L")
        self.add("BACK _ SETUP _ R")
        # End
        self.add("SETUP * CLEAN _ R")
        self.add("CLEAN | CLEAN | R")
        self.add("CLEAN 0 CLEAN | R")
        self.add("CLEAN _ HALT _ R")


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
