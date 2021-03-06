from enum import Enum

class FactState(Enum):
    DEFAULT = 1
    FALSE = 2
    TRUE = 3
    UNDETERMINED = 4
    OUT = 5
    LINKER = 6

class Fact:
    FactState = FactState.DEFAULT
    def __init__(self, FactStateCondition):
        self.FactState = FactStateCondition
    def print_state(self, letter):
        if self.FactState == FactState.DEFAULT:
            print(letter, "is False by default")
        elif self.FactState == FactState.FALSE:
            print(letter, "is False")
        elif self.FactState == FactState.TRUE:
            print(letter, "is True")
        elif self.FactState == FactState.UNDETERMINED:
            print(letter, "is undetermined")
        