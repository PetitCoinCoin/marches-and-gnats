from dataclasses import dataclass
from typing import Iterable, Literal

from utils.main import Colors

@dataclass
class Rule:
    state: str
    symbol: str
    new_state: str
    new_symbol: str
    direction: Literal["R", "L"]

    def __eq__(self, other):
        return self.state == other.state and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.state, self.symbol))
    
    def __str__(self) -> str:
        return f"{self.state} {self.symbol} {self.new_state} {self.new_symbol} {self.direction}"


class BaseMachine:
    """Defines a Turing Machine"""

    INIT: str = "INIT"
    HALT: str = "HALT"
    BLANK: str = "_"
    EMPTY: str = ""

    def __init__(self) -> None:
        self.rules: set[Rule] = set()
        self.state: str = self.INIT
        self.head: int = 0
        self.input: str = self.EMPTY
        self.tape: list[str] = []
        self.steps: int = 0

    def add(self, rule: str | Rule) -> None:
        added_rule = Rule(*rule.split(" ")) if isinstance(rule, str) else rule
        self.rules.add(added_rule)

    def batch_add(self, rules: Iterable[str | Rule]) -> None:
        for rule in rules:
            self.add(rule)

    def build_rules(self, *, rules_optimized: bool):
        if rules_optimized:
            self._build_rules_opt() 
        else:
            self._build_steps_opt()
    
    def play(self, tape: str, *, verbose: bool = False) -> None:
        self.tape = [char for char in tape]
        self.input = tape
        self.state = self.INIT
        self.head = 0
        rules_dict = self.__rules_to_dict()

        if verbose:
            print(self.pretty_tape)

        while self.state != self.HALT:
            symbol = self.tape[self.head]
            try:
                new_state, new_symbol, direction = rules_dict[self.state][symbol]
            except KeyError:
                print(f"{Colors.RED}Missing transition: symbol {symbol} in state {self.state}{Colors.END}")
                return
            self.tape[self.head] = new_symbol
            self.state = new_state
            self.head += 1 if direction == "R" else -1
            while self.head < 0:
                self.head += 1
                self.tape = [self.BLANK] + self.tape
            while self.head >= len(self.tape):
                self.tape.append(self.BLANK)
            if verbose:
                print(self.pretty_tape)
        print("".join(self.tape).replace(self.BLANK, self.EMPTY))

    @property
    def pretty_rules(self) -> str:
        return "\n".join(str(rule) for rule in self.rules)

    @property
    def pretty_tape(self) -> str:
        result = f"{Colors.BLUE}{self.state.ljust(10)}{Colors.END} "
        str_tape = "".join(self.tape)
        # head = self.head if self.head < len(str_tape) else len(str_tape) - 1
        result += f"{str_tape[:self.head]}{Colors.PURPLE}{str_tape[self.head]}{Colors.END}{str_tape[self.head + 1:]}"
        return result

    @property
    def stats(self) -> dict:
        return {
            "Number of rules": len(self.rules),
            "Number of states": self.__states_count(),
        }

    def _build_rules_opt(self):
        print(f"{Colors.ORANGE}No rules optimized for rules count{Colors.END}")
        self._build_steps_opt()

    @staticmethod
    def _build_steps_opt():
        raise NotImplementedError

    def __rules_to_dict(self) -> dict:
        result = dict()
        for rule in self.rules:
            if rule.state not in result:
                result[rule.state] = dict()
            result[rule.state][rule.symbol] = (rule.new_state, rule.new_symbol, rule.direction)
        return result

    def __states_count(self) -> int:
        states = set()
        for rule in self.rules:
            states.add(rule.state)
            states.add(rule.new_state)
        return len(states)
