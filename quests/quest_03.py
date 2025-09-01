from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    def _build_steps_opt(self):
        """652 movements, 6 rules, 3 states"""
        self.add("INIT 1 INIT 1 R")
        self.add("INIT 0 INIT 0 R")
        self.add("INIT _ ADD _ L")
        self.add("ADD 1 ADD 0 L")
        self.add("ADD 0 HALT 1 L")
        self.add("ADD _ HALT 1 R")


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
        print("self copied to clipboard!")
