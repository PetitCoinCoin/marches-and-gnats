from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    def _build_steps_opt(self):
        """20 379 movements, 4 rules, 3 states"""
        self.add("INIT | ODD _ R")
        self.add("ODD | INIT _ R")
        self.add("INIT _ HALT E R")
        self.add("ODD _ HALT O R")


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
