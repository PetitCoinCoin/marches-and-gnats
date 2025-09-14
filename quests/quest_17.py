from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):
    STEPS = 5

    def _build_steps_opt(self):
        """6257 movements, 81 rules, 41 states"""
        self.add("INIT - HALT _ R")
        self.add("INIT + SET+_1 + L")
        for i in range(1, self.STEPS + 1):
            fwd = "R" if i % 2 else "L"
            bwd = "L" if i % 2 else "R"

            self.add(f"SET+_{i} _ CHECK_{i}_0 + {fwd}")
            self.add(f"SET+_{i} - CHECK_{i}_0 + {fwd}")
            self.add(f"SET-_{i} + CHECK_{i}_1 - {fwd}")

            self.add(f"CHECK_{i}_0 + CHECK_{i}_01 + {fwd}")
            self.add(f"CHECK_{i}_0 - CHECK_{i}_00 - {fwd}")
            self.add(f"CHECK_{i}_1 + CHECK_{i}_1 - {fwd}")
            self.add(f"CHECK_{i}_1 - CHECK_{i}_10 - {fwd}")
            if i == self.STEPS:
                self.add(f"CHECK_{i}_1 _ HALT + {fwd}")
            else:
                self.add(f"CHECK_{i}_1 _ INIT_{i + 1} + {fwd}")
                self.add(f"INIT_{i + 1} _ CHECK_{i + 1}_0 + {bwd}")  # next step

            self.add(f"CHECK_{i}_01 + SET-_{i} + {bwd}")
            self.add(f"CHECK_{i}_01 - CHECK_{i}_10 - {fwd}")
            if i == self.STEPS:
                self.add(f"CHECK_{i}_01 _ HALT + {fwd}")
            else:
                self.add(f"CHECK_{i}_01 _ INIT_{i + 1} + {fwd}")
                self.add(f"INIT_{i + 1} _ CHECK_{i + 1}_0 + {bwd}")  # next step
            self.add(f"CHECK_{i}_00 + SET+_{i} + {bwd}")
            self.add(f"CHECK_{i}_00 - CHECK_{i}_00 - {fwd}")
            self.add(f"CHECK_{i}_10 + CHECK_{i}_01 + {fwd}")
            self.add(f"CHECK_{i}_10 - SET+_{i} - {bwd}")


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
