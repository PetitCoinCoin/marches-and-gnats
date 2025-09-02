from dataclasses import dataclass
from typing import Iterable, Literal

@dataclass
class Rule:
    state: str
    symbol: str
    new_state: str
    new_symbole: str
    direction: Literal["R", "L"]

    def __eq__(self, other):
        return self.state == other.state and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.state, self.symbol))
    
    def __str__(self) -> str:
        return f"{self.state} {self.symbol} {self.new_state} {self.new_symbole} {self.direction}"


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
        self.tape: str = self.EMPTY
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
    
    def _build_rules_opt(self):
        print("No rules optimized for rules count")
        self._build_steps_opt()

    @staticmethod
    def _build_steps_opt():
        raise NotImplementedError

    def play(self, tape: str) -> None:
        self.tape = tape
        self.input = tape
        print(self.tape)

    @property
    def pretty_rules(self) -> str:
        return "\n".join(str(rule) for rule in self.rules)

    @property
    def stats(self) -> dict:
        return {
            "Number of rules": len(self.rules),
            "Number of states": self.__states_count(),
        }

    def __states_count(self) -> int:
        states = set()
        for rule in self.rules:
            states.add(rule.state)
            states.add(rule.new_state)
        return len(states)
