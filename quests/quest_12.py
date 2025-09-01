from utils.machine import BaseMachine
from utils.main import arg_parser, set_clipboard_data


class Machine(BaseMachine):
    DIGITS = "0123456789"

    def _build_steps_opt(self):
        """20228 movements, 848 rules, 82 states"""
        for digit in self.DIGITS:
            self.add(f"INIT {digit} FILL {digit} L")
            self.add(f"FWD {digit} FWD {digit} R")
            self.add(f"RFWD {digit} RFWD {digit} R")
        # Add leading zero for carryover
        self.add("FILL _ SEP 0 L")
        self.add("SEP _ FWD # R")
        self.add("FWD + RFWD + R")
        self.add("FWD _ FWD _ R")
        self.add("RFWD _ SCAN _ L")
        for digit in self.DIGITS:
            self.add(f"SCAN {digit} OP_{digit} _ L")
            self.add(f"OP_{digit} + LOP_{digit} + L")
            self.add(f"LOP_{digit} _ LOP_{digit} _ L")
            self.add(f"LOP_{digit} # LDONE_{digit} # L")
            for other_digit in self.DIGITS:
                self.add(f"OP_{digit} {other_digit} OP_{digit} {other_digit} L")
                result = int(digit) + int(other_digit)
                if result >= 10:
                    self.add(f"LOP_{digit} {other_digit} SUM+_{result - 10} _ L")
                else:
                    self.add(f"LOP_{digit} {other_digit} SUM_{result} _ L")
            for other_digit in self.DIGITS:
                if digit != "9":  # max digit here is 8 because 9+9=18
                    result = int(other_digit) + 1
                    if result >= 10:
                        self.add(f"SUM+_{digit} {other_digit} SUM+_{digit} {result - 10} L")
                    else:
                        self.add(f"SUM+_{digit} {other_digit} SUM_{digit} {result} L")
                self.add(f"SUM_{digit} {other_digit} SUM_{digit} {other_digit} L")
            self.add(f"SUM_{digit} # RES_{digit} # L")
            for other_digit in self.DIGITS:
                self.add(f"RES_{digit} {other_digit} RES_{digit} {other_digit} L")
            self.add(f"RES_{digit} _ FWD {digit} R")

        self.add("SUM+_0 # MORE # R")
        self.add("MORE _ SUM_0 1 L")
        self.add("FWD # FWD # R")
        self.add("SCAN + RDONE _ L")
        self.add("RDONE _ RDONE _ L")
        self.add("RDONE # HALT _ R")

        for digit in self.DIGITS:
            self.add(f"RDONE {digit} RDONE_{digit} _ L")
            if digit != "0":
                self.add(f"RDONE_{digit} # RDONE_{digit} # L")
            for other_digit in self.DIGITS:
                self.add(f"RDONE_{digit} {other_digit} RDONE_{digit} {other_digit} L")
                self.add(f"LDONE_{digit} {other_digit} LDONE_{digit} {other_digit} L")
            self.add(f"RDONE_{digit} _ FWD_RDONE {digit} R")
            self.add(f"LDONE_{digit} _ FWD {digit} R")
            self.add(f"FWD_RDONE {digit} FWD_RDONE {digit} R")
        # check if the 0 carried is the leading 0
        self.add("RDONE_0 # CHECK # R")
        self.add("CHECK _ DONE _ L")
        self.add("CHECK 1 STILL 1 L")
        self.add("CHECK 0 STILL 0 L")
        self.add("STILL # RDONE_0 # L")
        self.add("DONE # HALT _ L")

        self.add("FWD_RDONE # FWD_RDONE # R")
        self.add("FWD_RDONE _ RDONE _ L")


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
