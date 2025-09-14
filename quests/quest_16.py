from utils.machine import BaseMachine
from utils.main import Colors, arg_parser, set_clipboard_data


class Machine(BaseMachine):
    ALPHABET = {
        "M": {
            "value": 1000,
            "lower": "DCLXVI",
            "sub": [],
        },
        "D": {
            "value": 500,
            "lower": "CLXVI",
            "sub": [],
        },
        "C": {
            "value": 100,
            "lower": "LXVI",
            "sub": [("M", 900), ("D", 400)],
        },
        "L": {
            "value": 50,
            "lower": "XVI",
            "sub": [],
        },
        "X": {
            "value": 10,
            "lower": "VI",
            "sub": [("C", 90), ("L", 40)],
        },
        "V": {
            "value": 5,
            "lower": "I",
            "sub": [],
        },
        "I": {
            "value": 1,
            "lower": "",
            "sub": [("X", 9), ("V", 4)],
        },
    }

    def _build_steps_opt(self):
        """Too many states"""
        # Init
        for char, data in self.ALPHABET.items():
            if not data["sub"]:
                self.add(f"INIT {char} ADD_{data["value"]} _ R")
            else:
                self.add(f"INIT {char} CHECK_{char}_0 _ R")

        # Handle M
        for t_value in (1000, 2000):
            self.add(f"ADD_{t_value} M ADD_{t_value + 1000} _ R")
        self.add("CHECK_C_0 M ADD_900 _ R")

        # Handle D
        for t_value in (0, 1000, 2000, 3000):
            if t_value:
                self.add(f"ADD_{t_value} D ADD_{t_value + 500} _ R")
            self.add(f"CHECK_C_{t_value} D ADD_{t_value + 400} _ R")

        # Handle C
        for t_value in (0, 1000, 2000, 3000):
            if t_value:
                self.add(f"ADD_{t_value} C CHECK_C_{t_value} _ R")
            for h_value in (200, 700):
                self.add(f"ADD_{t_value + h_value} C ADD_{t_value + h_value + 100} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} C ADD_{t_value + h_value + 200} _ R")
        for value in range(0, 3901, 100):
            self.add(f"CHECK_X_{value} C ADD_{value + 90} _ R")

        # Handle L
        for t_value in (0, 1000, 2000, 3000):
            for h_value in (0, 200, 300, 400, 500, 700, 800, 900):
                if t_value + h_value:
                    self.add(f"ADD_{t_value + h_value} L ADD_{t_value + h_value + 50} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} L ADD_{t_value + h_value + 150} _ R")
        for value in range(0, 3901, 100):
            self.add(f"CHECK_X_{value} L ADD_{value + 40} _ R")

        # Handle X
        for t_value in (0, 1000, 2000, 3000):
            for h_value in (0, 200, 300, 400, 500, 700, 800, 900):
                if t_value + h_value:
                    self.add(f"ADD_{t_value + h_value} X CHECK_X_{t_value + h_value} _ R")
                for d_value in (20, 70):
                    self.add(f"ADD_{t_value + h_value + d_value} X ADD_{t_value + h_value + t_value + 10} _ R")
                for d_value in (0, 50):
                    self.add(f"CHECK_X_{t_value + h_value + d_value} X ADD_{t_value + h_value + d_value + 20} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} X CHECK_X_{t_value + h_value + 100} _ R")
        for value in range(0, 3991, 10):
            self.add(f"CHECK_I_{value} X ADD_{value + 9} _ R")

        # Handle V
        for t_value in (0, 1000, 2000, 3000):
            for h_value in (0, 200, 300, 400, 500, 700, 800, 900):
                for d_value in (0, 20, 30, 40, 50, 70, 80, 90):
                    if t_value + h_value + d_value:
                        self.add(f"ADD_{t_value + h_value + d_value} V ADD_{t_value + h_value + d_value + 5} _ R")
                for d_value in (0, 50):
                    self.add(f"CHECK_X_{t_value + h_value + d_value} V ADD_{t_value + h_value + d_value + 15} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} V ADD_{t_value + h_value + 105} _ R")
        for value in range(0, 3991, 10):
            self.add(f"CHECK_I_{value} V ADD_{value + 4} _ R")

        # Handle I
        for t_value in (0, 1000, 2000, 3000):
            for h_value in (0, 200, 300, 400, 500, 700, 800, 900):
                for d_value in (0, 20, 30, 40, 50, 70, 80, 90):
                    if t_value + h_value + d_value:
                        self.add(f"ADD_{t_value + h_value + d_value} I CHECK_I_{t_value + h_value + d_value} _ R")
                    for u_value in (2, 7):
                        self.add(f"ADD_{t_value + h_value + d_value + u_value} I ADD_{t_value + h_value + t_value + u_value + 1} _ R")
                    for u_value in (0, 5):
                        self.add(f"CHECK_I_{t_value + h_value + d_value + u_value} I ADD_{t_value + h_value + d_value + u_value + 2} _ R")
                for d_value in (0, 50):
                    self.add(f"CHECK_X_{t_value + h_value + d_value} I CHECK_I_{t_value + h_value + d_value + 10} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} I CHECK_I_{t_value + h_value + 100} _ R")

        # Stop reading
        for t_value in (0, 1000, 2000, 3000):
            for h_value in (0, 100, 200, 300, 400, 500, 600, 700, 800, 900):  # 100 and 600 can be optimized
                for d_value in (0, 10, 20, 30, 40, 50, 60, 70, 80, 90):  # 10 and 60 can be optimized
                    for u_value in (0, 5):
                        self.add(f"CHECK_I_{t_value + h_value + d_value + u_value} _ ADD_{t_value + h_value + d_value + u_value + 1} _ R")
                for d_value in (0, 50):
                    self.add(f"CHECK_X_{t_value + h_value + d_value} _ ADD_{t_value + h_value + d_value + 10} _ R")
            for h_value in (0, 500):
                self.add(f"CHECK_C_{t_value + h_value} _ ADD_{t_value + h_value + 100} _ R")
    
        # Write final value
        for value in range(2, 4000):
            self.add(f"ADD_{value} _ ADD_{value - 1} | R")

        # End
        self.add("ADD_1 _ HALT | R")

    def _build_rules_opt(self):
        """165 786 movements, 1056 rules, 1006 states"""
        for char, data in self.ALPHABET.items():
            if not data["sub"]:
                self.add(f"INIT {char} COPY_{data["value"]} # L")
            else:
                self.add(f"INIT {char} FWD_{char} # R")
                self.add(f"FWD_{char} _ COPY_{data["value"]} _ L")
                self.add(f"FWD_{char} {char} COPY_{data["value"]} {char} L")
                if char != "I":
                    for other_char in data["lower"]:
                        self.add(f"FWD_{char} {other_char} COPY_{data["value"]} {other_char} L")
                    self.add(f"FWD_{char} {other_char} COPY_{data["value"]} {other_char} L")
            # Handle subtractions
            for other_char, sub_value in data["sub"]:
                self.add(f"FWD_{char} {other_char} COPY_{sub_value} # L")

        # Copy symbol value
        for value in [data["value"] for data in self.ALPHABET.values()] + [4, 9, 40, 90, 400, 900]:
            self.add(f"COPY_{value} # COPY_{value} # L")
            self.add(f"COPY_{value} | COPY_{value} | L")
        for value in range(2, 1001):
            self.add(f"COPY_{value} _ COPY_{value - 1} | L")
        self.add("COPY_1 _ INIT | R")

        # Next symbol
        self.add("INIT # INIT # R")
        self.add("INIT | INIT | R")

        # End
        self.add("INIT _ CLEAN _ L")
        self.add("CLEAN # CLEAN _ L")
        self.add("CLEAN | HALT | L")


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
