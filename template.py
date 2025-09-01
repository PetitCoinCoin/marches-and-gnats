from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    def _build_steps_opt(self):
        raise


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
