import random
import re

import sympy as sp


class ArithmeticSequence:
    """Szöveges számtani sorozatos feladat."""

    def __init__(self):
        self.first_term = None
        self.difference = None
        self.given_term = None
        self.given_sum = None
        self.given_index = None
        self.sum_first_index = None
        self.sum_second_index = None
        self.target_index = None
        self.solution = None

    def generateTask(self):
        self.first_term = random.randint(-10, 10)
        self.difference = random.choice([value for value in range(-5, 6) if value])
        self.given_index = random.randint(15, 30)
        self.sum_first_index = random.randint(2, self.given_index - 5)
        self.sum_second_index = random.randint(
            self.sum_first_index + 1, self.given_index - 2
        )
        self.target_index = random.randint(
            self.sum_second_index + 1, self.given_index - 1
        )
        self.given_term = (
            self.first_term + (self.given_index - 1) * self.difference
        )
        self.given_sum = (
            2 * self.first_term
            + (
                self.sum_first_index
                + self.sum_second_index
                - 2
            )
            * self.difference
        )
        self.solution = (
            self.first_term + (self.target_index - 1) * self.difference,
            self.difference,
        )
        return self.solution

    def get_latex(self):
        instruction = "Oldja meg a következő szöveges feladatot!"
        expression = (
            rf"\text{{Egy számtani sorozat }}{self.given_index}.\text{{ eleme }}"
            rf"{self.given_term}\text{{, a }}{self.sum_first_index}\text{{. és }}"
            rf"{self.sum_second_index}\text{{. elemének összege pedig }}"
            rf"{self.given_sum}\text{{. Mennyi a sorozat }}{self.target_index}"
            rf"\text{{. eleme és mennyi a differenciája?}}"
        )
        return instruction, expression

    def get_text(self):
        return (
            f"Egy számtani sorozat {self.given_index}. eleme {self.given_term}, "
            f"a {self.sum_first_index}. és {self.sum_second_index}. elemének "
            f"összege pedig {self.given_sum}. Mennyi a sorozat "
            f"{self.target_index}. eleme és mennyi a differenciája?"
        )

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_format(self):
        return f"a{self.target_index} = ..., d = ..."

    def get_answer_fields(self):
        return [
            {"label": rf"a_{{{self.target_index}}} =", "name": "target"},
            {"label": "d =", "name": "difference"},
        ]

    def validateSolution(self, student_solution):
        try:
            answer = str(student_solution).replace("−", "-").replace(" ", "")
            answer = re.sub(r"a\d+=|d=", "", answer, flags=re.IGNORECASE)
            answer = re.sub(r"\\frac\{(-?\d+)\}\{(\d+)\}", r"(\1/\2)", answer)
            values = [value for value in re.split(r"[,;]", answer) if value]
            if len(values) != 2:
                return False
            parsed = tuple(sp.Rational(value.strip("()")) for value in values)
            return parsed == self.solution
        except (TypeError, ValueError, sp.SympifyError):
            return False
