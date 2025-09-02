from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):
    def _build_steps_opt(self):
        """28 143 movements, 3 rules, 3 states"""
        self.add("INIT | FIND _ R")
        self.add("FIND | FIND | R")
        self.add("FIND + HALT | R")


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
