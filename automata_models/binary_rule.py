import numpy as np
import random
import numpy as np
from math import log2


LINEAR_BINARY_RULE_SPECIFIER = "bl"

EDGE_CASE_RANDOM = "random"
EDGE_CASE_PERIODIC = "periodic"

# https://stackoverflow.com/questions/1835018/how-to-check-if-an-object-is-a-list-or-tuple-but-not-string
def is_sequence(arg):
    return not hasattr(arg, "strip") and (
        hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")
    )


def is_binary(arg):
    try:
        return int(arg) in [0, 1]
    except:
        return False


def convert_triplet_to_int(triplet):
    result = 0

    if not (is_sequence(triplet) and len(triplet) == 3):
        raise ValueError("Triplet must be a list of length 3")

    for i in range(3):
        result += int(triplet[i]) * 2 ** (2 - i)

    return result


def is_linear_binary_edge_case(arg):
    return (
        is_sequence(arg)
        and hasattr(arg, "__len__")
        and all([is_binary(x) for x in arg])
    )


def get_binary_state_array_from_int(state_int, length):
    if log2(state_int) >= length:
        raise ValueError("State integer is too large")
    state_array = np.array([int(x) for x in bin(state_int)[2:]])
    return np.append(np.zeros(length - len(state_array)), state_array)


class BinaryLin3Rule:
    rule_size = 3
    rule_base_length = 8

    def __init__(self, edge_case=EDGE_CASE_RANDOM):
        self.edge_case = None
        self.convert_with_rule = None
        self.rule_str = None

        if is_binary(edge_case):
            self.edge_case = [edge_case, edge_case]

        if is_linear_binary_edge_case(edge_case) and len(edge_case) == 2:
            self.edge_case = list(edge_case)

        self.random_edge_case = edge_case == EDGE_CASE_RANDOM
        self.periodic_edge_case = edge_case == EDGE_CASE_PERIODIC

        if (
            not self.random_edge_case
            and not self.periodic_edge_case
            and self.edge_case is None
        ):
            raise ValueError(
                'Edge case must be either 1, 0, a list of 2, "random", or "periodic"'
            )

    def __str__(self):
        return LINEAR_BINARY_RULE_SPECIFIER + "3_" + self.get_edge_case_string() + "_" + self.rule_str

    def get_edge_case_string(self):
        if self.random_edge_case:
            return EDGE_CASE_RANDOM
        elif self.periodic_edge_case:
            return EDGE_CASE_PERIODIC
        else:
            return "[" + ",".join([str(x) for x in self.edge_case]) + "]"

    def set_rule_from_int(self, rule_int):
        if not 0 <= rule_int <= (2**BinaryLin3Rule.rule_base_length - 1):
            raise ValueError(
                f"Rule integer must be between 0 and {2**BinaryLin3Rule.rule_base_length - 1}"
            )

        return self.set_rule_from_string(bin(rule_int)[2:].zfill(BinaryLin3Rule.rule_base_length))

    def set_rule_from_string(self, rule_str):

        self.rule_str = rule_str

        if not (isinstance(rule_str, str) and all([is_binary(x) for x in rule_str])):
            raise ValueError("Rule string must be a string of 0s and 1s")

        if not len(rule_str) == BinaryLin3Rule.rule_base_length:
            raise ValueError(f"Rule string must be {BinaryLin3Rule.rule_base_length} characters long")

        self.rules_dictionary = dict()

        for i in range(len(rule_str)):
            self.rules_dictionary[i] = int(rule_str[len(rule_str)-i-1])

        self.convert_with_rule = lambda triplet: self.rules_dictionary[
            convert_triplet_to_int(triplet)
        ]

        return self

    def get_updated_state(self, initial_state):
        if self.convert_with_rule is None:
            raise ValueError("Rule has not been set")
        if not is_sequence(initial_state) or len(initial_state) < 2:
            raise ValueError("Initial state must be a list of length at least 2")

        result = np.ndarray(len(initial_state), dtype=int)
        if self.random_edge_case:
            result[0] = self.convert_with_rule(
                np.append([random.choice([0, 1])], initial_state[0:2])
            )
            result[-1] = self.convert_with_rule(
                np.append(initial_state[-2:], [random.choice([0, 1])])
            )
        elif self.periodic_edge_case:
            result[0] = self.convert_with_rule(
                np.append([initial_state[-1]], initial_state[0:2])
            )
            result[-1] = self.convert_with_rule(
                np.append(initial_state[-2:], [initial_state[0]])
            )
        else:
            result[0] = self.convert_with_rule(
                np.append([self.edge_case[0]], initial_state[0:2])
            )
            result[-1] = self.convert_with_rule(
                np.append(initial_state[-2:], [self.edge_case[1]])
            )

        for i in range(1, len(initial_state) - 1):
            result[i] = self.convert_with_rule(initial_state[i - 1 : i + 2])

        return result
