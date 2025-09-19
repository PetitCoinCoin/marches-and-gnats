from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):
    def _build_steps_opt(self):
        """X movements, X rules, X states"""
        self._build_rules_opt()

        # If division by 1, early stop
        self.add("ID ÷ CHECK ÷ R")
        self.add("CHECK | CHECK_1 | R")
        self.add("CHECK_1 | ID | R")
        self.add("CHECK_1 _ CLEAN_EARLY , L")
        self.add("CLEAN_EARLY | CLEAN_EARLY | L")
        self.add("CLEAN_EARLY , HALT _ L")


    def _build_rules_opt(self, *, from_steps: bool = False):
        """11 141 970 movements, 27 rules, 12 states"""
        # Setup
        self.add("INIT | SETUP | L")
        self.add("SETUP _ ID , R")
        self.add("ID | ID | R")
        if not from_steps:
            self.add("ID ÷ ID ÷ R")
        self.add("ID , ID , R")

        # Divide - First
        self.add("ID _ DIV _ L")
        self.add("DIV | DIVIDE _ L")
        self.add("DIVIDE | DIVIDE | L")
        self.add("DIVIDE ÷ APPLY _ L")
        self.add("DIVIDE _ APPLY _ L")
        self.add("APPLY # APPLY # L")
        self.add("APPLY | APPLIED # R")
        self.add("APPLIED # APPLIED # R")
        self.add("APPLIED _ ID _ R")
        self.add("DIV _ COUNT _ L")

        # Divide - next
        self.add("ID # SHIFT _ R")
        self.add("SHIFT # SHIFT | R")
        self.add("SHIFT _ ID | R")

        # Quotient
        self.add("COUNT # COUNT # L")
        self.add("COUNT | COUNT | L")
        self.add("COUNT , COUNT , L")
        self.add("COUNT _ ID | R")

        # Remainder
        self.add("APPLY , REMAINDER , R")
        self.add("REMAINDER # REMAINDER | R")
        
        # Clean
        self.add("REMAINDER _ CLEAN _ R")
        self.add("CLEAN | CLEAN _ R")
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
